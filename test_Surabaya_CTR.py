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

"""
Surabaya CTR :
074000S 1125600E - 074000S 1121500E - 072700S 1121000E - 072552S 1120610E thence clockwise along the circle of 40.0NM radius centered at on SBR VOR/DME to 074938S 1131530E - 074600S 1131200E - 074000S 1125600E

SBR VOR/DME
072226S 1124616E
"""

case_name = "Surabaya_CTR"

# Define fixed boundary points
fixed_points = [
    dms_to_decimal("074000S 1125600E"),
    dms_to_decimal("074000S 1121500E"),
    dms_to_decimal("072700S 1121000E"),
    dms_to_decimal("072552S 1120610E")
]

# Define arc center and radius
center_sbr_vor = dms_to_decimal("072226S 1124616E")  # SBR VOR/DME
arc_radius_nm = 40  # Convert to KM
arc_radius_km = arc_radius_nm * 1.852  

# Define arc start and end points
arc_start = dms_to_decimal("072552S 1120610E")
arc_end = dms_to_decimal("074938S 1131530E")

# Compute bearing angles
bearing_start = util.initial_bearing_angle(center_sbr_vor.latitude, center_sbr_vor.longitude, arc_start.latitude, arc_start.longitude)
bearing_end = util.initial_bearing_angle(center_sbr_vor.latitude, center_sbr_vor.longitude, arc_end.latitude, arc_end.longitude)

# Generate arc points
arc_points = util.generate_arc_points(
    arp=center_sbr_vor,
    bearing_start=bearing_start,
    bearing_end=bearing_end,
    distance_start_nm=arc_radius_nm,
    distance_end_nm=arc_radius_nm,
    step_degrees=5
)

# Convert points to tuples
arc_tuples = [(point.longitude, point.latitude) for point in arc_points]
fixed_tuples = [(point.longitude, point.latitude) for point in fixed_points]

# Additional closing points
closing_points = [
    dms_to_decimal("074600S 1131200E"),
    dms_to_decimal("074000S 1125600E")
]
closing_tuples = [(point.longitude, point.latitude) for point in closing_points]

# Combine all points
boundary_points = fixed_tuples + arc_tuples + [(point.longitude, point.latitude) for point in [arc_end]] + closing_tuples

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
plt.plot(lons, lats, marker='o', linestyle='-', label='Surabaya CTR')
plt.scatter(center_sbr_vor.longitude, center_sbr_vor.latitude, color='red', label='SBR VOR/DME', s=100)
plt.scatter([arc_start.longitude, arc_end.longitude], [arc_start.latitude, arc_end.latitude], color='green', label='Arc Start/End', s=150, edgecolors='black', linewidths=1.5)
plt.scatter(fixed_points[0].longitude, fixed_points[0].latitude, color='yellow', label='StartPoint', s=150, edgecolors='black', linewidths=1.5)

plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title(f"{case_name} Boundary and Arc")
plt.legend()
plt.grid()
plt.show()
