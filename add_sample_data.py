#!/usr/bin/env python3
"""
Skrypt do dodawania przykładowych danych historycznych do bazy danych
"""

import sqlite3
from datetime import datetime, timedelta
import random
from config import DATABASE_PATH

def add_sample_data():
    """Dodaje przykładowe dane z ostatnich 24 godzin"""

    # Połączenie z bazą danych
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # Sprawdź czy tabela istnieje
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pool_measurements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME NOT NULL,
            people_count INTEGER NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Generuj dane z ostatnich 24 godzin (co 30 minut)
    end_time = datetime.now()
    start_time = end_time - timedelta(hours=24)

    current_time = start_time
    measurements_added = 0

    print("Dodawanie przykładowych danych...")

    while current_time <= end_time:
        # Generuj realistyczne dane (więcej osób w godzinach 6-22, mniej w nocy)
        hour = current_time.hour

        if 6 <= hour <= 22:
            # Godziny otwarcia - więcej osób
            base_count = random.randint(10, 40)
            # Dodaj losowość
            people_count = max(0, base_count + random.randint(-5, 10))
        else:
            # Godziny nocne - mniej osób
            people_count = random.randint(0, 5)

        # Dodaj pomiar do bazy
        cursor.execute(
            "INSERT INTO pool_measurements (timestamp, people_count) VALUES (?, ?)",
            (current_time, people_count)
        )

        measurements_added += 1
        current_time += timedelta(minutes=30)

    # Zatwierdź zmiany
    conn.commit()
    conn.close()

    print(f"✅ Dodano {measurements_added} przykładowych pomiarów")
    print(f"   • Okres: {start_time.strftime('%Y-%m-%d %H:%M')} - {end_time.strftime('%Y-%m-%d %H:%M')}")
    print(f"   • Częstotliwość: co 30 minut")
    print(f"   • Zakres osób: 0-50")

if __name__ == "__main__":
    add_sample_data()
