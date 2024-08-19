import requests
import os

url = "https://local-business-data.p.rapidapi.com/search"

payload = {
	"queries": ["plumbers in texas", "hotels near san francisco", "restaurants in chicago"],
	"limit": 1000,
	"region": "us",
	"language": "en",
	"zoom": 13,
	"dedup": True
}
headers = {
	"x-rapidapi-key": os.environ["rapidapi_key"],
	"x-rapidapi-host": "local-business-data.p.rapidapi.com",
	"Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

print(response.json())