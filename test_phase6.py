
import unittest
from pathlib import Path
from logging_config import setup_logging
from error_handler import handle_error, safe_execute


class TestPhase6(unittest.TestCase):

    def test_logging_setup(self):
        logger = setup_logging()
        self.assertIsNotNone(logger)

    def test_error_handler(self):
        message = handle_error(
            ValueError("Test error"),
            "Test Context"
        )

        self.assertIn("An error occurred", message)

    def test_safe_execute_success(self):
        result = safe_execute(
            lambda: 10 + 20,
            "Addition"
        )

        self.assertEqual(result, 30)

    def test_safe_execute_error(self):
        result = safe_execute(
            lambda: 10 / 0,
            "Division"
        )

        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()