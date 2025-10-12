# SvelteFastApiBoilerplate

Kompletny boilerplate aplikacji todo z backendem FastAPI i frontendem SvelteKit. Repozytorium
zawiera konfigurację Docker Compose, prostą autoryzację JWT oraz wieloużytkownikowy moduł zadań.

## Najważniejsze katalogi

- `backend/` – FastAPI, SQLAlchemy, Celery, migracje Alembic.
- `frontend/` – aplikacja SvelteKit, TanStack Query, TailwindCSS.
- `infrastructure/` – pliki Docker Compose dla środowiska deweloperskiego.
- `docs/` – dodatkowe instrukcje (np. `NEXT_STEPS.md`).

## Szybki start

1. Uruchom kontenery: `cd infrastructure && docker compose up -d`.
2. Backend: `cd backend && python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt && alembic upgrade head && uvicorn app.main:app --reload`.
3. Frontend: `cd frontend && npm install && npm run generate:sdk && npm run dev -- --host 0.0.0.0 --port 5173`.

Szczegółowy opis kroków, opcjonalnych zadań Celery oraz dalszych usprawnień znajdziesz w `docs/NEXT_STEPS.md`.
