from flask import Flask, jsonify
import random

app = Flask(__name__)

@app.route("/data")
def data():
    return jsonify({
        "voltage": random.uniform(210, 240),
        "current": random.uniform(0, 10)
    })

app.run(debug=True)
