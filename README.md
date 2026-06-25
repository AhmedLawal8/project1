# project1

Want to be able to generate a full itinerary given:
- Duration (xx/xx/xxxx - xx/xx/xxxx)
- Location (What airport are you flying out of? to?[city])
- Budget (in usd?)


APIs?
- Places API (Google Maps API)
- Flight API (SerpAPI)
- Weather API (OpenWeather)
- Hotel API (SerpAPI)


## Step-by-Step Process

- [x] Work on flights.py and create the function to parse serpAPI response for available flights data
- [x] Get user input for airport departure and origin along with corresponding dates
- [x] Integrate weather API(destination weather based on travel dates), (simple data forecast summary (temp + conditions))
- [x] Integrate Places API (Google Maps) (Fetch top attractions for destination), (Fetch restaurants + key landmarks)
- [ ] Build Data Context layer (Combine flights + weather + places into one structured object)
- [ ] Design GenAI prompt + schema (Define Input format) ( Design output format)
- [ ] Define database-ready data structure (Mainly summaries) (Will maybe update to refactor for users)

# Waypoint

Waypoint is a CLI App that generates personalized travel itineraries. Waypoint combines real-time flight availability, destination weather forecasts, local attraction data, and Google's Generative AI API to ouptput structured and readable travel plans directly into terminal.

## Features

* **Flight Integration:** Fetches real-time flight data based on origin and destination IATA codes (e.g. ATL, HND)
* **Weather Forecasting:** Provides weather condition summaries tailored to your travel dates and locations
* **Local Attractions:** Retrieves top landmarks, attractions, and restaurants for your destination.
* **AI-Powered itineraries:** Combines all data into a cohesive daily itinerary using a GenAI context layer.
* **Rich Terminal UI:** Utilizes the 'rich' library to render readable markdown and console outputs.

## APIs

This project relies on the following APIs to aggregate travel data:
* **Serp API:** Parses available flight data.
* **Google Places API:** Fetches top attractions and local points of interest.
* **Google GenAI API:** Generates the final summary and itinerary.
* **OpenWeather API:** Retrieves destination weather forecasts.

## Getting Started

### Prerequisites
* Python Installation
* Dependencies
* Valid API Keys

### Installation
  git clone https://github.com/AhmedLawal8/project1.git
  cd project1