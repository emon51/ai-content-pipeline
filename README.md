# AI Content Pipeline

An end-to-end content processing system that accepts property data, enhances it using AI (SEO transformation via Groq), stores results in MinIO (S3-compatible) and generates structured per-ID output files.

---
## Overview

The pipeline accepts property data (title, description, CSV of IDs) from a React frontend, processes and stores the data in MinIO, enhances the content using the Groq AI API for SEO optimization, and generates structured per-ID JSON output files.

---

## Tech Stack

| Layer    | Technology                        |
|----------|-----------------------------------|
| Frontend | React + Vite                      |
| Backend  | Django REST Framework             |
| Storage  | MinIO (S3-compatible)             |
| AI       | Groq API (`llama-3.3-70b-versatile`)       |
| Runtime  | Docker + Docker Compose           |

---

## Project Structure

```
content-pipeline/
├── docker-compose.yml
├── .gitignore
├── README.md
├── backend/
│   ├── Dockerfile
│   ├── .env                     
│   ├── requirements.txt
│   ├── manage.py
│   ├── core/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   └── pipeline/
│       ├── serializers.py
│       ├── views.py
│       ├── urls.py
│       └── services/
│           ├── csv_parser.py
│           ├── storage.py
│           ├── ai_processor.py
│           └── id_generator.py
└── frontend/
    ├── Dockerfile
    ├── package.json
    ├── vite.config.js
    └── src/
        ├── App.jsx
        ├── App.css
        ├── api/
        │   └── pipeline.js
        └── components/
            ├── PipelineForm.jsx
            └── PipelineResult.jsx
```

---

## Quick Setup

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and Docker Compose
- A [Groq API key](https://console.groq.com/keys)

### 1. Clone the repository

```bash
git clone https://github.com/emon51/ai-content-pipeline.git
cd ai-content-pipeline
```

### 2. Configure environment

```bash
cp backend/.env.example backend/.env
```

Edit `backend/.env` and fill in your values:

```env
DJANGO_SECRET_KEY=your-secret-key
GROQ_API_KEY=your-groq-api-key
```

### 3. Start all services

```bash
docker compose up --build
```

### 4. Open the app

Navigate to **http://localhost:5173** in your browser.

---

## Environment Variables

| Variable                 | Description                          | Default              |
|--------------------------|--------------------------------------|----------------------|
| `DJANGO_SECRET_KEY`      | Django secret key                    | —                    |
| `DEBUG`                  | Django debug mode                    | `True`               |
| `AWS_ACCESS_KEY_ID`      | MinIO access key                     | `minioadmin`         |
| `AWS_SECRET_ACCESS_KEY`  | MinIO secret key                     | `minioadmin`         |
| `AWS_STORAGE_BUCKET_NAME`| MinIO bucket name                    | `rebrand-content`    |
| `AWS_S3_ENDPOINT_URL`    | MinIO endpoint (internal)            | `http://minio:9000`  |
| `AWS_S3_REGION_NAME`     | S3 region                            | `us-east-1`          |
| `GROQ_API_KEY`           | Groq API key                         | —                    |
| `GROQ_MODEL`             | Groq model name                      | `llama-3.3-70b-versatile`     |

---

## API Reference

### `POST /api/process/`

Runs the full pipeline — parses CSV, stores input, enhances content via AI, generates per-ID files.

**Request** — `multipart/form-data`

| Field         | Type   | Description                        |
|---------------|--------|------------------------------------|
| `site_name`   | string | Site identifier (e.g. `rentbyowner.com`) |
| `title`       | string | Property title                     |
| `description` | string | Property description               |
| `csv_file`    | file   | CSV file with `id` column          |

**CSV Format**

```csv
id,title,description
```


**Error Responses**

| Status | Reason                          |
|--------|---------------------------------|
| `400`  | Invalid input or bad CSV        |
| `500`  | Storage or AI processing failed |

---

## Pipeline Flow

```
Frontend (React)
     │  POST multipart/form-data
     ▼
Backend (DRF) /api/process/
     │
     ├── 1. Validate input (serializer)
     ├── 2. Parse & deduplicate CSV IDs
     ├── 3. Store input.json → MinIO
     ├── 4. Enhance via Groq AI (title + description)
     ├── 5. Store ai_response.json → MinIO
     └── 6. Generate per-ID .json files → MinIO
```

---

## MinIO Storage Structure

```
rebrand-content/
└── {site_name}/
    └── details/
        ├── input/
        │   └── input.json          ← raw parsed input
        ├── output/
        │   └── ai_response.json    ← Groq AI output
        ├── BC-12199453.json        ← per-ID file
        └── BC-12443396.json        ← per-ID file
```


## Service URLs

| Service        | URL                        | Credentials                  |
|----------------|----------------------------|------------------------------|
| Frontend       | http://localhost:5173      | —                            |
| Backend API    | http://localhost:8000/api/ | —                            |
| MinIO Console  | http://localhost:9001      | `minioadmin` / `minioadmin`  |
| MinIO API      | http://localhost:9000      | —                            |