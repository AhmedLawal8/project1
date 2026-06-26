import sys, os
#Make sure system path is at project1 directory to access src folder 
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import patch
from src.weather import get_weather

class TestWeather(unittest.TestCase):

  @patch("requests.get")
  def test_weather_parsing(self, mock_get):
    mock_get.return_value.json.return_value = {
      "days": [
        {
          "datetime": "2026-07-01",
          "tempmax": 80,
          "tempmin": 65,
          "description": "Sunny"
        }
      ]
    }

    result = get_weather("2026-07-01", "2026-07-01", 40.7, -73.9, "JFK")

    self.assertEqual(result[0]["place"], "JFK")
    self.assertEqual(result[0]["temp_max"], 80)
    self.assertEqual(result[0]["description"], "Sunny")

if __name__ == "__main__":
    unittest.main()