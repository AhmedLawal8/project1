import sys
import os

# Make sure system path is at project1 directory to access src folder
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.db import Base, insert_itinerary, get_itinerary
from datetime import date

class TestDB(unittest.TestCase):

    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:")

        # Create table in test DB
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)

        self.session = Session()

    def test_insert_and_fetch(self):
        insert_itinerary(
            self.session,
            "testuser",
            "JFK",
            "LAX",
            date(2026, 7, 1),
            date(2026, 7, 5),
            "test itinerary",
        )

        result = get_itinerary(self.session, "testuser", 1)

        self.assertIsNotNone(result)
        self.assertEqual(result.origin, "JFK")


if __name__ == "__main__":
    unittest.main()
