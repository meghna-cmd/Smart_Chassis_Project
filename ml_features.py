import pandas as pd
import numpy as np

INPUT_TRAIN = "train_dataset.csv"
INPUT_TEST = "test_dataset.csv"

def extract_features(data):
    features = pd.DataFrame()

    features["RMS"] = np.sqrt((data ** 2).mean(axis=1))
    features["Standard_Deviation"] = data.std(axis=1)
    features["Peak_to_Peak"] = data.max(axis=1) - data.min(axis=1)

    return features


train_data = pd.read_csv(INPUT_TRAIN)
test_data = pd.read_csv(INPUT_TEST)

train_features = extract_features(train_data)
test_features = extract_features(test_data)

train_features.to_csv("train_features.csv", index=False)
test_features.to_csv("test_features.csv", index=False)

print("Training Features Shape:", train_features.shape)
print("Testing Features Shape:", test_features.shape)

print("\nTraining Feature Sample:")
print(train_features.head())

print("\nML Feature Extraction Completed Successfully!")