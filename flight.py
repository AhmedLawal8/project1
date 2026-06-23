def format_flight_data(flight_data):

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

