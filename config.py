# Konfiguracja aplikacji monitorującej basen
import os

# URL endpointu basenu (ze zmiennej środowiskowej lub domyślny)
POOL_API_URL = os.environ.get("POOL_API_URL", "https://api.example.com/pool/occupancy")

# Timeout dla zapytań HTTP (w sekundach)
REQUEST_TIMEOUT = 10

# Ścieżka do bazy danych
DATABASE_PATH = "pool_data.db"

# Port na którym będzie działać aplikacja (z Render używa zmiennej środowiskowej)
APP_PORT = int(os.environ.get("PORT", 8000))

# Host aplikacji
APP_HOST = "0.0.0.0"

# Maksymalna liczba pomiarów do wyświetlenia na wykresie
MAX_DISPLAY_MEASUREMENTS = 48
