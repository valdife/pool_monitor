#!/usr/bin/env python3
"""
Pool Monitor - Aplikacja do monitorowania liczby osób na basenie
"""

import uvicorn
import sys
import os
from app import app, init_database, scheduler

def print_banner():
    """Wyświetla banner aplikacji"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                    🏊‍♂️ POOL MONITOR 🏊‍♂️                    ║
    ║                                                              ║
    ║  Aplikacja do monitorowania liczby osób na basenie          ║
    ║  w czasie rzeczywistym                                       ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_dependencies():
    """Sprawdza czy wszystkie zależności są zainstalowane"""
    try:
        import fastapi
        import uvicorn
        import sqlite3
        import requests
        import apscheduler
        import jinja2
        print("✅ Wszystkie zależności są zainstalowane")
        return True
    except ImportError as e:
        print(f"❌ Brakująca zależność: {e}")
        print("Zainstaluj zależności: pip install -r requirements.txt")
        return False

def main():
    """Główna funkcja uruchamiająca aplikację"""
    print_banner()

    # Sprawdź zależności
    if not check_dependencies():
        sys.exit(1)

    # Inicjalizuj bazę danych
    print("🗄️  Inicjalizacja bazy danych...")
    init_database()

    # Sprawdź status schedulera
    if scheduler.running:
        print("⏰ Scheduler jest aktywny")
    else:
        print("⚠️  Scheduler nie jest aktywny")

    # Informacje o konfiguracji
    from config import APP_HOST, APP_PORT, POOL_API_URL
    print(f"\n📊 Konfiguracja:")
    print(f"   • Host: {APP_HOST}")
    print(f"   • Port: {APP_PORT}")
    print(f"   • URL endpointu: {POOL_API_URL}")

    print(f"\n🚀 Uruchamianie aplikacji...")
    print(f"   • Aplikacja będzie dostępna pod: http://{APP_HOST}:{APP_PORT}")
    print(f"   • API dokumentacja: http://{APP_HOST}:{APP_PORT}/docs")
    print(f"   • Naciśnij Ctrl+C aby zatrzymać")

    try:
        uvicorn.run(
            app,
            host=APP_HOST,
            port=APP_PORT,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n\n🛑 Zatrzymywanie aplikacji...")
        scheduler.shutdown()
        print("✅ Aplikacja została zatrzymana")

if __name__ == "__main__":
    main()
