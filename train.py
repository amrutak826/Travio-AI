import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.preprocessing import LabelEncoder

df = pd.read_csv("data/flights.csv")

# Encode categorical columns
encoders = {}
categorical_cols = ["airline", "source_city", "destination_city", "class"]

for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    encoders[col] = le

# Features
X = df[
    [
        "airline",
        "source_city",
        "destination_city",
        "days_left",
        "duration",
        "stops",
        "class"
    ]
]

y = df["price"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestRegressor(
    n_estimators=200,
    random_state=42
)

model.fit(X_train, y_train)

preds = model.predict(X_test)

mae = mean_absolute_error(y_test, preds)
print("MAE:", mae)

with open("models/flight_price_model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("models/encoders.pkl", "wb") as f:
    pickle.dump(encoders, f)