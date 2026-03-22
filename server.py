from flask import Flask, request, jsonify
import os

app = Flask(__name__)

latest_data = {"voltage": 0, "current": 0}

@app.route("/update", methods=["POST"])
def update():
    data = request.json
    latest_data["voltage"] = data.get("voltage", 0)
    latest_data["current"] = data.get("current", 0)
    return jsonify({"status": "received"})

@app.route("/data")
def data():
    return jsonify(latest_data)

# 🔥 THIS PART IS VERY IMPORTANT
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)