import os
import requests
from datetime import datetime

from src.config import GOOGLE_PLACES_API_KEY

def calculate_max_results(start_date_str, end_date_str):

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
        
    calculated_results = duration * 3
    
    # Google Places API (New) maxResultCount must be between 1 and 20
    return min(calculated_results, 20)
      
  except ValueError as e:
      print(f"Error parsing dates: {e}. Defaulting max_results to 10.")
      return 10

def get_top_attractions(lat, lon, start_date, end_date):

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
    "textQuery": f"popular attractions museums parks food experiences",
    "locationBias": {
      "circle": {
        "center": {"latitude": lat, "longitude": lon},
        "radius": 20000
      }
    },
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
