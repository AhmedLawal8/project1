import requests

from src.config import VISUAL_CROSSING_KEY


def get_weather(origin_date, destination_date, lat, lon, place):

    base_url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{lat},{lon}/{origin_date}/{destination_date}"

    params = {
        "unitGroup": "us",
        "key": VISUAL_CROSSING_KEY,
        "contentType": "json",
        "include": "days",
    }

    try:

        response = requests.get(base_url, params=params)
        data = response.json()

    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
    except requests.exceptions.ConnectionError as e:
        print(f"Connection Error: {e}")
    except requests.exceptions.Timeout as e:
        print(f"Request Timeout: {e}")
    except requests.exceptions.RequestException as e:
        print(f"An unexpected error has occured: {e}")

    weather_data = []
    for day in data.get("days", []):
        weather = {
            "place": place,
            "date": day.get("datetime"),
            "temp_max": day.get("tempmax"),
            "temp_min": day.get("tempmin"),
        }
        current_condition = day.get("description")
        if current_condition != "":
            weather["description"] = current_condition
        else:
            weather["description"] = "No condition specified"
        weather_data.append(weather)

    return weather_data
