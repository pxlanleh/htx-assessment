# HTX Assessment

End-to-end pipeline featuring an ASR microservice, Elasticsearch backend, and Search UI frontend.

## Deployment URL

> _To be updated after cloud deployment (Task 6)_

---

## Repository Structure

```
htx-assessment/
├── asr/                  # Task 2 — ASR microservice
├── elastic-backend/      # Task 4 — Elasticsearch 2-node cluster
├── search-ui/            # Task 5 — Search UI frontend
├── deployment-design/    # Task 3 — Architecture diagram
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Prerequisites

- Python 3.10+
- Docker & Docker Compose
- pip

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/pxlanleh/htx-assessment.git
cd htx-assessment
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Task 2 — ASR Service

### Run locally

```bash
cd asr
uvicorn asr_api:app --host 0.0.0.0 --port 8001
```

### Run with Docker

```bash
cd asr
docker build -t asr-api .
docker run -p 8001:8001 asr-api
```

### Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| GET | `http://localhost:8001/ping` | Health check — returns `pong` |
| POST | `http://localhost:8001/asr` | Transcribe an mp3 file |

### Example request

```bash
curl -F 'file=@/path/to/sample.mp3' http://localhost:8001/asr
```

### Batch decode (Common Voice)

```bash
cd asr
python cv-decode.py
```

---

## Task 4 — Elasticsearch Backend

```bash
cd elastic-backend
docker compose up -d
python cv-index.py
```

- URL: `http://localhost:9200`
- Index: `cv-transcriptions`

---

## Task 5 — Search UI

```bash
cd search-ui
docker compose up -d
```

- URL: `http://localhost:3000`

---

## Assumptions

- Audio files are resampled to 16kHz before inference.
- The Common Voice dataset (`cv-valid-dev/`) is not committed to the repository due to size.
- Cloud deployment uses AWS EC2 (free tier) with Docker Compose — no managed services.
