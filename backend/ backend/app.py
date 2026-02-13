from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)
CORS(app)

client = MongoClient("mongodb://localhost:27017/")
db = client["smart_farming"]
collection = db["sensor_data"]

PUMP_STATUS = "OFF"
MOISTURE_THRESHOLD = 40

@app.route('/data', methods=['POST'])
def receive_data():
    global PUMP_STATUS
    
    data = request.json
    data["timestamp"] = datetime.now()

    # Auto irrigation logic
    if data["moisture"] < MOISTURE_THRESHOLD:
        PUMP_STATUS = "ON"
    else:
        PUMP_STATUS = "OFF"

    data["pump_status"] = PUMP_STATUS
    collection.insert_one(data)

    return jsonify({"pump_status": PUMP_STATUS})

@app.route('/data', methods=['GET'])
def get_data():
    latest = collection.find().sort("_id", -1).limit(10)
    result = []
    for item in latest:
        item["_id"] = str(item["_id"])
        result.append(item)
    return jsonify(result)

@app.route('/control', methods=['POST'])
def control():
    global PUMP_STATUS
    action = request.json['action']
    PUMP_STATUS = action.upper()
    return jsonify({"pump_status": PUMP_STATUS})

@app.route('/status', methods=['GET'])
def status():
    return jsonify({"pump_status": PUMP_STATUS})

if __name__ == '__main__':
    app.run(debug=True)
