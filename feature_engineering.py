
import pandas as pd
import numpy as np
from pathlib import Path

from project_config import (
    WINDOW_SIZE,
    DATASET_FILE
)


# Output folder তৈরি
output_folder = Path("outputs")
output_folder.mkdir(exist_ok=True)


# Step 1: Load Dataset
data = pd.read_excel(DATASET_FILE, header=None)


# Step 2: Clean Dataset
data = data.iloc[5:, 2:]

data.columns = [
    "Crack1_30",
    "Crack1_50",
    "Crack2_30",
    "Crack2_50",
    "Crack3_30",
    "Crack3_50",
    "Crack4_30",
    "Crack4_50",
    "Crack5_30",
    "Crack5_50",
    "Crack6_30",
    "Crack6_50"
]

data = data.apply(pd.to_numeric, errors="coerce")


# Step 3: Feature Engineering Function
def calculate_features(signal):

    signal = np.asarray(signal)

    rms = np.sqrt(np.mean(signal ** 2))

    std = np.std(signal)

    peak_to_peak = (
        np.max(signal) - np.min(signal)
    )

    absolute_signal = np.abs(signal)

    mean_absolute = np.mean(absolute_signal)

    if mean_absolute != 0:
        crest_factor = (
            np.max(absolute_signal) / mean_absolute
        )
    else:
        crest_factor = 0

    return {
        "RMS": rms,
        "STD": std,
        "Peak_to_Peak": peak_to_peak,
        "Crest_Factor": crest_factor
    }


# Step 4: Window-Based Feature Extraction
results = []

for column in data.columns:

    signal = data[column].dropna().to_numpy()

    for start in range(
        0,
        len(signal) - WINDOW_SIZE + 1,
        WINDOW_SIZE
    ):

        window = signal[
            start:start + WINDOW_SIZE
        ]

        features = calculate_features(window)

        features["Signal"] = column
        features["Window_Start"] = start
        features["Window_Size"] = WINDOW_SIZE

        results.append(features)


# Step 5: Create DataFrame
feature_df = pd.DataFrame(results)


# Step 6: Arrange Columns
feature_df = feature_df[
    [
        "Signal",
        "Window_Start",
        "Window_Size",
        "RMS",
        "STD",
        "Peak_to_Peak",
        "Crest_Factor"
    ]
]


# Step 7: Save Features
output_file = (
    output_folder / "feature_engineering_results.csv"
)

feature_df.to_csv(
    output_file,
    index=False
)


# Step 8: Display Results
print("\nSMART CHASSIS FEATURE ENGINEERING")
print("----------------------------------------")

print("Window Size:", WINDOW_SIZE)

print("Total Windows:", len(feature_df))

print("\nFeature Preview:")
print(feature_df.head())

print("\nFeatures saved successfully.")
print("File:", output_file)