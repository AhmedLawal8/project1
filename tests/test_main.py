import unittest
from main import validate_date

class TestDateValidation(unittest.TestCase):

  def test_valid_date(self):
    result = validate_date("2026-07-01")
    self.assertEqual(result.isoformat(), "2026-07-01")
  
  def test_invalid_date(self):
    result = validate_date("07-01-2026")
    self.assertIsNone(result)