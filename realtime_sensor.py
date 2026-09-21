"""Real-time vibration sensor simulator for the Smart Chassis project.

This module simulates accelerometer readings until a real sensor/serial source
is connected. It is not a substitute for real vehicle testing.
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Iterator

import numpy as np


@dataclass
class SensorReading:
    timestamp: float
    acceleration: float
    anomaly: bool


def generate_vibration_stream(
    sample_rate: float = 100.0,
    duration: float = 10.0,
    base_frequency: float = 5.0,
    noise_level: float = 0.15,
    anomaly_probability: float = 0.02,
    seed: int = 42,
) -> Iterator[SensorReading]:
    """Yield simulated vibration readings one sample at a time."""
    if sample_rate <= 0:
        raise ValueError("sample_rate must be greater than zero")
    if duration <= 0:
        raise ValueError("duration must be greater than zero")
    if not 0 <= anomaly_probability <= 1:
        raise ValueError("anomaly_probability must be between 0 and 1")

    rng = np.random.default_rng(seed)
    total_samples = int(sample_rate * duration)

    for sample in range(total_samples):
        timestamp = sample / sample_rate
        anomaly = bool(rng.random() < anomaly_probability)
        amplitude = 3.0 if anomaly else 1.0
        acceleration = (
            amplitude * np.sin(2 * np.pi * base_frequency * timestamp)
            + rng.normal(0, noise_level)
        )

        yield SensorReading(
            timestamp=timestamp,
            acceleration=float(acceleration),
            anomaly=anomaly,
        )


def collect_readings(**kwargs) -> list[SensorReading]:
    """Collect a finite simulated stream without waiting in real time."""
    return list(generate_vibration_stream(**kwargs))


if __name__ == "__main__":
    for reading in generate_vibration_stream(duration=2):
        print(
            f"time={reading.timestamp:.2f}s | "
            f"acceleration={reading.acceleration:.4f} | "
            f"anomaly={reading.anomaly}"
        )
        time.sleep(0.01)
