import sys, os

# Make sure system path is at project1 directory to access src folder
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import unittest
from unittest.mock import patch
from src.flight import get_flight_data


class TestFlights(unittest.TestCase):

    @patch("src.flight.serpapi.Client")
    def test_flight_parsing(self, MockClient):

        outbound_resp = {
            "best_flights": [
                {
                    "price": 200,
                    "total_duration": 300,
                    "departure_token": "mock_token_123",
                    "flights": [
                        {
                            "departure_airport": {"name": "JFK", "time": "10:00"},
                            "arrival_airport": {"name": "LAX", "time": "13:00"},
                            "airline": "Delta",
                            "airplane": "A320",
                        }
                    ],
                }
            ]
        }

        return_resp = {
            "best_flights": [
                {
                    "price": 180,
                    "total_duration": 320,
                    "departure_token": "mock_token_456",
                    "flights": [
                        {
                            "departure_airport": {"name": "LAX", "time": "15:00"},
                            "arrival_airport": {"name": "JFK", "time": "23:00"},
                            "airline": "United",
                            "airplane": "B737",
                        }
                    ],
                }
            ]
        }

        instance = MockClient.return_value
        instance.search.side_effect = [outbound_resp, return_resp]

        result = get_flight_data("JFK", "LAX", "2026-07-01", "2026-07-05")

        self.assertIn("outbound", result)
        self.assertIn("return", result)

        outbound = result["outbound"][0]
        self.assertEqual(outbound["price"], 200)


if __name__ == "__main__":
    unittest.main()
