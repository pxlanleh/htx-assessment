# HTX Assessment

## Repository Structure

```
htx-assessment/
├── asr/                  # Task 2 — ASR microservice
│   ├── asr_api.py        # FastAPI app with /ping and /asr endpoints
│   ├── cv-decode.py      # Batch transcription script for Common Voice
│   ├── Dockerfile        # Docker image for the ASR API
│   └── requirements.txt  # ASR API dependencies
├── deployment-design/    # Task 3 — Architecture diagram
│   └── design.pdf        # AWS deployment architecture (draw.io)
├── elastic-backend/      # Task 4 — Elasticsearch 2-node cluster
│   ├── docker-compose.yml
│   └── cv-index.py       # Indexes cv-valid-dev.csv into Elasticsearch
├── search-ui/            # Task 5 — Search UI frontend
│   ├── docker-compose.yml
│   ├── Dockerfile
│   ├── src/App.js        # Search UI configuration
│   └── package.json
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

---

## Task 2 — ASR Service

ASR microservice using [facebook/wav2vec2-large-960h](https://huggingface.co/facebook/wav2vec2-large-960h).

| Method | URL | Description |
|--------|-----|-------------|
| GET | `http://localhost:8001/ping` | Health check — returns `pong` |
| POST | `http://localhost:8001/asr` | Transcribe an mp3 file |

### Run with Docker

```bash
cd asr
docker build -t asr-api .
docker run -p 8001:8001 asr-api
```

### Example

```bash
curl -F 'file=@cv-valid-dev/sample-000000.mp3' http://localhost:8001/asr
```
```json
{"transcription": "BEFORE HE HAD TIME TO ANSWER", "duration": "4.2"}
```

### Batch decode

Place `cv-valid-dev/` folder inside `asr/`, then:
```bash
cd asr
python cv-decode.py
```

### Assumptions
- Audio inputs are resampled to 16kHz mono before inference.
- The Common Voice dataset is not committed due to size.

---

## Task 3 — Deployment Architecture

Architecture diagram saved as `deployment-design/design.pdf`. All services deployed on a single AWS EC2 instance (free tier) using Docker Compose. No managed services used.

### Assumptions
- Single EC2 instance (t2.micro) hosts all containers for free tier compatibility.
- A 3-node Elasticsearch cluster is recommended in production to avoid split-brain issues.

---

## Task 4 — Elasticsearch Backend

2-node Elasticsearch cluster at `http://localhost:9200`, index: `cv-transcriptions`.

```bash
cd elastic-backend
docker compose up -d
python cv-index.py
```

### Assumptions
- xpack security disabled for simplicity.
- CORS enabled for Search UI access from localhost:3000.

---

## Task 5 — Search UI

Frontend search application at `http://localhost:3000`.

Searchable fields: `generated_text`. Filterable fields: `duration`, `age`, `gender`, `accent`.

```bash
cd search-ui
docker compose up --build -d
```

### Assumptions
- Search UI connects directly to Elasticsearch at localhost:9200. In production, requests should be proxied through a backend.