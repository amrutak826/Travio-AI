import requests

city = input("City: ")

url = f"https://www.abhibus.com/wap/abus-autocompleter/api/v1/results?s={city}"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)

print("Status:", response.status_code)

print("\nFULL RESPONSE:\n")
print(response.text)