import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import pickle

df = pd.read_csv("bus_dataset.csv")

# Convert dates

df["collection_date"] = pd.to_datetime(df["collection_date"])
df["journey_date"] = pd.to_datetime(df["journey_date"])

# Days before journey

df["days_before_journey"] = (
    df["journey_date"] - df["collection_date"]
).dt.days

# Encoders

source_encoder = LabelEncoder()
destination_encoder = LabelEncoder()

df["source"] = source_encoder.fit_transform(df["source"])
df["destination"] = destination_encoder.fit_transform(df["destination"])

# Features

X = df[
    [
        "source",
        "destination",
        "seats",
        "rating",
        "days_before_journey"
    ]
]

y = df["fare"]

# Model

model = RandomForestRegressor(
    n_estimators=200,
    random_state=42
)

model.fit(X, y)

# Save

pickle.dump(
    model,
    open("fare_model.pkl", "wb")
)

pickle.dump(
    source_encoder,
    open("source_encoder.pkl", "wb")
)

pickle.dump(
    destination_encoder,
    open("destination_encoder.pkl", "wb")
)

print("Model Trained Successfully")