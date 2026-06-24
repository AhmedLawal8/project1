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
- [ ] Integrate Places API (Google Maps) (Fetch top attractions for destination), (Fetch restaurants + key landmarks)
- [ ] Build Data Context layer (Combine flights + weather + places into one structured object)
- [ ] Design GenAI prompt + schema (Define Input format) ( Design output format)
- [ ] Define database-ready data structure (Mainly summaries) (Will maybe update to refactor for users)

