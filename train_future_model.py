import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error

df = pd.read_csv("data/atp1d.csv")

target = "LBL_ALLminpA_fut_001"

X = df.drop(columns=[target])
y = df[target]

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42
)

model = XGBRegressor(
    n_estimators=300,
    learning_rate=0.05,
    max_depth=6
)

model.fit(X_train, y_train)

preds = model.predict(X_test)

print("Future MAE:", mean_absolute_error(y_test, preds))

pickle.dump(model, open("models/future_price_model.pkl", "wb"))