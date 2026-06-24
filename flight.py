from config import SERP_API_KEY
import serpapi

def get_flight_data(origin, destination, from_date, to_date):

  client = serpapi.Client(api_key=SERP_API_KEY)
  
  flight_data = client.search({
    "engine": "google_flights",
    "departure_id": origin,
    "arrival_id": destination,
    "currency": "USD",
    "type": "1",
    "outbound_date": from_date,
    "return_date" : to_date
  })
 
  flight_options = []

  for flight in flight_data.get("best_flights", []):
    
    #Extract price and duration
    option = {
      "price" : flight.get("price"),
      "duration" : flight.get("total_duration"),
      "routes" : [],
      "airlines" : set()
    }

    #Flights can have multiple transfers so append each "trip" to routes
    for segment in flight.get("flights", []):
      dep = segment.get("departure_airport", {})
      arr = segment.get("arrival_airport", {})

      trip = {
        "from" : dep.get("name"),
        "from_time" : dep.get("time"),
        "to" : arr.get("name"),
        "to_time" : arr.get("time"),
        "airplane" : segment.get("airplane", "Unknown"),
        "airline" : segment.get("airline", "Unknown")
      }

      #Add to routes
      option["routes"].append(trip)
      #Store all airlines used
      option["airlines"].add(trip["airline"])


    flight_options.append(option)

  return flight_options