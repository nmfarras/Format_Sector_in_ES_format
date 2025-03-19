from geopy import Point
from geopy.distance import geodesic
import util
import matplotlib.pyplot as plt
import re

# Convert DMS (Degrees, Minutes, Seconds) to decimal degrees
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

"""
FRANSISKUS XAVERIUS SEDA ATZ :
A circle with radius of 5 NM centred on MOF VOR/DME

MOF VOR/DME
S0082853 E1195305
"""

case_name = "WATC_ATZ"

# Define circle center and radius
center_point = dms_to_decimal("083827S 1221422E")

circle_radius_nm = 5
circle_radius_km = circle_radius_nm * 1.852  # Convert NM to KM

# Generate circle points
# Generate arc points
circle_points = util.generate_arc_points(
    arp=center_point,
    bearing_start=0,
    bearing_end=360,
    distance_start_nm=circle_radius_nm,
    distance_end_nm=circle_radius_nm,
    step_degrees=10
)

# Convert to coordinate tuples
boundary_points = [(point.longitude, point.latitude) for point in circle_points]

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
plt.plot(lons, lats, marker='o', linestyle='-', label='WATC ATZ')
plt.scatter(center_point.longitude, center_point.latitude, color='red', label='MOF VOR/DME', s=100)

plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title(f"{case_name} Boundary")
plt.legend()
plt.grid()
plt.show()
