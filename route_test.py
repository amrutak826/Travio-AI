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


source = input("Enter Source City: ")
destination = input("Enter Destination City: ")

source_id = get_city_id(source)
destination_id = get_city_id(destination)

print("\nRESULT")
print("Source      :", source)
print("Source ID   :", source_id)

print("Destination :", destination)
print("Destination ID :", destination_id)