# HTX Assessment

**Candidate:** Phelan Lee

## Repository Structure

```
htx-assessment/
├── asr/                  # Task 2 — ASR microservice
│   ├── asr_api.py
│   ├── cv-decode.py
│   ├── Dockerfile
│   └── requirements.txt
├── deployment-design/    # Task 3 — Architecture diagram
│   └── design.pdf
├── elastic-backend/      # Task 4 — Elasticsearch 2-node cluster
│   ├── docker-compose.yml
│   └── cv-index.py
├── search-ui/            # Task 5 — Search UI frontend
│   ├── docker-compose.yml
│   ├── Dockerfile
│   ├── src/App.js
│   └── package.json
├── essay.pdf              # Task 8 — Model monitoring essay
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Setup

```bash
git clone https://github.com/pxlanleh/htx-assessment.git
cd htx-assessment
pip install -r requirements.txt
```

**Note:** The Common Voice dataset (`cv-valid-dev/`) is not included due to size. Download it and place it in `asr/cv-valid-dev/` before running the services.

---

## Running the Services

**ASR API**
```bash
cd asr
docker build -t asr-api .
docker run -p 8001:8001 asr-api
```

**Elasticsearch**
```bash
cd elastic-backend
docker compose up -d
python cv-index.py
```

**Search UI**
```bash
cd search-ui
docker compose up --build -d
```

---

## Deployment URL (Task 6)

**Live URL:** http://54.252.241.194:3000

---

## Assumptions

- **Task 2:** Audio inputs are resampled to 16kHz mono before inference. Uploaded files are deleted after processing.
- **Task 3:** Single EC2 instance hosts all containers for free tier compatibility. In production, a 2-node Elasticsearch cluster across separate instances is recommended.
- **Task 5:** Search UI connects directly to Elasticsearch. In production, a backend proxy should be used.
- **Task 6:** Single Elasticsearch node used due to free tier memory constraints. 2-node configuration preserved in `elastic-backend/docker-compose.yml`. Elasticsearch exposed on port 8080 instead of 9200 for broader network compatibility.