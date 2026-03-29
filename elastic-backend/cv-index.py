# Task 4e: Index cv-valid-dev.csv into Elasticsearch.

import pandas as pd
from elasticsearch import Elasticsearch, helpers

ES_URL = "http://localhost:9200"
INDEX_NAME = "cv-transcriptions"
CSV_PATH = "../asr/cv-valid-dev/cv-valid-dev.csv"

def create_index(es: Elasticsearch):
    mappings = {
        "mappings": {
            "properties": {
                "filename":       {"type": "keyword"},
                "generated_text": {"type": "text"},
                "duration":       {"type": "float"},
                "age":            {"type": "keyword"},
                "gender":         {"type": "keyword"},
                "accent":         {"type": "keyword"},
            }
        }
    }
    if not es.indices.exists(index=INDEX_NAME):
        es.indices.create(index=INDEX_NAME, body=mappings)
        print(f"Created index: {INDEX_NAME}")
    else:
        print(f"Index already exists: {INDEX_NAME}")

def clean(value, default=""):
    return default if pd.isna(value) else value

def generate_docs(df: pd.DataFrame):
    for _, row in df.iterrows():
        yield {
            "_index": INDEX_NAME,
            "_source": {
                "filename":       clean(row.get("filename"), ""),
                "generated_text": clean(row.get("generated_text"), ""),
                "duration":       clean(row.get("duration"), None),
                "age":            clean(row.get("age"), ""),
                "gender":         clean(row.get("gender"), ""),
                "accent":         clean(row.get("accent"), ""),
            }
        }

def main():
    es = Elasticsearch(ES_URL)

    if not es.ping():
        print("Could not connect to Elasticsearch. Is it running?")
        return

    print(f"Connected to Elasticsearch at {ES_URL}")

    create_index(es)
    df = pd.read_csv(CSV_PATH)
    total = len(df)
    print(f"Indexing {total} records into '{INDEX_NAME}'...")

    success, failed = helpers.bulk(es, generate_docs(df), raise_on_error=False)
    print(f"Done. {success} indexed, {failed} failed.")

if __name__ == "__main__":
    main()