import requests

city = input("Enter city name: ")

url = f"https://www.abhibus.com/wap/abus-autocompleter/api/v1/results?s={city}"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)

print("Status:", response.status_code)

if response.status_code == 200:

    data = response.json()

    print("\nResults Found:", len(data))

    for item in data[:10]:

        print("\nID   :", item.get("id"))
        print("City :", item.get("label"))

else:

    print(response.text)
    