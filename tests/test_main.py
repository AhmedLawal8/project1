import sys, os

# Make sure system path is at project1 directory to access src folder
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import unittest
from main import validate_date


class TestDateValidation(unittest.TestCase):

    def test_valid_date(self):
        result = validate_date("2026-07-01")
        self.assertEqual(result.isoformat(), "2026-07-01")

    def test_invalid_date(self):
        result = validate_date("07-01-2026")
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
