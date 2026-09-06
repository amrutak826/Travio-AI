import requests

def get_city_id(city_name):

    url = f"https://www.abhibus.com/wap/abus-autocompleter/api/v1/results?s={city_name}"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:

        data = response.json()

        if len(data) > 0:
            return data[0]["id"]

    return None


# ===========================
# USER INPUT
# ===========================

source = input("Enter Source City: ")
destination = input("Enter Destination City: ")
journey_date = input("Enter Journey Date (YYYY-MM-DD): ")

source_id = get_city_id(source)
destination_id = get_city_id(destination)

print("\nSource ID:", source_id)
print("Destination ID:", destination_id)

if source_id is None or destination_id is None:
    print("\nInvalid city name.")
    exit()


# ===========================
# BUS SEARCH API
# ===========================

url = "https://www.abhibus.com/buslist/v2/services"

headers = {
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/json",
    "Origin": "https://www.abhibus.com",
    "Referer": "https://www.abhibus.com/"
}

payload = {
    "source": source.title(),
    "sourceid": source_id,
    "destination": destination.title(),
    "destinationid": destination_id,
    "jdate": journey_date,
    "prd": "mobile",
    "filters": "1",
    "isReturnJourney": "0",
    "version": "105"
}

response = requests.post(
    url,
    headers=headers,
    json=payload
)

print("\nStatus:", response.status_code)

if response.status_code != 200:
    print("Request Failed")
    print(response.text[:500])
    exit()

data = response.json()

services = data.get("services", [])

print("\nTotal Buses Found:", len(services))

print("\nTOP 20 BUSES\n")

for bus in services[:20]:

    operator = bus.get("travelerAgentName", "N/A")

    service = bus.get("serviceName", "N/A")

    bus_type = bus.get("busServiceTypeName", "N/A")

    fare = bus.get("fares", {}).get("fare", "N/A")

    seats = bus.get("seats", {}).get("availableSeats", "N/A")

    departure = bus.get("timings", {}).get("startTime", "N/A")

    arrival = bus.get("timings", {}).get("arriveTime", "N/A")

    rating = bus.get("rating", "N/A")

    print("=" * 70)

    print("Operator   :", operator)

    print("Service    :", service)

    print("Bus Type   :", bus_type)

    print("Departure  :", departure)

    print("Arrival    :", arrival)

    print("Fare       : ₹", fare)

    print("Seats Left :", seats)

    print("Rating     :", rating)