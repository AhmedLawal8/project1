import requests
import os

from dotenv import load_dotenv

# Use the free 2.5 current weather endpoint
url = "https://api.openweathermap.org/data/2.5/weather"

load_dotenv()

# It's cleaner to pass parameters as a dictionary
OPEN_WEATHER_KEY = os.getenv("OPEN_WEATHER_KEY")
params = {
    "lat": 52.2297,
    "lon": 21.0122,
    "units": "metric",
    "lang": "en",
    "appid": OPEN_WEATHER_KEY # Replace this!
}

response = requests.get(url, params=params)

if response.status_code == 200:
    print(response.json())
else:
    print(f"Error {response.status_code}: {response.text}")



# example_response = 
# {'coord': {'lon': 21.0118, 'lat': 52.2298},
#  'weather': [{'id': 804, 'main': 'Clouds',
#   'description': 'overcast clouds', 'icon': '04n'}],
#    'base': 'stations',
#     'main':
#      {'temp': 19.67, 
#      'feels_like': 19.29, 
#      'temp_min': 17.02, 
#      'temp_max': 21.07, 
#      'pressure': 1019, 
#      'humidity': 61, 
#      'sea_level': 1019, 
#      'grnd_level': 1009}, 
#      'visibility': 10000, 
#      'wind': {'speed': 1.69, 'deg': 338, 'gust': 3.29}, 
#      'clouds': {'all': 85}, 
#      'dt': 1782245598, 
#      'sys': {'type': 2, 'id': 2032856, 'country': 'PL', 'sunrise': 1782180890, 'sunset': 1782241278}, 
#      'timezone': 7200, 'id': 756135, 'name': 'Warsaw', 'cod': 200}