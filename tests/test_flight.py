import sys, os
#Make sure system path is at project1 directory to access src folder 
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import patch
from src.flight import get_flight_data

class TestFlights(unittest.TestCase):

  @patch("src.flight.serpapi.Client")
  def test_flight_parsing(self, MockClient):

    mock_response = {
      "best_flights": [
        {
          "price": 200,
          "total_duration": 300,
          "flights": [
            {
                "departure_airport": {"name": "JFK", "time": "10:00"},
                "arrival_airport": {"name": "LAX", "time": "13:00"},
                "airline": "Delta",
                "airplane": "A320"
            }
          ]
        }
      ]
    }

    instance = MockClient.return_value
    instance.search.return_value = mock_response

    result = get_flight_data("JFK", "LAX", "2026-07-01", "2026-07-05")

    self.assertEqual(len(result), 1)
    self.assertEqual(result[0]["price"], 200)
    self.assertEqual(result[0]["airlines"], {"Delta"})

if __name__ == "__main__":
    unittest.main()


