from flask import Flask, request, jsonify
import pandas as pd
from typing import List, Dict
import os
# import requests
import pandas as pd
# import time
import numpy as np
import math
from geopy.distance import geodesic
# import folium
# from folium.plugins import MarkerCluster
import random

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


class Trip:
    def _init_(self, trip_id, shipment_ids, latitudes, longitudes, time_slot, num_shipments, mst_dist, trip_time, vehicle_type):
        self.trip_id = trip_id
        self.shipment_ids = shipment_ids
        self.latitudes = latitudes
        self.longitudes = longitudes
        self.time_slot = time_slot
        self.num_shipments = num_shipments
        self.mst_dist = mst_dist
        self.trip_time = trip_time
        self.vehicle_type = vehicle_type

    def to_dict(self):
        """Convert Trip object to dictionary for DataFrame conversion."""
        return {
            'trip_id': self.trip_id,
            'shipment_ids': self.shipment_ids,
            'latitudes': self.latitudes,
            'longitudes': self.longitudes,
            'time_slot': self.time_slot,
            'num_shipments': self.num_shipments,
            'mst_dist': self.mst_dist,
            'trip_time': self.trip_time,
            'vehicle_type': self.vehicle_type
        }

# class Shipment:
#     def __init__(self, shipment_id, latitude, longitude, time):
#         self.shipment_id = shipment_id
#         self.location = {"lat": latitude, "lng": longitude}
#         self.time = time

# class Trip:
#     def __init__(self, trip_id, shipments, mst_dist, trip_time, vehicle_type, avg_speed, min_speed, max_speed):
#         self.trip_id = trip_id
#         self.shipments = shipments
#         self.mst_dist = mst_dist
#         self.trip_time = trip_time
#         self.vehicle_type = vehicle_type
#         self.avg_speed = avg_speed
#         self.min_speed = min_speed
#         self.max_speed = max_speed



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
    shipments_df = pd.read_csv(file1_path)
    vehicle_df = pd.read_csv(file2_path)

    facility_location = (19.11011, 72.8496466)

    for index, row in shipments_df.iterrows():
        shipment_location = (row['Latitude'], row['Longitude'])
        distance = get_road_distance(facility_location, shipment_location)
        shipments_df.at[index, 'MST_DIST'] = distance

    shipments_df.to_csv('/content/processed_shipments.csv', index=False)


    shipment_df = pd.read_csv("processed_shipments.csv")
    vehicle_df = pd.read_csv("vehicles.csv")[:3]

    shipments_path = '/content/processed_shipments.csv'
    # Expected columns: Shipment_ID, Latitude, Longitude, MST_DIST, Delivery Timeslot, etc.
    vehicles_path = '/content/vehicles.csv'
    # Expected columns: Vehicle Type, Number, Shipments_Capacity, Max Trip Radius (in KM)

    # Load CSVs
    shipments_df = pd.read_csv(shipments_path)
    vehicle_df = pd.read_csv(vehicles_path)[:3]  # Only consider the first 3 vehicle types

    # Define facility center coordinates (latitude, longitude)
    facility = (19.11011, 72.8496466)

    # Run the clustering optimization
    optimized_trips_df = optimize_trips_clustering(shipments_df, vehicle_df, facility)

    # Save the optimized trips to CSV (columns: trip_id, shipment_ids, latitudes, longitudes,
    # time_slot, num_shipments, mst_dist, trip_time, vehicle_type)
    output_csv_path = '/content/Optimized_Trips.csv'
    optimized_trips_df.to_csv(output_csv_path, index=False)




    # Folium Code..................................\
    #     # Load the Optimized_Trips.csv file
    # trips_df = pd.read_csv('/content/Optimized_Trips.csv')

    # # Initialize the map centered at the facility center
    # facility_lat =19.11011  # Replace with the actual latitude of the facility center
    # facility_lon = 72.8496466# Replace with the actual longitude of the facility center
    # facility_map = folium.Map(location=[facility_lat, facility_lon], zoom_start=12)

    # # Create a MarkerCluster to group markers together
    # marker_cluster = MarkerCluster().add_to(facility_map)

    # # Add a marker for the facility center
    # folium.Marker(
    #     location=[facility_lat, facility_lon],
    #     popup="Facility Center",
    #     icon=folium.Icon(color='blue', icon='cloud')
    # ).add_to(facility_map)

    # # Function to generate random colors for different trips
    # def random_color():
    #     return f'#{random.randint(0, 0xFFFFFF):06x}'

    # # Loop through each trip in the DataFrame
    # for i, trip in trips_df.iterrows():
    #     shipment_ids = eval(trip['shipment_ids'])  # Convert string to list
    #     latitudes = eval(trip['latitudes'])  # Convert string to list
    #     longitudes = eval(trip['longitudes'])  # Convert string to list
    #     trip_id = trip['trip_id']  # Extract trip_id

    #     # Generate a random color for the trip
    #     trip_color = random_color()

    #     # Create a list of all coordinates for the trip (starting from the facility center)
    #     trip_coordinates = [(facility_lat, facility_lon)]  # Starting point: Facility center
    #     for lat, lon in zip(latitudes, longitudes):
    #         trip_coordinates.append((lat, lon))  # Add shipment locations

    #     # Add the return path to the facility center
    #     trip_coordinates.append((facility_lat, facility_lon))

    #     # Add a polyline for the trip path
    #     folium.PolyLine(
    #         trip_coordinates,
    #         color=trip_color,
    #         weight=4,
    #         opacity=0.7
    #     ).add_to(facility_map)

    #     # Add a landmark marker for each shipment in this trip
    #     for lat, lon, shipment_id in zip(latitudes, longitudes, shipment_ids):
    #         folium.Marker(
    #             location=[lat, lon],
    #             popup=f"Shipment ID: {shipment_id} | Trip ID: {trip_id}",
    #             icon=folium.Icon(color=trip_color, icon='map-marker', prefix='fa')  # Color-coded landmark icon
    #         ).add_to(marker_cluster)

    # #
    # facility_map.save('/content/optimized_trip_map_with_paths_return.html')


    # Mock Data (Replace with actual logic)
    # trips = [
    #     Trip(
    #         trip_id="1",
    #         shipments=[
    #             Shipment(1, 19.076, 72.877, "10:00 AM").__dict__,
    #             Shipment(2, 28.704, 77.102, "12:30 PM").__dict__
    #         ],
    #         mst_dist=50.0,
    #         trip_time=1.5,
    #         vehicle_type="Truck",
    #         avg_speed=80.0,
    #         min_speed=60.0,
    #         max_speed=75.0
    #     ).__dict__,
    #     Trip(
    #         trip_id="2",
    #         shipments=[
    #             Shipment(3, 28.704, 77.102, "2:00 PM").__dict__,
    #             Shipment(4, 19.076, 72.877, "4:30 PM").__dict__
    #         ],
    #         mst_dist=30.0,
    #         trip_time=1.0,
    #         vehicle_type="Van",
    #         avg_speed=70.0,
    #         min_speed=50.0,
    #         max_speed=65.0
    #     ).__dict__
    # ]

    # return jsonify(trips)

if __name__ == "__main__":
    app.run(debug=True)

def calculate_distance(coord1, coord2):
    return geodesic(coord1, coord2).km

def get_road_distance(coord1, coord2):
    return calculate_distance(coord1, coord2)


def route_distance(route_coords, facility):
    """
    Given a list of shipment coordinates (route_coords) and the facility coordinate,
    compute the total route distance if the trip starts at the facility, visits the
    shipments in the given order, and returns to the facility.
    """
    if not route_coords:
        return 0.0
    total = 0.0
    # from facility to first shipment
    total += calculate_distance(facility, route_coords[0])
    # between successive shipments
    for i in range(len(route_coords)-1):
        total += calculate_distance(route_coords[i], route_coords[i+1])
    # from last shipment back to facility
    total += calculate_distance(route_coords[-1], facility)
    return total
# ----------------------------
# Helper Functions
# ----------------------------

def angle_from_facility(shipment, facility):
    """
    Compute the polar angle (in radians) of a shipment's coordinates relative to the facility.
    """
    dlat = shipment['Latitude'] - facility[0]
    dlon = shipment['Longitude'] - facility[1]
    return math.atan2(dlat, dlon)

# ----------------------------
# Main Clustering Optimization Function
# ----------------------------

def optimize_trips_clustering(shipments_df, vehicle_df, facility):
    # """
    # For each delivery timeslot, group shipments using a sweep (angle-based) approach.
    # For each vehicle type (and available vehicle instance), build a trip by iterating
    # over the shipments (sorted by angle) and adding shipments one by one if:
    #    - The trip’s shipment count is within capacity,
    #    - And the total route distance (facility -> shipments in order -> facility) does not exceed max trip radius.
    # Returns a DataFrame of trips with columns:
    #   trip_id, shipment_ids, latitudes, longitudes, time_slot, num_shipments,
    #   mst_dist (total route distance), trip_time, vehicle_type.
    # """
    trips = []
    trip_id_counter = 1
    # Work on a copy and add an 'assigned' flag for shipments
    shipments_df = shipments_df.copy()
    shipments_df['assigned'] = False

    # Process shipments grouped by Delivery Timeslot
    for time_slot, group in shipments_df.groupby('Delivery Timeslot'):
        group = group.copy()
        # Compute polar angle relative to facility for each shipment
        group['angle'] = group.apply(lambda row: angle_from_facility(row, facility), axis=1)
        # Sort shipments by angle (sweep order)
        group = group.sort_values('angle').reset_index(drop=True)

        # While there remain unassigned shipments in this timeslot, form clusters (trips)
        while group[~group['assigned']].shape[0] > 0:
            # For each available vehicle type (one by one)
            for _, vehicle in vehicle_df.iterrows():
                # Convert vehicle parameters:
                cap_val = vehicle['Shipments_Capacity']
                max_rad_val = vehicle['Max Trip Radius (in KM)']
                num_val = vehicle['Number']

                capacity = float('inf') if str(cap_val).strip().lower() == "any" else int(cap_val)
                max_radius = float('inf') if str(max_rad_val).strip().lower() == "any" else float(max_rad_val)+40
                num_vehicles = float('inf') if str(num_val).strip().lower() == "any" else int(num_val)

                vehicles_used = 0
                # Form trips until available vehicles of this type are exhausted
                while vehicles_used < num_vehicles and group[~group['assigned']].shape[0] > 0:
                    cluster_indices = []
                    cluster_coords = []

                    # Sweep through the sorted group; add unassigned shipments if they fit the constraints
                    for idx, row in group.iterrows():
                        if not row['assigned']:
                            tentative_indices = cluster_indices + [idx]
                            tentative_coords = cluster_coords + [(row['Latitude'], row['Longitude'])]
                            # Check capacity constraint
                            if len(tentative_indices) > capacity:
                                continue
                            # Compute full route distance (facility -> shipments in tentative order -> facility)
                            tentative_route_distance = route_distance(tentative_coords, facility)
                            if tentative_route_distance <= max_radius:
                                # Accept the shipment in the current cluster
                                cluster_indices = tentative_indices
                                cluster_coords = tentative_coords
                            # Else: skip this shipment (it might be too far to add)

                    # If no shipment could be added, break out of the inner loop
                    if len(cluster_indices) == 0:
                        break

                    # Mark the shipments in this cluster as assigned (in group and in shipments_df)
                    shipment_ids = []
                    latitudes = []
                    longitudes = []
                    for idx in cluster_indices:
                        group.at[idx, 'assigned'] = True
                        shipment_id = group.at[idx, 'Shipment ID']
                        shipment_ids.append(shipment_id)
                        latitudes.append(group.at[idx, 'Latitude'])
                        longitudes.append(group.at[idx, 'Longitude'])
                        # Update the global shipments_df as well
                        shipments_df.loc[shipments_df['Shipment ID'] == shipment_id, 'assigned'] = True

                    # Compute final route distance and estimated trip time (assume 50 km/h speed)
                    final_distance = route_distance(cluster_coords, facility)
                    trip_time = (final_distance / 50.0) * 60  # minutes

                    trips.append({
                        'trip_id': f'T{trip_id_counter}',
                        'shipment_ids': shipment_ids,
                        'latitudes': latitudes,
                        'longitudes': longitudes,
                        'time_slot': time_slot,
                        'num_shipments': len(shipment_ids),
                        'mst_dist': final_distance,
                        'trip_time': trip_time,
                        'vehicle_type': vehicle['Vehicle Type']
                    })
                    trip_id_counter += 1
                    vehicles_used += 1
            # End for each vehicle type
        # End while unassigned shipments remain for this timeslot
    # End for each timeslot

    return pd.DataFrame(trips)