#!/usr/bin/env python3
"""
Skrypt testowy do sprawdzenia parsowania danych z endpointu basenu
"""

import json
import re

# Przykładowa odpowiedź z endpointu
sample_response = [
    {
        "title": "Pływalnia Sportowa",
        "content": "Aktualnie na pływalni: 116 osób<br />Maksymalnie: 120 osób",
        "type": "pływalnia sportowa",
        "id": 1,
        "isActive": True,
        "createdAt": "2022-04-29T01:27:21+02:00",
        "updateAt": "2022-04-29T01:27:21+02:00",
        "active": True
    },
    {
        "title": "Pływalnia Rodzinna",
        "content": "Aktualnie na pływalni: 0 osób<br />Maksymalnie: 150 osób",
        "type": "pływalnia rodzinna",
        "id": 2,
        "isActive": True,
        "createdAt": "2022-05-05T23:25:56+02:00",
        "updateAt": "2022-05-05T23:25:56+02:00",
        "active": True
    },
    {
        "title": "Pływalnia Kameralna",
        "content": "Aktualnie na pływalni: 26 osób<br />Maksymalnie: 30 osób",
        "type": "pływalnia kameralna",
        "id": 4,
        "isActive": True,
        "createdAt": "2022-07-31T11:01:56+02:00",
        "updateAt": "2022-07-31T11:01:56+02:00",
        "active": True
    },
    {
        "title": "Lodowisko",
        "content": "Aktualnie na ślizgawce: 0 osób<br />Maksymalnie: 300 osób",
        "type": "lodowisko",
        "id": 5,
        "isActive": True,
        "createdAt": "2022-08-08T09:46:01+02:00",
        "updateAt": "2022-08-08T09:46:01+02:00",
        "active": True
    }
]

def test_parsing():
    """Testuje parsowanie danych z endpointu"""
    print("🧪 Test parsowania danych z endpointu basenu")
    print("=" * 50)

    # Szukamy "Pływalnia Sportowa" w tablicy
    for facility in sample_response:
        if facility.get('title') == 'Pływalnia Sportowa':
            content = facility.get('content', '')
            print(f"✅ Znaleziono: {facility['title']}")
            print(f"📝 Content: {content}")

            # Parsujemy liczbę osób z content
            match = re.search(r'Aktualnie na pływalni: (\d+) osób', content)
            if match:
                people_count = int(match.group(1))
                print(f"👥 Liczba osób: {people_count}")
                return people_count
            else:
                print(f"❌ Nie można sparsować liczby osób z content: {content}")
                return None

    print("❌ Nie znaleziono 'Pływalnia Sportowa' w odpowiedzi")
    return None

def test_different_scenarios():
    """Testuje różne scenariusze"""
    print("\n🔄 Test różnych scenariuszy")
    print("=" * 30)

    scenarios = [
        "Aktualnie na pływalni: 0 osób<br />Maksymalnie: 120 osób",
        "Aktualnie na pływalni: 50 osób<br />Maksymalnie: 120 osób",
        "Aktualnie na pływalni: 120 osób<br />Maksymalnie: 120 osób",
        "Aktualnie na pływalni: 99 osób<br />Maksymalnie: 120 osób"
    ]

    for i, content in enumerate(scenarios, 1):
        match = re.search(r'Aktualnie na pływalni: (\d+) osób', content)
        if match:
            people_count = int(match.group(1))
            print(f"Scenariusz {i}: {people_count} osób")
        else:
            print(f"Scenariusz {i}: Błąd parsowania")

if __name__ == "__main__":
    result = test_parsing()
    test_different_scenarios()

    if result is not None:
        print(f"\n✅ Test zakończony sukcesem! Liczba osób: {result}")
    else:
        print(f"\n❌ Test nie powiódł się")
