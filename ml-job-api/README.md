# 🌐 ML Job API

**Asynchronous microservice** built with `FastAPI`, `SQLAlchemy`, `Alembic`, and `Celery`.

---

## 🔍 Overview

The application exposes RESTful endpoints to:

- **Upload**, **download**, **list**, and **delete** arbitrary files (e.g. input data).

- **Retrieve** and parse FITS spectra metadata.

- Manage ML jobs (e.g. **create**, **start**, **abort**, **complete**).

- **Track** human-in-the-loop “labellings” for active ML workflows.

It leverages `PostgreSQL` (**ML Job DB**)/`SQLAlchemy` for metadata persistence, `RabbitMQ` (**ML Job Queue**)/`Celery` for job orchestration, and the local filesystem/`aiofiles` for file & spectral storage.

---

## 📍 Features

- `FastAPI` driven OpenAPI docs.

- Asynchronous I/O with `asyncpg` & `aiofiles`.

- `Celery` + `RabbitMQ` job queue. 

- `SQLAlchemy` + `Alembic` migrations.

- `Pydantic` models & settings for robust validation. 

---

## ⚙️ Tech Stack

- `Python 3.13 ` 

- `FastAPI`  

- `Pydantic`  

- `SQLAlchemy 2.0` + `Alembic`

- `Celery 5`
 
- `Astropy` for FITS parsing

- `Docker` & `Docker Compose`
