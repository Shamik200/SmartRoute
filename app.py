from flask import Flask, request, jsonify
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests from Android app

@app.route('/process', methods=['POST'])
def process_files():
    if 'file1' not in request.files or 'file2' not in request.files:
        return jsonify({"error": "Files missing"}), 400

    file1 = request.files['file1']
    file2 = request.files['file2']

    df_shipments = pd.read_csv(file1)
    df_vehicles = pd.read_csv(file2)

    trips = generate_trips(df_shipments, df_vehicles)

    return jsonify(trips)

def generate_trips(shipments, vehicles):
    trips = []
    for i in range(min(len(shipments), len(vehicles))):
        trips.append({
            "tripId": str(i + 1),
            "shipments": [{"id": i, "location": {"lat": 19.0 + i, "lng": 72.0 + i}, "timeSlot": "10:00 AM"}],
            "mstDistance": 50.0,
            "tripTime": 1.5,
            "vehicleType": "Truck",
            "capacityUtilization": 80.0,
            "timeUtilization": 60.0,
            "coverageUtilization": 75.0
        })
    return trips

if __name__ == '__main__':
    app.run(debug=True)
