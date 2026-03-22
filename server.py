from flask import Flask, request, jsonify

app = Flask(__name__)

# Store latest values
latest_data = {
    "voltage": 0,
    "current": 0
}

# ESP32 will SEND data here
@app.route("/update", methods=["POST"])
def update():
    data = request.json
    latest_data["voltage"] = data.get("voltage", 0)
    latest_data["current"] = data.get("current", 0)
    return jsonify({"status": "received"})

# Streamlit will GET data from here
@app.route("/data")
def data():
    return jsonify(latest_data)

app.run(debug=True)