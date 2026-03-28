# HTX Assessment

## Repository Structure

```
htx-assessment/
├── asr/                  # Task 2 — ASR microservice
│   ├── asr_api.py        # FastAPI app with /ping and /asr endpoints
│   ├── cv-decode.py      # Batch transcription script for Common Voice
│   ├── Dockerfile        # Docker image for the ASR API
│   ├── requirements.txt  # ASR API dependencies
│   └── cv-valid-dev/     # Common Voice dataset (not committed)
├── elastic-backend/      # Task 4 — Elasticsearch backend (coming soon)
├── search-ui/            # Task 5 — Search UI frontend (coming soon)
├── deployment-design/    # Task 3 — Architecture diagram (coming soon)
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Setup

### Clone the repository

```bash
git clone https://github.com/pxlanleh/htx-assessment.git
cd htx-assessment
```

### Install dependencies

```bash
pip install -r requirements.txt
```

---

## Task 2 — ASR Service

Automatic Speech Recognition microservice using [facebook/wav2vec2-large-960h](https://huggingface.co/facebook/wav2vec2-large-960h).

### Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| GET | `http://localhost:8001/ping` | Health check — returns `pong` |
| POST | `http://localhost:8001/asr` | Transcribe an mp3 file |

### Run locally

```bash
uvicorn asr.asr_api:app --host 0.0.0.0 --port 8001
```

### Run with Docker

```bash
cd asr
docker build -t asr-api .
docker run -p 8001:8001 asr-api
```

### Example request

```bash
curl -F 'file=@/path/to/sample.mp3' http://localhost:8001/asr
```

### Example response

```json
{"transcription": "BEFORE HE HAD TIME TO ANSWER", "duration": "4.2"}
```

### Batch decode (Common Voice)

Place the `cv-valid-dev/` folder inside `asr/`, then run:

```bash
cd asr
python cv-decode.py
```

This transcribes all 4,076 mp3 files and saves results into `cv-valid-dev/cv-valid-dev.csv` under a new `generated_text` column.

### Assumptions

- Audio inputs are resampled to 16kHz mono before inference.
- The Common Voice dataset (`cv-valid-dev/`) is not committed to the repository due to size.