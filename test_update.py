import requests

# 🔗 Your backend URL
url = "https://fault-backend-itqk.onrender.com/update"

# 📦 Test data (2-node format)
data = {
    "nodeA_voltage": 230,
    "nodeA_current": 5,
    "nodeB_voltage": 150,   # simulate fault
    "nodeB_current": 6
}

# 🚀 Send POST request
response = requests.post(url, json=data)

print("Status Code:", response.status_code)
print("Response:", response.text)