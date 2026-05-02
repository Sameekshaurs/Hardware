from flask import Flask, request, jsonify
import os

app = Flask(__name__)

latest_data = {
    "nodeA_voltage": 0,
    "nodeA_current": 0,
    "nodeB_voltage": 0,
    "nodeB_current": 0
}

@app.route("/update", methods=["POST"])
def update():
    data = request.json

    latest_data["nodeA_voltage"] = data.get("nodeA_voltage", 0)
    latest_data["nodeA_current"] = data.get("nodeA_current", 0)
    latest_data["nodeB_voltage"] = data.get("nodeB_voltage", 0)
    latest_data["nodeB_current"] = data.get("nodeB_current", 0)

    return jsonify({
        "status": "received",
        "data": latest_data   # 🔥 ADD THIS
    })

@app.route("/data")
def data():
    return jsonify(latest_data)

# 🔥 THIS PART IS VERY IMPORTANT
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)