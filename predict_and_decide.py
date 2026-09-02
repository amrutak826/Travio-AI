import pickle
import pandas as pd

future_model = pickle.load(
    open("models/future_price_model.pkl", "rb")
)

# Example live data from Amadeus
live_price = 5400

sample = pd.read_csv("data/atp1d.csv").drop(
    columns=["LBL_ALLminpA_fut_001"]
).iloc[[0]]

predicted_future = future_model.predict(sample)[0]

print("Live price:", live_price)
print("Predicted future price:", predicted_future)

threshold = predicted_future * 1.02

if live_price <= threshold:
    decision = "AUTO BOOK"
else:
    decision = "WAIT"

print("Decision:", decision)