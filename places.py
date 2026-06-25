import os
import requests
from datetime import datetime

from config import GOOGLE_PLACES_API_KEY

def calculate_max_results(start_date_str: str, end_date_str: str):
    """
    Calculates max_results as 2 * duration of the trip in days.
    Caps the result at 20 due to Google Places API constraints.
    """
    try:
        # Parse the YYYY-MM-DD date strings
        date_format = "%Y-%m-%d"
        start_date = datetime.strptime(start_date_str, date_format)
        end_date = datetime.strptime(end_date_str, date_format)
        
        # Calculate duration in days
        duration = (end_date - start_date).days
        
        # Ensure duration is at least 1 day to avoid 0 results
        if duration <= 0:
            duration = 1
            
        calculated_results = duration * 2
        
        # Google Places API (New) maxResultCount must be between 1 and 20
        return min(calculated_results, 20)
        
    except ValueError as e:
        print(f"Error parsing dates: {e}. Defaulting max_results to 10.")
        return 10

def get_top_attractions(airport_code: str, start_date: str, end_date: str):
    """
    Fetches top attractions for the city served by a given airport code.
    The number of results fetched scales with the length of the trip.
    
    Args:
        airport_code (str): The 3-letter IATA airport code (e.g., "JFK").
        start_date (str): Departure date in "YYYY/MM/DD" format.
        end_date (str): Return date in "YYYY/MM/DD" format.
        
    Returns:
        A list of dictionaries containing attraction details.
    """

    # Calculate dynamic max results based on trip duration
    max_results = calculate_max_results(start_date, end_date)
    print(f"Trip duration calculated. Fetching up to {max_results} attractions...")

    url = "https://places.googleapis.com/v1/places:searchText"

    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": GOOGLE_PLACES_API_KEY,
        "X-Goog-FieldMask": "places.displayName,places.formattedAddress,places.rating,places.userRatingCount,places.priceLevel,places.types"
    }

    payload = {
        "textQuery": f"top tourist attractions in the primary city served by {airport_code} airport",
        "languageCode": "en",
        "maxResultCount": max_results
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()

        attractions = []
        for place in data.get("places", []):
            name = place.get("displayName", {}).get("text", "Unknown")
            address = place.get("formattedAddress", "No address available")
            rating = place.get("rating", "N/A")
            total_ratings = place.get("userRatingCount", 0)
            price_level = place.get("priceLevel", "PRICE_LEVEL_UNSPECIFIED")
            types = place.get("types", [])

            attractions.append({
                "name": name,
                "address": address,
                "rating": rating,
                "total_ratings": total_ratings,
                "price_level": price_level,
                "types": types
            })

        return attractions

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from Google Places API: {e}")
        return []

# if __name__ == "__main__":
#     # Test case: 4-day trip should equal 8 results
#     test_airport = "JFK"
#     start = "2026-07-01"
#     end = "2026-07-05"
    
#     results = get_top_attractions(test_airport, start, end)
#     print(f"\nFound {len(results)} attractions:")
#     for idx, place in enumerate(results, 1):
#         print(f"{idx}. {place['name']} ({place['price_level']})")