# Pool Monitor 🏊‍♂️

Aplikacja do monitorowania liczby osób na basenie w czasie rzeczywistym.

## Funkcjonalności

- **Automatyczne pomiary** - co 30 minut od 7:00 do 21:00
- **Baza danych SQLite** - przechowywanie historycznych danych
- **Interaktywny wykres** - wizualizacja danych z Chart.js
- **Statystyki** - ostatni pomiar, średnia, maksimum
- **API REST** - dostęp do danych przez endpointy
- **Nowoczesny UI** - responsywny interfejs webowy
- **Bezpieczeństwo** - URL API ukryty w zmiennych środowiskowych

## Instalacja

1. **Sklonuj repozytorium:**
```bash
git clone <repository-url>
cd pool_monitor
```

2. **Zainstaluj zależności:**
```bash
pip install -r requirements.txt
```

3. **Skonfiguruj endpoint basenu:**
   - Utwórz plik `.env` na podstawie `.env.example`
   - Ustaw `POOL_API_URL` na właściwy URL endpointu basenu
   - Lub ustaw zmienną środowiskową `POOL_API_URL`

## Uruchomienie

```bash
python start.py
```

Aplikacja będzie dostępna pod adresem: http://localhost:8000

## Konfiguracja

Główne ustawienia w pliku `config.py`:

- `POOL_API_URL` - URL endpointu basenu (ze zmiennej środowiskowej)
- `APP_PORT` - port aplikacji (automatycznie z Render)
- `MAX_DISPLAY_MEASUREMENTS` - liczba pomiarów na wykresie

## Bezpieczeństwo

- **URL API jest ukryty** w zmiennych środowiskowych
- **Nie jest widoczny** w kodzie źródłowym
- **Można go zmienić** bez modyfikacji kodu
- **Bezpieczne deploymenty** na Render/Heroku

## API Endpoints

- `GET /` - Główna strona z wykresem
- `GET /api/data` - Dane do wykresu (ostatnie 48 pomiarów)
- `POST /api/test` - Dodaj testowy pomiar
- `GET /api/status` - Status aplikacji i ostatni pomiar
- `GET /ping` - Endpoint do pingowania (dla Render)

## Struktura bazy danych

```sql
CREATE TABLE pool_measurements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME NOT NULL,
    people_count INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## Funkcje

### Automatyczne pomiary
- Scheduler uruchamia się co 30 minut od 7:00 do 21:00
- Pobiera dane z konfigurowanego endpointu
- Zapisuje wyniki do bazy SQLite

### Wizualizacja
- Interaktywny wykres liniowy
- Statystyki w czasie rzeczywistym
- Automatyczne odświeżanie co 5 minut

### Testowanie
- Przycisk "Dodaj testowy pomiar" generuje losowe dane
- Przydatne do testowania bez prawdziwego endpointu

## Rozwój

Aplikacja jest napisana w Python z użyciem:
- **FastAPI** - nowoczesny framework webowy
- **SQLite** - lekka baza danych
- **APScheduler** - planowanie zadań
- **Chart.js** - wykresy JavaScript
- **Jinja2** - szablony HTML

## Licencja

MIT License
