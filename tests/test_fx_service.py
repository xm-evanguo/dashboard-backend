import os
import unittest

import pandas as pd

from domain.fx_service import FXService


class TestFXService(unittest.TestCase):
    def setUp(self):
        # Set up the FXService with a path to the test CSV file in the resources directory
        self.fx_service = FXService()
        test_csv_path = os.path.join(
            os.path.dirname(__file__), "resources", "test_fx_data.csv"
        )
        self.fx_service.fx_data_path = test_csv_path

    def test_process_fx_data(self):
        # Run the method under test
        average_rate, current_rate = self.fx_service.process_fx_data()

        # Assertions to verify the expected outcomes
        self.assertIsNotNone(average_rate)
        self.assertIsNotNone(current_rate)

        # Additional test to check the correctness of the data manipulation
        test_data = pd.read_csv(self.fx_service.fx_data_path)
        self.assertIn("date", test_data.columns)
        self.assertIn("exchange_rate", test_data.columns)


if __name__ == "__main__":
    unittest.main()
