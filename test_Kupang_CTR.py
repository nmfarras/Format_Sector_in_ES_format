from geopy import Point
from geopy.distance import geodesic
import util
import matplotlib.pyplot as plt
import re

def dms_to_decimal(dms_str):
    """Convert DMS (Degrees, Minutes, Seconds) to decimal degrees."""
    match = re.match(r"(\d{2})(\d{2})(\d{2})([NS])\s*(\d{3})(\d{2})(\d{2})([EW])", dms_str)
    if not match:
        raise ValueError(f"Invalid DMS format: {dms_str}")

    lat_sign = -1 if match.group(4) == 'S' else 1
    lat = lat_sign * (int(match.group(1)) + int(match.group(2)) / 60 + int(match.group(3)) / 3600)

    lon_sign = -1 if match.group(8) == 'W' else 1
    lon = lon_sign * (int(match.group(5)) + int(match.group(6)) / 60 + int(match.group(7)) / 3600)

    return Point(lat, lon)

# Kupang CTR prompt:
"""
Kupang (CTR):
A circle with radius of 30 NM centred on “KPG” VOR/DME (S010.10.00.328 E123.41.30.508)
"""

case_name = "Kupang_CTR"

# Define center and radius
kpg_vor = dms_to_decimal("101000S 1234130E")
arc_radius_nm = 30
arc_radius_km = arc_radius_nm * 1.852

# Generate circle points
circle_points = util.generate_arc_points(
    arp=kpg_vor,
    bearing_start=0,
    bearing_end=360,
    distance_start_nm=arc_radius_nm,
    distance_end_nm=arc_radius_nm,
    step_degrees=5
)

# Convert points to tuples
circle_tuples = [(point.longitude, point.latitude) for point in circle_points]
boundary_points = circle_tuples + [circle_tuples[0]]  # Closing the circle

# Export KML
util.create_kml_polygon(f"{case_name}.kml", boundary_points)

# Format output
formatted_output = util.format_coor_points(boundary_points, case_name, "B")
print(formatted_output)

with open(f"{case_name}.txt", "w") as f:
    f.write(formatted_output)

# Plot
lons, lats = zip(*boundary_points)

plt.figure(figsize=(8, 8))
plt.plot(lons, lats, marker='o', linestyle='-', label='Kupang CTR')
plt.scatter(kpg_vor.longitude, kpg_vor.latitude, color='red', label='KPG VOR', s=100)
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title(f"{case_name} Boundary")
plt.legend()
plt.grid()
plt.show()

