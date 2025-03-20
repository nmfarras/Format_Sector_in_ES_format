from geopy import Point
from geopy.distance import geodesic
import util
import matplotlib.pyplot as plt
import re

def dms_to_decimal(dms_str):
    """Convert DMS (Degrees, Minutes, Seconds) to decimal degrees."""
    match = re.match(r"(\d{2})(\d{2})(\d{2}\.?\d*)([NS])\s*(\d{3})(\d{2})(\d{2}\.?\d*)([EW])", dms_str)
    if not match:
        raise ValueError(f"Invalid DMS format: {dms_str}")

    lat_sign = -1 if match.group(4) == 'S' else 1
    lat = lat_sign * (int(match.group(1)) + int(match.group(2)) / 60 + float(match.group(3)) / 3600)

    lon_sign = -1 if match.group(8) == 'W' else 1
    lon = lon_sign * (int(match.group(5)) + int(match.group(6)) / 60 + float(match.group(7)) / 3600)

    return Point(lat, lon)

"""
JAKARTA TERMINAL SOUTH (TS) TMA:
060000S 1065512E - 061816S 1075457E thence clockwise along the circle of 75 NM radius centered at 060700S 1064030E to 064716S 1074411E - 064716S 1065700E - 072032S 1065700E thence clockwise along the circle of 75 NM radius centered at 060700S 1064030E to 063728S 1053136E - 060000S 1065512E
"""

case_name = "Jakarta_TS_TMA"

# Define fixed boundary points
points = [
    dms_to_decimal("060000S 1065512E"),
    dms_to_decimal("061816S 1075457E"),
    dms_to_decimal("064716S 1074411E"),
    dms_to_decimal("064716S 1065700E"),
    dms_to_decimal("072032S 1065700E"),
    dms_to_decimal("063728S 1053136E"),
    dms_to_decimal("060000S 1065512E")
]

# Define arc center and radius
arc_center = dms_to_decimal("060700S 1064030E")  # Arc center for the circles
arc_radius_nm = 75  # Convert to KM
arc_radius_km = arc_radius_nm * 1.852  

# Generate arc points
arc1 = util.generate_arc_points(
    arp=arc_center,
    bearing_start=util.initial_bearing_angle(arc_center.latitude, arc_center.longitude, points[1].latitude, points[1].longitude),
    bearing_end=util.initial_bearing_angle(arc_center.latitude, arc_center.longitude, points[2].latitude, points[2].longitude),
    distance_start_nm=arc_radius_nm,
    distance_end_nm=arc_radius_nm,
    step_degrees=5
)

arc2 = util.generate_arc_points(
    arp=arc_center,
    bearing_start=util.initial_bearing_angle(arc_center.latitude, arc_center.longitude, points[4].latitude, points[4].longitude),
    bearing_end=util.initial_bearing_angle(arc_center.latitude, arc_center.longitude, points[5].latitude, points[5].longitude),
    distance_start_nm=arc_radius_nm,
    distance_end_nm=arc_radius_nm,
    step_degrees=10
)

# Convert points to tuples
arc1_tuples = [(point.longitude, point.latitude) for point in arc1]
arc2_tuples = [(point.longitude, point.latitude) for point in arc2]
fixed_tuples = [(p.longitude, p.latitude) for p in points]

# Combine all points
boundary_points = [fixed_tuples[0]] + [(p.longitude, p.latitude) for p in [points[1]]]+ arc1_tuples + fixed_tuples[2:5] + arc2_tuples + [(p.longitude, p.latitude) for p in [points[5]]] + [fixed_tuples[-1]]

# Export KML
util.create_kml_polygon(f"{case_name}.kml", boundary_points)

# Format output
formatted_output = util.format_coor_points(boundary_points, case_name)
print(formatted_output)

with open(f"{case_name}.txt", "w") as f:
    f.write(formatted_output)

# Plot
lons, lats = zip(*boundary_points)

plt.figure(figsize=(8, 8))
plt.plot(lons, lats, marker='o', linestyle='-', label='Jakarta TS TMA')
plt.scatter(arc_center.longitude, arc_center.latitude, color='red', label='Arc Center', s=100)
plt.scatter(points[0].longitude, points[0].latitude, color='yellow', label='StartPoint', s=450, edgecolors='black', linewidths=1.5)
plt.scatter([p.longitude for p in points], [p.latitude for p in points], color='green', label='Boundary Points', s=150, edgecolors='black', linewidths=1.5)

plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title(f"{case_name} Boundary and Arc")
plt.legend()
plt.grid()
plt.show()