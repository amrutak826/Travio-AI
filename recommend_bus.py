import requests
import pickle
from datetime import datetime

# ==========================
# LOAD TRAINED MODEL
# ==========================

model = pickle.load(open("fare_model.pkl", "rb"))
source_encoder = pickle.load(open("source_encoder.pkl", "rb"))
destination_encoder = pickle.load(open("destination_encoder.pkl", "rb"))

# ==========================
# CITY LOOKUP
# ==========================

def get_city_id(city_name):

    url = f"https://www.abhibus.com/wap/abus-autocompleter/api/v1/results?s={city_name}"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return None

    data = response.json()

    if len(data) == 0:
        return None

    return data[0]["id"]


# ==========================
# USER INPUT
# ==========================

source_city = input("Enter Source City: ").strip()
destination_city = input("Enter Destination City: ").strip()
journey_date = input("Enter Journey Date (YYYY-MM-DD): ").strip()

# ==========================
# GET IDS
# ==========================

source_id = get_city_id(source_city)
destination_id = get_city_id(destination_city)

print("\nSource ID:", source_id)
print("Destination ID:", destination_id)

if source_id is None:
    print("Source city not found")
    exit()

if destination_id is None:
    print("Destination city not found")
    exit()

# ==========================
# BUS SEARCH
# ==========================

url = "https://www.abhibus.com/buslist/v2/services"

headers = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0"
}

payload = {
    "sourceid": source_id,
    "destinationid": destination_id,
    "jdate": journey_date,
    "source": source_city,
    "destination": destination_city
}

response = requests.post(
    url,
    headers=headers,
    json=payload
)

print("\nStatus:", response.status_code)

if response.status_code != 200:
    print("Request Failed")
    exit()

data = response.json()

services = data.get("services", [])

print("Total Buses Found:", len(services))

if len(services) == 0:
    print("No buses found")
    exit()

# ==========================
# FIND BEST BUS
# ==========================

best_bus = None
best_score = -999999

for bus in services:

    fare = bus.get("fares", {}).get("fare", 0)

    seats = bus.get("seats", {}).get("availableSeats", 0)

    rating = float(bus.get("rating", 0))

    score = (rating * 10) + seats - (fare / 100)

    if score > best_score:
        best_score = score
        best_bus = bus

# ==========================
# EXTRACT DETAILS
# ==========================

operator = best_bus.get("travelerAgentName", "N/A")

bus_type = best_bus.get("busServiceTypeName", "N/A")

departure = best_bus.get("timings", {}).get("startTime", "N/A")

arrival = best_bus.get("timings", {}).get("arriveTime", "N/A")
print("\nTIMINGS DATA:")
print(best_bus["timings"])

fare = best_bus.get("fares", {}).get("fare", 0)

seats = best_bus.get("seats", {}).get("availableSeats", 0)

rating = float(best_bus.get("rating", 0))

# ==========================
# AI FARE PREDICTION
# ==========================

try:

    source_encoded = source_encoder.transform(
        [source_city]
    )[0]

    destination_encoded = destination_encoder.transform(
        [destination_city]
    )[0]

    collection_date = datetime.today()

    journey_dt = datetime.strptime(
        journey_date,
        "%Y-%m-%d"
    )

    days_before_journey = (
        journey_dt - collection_date
    ).days

    predicted_fare = model.predict([[
        source_encoded,
        destination_encoded,
        seats,
        rating,
        days_before_journey
    ]])[0]

except Exception as e:

    print("Prediction Error:", e)

    predicted_fare = fare

# ==========================
# RECOMMENDATION
# ==========================

if predicted_fare > fare:
    recommendation = "BOOK NOW"
else:
    recommendation = "WAIT"

# ==========================
# OUTPUT
# ==========================

print("\n")
print("=" * 60)
print("                    TRAVIO AI BUS")
print("=" * 60)

print(f"\nRoute: {source_city} ➜ {destination_city}")

print(f"\nOperator: {operator}")

print(f"\nBus Type: {bus_type}")

print(f"\nTravel Date: {journey_date}")

print("-" * 60)

print(f"\nLive Fare: ₹{fare}")

print(f"\nPredicted Fare: ₹{round(predicted_fare, 2)}")

print(f"\nRecommendation: {recommendation}")

print(f"\nAvailable Seats: {seats}")

print(f"\nRating: {rating}")

print("\nReason:")

if rating >= 4:
    print("✓ High Rating")

if seats >= 20:
    print("✓ Good Seat Availability")

if predicted_fare > fare:
    print("✓ Expected Fare Increase")

if predicted_fare <= fare:
    print("✓ Better Fare May Be Available")

print("\n" + "=" * 60)