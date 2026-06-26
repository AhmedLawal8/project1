import sys, os
#Make sure system path is at project1 directory to access src folder 
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

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
