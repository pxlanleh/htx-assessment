// Task 5: Search UI frontend
// Connects to Elasticsearch at http://localhost:9200

import React from "react";
import ElasticsearchAPIConnector from "@elastic/search-ui-elasticsearch-connector";
import {
  SearchProvider,
  SearchBox,
  Results,
  Facet,
  Sorting,
  PagingInfo,
  ResultsPerPage,
  Paging,
  WithSearch,
} from "@elastic/react-search-ui";
import { Layout } from "@elastic/react-search-ui-views";
import "@elastic/react-search-ui-views/lib/styles/styles.css";

const connector = new ElasticsearchAPIConnector({
  host: "http://localhost:9200",
  index: "cv-transcriptions",
});

const config = {
  apiConnector: connector,
  alwaysSearchOnInitialLoad: true,
  searchQuery: {
    search_fields: {
      generated_text: { weight: 3 },
    },
    result_fields: {
      filename:       { raw: {} },
      generated_text: { raw: {}, snippet: { size: 200, fallback: true } },
      duration:       { raw: {} },
      age:            { raw: {} },
      gender:         { raw: {} },
      accent:         { raw: {} },
    },
    facets: {
      age:    { type: "value", size: 10 },
      gender: { type: "value", size: 10 },
      accent: { type: "value", size: 10 },
      duration: {
        type: "range",
        ranges: [
          { from: 0,  to: 5,  name: "0 – 5s" },
          { from: 5,  to: 10, name: "5 – 10s" },
          { from: 10, to: 20, name: "10 – 20s" },
          { from: 20,         name: "20s+" },
        ],
      },
    },
    disjunctiveFacets: ["gender", "age", "accent"],
  },
};

export default function App() {
  return (
    <SearchProvider config={config}>
      <WithSearch mapContextToProps={({ wasSearched }) => ({ wasSearched })}>
        {({ wasSearched }) => (
          <div className="App">
            <Layout
              header={<SearchBox />}
              sideContent={
                <div>
                  <Facet field="gender"   label="Gender" />
                  <Facet field="age"      label="Age" />
                  <Facet field="accent"   label="Accent" />
                  <Facet field="duration" label="Duration" />
                </div>
              }
              bodyContent={
                <Results
                  titleField="filename"
                  resultView={({ result }) => (
                    <div style={{ padding: "10px", borderBottom: "1px solid #eee" }}>
                      <strong>{result.filename?.raw}</strong>
                      <p
                        dangerouslySetInnerHTML={{
                          __html: result.generated_text?.snippet || result.generated_text?.raw,
                        }}
                      />
                      <small>
                        Duration: {result.duration?.raw}s &nbsp;|&nbsp;
                        Age: {result.age?.raw || "N/A"} &nbsp;|&nbsp;
                        Gender: {result.gender?.raw || "N/A"} &nbsp;|&nbsp;
                        Accent: {result.accent?.raw || "N/A"}
                      </small>
                    </div>
                  )}
                />
              }
              bodyHeader={
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", flexWrap: "wrap" }}>
                  {wasSearched && <PagingInfo />}
                  {wasSearched && <ResultsPerPage />}
                  {wasSearched && (
                    <Sorting
                      label="Sort by"
                      sortOptions={[
                        { name: "Relevance", value: [] },
                        { name: "Duration (asc)", value: [{ field: "duration", direction: "asc" }] },
                        { name: "Duration (desc)", value: [{ field: "duration", direction: "desc" }] },
                      ]}
                    />
                  )}
                </div>
              }
              bodyFooter={<Paging />}
            />
          </div>
        )}
      </WithSearch>
    </SearchProvider>
  );
}
