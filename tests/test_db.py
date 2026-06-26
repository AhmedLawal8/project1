import unittest
from src.places import calculate_max_results

class TestPlaces(unittest.TestCase):
  
  def test_short_trip(self):
    result = calculate_max_results("2026-07-01", "2026-07-03")
    self.assertEqual(result, 6)
  
  def test_cap_at_20(self):
    result = calculate_max_results("2026-07-01", "2026-07-20")
    self.assertLessEqual(result, 20)

if __name__ == "__main__":
  unittest.main()