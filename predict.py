import pickle
import pandas as pd

model = pickle.load(open("models/flight_price_model.pkl", "rb"))
encoders = pickle.load(open("models/encoders.pkl", "rb"))

sample = {
    "airline": "Indigo",
    "source_city": "Bangalore",
    "destination_city": "Delhi",
    "days_left": 15,
    "duration": 2.5,
    "stops": 0,
    "class": "Economy"
}

for col in ["airline", "source_city", "destination_city", "class"]:
    sample[col] = encoders[col].transform([sample[col]])[0]

input_df = pd.DataFrame([sample])

predicted_price = model.predict(input_df)[0]

print("Predicted Price:", predicted_price)