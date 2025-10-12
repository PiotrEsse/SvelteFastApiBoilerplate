# Backend

## Uruchamianie aplikacji

1. Zainstaluj zależności (np. `pip install -r requirements.txt`).
2. Ustaw wymagane zmienne środowiskowe (np. `DATABASE_URL`, `CELERY_BROKER_URL`).
3. Uruchom serwer API FastAPI: `uvicorn app.main:app --reload` (polecenie wykonuj z katalogu `backend`).

## Zadania asynchroniczne

Do obsługi powiadomień o zbliżających się terminach wykorzystywany jest Celery.

### Uruchamianie workera i harmonogramu

Aby przetwarzać zadania oraz harmonogram (Celery Beat) uruchom:

```bash
celery -A app.celery_app worker -B
```

Polecenie uruchom z katalogu `backend`, tak aby moduł `app.celery_app` był dostępny na ścieżce Pythona. Harmonogram domyślnie sprawdza zadania z terminem w ciągu kolejnych 60 minut, interwał można zmienić ustawiając zmienną środowiskową `REMINDER_INTERVAL_MINUTES`.

## Ręczne wywołanie przypomnień

Na potrzeby testów dostępny jest endpoint `POST /api/todos/trigger-reminders`, który uruchamia zadanie przypomnień i zwraca identyfikator zadania Celery.
