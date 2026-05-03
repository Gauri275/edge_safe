# Edge-Safe — Offline Emergency Assistant

> An offline-first AI-powered emergency assistant that provides critical guidance without internet connectivity. Runs locally on smartphones and laptops using a quantized AI model.

---

## Table of Contents

- [About](#about)
- [Problem Statement](#problem-statement)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the App](#running-the-app)
- [API Routes](#api-routes)
- [Supported Languages](#supported-languages)
- [Team](#team)

---

## About

Edge-Safe is a fully offline emergency assistant application that works without internet or mobile network connectivity. During disasters, when networks fail, Edge-Safe provides instant first aid guidance, evacuation instructions, nearby shelter information, and multilingual support — all running locally on the device using a quantized LLM via Ollama.

---

## Problem Statement

During disasters such as floods, earthquakes, and fires:
- Internet and mobile networks fail
- People cannot access online emergency apps or chatbots
- Most existing solutions depend entirely on cloud services
- No access to real-time help when it is needed most

**Edge-Safe solves this by running everything locally — AI, database, maps, and translation.**

---

## Features

| Feature | Description |
|---|---|
| Fully Offline | Works with zero internet or mobile network |
| On-device AI | Quantized TinyLLaMA model via Ollama |
| First Aid DB | SQLite database with 30+ verified emergency entries |
| 7 Languages | English, Hindi, Marathi, Malayalam, Tamil, Telugu, Kannada |
| Voice Input | Speak queries in your language |
| Text-to-Speech | Response read aloud in your language |
| Offline Maps | Preloaded OpenStreetMap tiles with shelter pins |
| Evacuation Info | Preloaded routes for flood, fire, earthquake |
| Shelter Finder | Nearest relief camps shown on map |
| Disaster Modes | General, Medical, Flood, Fire, Earthquake |
| Two-tier Translation | Hardcoded phrases (instant) + AI fallback |
| No Login Required | Opens instantly, no account needed |

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Flutter (Android/iOS) |
| Backend | Python + Flask |
| AI Runtime | Ollama (TinyLLaMA quantized) |
| Database | SQLite |
| Translation | Hardcoded dictionary + Ollama AI |
| Maps | Folium + OpenStreetMap preloaded tiles |
| Voice | Flutter speech_to_text + flutter_tts |

---

## Project Structure

```
edge-safe/
├── .gitignore
├── README.md
├── backend/
│   ├── app.py                  ← Main Flask server (all API routes)
│   ├── database.py             ← SQLite connection and query functions
│   ├── ai_service.py           ← Ollama AI communication
│   ├── translator_service.py   ← Offline translation (hardcoded + AI)
│   ├── map_service.py          ← Offline map generation with Folium
│   ├── db_seed.py              ← Seeds emergency data into SQLite
│   ├── reset_db.py             ← Resets and re-creates database
│   ├── download_map_tiles.py   ← Downloads OSM tiles for offline maps
│   ├── check_all.py            ← Full system health checker
│   ├── test.http               ← API test file for VS Code REST Client
│   ├── emergency.db            ← SQLite database (auto-generated)
│   └── static/
│       ├── maps/               ← Generated HTML map files
│       └── tiles/              ← Preloaded OpenStreetMap tiles
└── frontend/
    ├── pubspec.yaml
    └── lib/
        ├── main.dart
        ├── utils/
        │   └── constants.dart
        ├── services/
        │   ├── api_service.dart
        │   ├── voice_service.dart
        │   └── prefs_service.dart
        ├── screens/
        │   ├── splash_screen.dart
        │   ├── main_screen.dart
        │   ├── home_screen.dart
        │   ├── map_screen.dart
        │   ├── firstaid_screen.dart
        │   └── settings_screen.dart
        └── widgets/
            ├── mode_selector.dart
            ├── response_card.dart
            └── language_picker.dart
```

---

## Prerequisites

Make sure these are installed before starting:

| Tool | Version | Download |
|---|---|---|
| Python | 3.11+ | https://python.org |
| Flutter | 3.x | https://flutter.dev |
| Ollama | Latest | https://ollama.ai |
| VS Code | Latest | https://code.visualstudio.com |
| Android Studio | Latest | https://developer.android.com/studio |
| Git | Latest | https://git-scm.com |

---

## Installation

### Step 1 — Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/edge-safe.git
cd edge-safe
```

### Step 2 — Set up Python virtual environment

```bash
cd backend
python -m venv venv

# Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# Windows (Command Prompt)
venv\Scripts\activate

# Mac / Linux
source venv/bin/activate
```

### Step 3 — Install Python dependencies

```bash
pip install flask flask-cors requests folium
```

### Step 4 — Pull Ollama AI model

```bash
# Install Ollama from https://ollama.ai first, then:
ollama pull tinyllama
```

### Step 5 — Seed the database

```bash
cd backend
python db_seed.py
```

Expected output:
```
Tables created successfully.
Database seeded successfully at: emergency.db
  First aid entries: 29
  Shelters: 8
  Evacuation routes: 6
```

### Step 6 — Install Flutter dependencies

```bash
cd ../frontend
flutter pub get
```

### Step 7 — Download offline map tiles (optional)

```bash
cd backend
python download_map_tiles.py
```

---

## Running the App

You need **two terminals** running simultaneously.

### Terminal 1 — Start Flask backend

```bash
cd backend
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
python app.py
```

You should see:
```
Starting Edge-Safe backend on http://localhost:5000
 * Running on http://0.0.0.0:5000
```

### Terminal 2 — Start Flutter app

```bash
cd frontend
flutter run
```

> **Note for real device:** Change `baseUrl` in `lib/utils/constants.dart` from `10.0.2.2` to your PC's local IP address (e.g., `192.168.1.5`). Both devices must be on the same WiFi.

---

## API Routes

| Method | Route | Description |
|---|---|---|
| GET | `/health` | Check backend and Ollama status |
| GET | `/firstaid?q=choking&lang=en` | Search first aid by condition |
| GET | `/shelters?city=Solapur` | Get nearby shelters |
| GET | `/evacuation?type=flood&lang=en` | Get evacuation instructions |
| POST | `/ask` | Main emergency query (DB first, then AI) |
| POST | `/ask_translated` | Query with auto-translation |
| POST | `/translate` | Translate any text offline |
| GET | `/map?type=flood&city=Solapur` | Get offline shelter map HTML |
| GET | `/evacmap?type=flood&city=Solapur` | Get evacuation route map |
| GET | `/languages` | List supported languages |

### Example request

```bash
curl -X POST http://localhost:5000/ask \
  -H "Content-Type: application/json" \
  -d '{"query": "someone is bleeding", "mode": "medical", "lang": "en", "city": "Solapur"}'
```

### Example response

```json
{
  "answer": "1. Apply firm direct pressure using a clean cloth...",
  "source": "database",
  "confidence": "high",
  "shelters": [],
  "lang": "en"
}
```

---

## Supported Languages

| Language | Code | Voice Input | TTS Output | DB Entries |
|---|---|---|---|---|
| English | en | Yes | Yes | 10+ |
| Hindi | hi | Yes | Yes | 3+ |
| Marathi | mr | Yes | Yes | 3+ |
| Malayalam | ml | Yes | Yes | 3+ |
| Tamil | ta | Yes | Yes | 3+ |
| Telugu | te | Yes | Yes | 3+ |
| Kannada | kn | Yes | Yes | 3+ |

**Translation flow:**
```
User speaks in Malayalam
       ↓
Translated to English (hardcoded dict / Ollama)
       ↓
Searched in SQLite DB or answered by AI
       ↓
Answer translated back to Malayalam
       ↓
Displayed + spoken aloud via TTS
```

---

## System Health Check

Run the automated checker to verify all components:

```bash
cd backend
python check_all.py
```

Expected output:
```
=======================================================
Edge-Safe Full System Check
=======================================================
  PASS  Health check
  PASS  Ollama online
  PASS  First aid EN
  PASS  First aid HI
  ...
=======================================================
PASSED: 24  |  WARNED: 0  |  FAILED: 0
=======================================================
```

---

## How It Works

```
User opens app (no internet needed)
          ↓
Types or speaks query in their language
          ↓
Voice → translated to English via hardcoded dict
          ↓
SQLite DB searched first (fast, verified)
          ↓ not found
Ollama TinyLLaMA AI answers locally
          ↓
Answer translated back to user language
          ↓
Response shown + read aloud via TTS
          ↓
Offline map shows nearby shelters
```

---

## Team

| Member | Role |
|---|---|
| Member A | AI Backend — Ollama integration, ai_service.py |
| Member B | Database — SQLite schema, db_seed.py, emergency data |
| Member C | Frontend — Flutter UI, voice input, map screen |
| Member D | Testing, documentation, deployment, viva prep |

---

## Acknowledgements

- [Ollama](https://ollama.ai) — Local AI model runtime
- [TinyLLaMA](https://github.com/jzhang38/TinyLlama) — Quantized language model
- [OpenStreetMap](https://openstreetmap.org) — Offline map tiles
- [Folium](https://python-visualization.github.io/folium/) — Map generation
- [Flutter](https://flutter.dev) — Cross-platform frontend

---

## License

This project is developed for academic purposes.  
Amity University Mumbai / College Submission — 2026.
