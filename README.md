# Waypoint - AI Travel Partner

## Overview

Waypoint is an AI-powered travel planning agent that generates a full, personalized itinerary from just a few inputs. 
Tell it where you're going and when and it handles the rest, pulling real flight data, local weather forecasts, and top 
attractions to build a day-by-day plan that actually makes sense. Maybe this trip will finally make it out of the gc.

---

## What it does

Give Waypoint:
 
- A departure airport
- A destination airport
- Your travel dates

It helps you plan multiple trips from start to finish and allows you to save them for later retrieval.

From this, users can see a customized itinerary using flight data, weather data, attractions at destination, and reasoning.

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/AhmedLawal8/project1.git
cd project1
```

### 2. Set up API Keys

```bash
cp .env.example .env
```

Then open `.env` and fill in your keys. You'll need four:

| API | What it's for | Link |
|-----|--------------|------|
| SerpApi | Flight data | https://serpapi.com/google-flights-api |
| Visual Crossing | Weather forecasts | https://www.visualcrossing.com/weather-api |
| Google Places | Attractions at destination | https://developers.google.com/maps/documentation/places/web-service/overview |
| Google GenAI | Itinerary generation | https://ai.google.dev/gemini-api/docs |

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

From the project root:

```bash
python main.py
```

## Usage

**Step 1 - Enter a username**
 
Waypoint uses your username to save and retrieve itineraries. If it's your first time, a profile gets created automatically. 
Come back with the same username and your past itineraries are waiting for you.

> **Heads up:** There's no authentication - this was intentional to keep things simple. Pick something unique 

so you don't accidentally collide with another user's profile.
Try to choose a unique username, as duplicates may overwrite or mix results. This was intentional to keep the project simple and fun.

**Step 2 - Enter your trip details**
 
- Departure airport code (e.g. `JFK`)
- Destination airport code (e.g. `LAX`)
- Departure date
- Return date

Not sure of your airport code? Check `iata-icao.csv` in the project root for the full list.
 
**Step 3 - Get your itinerary**

Waypoint fetches everything in the background and hands you back a structured day-by-day plan.

## Project Structure
project1/
│
├── main.py
├── requirements.txt
├── requirements-dev.txt
├── .env.example
├── iata-icao.csv
├── README.md
│
├── src/
│   ├── config.py
│   ├── db.py
│   ├── flight.py
│   ├── genai.py
│   ├── weather.py
│   └── places.py
│
├── tests/
│   ├── test_db.py
│   ├── test_date_validation.py
│   └── ...
│
└── waypoint.db

## Testing 
Run all unit tests fromt he project root:

```bash
python -m unittest discover -s tests
```

### Whats Next
A few things on the radar for future iterations - factoring in user interests for better personalization, maybe a proper frontend, and even multi-city trip support. 

***Till Next Time!***






