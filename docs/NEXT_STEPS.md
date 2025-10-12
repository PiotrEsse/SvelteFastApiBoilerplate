# Next Steps Checklist

This project already contains a working FastAPI + SvelteKit todo boilerplate. After cloning the
repository you can follow the steps below to run it end-to-end.

## 1. Bootstrap the containers

```bash
cd infrastructure
docker compose up -d
```

> The `app` container is meant for local development (it has both the backend and frontend source
> code mounted into `/workspaces`). The `db` and `redis` containers host PostgreSQL and Redis
> respectively.

## 2. Prepare the backend

```bash
cd backend
cp .env.example .env  # on Windows use: copy .env.example .env
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

> Tip: before running the server, open `.env` and adjust secrets (e.g. `SECRET_KEY`) if needed.

This spins up the FastAPI server with authentication, todo CRUD, and Celery integration already
configured. The API is reachable at `http://localhost:8000` and exposes the OpenAPI spec under
`/openapi.json`.

## 3. Prepare the frontend

```bash
cd frontend
npm install
npm run generate:sdk
npm run dev -- --host 0.0.0.0 --port 5173
```

> Ensure the FastAPI server is already running before calling `npm run generate:sdk`, as the script
> downloads the OpenAPI schema from `http://localhost:8000/openapi.json`.

The SvelteKit dev server listens on port `5173` and communicates with the backend using the
credentials-aware SDK generated from OpenAPI.

## 4. (Optional) Start Celery worker

```bash
cd backend
source .venv/bin/activate
celery -A app.celery_app worker -B --loglevel=info
```

This enables scheduled reminder jobs for todo deadlines. The beat scheduler frequency can be tuned
via environment variables documented in `README-backend.md`.

## 5. Seed demo data (optional)

To quickly test the UI you can register via the `/register` page in the frontend, or call
`POST /api/auth/register` with an email/password payload. Afterwards log in at `/login` and dodaj
kilka zadań poprzez `/todos/new`.

---

At this point the boilerplate is ready for development. The remaining tasks are entirely optional:

- Configure CI (e.g. GitHub Actions) to run `pytest`, `npm run lint`, and `npm run test`.
- Add production-grade settings (Traefik/NGINX, HTTPS certificates, secrets management).
- Extend the Celery tasks to deliver real notifications (e.g. email/SMS).

If you only need a functional todo app boilerplate, no further setup is required.
