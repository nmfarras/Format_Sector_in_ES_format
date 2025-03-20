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
SOLO TMA:
072236S 1110308E - 072600S 1110000E - 074824S 1105441E thence clockwise along the circle of 20 NM radius centered at SO NDB to 072236S 1110308E

SO NDB
073043S 1104447E
"""

case_name = "SOLO_TMA"

# Define fixed boundary points
point_1 = dms_to_decimal("072236S 1110308E")
point_2 = dms_to_decimal("072600S 1110000E")
point_3 = dms_to_decimal("074824S 1105441E")

# Define arc center and radius
so_ndb = dms_to_decimal("073043.7S 1104447.6E")  # SO NDB
arc_radius_nm = 20  # Convert to KM
arc_radius_km = arc_radius_nm * 1.852

print(so_ndb)

# Compute bearing angles
bearing_start = util.initial_bearing_angle(so_ndb.latitude, so_ndb.longitude, point_3.latitude, point_3.longitude)
bearing_end = util.initial_bearing_angle(so_ndb.latitude, so_ndb.longitude, point_1.latitude, point_1.longitude)

# Generate arc points
arc_points = util.generate_arc_points(
    arp=so_ndb,
    bearing_start=bearing_start,
    bearing_end=bearing_end,
    distance_start_nm=arc_radius_nm,
    distance_end_nm=arc_radius_nm,
    step_degrees=10
)

# Convert points to tuples
arc_tuples = [(point.longitude, point.latitude) for point in arc_points]
fixed_tuples = [(point_1.longitude, point_1.latitude), (point_2.longitude, point_2.latitude), (point_3.longitude, point_3.latitude)]

# Combine all points
boundary_points = fixed_tuples + arc_tuples + [fixed_tuples[0]]  # Closing the polygon

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
plt.plot(lons, lats, marker='o', linestyle='-', label='SOLO TMA')
plt.scatter(so_ndb.longitude, so_ndb.latitude, color='red', label='SO NDB', s=100)
plt.scatter(point_1.longitude, point_1.latitude, color='yellow', label='StartPoint', s=450, edgecolors='black', linewidths=1.5)
plt.scatter([point_1.longitude, point_2.longitude, point_3.longitude], [point_1.latitude, point_2.latitude, point_3.latitude], color='green', label='Fixed Points', s=150, edgecolors='black', linewidths=1.5)

plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title(f"{case_name} Boundary and Arc")
plt.legend()
plt.grid()
plt.show()