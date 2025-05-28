# ML Job Manager

Monorepo containing three components for an end-to-end ML job orchestration platform:

```
ml-job-manager/
├── ml-job-api/       ← ML Job API FastAPI microservice (REST API)
├── ml-job-ui/        ← ML Job UI React frontend (Web Interface + Spectra Visualizations)
├── ml-job-worker/    ← ML Job Worker Celery Worker (Data Preprocessing & Active ML)
├── docker-compose.yml
└── README.md         ← this file
```

---

## 🚀 Features

- **ML Job API**  
  – CRUD endpoints for **jobs**, **labellings**, **spectra**, **file** storage.
  – Async `PostgreSQL` persistence, `Alembic` migrations.  
  – `Celery` integration for dispatching jobs.

- **ML Job Worker**  
  – `Celery` jobs: Data Preprocessing & Active ML pipelines.
  – `TensorFlow` CNN, `Scikit-Learn` utilities (SMOTE, t-SNE).
  – `HTTPX` callbacks to **ML Job API**.

- **ML Job UI**  
  – `React` + `Tailwind` dashboard. 
  – Live **job status**, **spectra view**, **labelling workflow**.

- **DevOps**  
  – `Docker` & `Docker Compose` for full-stack local development.
  – Environment-driven configuration via `.env` and Pydantic.

---

## 📦 Prerequisites

- `Docker` & `Docker Compose` ≥ v2.0. 
- Nvidia GPU for **ML Job Worker** `TensorFlow` CNN computations.

---

## 🔧 Quickstart

Clone the repo:

```bash
git clone https://github.com/bursasha/ml-job-manager.git
cd ml-job-manager
```

Create a .env in the project root (see .env.example for all keys):

```dotenv
DEBUG=True
FILES_DIR_PATH=...
SPECTRA_DIR_PATH=...
JOB_QUEUE=jobs

#

UI_PORT=10000

#

API_PORT=10100
ENGINE_CONNECTION_TIMEOUT=3

#

WORKER_PORT=10200
BROKER_CONNECTION_TIMEOUT=3
API_CONNECTION_TIMEOUT=3

#

POSTGRES_USER=...
POSTGRES_PASSWORD=...
POSTGRES_DB=...

#

RABBITMQ_MANAGEMENT_PORT=10300
RABBITMQ_DEFAULT_USER=...
RABBITMQ_DEFAULT_PASS=...
```

Bring up the entire stack:

```bash
docker compose up
```

This will launch following services:
- **ML Job UI** (`React`)
- **ML Job API** (`FastAPI`)
- **ML Job Worker** (`Celery`)
- **ML Job Queue** (`RabbitMQ`)
- **ML Job DB** (`PostgreSQL`)

You can now:
- Visit the UI at http://localhost:10000
- Browse API docs at http://localhost:10100/docs

---

## ⚙️ Stop & Remove Containers

Stop:

```bash
docker compose stop
```

Remove: 

```bash
docker compose down
```

---

## 📈 View Logs

```bash
docker compose logs -f ml-job-ui
docker compose logs -f ml-job-api
docker compose logs -f ml-job-worker
docker compose logs -f ml-job-queue
docker compose logs -f ml-job-db
```
