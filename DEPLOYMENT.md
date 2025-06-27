# Deployment na Render

## Krok 1: Przygotuj repozytorium GitHub

1. Utwórz nowe repozytorium na GitHub
2. Wypchnij kod:
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/TWOJA_NAZWA/pool_monitor.git
git push -u origin main
```

## Krok 2: Skonfiguruj Render

1. Przejdź na [render.com](https://render.com)
2. Zarejestruj się/zaloguj
3. Kliknij "New +" → "Web Service"
4. Podłącz swoje repozytorium GitHub
5. Wybierz repozytorium `pool_monitor`

## Krok 3: Konfiguracja aplikacji

**Nazwa:** `pool-monitor` (lub inna)
**Środowisko:** `Python 3`
**Build Command:** `pip install -r requirements.txt`
**Start Command:** `uvicorn app:app --host 0.0.0.0 --port $PORT`

## Krok 4: Zmienne środowiskowe (WAŻNE!)

W sekcji "Environment Variables" dodaj:

**POOL_API_URL** = `https://miejskoaktywni.pl/api/activities_table_items`

To ukryje prawdziwy URL API przed użytkownikami!

## Krok 5: Uruchom deployment

1. Kliknij "Create Web Service"
2. Poczekaj na zakończenie builda (2-3 minuty)
3. Aplikacja będzie dostępna pod adresem: `https://pool-monitor.onrender.com`

## Krok 6: Skonfiguruj monitoring (WAŻNE!)

Aby aplikacja nie była wyłączana, skonfiguruj UptimeRobot:

1. Przejdź na [uptimerobot.com](https://uptimerobot.com)
2. Zarejestruj się (darmowe)
3. Dodaj nowy monitor:
   - **Typ:** HTTP(s)
   - **URL:** `https://pool-monitor.onrender.com/ping`
   - **Interwał:** 5 minut
   - **Alert:** Email (opcjonalnie)

## Testowanie

1. Sprawdź główną stronę: `https://pool-monitor.onrender.com`
2. Sprawdź API: `https://pool-monitor.onrender.com/api/status`
3. Sprawdź ping: `https://pool-monitor.onrender.com/ping`

## Bezpieczeństwo

- URL API jest ukryty w zmiennych środowiskowych
- Nie będzie widoczny w kodzie źródłowym
- Można go zmienić bez modyfikacji kodu

## Koszty

- **Render:** Darmowe 750h/miesiąc (wystarczy na 24/7)
- **UptimeRobot:** Darmowe 50 monitorów
- **Łącznie:** Darmowe!

## Rozwiązywanie problemów

1. **Aplikacja się nie uruchamia:**
   - Sprawdź logi w Render Dashboard
   - Upewnij się, że wszystkie pliki są w repozytorium

2. **Błąd bazy danych:**
   - Render tworzy nową bazę przy każdym restarcie
   - Dane będą resetowane

3. **Aplikacja jest wyłączana:**
   - Sprawdź czy UptimeRobot pinguje `/ping`
   - Zwiększ interwał pingowania do 3 minut

4. **Nie pobiera danych z API:**
   - Sprawdź czy zmienna POOL_API_URL jest ustawiona w Render
   - Sprawdź logi aplikacji
