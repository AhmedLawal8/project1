from datetime import datetime
import os
import sys

import pandas as pd
import serpapi
from dotenv import load_dotenv

from flight import get_flight_data
from places import calculate_max_results, get_top_attractions
from weather import get_weather

def main():

  #Store Airport DataFrame 
  try:
    df = pd.read_csv("iata-icao.csv").set_index("iata")  

  except Exception as e:
    print("Error Opening File: ", e)
    sys.exit(1)

  valid_airport_names = set(df.index.dropna().str.upper())

  print("=" * 30) 
  print("|   Welcome to Waypoint!!!   |")
  print("=" * 30) 

  origin = validate_code("What airport are you departing from (e.g. JFK): ", valid_airport_names)
  destination = validate_code("What airport are you arriving at (e.g. LGA): ", valid_airport_names)

  while True:
    from_date = input("When do you plan on leaving (yyyy-mm-dd): ").strip()
    to_date = input("When do you plan on returning (yyyy-mm-dd): ").strip()

    from_date_obj = validate_date(from_date)
    to_date_obj = validate_date(to_date)
    if not from_date_obj or not to_date_obj:
      print("Invalid Date format. Please use yyyy-mm-dd")
    elif from_date_obj >= to_date_obj:
      print("Return Date must be after departure date")
    else:
      break
  
  budget = validate_budget("Enter your budget: $")
  
  data = get_flight_data(origin, destination, from_date, to_date)
  
  print(data)
  print(get_top_attractions(destination, from_date, to_date))

  #Origin airport location data 0 for lat 1 for lon
  location_origin = get_lat_lon(df, origin)
  location_destination = get_lat_lon(df, destination)

  #location_origin[0] for lat & location_origin[1] for lon
  weather_origin = get_weather(from_date, from_date, location_origin[0], location_origin[1], origin)
  weather_destination = get_weather(from_date, to_date, location_destination[0], location_destination[1], destination)
  print(weather_origin)
  print(weather_destination)

  
def validate_code(text, valid_airport_names):

  while True:
    code = input(text).strip().upper()
    if code not in valid_airport_names:
      print("Enter a valid airport code")
    else:
      return code

def validate_date(date_str):
  try:
    return datetime.strptime(date_str, "%Y-%m-%d")  
  except ValueError:
    return None

def validate_budget(text):
  while True:
    try:
      budget = float(input(text).strip())
      if budget <= 0:
        print("Budget must be greater than 0")
      else:
        return budget
    except ValueError:
      print("Enter a valid number")

def get_lat_lon(df, code):
  lat = df.loc[code, "latitude"]
  lon = df.loc[code, "longitude"]
  return lat, lon

main()