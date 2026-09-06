import requests
import pandas as pd
import os
from datetime import date


def get_city_id(city_name):

    url = f"https://www.abhibus.com/wap/abus-autocompleter/api/v1/results?s={city_name}"

    response = requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0"
        }
    )

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

collection_date = str(date.today())

# ==========================
# CITY IDS
# ==========================

source_id = get_city_id(source_city)

if source_id is None:
    print("Source city not found")
    exit()

destination_id = get_city_id(destination_city)

if destination_id is None:
    print("Destination city not found")
    exit()

print("\nSource ID:", source_id)
print("Destination ID:", destination_id)

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

print("\nBus API Status:", response.status_code)

if response.status_code != 200:
    print("Bus Search Failed")
    exit()

data = response.json()

services = data.get("services", [])

print("Total Buses Found:", len(services))

if len(services) == 0:
    print("No buses found")
    exit()

# ==========================
# BUILD DATASET
# ==========================

dataset = []

for bus in services:

    fare = bus.get("fares", {}).get("fare", 0)

    seats = bus.get("seats", {}).get("availableSeats", 0)

    rating = float(bus.get("rating", 0))

    operator = bus.get("travelerAgentName", "Unknown")

    dataset.append([
        collection_date,
        journey_date,
        source_city,
        destination_city,
        operator,
        fare,
        seats,
        rating
    ])

new_df = pd.DataFrame(
    dataset,
    columns=[
        "collection_date",
        "journey_date",
        "source",
        "destination",
        "operator",
        "fare",
        "seats",
        "rating"
    ]
)

# ==========================
# SAVE / APPEND CSV
# ==========================

if os.path.exists("bus_dataset.csv"):

    old_df = pd.read_csv("bus_dataset.csv")

    final_df = pd.concat(
        [old_df, new_df],
        ignore_index=True
    )

else:

    final_df = new_df

final_df.to_csv(
    "bus_dataset.csv",
    index=False
)

print("\nSaved", len(new_df), "records")
print("Total Dataset Rows:", len(final_df))