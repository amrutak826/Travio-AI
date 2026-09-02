import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error

df = pd.read_excel("data/Data_Train.xlsx")

# -------------------
# Feature engineering
# -------------------
df["Journey_Day"] = pd.to_datetime(
    df["Date_of_Journey"], dayfirst=True
).dt.day

df["Journey_Month"] = pd.to_datetime(
    df["Date_of_Journey"], dayfirst=True
).dt.month

df["Dep_Hour"] = df["Dep_Time"].str.split(":").str[0].astype(int)
df["Dep_Min"] = df["Dep_Time"].str.split(":").str[1].astype(int)

df["Duration_Hours"] = df["Duration"].str.extract(r'(\d+)h').fillna(0).astype(int)
df["Duration_Mins"] = df["Duration"].str.extract(r'(\d+)m').fillna(0).astype(int)

stop_map = {
    "non-stop": 0,
    "1 stop": 1,
    "2 stops": 2,
    "3 stops": 3,
    "4 stops": 4
}
df["Stops"] = df["Total_Stops"].map(stop_map)

# Encode categorical columns
categorical_cols = ["Airline", "Source", "Destination"]

encoders = {}

for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    encoders[col] = le

features = [
    "Airline",
    "Source",
    "Destination",
    "Journey_Day",
    "Journey_Month",
    "Dep_Hour",
    "Dep_Min",
    "Duration_Hours",
    "Duration_Mins",
    "Stops"
]

X = df[features]
y = df["Price"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestRegressor(
    n_estimators=300,
    random_state=42
)

model.fit(X_train, y_train)

preds = model.predict(X_test)

print("MAE:", mean_absolute_error(y_test, preds))

pickle.dump(model, open("models/base_price_model.pkl", "wb"))
pickle.dump(encoders, open("models/base_encoders.pkl", "wb"))
