from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import sqlite3
import requests
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import json
import os
from config import *

app = FastAPI(title="Pool Monitor", description="Aplikacja do monitorowania liczby osób na basenie")

# Konfiguracja szablonów HTML
templates = Jinja2Templates(directory="templates")

# Konfiguracja scheduler
scheduler = BackgroundScheduler()
scheduler.start()

def init_database():
    """Inicjalizacja bazy danych"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pool_measurements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME NOT NULL,
            people_count INTEGER NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def fetch_pool_data():
    """Pobiera dane z endpointu basenu"""
    print(f"Próba pobrania danych z: {POOL_API_URL}")
    try:
        response = requests.get(POOL_API_URL, timeout=REQUEST_TIMEOUT)
        print(f"Status odpowiedzi: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print(f"Otrzymano {len(data)} obiektów z endpointu")

            # Szukamy "Pływalnia Sportowa" w tablicy
            for facility in data:
                if facility.get('title') == 'Pływalnia Rodzinna':
                    content = facility.get('content', '')
                    print(f"Znaleziono Pływalnię Rodzinną")
                    print(f"Content: {content}")

                    # Parsujemy liczbę osób z content (format: "Aktualnie na pływalni: X osób")
                    import re
                    match = re.search(r'Aktualnie na pływalni: (\d+) osób', content)
                    if match:
                        people_count = int(match.group(1))
                        print(f"Sparsowano liczbę osób: {people_count}")
                        return people_count
                    else:
                        print(f"Nie można sparsować liczby osób z content: {content}")
                        return None

            print("Nie znaleziono 'Pływalnia Rodzinna' w odpowiedzi")
            print(f"Dostępne obiekty: {[f.get('title', 'Brak tytułu') for f in data]}")
            return None
        else:
            print(f"Błąd podczas pobierania danych: {response.status_code}")
            print(f"Treść odpowiedzi: {response.text[:200]}...")
            return None
    except Exception as e:
        print(f"Błąd podczas pobierania danych: {e}")
        return None

def save_measurement(people_count):
    """Zapisuje pomiar do bazy danych"""
    if people_count is not None:
        print(f"Zapisuję pomiar: {people_count} osób")
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO pool_measurements (timestamp, people_count) VALUES (?, ?)",
            (datetime.now(), people_count)
        )
        conn.commit()
        conn.close()
        print(f"Zapisano pomiar: {people_count} osób o {datetime.now()}")
    else:
        print("Pomiar nie został zapisany (people_count = None)")

def scheduled_task():
    """Zadanie wykonywane przez scheduler"""
    print(f"\nWykonuję zaplanowane zadanie o {datetime.now()}")
    print("=" * 50)

    people_count = fetch_pool_data()
    save_measurement(people_count)

    print("=" * 50)
    print(f"Zadanie zakończone o {datetime.now()}\n")

# Inicjalizacja bazy danych przy starcie
init_database()

# Wykonaj pierwszy pomiar od razu po starcie
scheduled_task()

# Uruchomienie schedulera
scheduler.add_job(
    func=scheduled_task,
    trigger=CronTrigger(hour='7-21', minute='0,30', second='0'),
    id='pool_monitor',
    name=f'Monitor basenu co 30 minut',
    replace_existing=True
)

@app.head("/")
async def root_head():
    """HEAD request dla głównego endpointu - używane przez health checki"""
    return {"status": "ok"}

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Główna strona z wykresem"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/data")
async def get_data():
    """Endpoint API zwracający dane do wykresu"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute(f"""
        SELECT timestamp, people_count
        FROM pool_measurements
        ORDER BY timestamp DESC
        LIMIT {MAX_DISPLAY_MEASUREMENTS}
    """)
    rows = cursor.fetchall()
    conn.close()

    data = []
    for row in rows:
        data.append({
            "timestamp": row[0],
            "people_count": row[1]
        })

    return {"data": data}

@app.post("/api/test")
async def test_measurement():
    """Endpoint do testowania - dodaje losowy pomiar"""
    import random
    people_count = random.randint(0, 50)
    save_measurement(people_count)
    return {"message": f"Dodano testowy pomiar: {people_count} osób"}

@app.get("/api/status")
async def get_status():
    """Status aplikacji i ostatni pomiar"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT timestamp, people_count
        FROM pool_measurements
        ORDER BY timestamp DESC
        LIMIT 1
    """)
    row = cursor.fetchone()
    conn.close()

    # Sprawdź czy URL API jest skonfigurowany
    api_configured = POOL_API_URL != "https://api.example.com/pool/occupancy"

    if row:
        return {
            "last_measurement": {
                "timestamp": row[0],
                "people_count": row[1]
            },
            "scheduler_running": scheduler.running,
            "config": {
                "schedule": "Co 30 minut od 7:00 do 21:00",
                "api_configured": api_configured
            }
        }
    else:
        return {
            "last_measurement": None,
            "scheduler_running": scheduler.running,
            "config": {
                "schedule": "Co 30 minut od 7:00 do 21:00",
                "api_configured": api_configured
            }
        }

@app.get("/ping")
async def ping():
    """Endpoint do pingowania - utrzymuje aplikację aktywną na Render"""
    return {"status": "pong", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=APP_HOST, port=APP_PORT)
