from src.config import SERP_API_KEY
import serpapi


def parse_flights(flight_data):
    flight_options = []

    for flight in flight_data:

        # Extract price and duration
        option = {
            "price": flight.get("price"),
            "duration": flight.get("total_duration"),
            "routes": [],
            "airlines": set(),
        }

        # Flights can have multiple transfers so append each "trip" to routes
        for segment in flight.get("flights", []):
            dep = segment.get("departure_airport", {})
            arr = segment.get("arrival_airport", {})

            trip = {
                "from": dep.get("name"),
                "from_time": dep.get("time"),
                "to": arr.get("name"),
                "to_time": arr.get("time"),
                "airplane": segment.get("airplane", "Unknown"),
                "airline": segment.get("airline", "Unknown"),
            }

            # Add to routes
            option["routes"].append(trip)
            # Store all airlines used
            option["airlines"].add(trip["airline"])

        flight_options.append(option)

    return flight_options


def get_flight_data(origin, destination, from_date, to_date):

    client = serpapi.Client(api_key=SERP_API_KEY)

    outbound_data = client.search(
        {
            "engine": "google_flights",
            "departure_id": origin,
            "arrival_id": destination,
            "currency": "USD",
            "type": "1",
            "outbound_date": from_date,
            "return_date": to_date,
        }
    )

    outbound_options = outbound_data.get("best_flights", [])

    if not outbound_options:
        print("No outbound flights found.")
        return {"outbound": [], "return": []}

    departure_token = outbound_options[0].get("departure_token")
    best_outbound = parse_flights(outbound_options[:1])

    best_return = []

    if departure_token:
        return_data = client.search(
            {
                "engine": "google_flights",
                "departure_id": origin,
                "arrival_id": destination,
                "currency": "USD",
                "type": "1",
                "outbound_date": from_date,
                "return_date": to_date,
                "departure_token": departure_token,
            }
        )

        return_options = return_data.get("best_flights", [])

        if not return_options:
            print("No return flights found. ")
        else:
            best_return = parse_flights(return_options[:1])

    else:
        print("No departure token found, skipping return flight lookup.")

    print("Generated Flight Options Sucess!")
    return {"outbound": best_outbound, "return": best_return}
