import requests

url = "https://fault-backend-itqk.onrender.com/update"

data = {
    "voltage": 230,
    "current": 7
}

response = requests.post(url, json=data)

print(response.status_code)
print(response.text)