import io
import unittest
from unittest.mock import Mock

from domain.fx_service import FXService


class TestFXService(unittest.TestCase):
    def setUp(self):
        # Mock OSSStorage
        self.mock_oss_storage = Mock()

        # Fake CSV content
        self.fake_csv_content = (
            "timestamp,exchange_rate\n2024-01-01,0.78\n2024-01-02,0.79"
        )

        # Set up the FXService with the mocked OSSStorage
        self.fx_service = FXService()
        self.fx_service.oss_storage = self.mock_oss_storage

    def test_process_fx_data(self):
        # Mock the 'get' method of OSSStorage to return the fake CSV content
        self.mock_oss_storage.get.return_value = self.fake_csv_content.encode()

        # Run the method under test
        average_rate, current_rate = self.fx_service.process_fx_data()

        # Assertions to verify the expected outcomes
        self.assertIsNotNone(average_rate)
        self.assertIsNotNone(current_rate)
        self.mock_oss_storage.put.assert_called_once()  # Check if 'put' was called

        # Additional assertions can be added as per requirements


if __name__ == "__main__":
    unittest.main()
