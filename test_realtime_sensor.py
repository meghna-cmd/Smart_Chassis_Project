import unittest

from realtime_sensor import collect_readings, generate_vibration_stream


class TestRealtimeSensor(unittest.TestCase):
    def test_expected_sample_count(self):
        readings = collect_readings(sample_rate=20, duration=2)
        self.assertEqual(len(readings), 40)

    def test_reproducible_output(self):
        first = collect_readings(sample_rate=10, duration=1, seed=7)
        second = collect_readings(sample_rate=10, duration=1, seed=7)
        self.assertEqual(first, second)

    def test_invalid_sample_rate(self):
        with self.assertRaises(ValueError):
            list(generate_vibration_stream(sample_rate=0))


if __name__ == "__main__":
    unittest.main()
