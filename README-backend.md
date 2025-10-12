# Backend

## Uruchamianie aplikacji

1. Wejdź do katalogu `backend` i skopiuj plik konfiguracyjny: `cp .env.example .env` (na Windows `copy .env.example .env`).
2. Utwórz i aktywuj środowisko wirtualne: `python -m venv .venv && source .venv/bin/activate`.
3. Zainstaluj zależności: `pip install -r requirements.txt`.
4. Wykonaj migracje bazy: `alembic upgrade head`.
5. Uruchom serwer API FastAPI: `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`.

## Zadania asynchroniczne

Do obsługi powiadomień o zbliżających się terminach wykorzystywany jest Celery. W pliku `.env`
określ adres brokera (`CELERY_BROKER_URL`) oraz backend (`CELERY_RESULT_BACKEND`).

### Uruchamianie workera i harmonogramu

Aby przetwarzać zadania oraz harmonogram (Celery Beat) uruchom:

```bash
celery -A app.celery_app worker -B
```

Polecenie uruchom z katalogu `backend`, tak aby moduł `app.celery_app` był dostępny na ścieżce Pythona. Harmonogram domyślnie sprawdza zadania z terminem w ciągu kolejnych 60 minut, interwał można zmienić ustawiając zmienną środowiskową `REMINDER_INTERVAL_MINUTES`.

## Ręczne wywołanie przypomnień

Na potrzeby testów dostępny jest endpoint `POST /api/todos/trigger-reminders`, który uruchamia zadanie przypomnień i zwraca identyfikator zadania Celery.
