from datetime import datetime
import os

import pandas as pd
import serpapi
from dotenv import load_dotenv

from flight import get_flight_data
from places import calculate_max_results, get_top_attractions

def main():

  valid_airport_names = load_airports()

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

def load_airports():
  try:
    df = pd.read_csv("iata-icao.csv")
    return set(df['iata'].dropna().str.upper())
  except Exception as e:
    print("Error Opening File: ", e)

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

main()