from geopy import Point
from geopy.distance import geodesic
import util
import matplotlib.pyplot as plt
import re

def dms_to_decimal(dms_str):
    """Convert DMS (Degrees, Minutes, Seconds) or DMS with decimal seconds to decimal degrees."""
    match = re.match(r"(\d{2})(\d{2})(\d{2}(?:\.\d*)?)([NS])\s*(\d{3})(\d{2})(\d{2}(?:\.\d*)?)([EW])", dms_str)
    if not match:
        raise ValueError(f"Invalid DMS format: {dms_str}")
    
    lat_sign = -1 if match.group(4) == 'S' else 1
    lat = lat_sign * (int(match.group(1)) + int(match.group(2)) / 60 + float(match.group(3)) / 3600)
    
    lon_sign = -1 if match.group(8) == 'W' else 1
    lon = lon_sign * (int(match.group(5)) + int(match.group(6)) / 60 + float(match.group(7)) / 3600)
    
    return Point(lat, lon)

"""
JAKARTA TERMINAL EAST (TE) TMA
060000S 1065512E - 045656S 1070811E thence clockwise along the circle of 75 NM radius centered at 060700S 1064030E to 061816S 1075457E - 060000S 1065512E
"""

case_name = "Jakarta_TE_TMA"

# Define fixed boundary points
point_start = dms_to_decimal("060000S 1065512E")
point_mid = dms_to_decimal("045656S 1070811E")
point_end = dms_to_decimal("061816S 1075457E")

# Define arc center and radius
arc_center = dms_to_decimal("060700S 1064030E")  # Arc center
arc_radius_nm = 75  # Convert to KM
arc_radius_km = arc_radius_nm * 1.852

# Compute bearing angles
bearing_start = util.initial_bearing_angle(arc_center.latitude, arc_center.longitude, point_mid.latitude, point_mid.longitude)
bearing_end = util.initial_bearing_angle(arc_center.latitude, arc_center.longitude, point_end.latitude, point_end.longitude)

# Generate arc points
arc_points = util.generate_arc_points(
    arp=arc_center,
    bearing_start=bearing_start,
    bearing_end=bearing_end,
    distance_start_nm=arc_radius_nm,
    distance_end_nm=arc_radius_nm,
    step_degrees=10
)

# Convert points to tuples
arc_tuples = [(point.longitude, point.latitude) for point in arc_points]
fixed_tuples = [(point_start.longitude, point_start.latitude), (point_mid.longitude, point_mid.latitude), (point_end.longitude, point_end.latitude)]

# Combine all points
boundary_points = fixed_tuples[:2] + arc_tuples + [fixed_tuples[-1]] + [fixed_tuples[0]]  # Closing the polygon

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
plt.plot(lons, lats, marker='o', linestyle='-', label='Jakarta TE TMA')
plt.scatter(arc_center.longitude, arc_center.latitude, color='red', label='Arc Center', s=100)
plt.scatter(point_start.longitude, point_start.latitude, color='yellow', label='StartPoint', s=450, edgecolors='black', linewidths=1.5)
plt.scatter([point_start.longitude, point_mid.longitude, point_end.longitude], [point_start.latitude, point_mid.latitude, point_end.latitude], color='green', label='Fixed Points', s=150, edgecolors='black', linewidths=1.5)

plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title(f"{case_name} Boundary and Arc")
plt.legend()
plt.grid()
plt.show()
