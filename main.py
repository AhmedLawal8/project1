from datetime import datetime
import os
import sys

import pandas as pd
import serpapi
from dotenv import load_dotenv

from flight import get_flight_data
from places import calculate_max_results, get_top_attractions
from weather import get_weather
from genai import generate_itinerary
from db import make_db, insert_itinerary, get_list_of_itineraries, get_itinerary, get_user

from rich.console import Console
from rich.markdown import Markdown


def main():
  console = Console()
  #Store Airport DataFrame 
  df = load_airports()

  valid_airport_names = set(df.index.dropna().str.upper())

  print("=" * 30) 
  print("|   Welcome to Waypoint!!!   |")
  print("=" * 30) 

  print("\nWhat is your username: ")
  user = input("> ")

  #Get sesison to query db
  session = make_db()

  exists = get_user(session, user)

  print("\nSearching...")

  #If user exists display amount of itineraries and main option
  if exists:

    print(f"\nWelcome Back {user}!")

    ans = 0
    while ans != 3:
      
      count = get_itineraries_count(session, user)
      print(f"You have {count} saved itineraries.")
      
      try:
        ans = int(input("Choice: \n>").strip())
      except ValueError:
        print("Enter a valid number")
      
      if not 1 <= ans <= 3:
        print("Choose 1, 2 or 3")
        continue

      print("\n1. Create an itinerary")
      print("2. View Itineraries")
      print("3. Exit")

      match ans:
        case 1:
          create_itinerary()
        case 2:
          view_itineraries()

      





def load_airports():
  try:
    df = pd.read_csv("iata-icao.csv").set_index("iata")  
    return df
  except Exception as e:
    print("Error Opening File: ", e)
    sys.exit(1)

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

def get_lat_lon(df, code):
  lat = df.loc[code, "latitude"]
  lon = df.loc[code, "longitude"]
  return lat, lon

def create_itinerary(session, username):
  origin = validate_code("What airport are you departing from (e.g. JFK): ", valid_airport_names)
  destination = validate_code("What airport are you arriving at (e.g. LAX): ", valid_airport_names)

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

  flight_data = get_flight_data(origin, destination, from_date, to_date)
  places = get_top_attractions(destination, from_date, to_date)

  location_origin = get_lat_lon(df, origin)
  location_destination = get_lat_lon(df, destination)

  weather_origin = get_weather(from_date, from_date, location_origin[0], location_origin[1], origin)
  weather_destination = get_weather(from_date, to_date, location_destination[0], location_destination[1], destination)
  print("Gathered Weather Data!")

  # print(weather_origin)
  # print(weather_destination)
  # print(flight_data)
  # print(places)
  #location_origin[0] for lat & location_origin[1] for lon
  print("Loading response...")
  res = Markdown(generate_itinerary(flight_data, weather_origin, weather_destination, places))

  console.print(res)
  insert_itinerary(session, username, origin, destination, from_date, to_date, res)
  print("\n\nSaved to profile!")




main()