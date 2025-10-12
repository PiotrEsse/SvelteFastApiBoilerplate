# Frontend (SvelteKit)

Nowy frontend korzysta z SvelteKit, TanStack Query oraz TailwindCSS/Flowbite. Poniżej znajdziesz
informacje potrzebne do uruchomienia aplikacji oraz krótki przewodnik po dostępnych funkcjach.

## Wymagania

- Node.js 18+
- npm (zalecane) – możesz oczywiście skorzystać z pnpm lub yarn, ale wszystkie przykłady używają `npm`

## Instalacja zależności

```bash
cd frontend
npm install
```

## Generowanie SDK

W repozytorium backendu dostępny jest plik OpenAPI. Aby zsynchronizować typy i klienta API, uruchom:

```bash
npm run generate:sdk
```

Domyślnie komenda korzysta z endpointu `http://localhost:8000/openapi.json` i wygeneruje aktualnego
klienta w katalogu `src/lib/api`.

## Uruchamianie środowiska deweloperskiego

```bash
npm run dev -- --host 0.0.0.0 --port 5173
```

Aplikacja domyślnie nasłuchuje na porcie `5173`. Backend FastAPI powinien działać równolegle na
porcie `8000`, aby zapytania API mogły być obsługiwane.

## Budowanie produkcyjne

```bash
npm run build
```

Zbudowana aplikacja trafi do katalogu `.svelte-kit/output`. Możesz ją podglądnąć poleceniem `npm run preview`.

## Demo logowania

Domyślne punkty końcowe backendu FastAPI pozwalają na utworzenie konta testowego poprzez stronę
`/register`. Po pomyślnej rejestracji zostaniesz przekierowany na stronę logowania. Jeśli na backendzie
istnieje już konto demo (np. `demo@example.com` / `demo1234`), możesz użyć tych danych na stronie
`/login`. Po zalogowaniu dostępna jest lista zadań (`/todos`), formularz tworzenia (`/todos/new`) oraz
edycji (`/todos/[id]`).

Formularze korzystają z walidacji Zod, a zapytania do backendu wykonywane są przez TanStack Query,
co zapewnia cache'owanie danych oraz optymistyczne odświeżanie listy zadań.
