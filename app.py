from flask import Flask, request, jsonify
import pandas as pd
from typing import List, Dict
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

class Shipment:
    def __init__(self, shipment_id, latitude, longitude, time):
        self.shipment_id = shipment_id
        self.location = {"lat": latitude, "lng": longitude}
        self.time = time

class Trip:
    def __init__(self, trip_id, shipments, mst_dist, trip_time, vehicle_type, avg_speed, min_speed, max_speed):
        self.trip_id = trip_id
        self.shipments = shipments
        self.mst_dist = mst_dist
        self.trip_time = trip_time
        self.vehicle_type = vehicle_type
        self.avg_speed = avg_speed
        self.min_speed = min_speed
        self.max_speed = max_speed

@app.route("/")
def home():
    return jsonify({"message": "Flask app deployed successfully!"})

@app.route("/predict", methods=["POST"])
def predict():
    if "file1" not in request.files or "file2" not in request.files:
        return jsonify({"error": "Both CSV files are required"}), 400

    file1 = request.files["file1"]
    file2 = request.files["file2"]

    file1_path = os.path.join(UPLOAD_FOLDER, file1.filename)
    file2_path = os.path.join(UPLOAD_FOLDER, file2.filename)

    file1.save(file1_path)
    file2.save(file2_path)

    # Load CSV files
    df1 = pd.read_csv(file1_path)
    df2 = pd.read_csv(file2_path)

    # Sample processing (merge CSVs)
    merged_df = pd.concat([df1, df2], ignore_index=True)

    # Mock Data (Replace with actual logic)
    trips = [
        Trip(
            trip_id="1",
            shipments=[
                Shipment(1, 19.076, 72.877, "10:00 AM").__dict__,
                Shipment(2, 28.704, 77.102, "12:30 PM").__dict__
            ],
            mst_dist=50.0,
            trip_time=1.5,
            vehicle_type="Truck",
            avg_speed=80.0,
            min_speed=60.0,
            max_speed=75.0
        ).__dict__,
        Trip(
            trip_id="2",
            shipments=[
                Shipment(3, 28.704, 77.102, "2:00 PM").__dict__,
                Shipment(4, 19.076, 72.877, "4:30 PM").__dict__
            ],
            mst_dist=30.0,
            trip_time=1.0,
            vehicle_type="Van",
            avg_speed=70.0,
            min_speed=50.0,
            max_speed=65.0
        ).__dict__
    ]

    return jsonify(trips)

if __name__ == "__main__":
    app.run(debug=True)
