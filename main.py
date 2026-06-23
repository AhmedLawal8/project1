import flight
import serpapi


print("Welcome to Waypoint")
#Ensure that origin and detination have only 3 letters
origin = input("What airport are you departing from (e.g. JFK): ")
destination = input("What airport are you arriving at (e.g. LAG): ")
#Format in date
from_date = input("When do you plan on leaving (yyyy-mm-dd): ")
to_date = input("When do you plan on returning (yyyy-mm-dd): ")
budget = int(input("What is your budget: $"))
print(type(budget))

client = serpapi.Client(api_key="")
results = client.search({
  "engine": "google_flights",
  "departure_id": "CDG",
  "arrival_id": "AUS",
  "currency": "USD",
  "type": "2",
  "outbound_date": "2026-06-24"
})
best_flights = results["best_flights"]

print(best_flights)
