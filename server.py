from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# 🔥 GLOBAL STORE
latest_data = {
    "nodeA_voltage": 0,
    "nodeA_current": 0,
    "nodeB_voltage": 0,
    "nodeB_current": 0
}

@app.route("/update", methods=["POST"])
def update():
    global latest_data
    data = request.json

    latest_data = {
        "nodeA_voltage": data.get("nodeA_voltage", 0),
        "nodeA_current": data.get("nodeA_current", 0),
        "nodeB_voltage": data.get("nodeB_voltage", 0),
        "nodeB_current": data.get("nodeB_current", 0)
    }

    print("UPDATED DATA:", latest_data)  # debug

    return jsonify({
        "status": "received",
        "data": latest_data
    })


@app.route("/data")
def data():
    print("SENDING DATA:", latest_data)  # debug
    return jsonify(latest_data)


# 🔥 CORRECT RUN
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    print(f"Running on port: {port}")
    app.run(host="0.0.0.0", port=port)