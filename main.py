import sys
import pandas as pd
from datetime import datetime, date
from zoneinfo import ZoneInfo

from rich.console import Console
from rich.markdown import Markdown

from src.flight import get_flight_data
from src.places import get_top_attractions
from src.weather import get_weather
from src.genai import generate_itinerary
from src.db import (
    make_db,
    insert_itinerary,
    get_list_of_itineraries,
    get_itinerary,
    get_user,
    get_itineraries_count,
)


def main():
    console = Console()

    # Store Airport DataFrame
    df = load_airports()
    valid_airport_names = set(df.index.dropna().str.upper())

    print("=" * 30)
    print("|   Welcome to Waypoint!!!   |")
    print("=" * 30)

    user = input("\nWhat is your username:\n> ")

    # Get sesison to query db
    session = make_db()

    exists = get_user(session, user)

    print("\nSearching...\n")

    # If User does not exist give 2 prompts to create or exit
    if not exists:

        print(f"Hello {user}, you're new here!")
        while True:

            print("\n1. Create first itinerary")
            print("2. Exit")

            try:
                ans = int(input("\n>").strip())
            except ValueError:
                print("Enter a valid number")
                continue

            if ans == 1:
                create_itinerary(session, user, df, valid_airport_names, console)

                # After creating make sure user now exists
                exists = True
                break
            elif ans == 2:
                print("Goodbye!")
                session.close()
                return
            else:
                print("Choose 1 or 2")

    # If user does exist give 3 prompts to create, view saved or exit
    if exists:

        print(f"Welcome Back {user}!")

        ans = 0
        while ans != 3:

            count = get_itineraries_count(session, user)
            print(f"You have {count} saved itineraries.\n")

            print("1. Create an itinerary")
            print("2. View Itineraries")
            print("3. Exit")

            try:
                ans = int(input("\n>").strip())
            except ValueError:
                print("Enter a valid number")
                continue

            if ans == 1:
                create_itinerary(session, user, df, valid_airport_names, console)

            elif ans == 2:
                view_itineraries(session, user, console)

            elif ans == 3:
                print("Hope you enjoyed using Waypoint!")
                session.close()
                break

            else:
                print("Choose 1,2 or 3")


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
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return None


def get_valid_dates():
    today = date.today()

    while True:

        from_date = input("When do you plan on departing (yyyy-mm-dd): ").strip()
        from_date_obj = validate_date(from_date)

        if not from_date_obj:
            print("Invalid Date format")
            continue

        if from_date_obj < today:
            print("Departure date cannot be in the past")
            continue

        to_date = input("When do you plan on returning (yyyy-mm-dd): ").strip()
        to_date_obj = validate_date(to_date)

        if not to_date_obj:
            print("Invalid Date format")
            continue

        if from_date_obj >= to_date_obj:
            print("Return Date must be after departure date")
            continue

        return from_date_obj, to_date_obj


def get_lat_lon(df, code):
    lat = df.loc[code, "latitude"]
    lon = df.loc[code, "longitude"]
    return lat, lon


def create_itinerary(session, username, df, valid_airport_names, console):
    origin = validate_code(
        "What airport are you departing from (e.g. JFK): ", valid_airport_names
    )
    destination = validate_code(
        "What airport are you arriving at (e.g. LAX): ", valid_airport_names
    )

    # To store in db as Date object
    from_date_obj, to_date_obj = get_valid_dates()

    # Convert to get string for apis
    from_date_str = from_date_obj.strftime("%Y-%m-%d")
    to_date_str = to_date_obj.strftime("%Y-%m-%d")

    flight_data = get_flight_data(origin, destination, from_date_str, to_date_str)

    location_origin = get_lat_lon(df, origin)
    location_destination = get_lat_lon(df, destination)

    places = get_top_attractions(
        location_destination[0], location_destination[1], from_date_str, to_date_str
    )

    weather_origin = get_weather(
        from_date_str, from_date_str, location_origin[0], location_origin[1], origin
    )
    weather_destination = get_weather(
        from_date_str,
        to_date_str,
        location_destination[0],
        location_destination[1],
        destination,
    )
    print("Gathered Weather Data!")

    print("Loading response...")
    res = generate_itinerary(flight_data, weather_origin, weather_destination, places)

    console.print(Markdown(res))

    insert_itinerary(
        session, username, origin, destination, from_date_obj, to_date_obj, res
    )
    print("\n\nSaved Itinerary to profile!")


def view_itineraries(session, username, console):
    itineraries = get_list_of_itineraries(session, username)

    if not itineraries:
        print("No itineraries found.")
        return

    print("\nYour itineraries\n")

    for row in itineraries:
        est_time = row.created_at.astimezone(ZoneInfo("America/New_York"))

        print(f"{row.id}. {row.origin} -> {row.destination}")
        print(f"   {row.start_date} -> {row.end_date}")
        print(f"   Created: {est_time.strftime('%Y-%m-%d %I:%M %P')}")
        print("-" * 40)

    valid_ids = {row.id for row in itineraries}

    while True:
        choice = input("\nEnter itinerary ID (or 'q' to quit): ")

        if choice.lower() == "q":
            return

        if not choice.isdigit():
            print("Please enter a number")
            continue

        choice = int(choice)

        if choice not in valid_ids:
            print("That ID doesnt exist. Try again")
            continue

        break

    itinerary = get_itinerary(session, username, choice)

    if not itinerary:
        print("Could not retrieve itinerary")
        return

    res = itinerary.itinerary

    print("\nFull Itinerary\n")
    console.print(Markdown(res))


if __name__ == "__main__":
    main()
