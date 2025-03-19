from geopy import Point
from geopy.distance import geodesic
import util
import matplotlib.pyplot as plt
import numpy as np
import re

def dms_to_decimal(dms_str):
    """Convert DMS (Degrees, Minutes, Seconds) to decimal degrees."""
    match = re.match(r"(\d{2})°?(\d{2})?'?(\d{2}(\.\d+)?)?\"?([NS])\s*(\d{3})°?(\d{2})?'?(\d{2}(\.\d+)?)?\"?([EW])", dms_str)
    if not match:
        raise ValueError(f"Invalid DMS format: {dms_str}")

    lat_sign = -1 if match.group(5) == 'S' else 1
    lat = lat_sign * (int(match.group(1)) + int(match.group(2)) / 60 + (float(match.group(3) or 0) / 3600))

    lon_sign = -1 if match.group(10) == 'W' else 1
    lon = lon_sign * (int(match.group(6)) + int(match.group(7)) / 60 + (float(match.group(8) or 0) / 3600))

    return Point(lat, lon)


"""
Prompt

MAJALENGKA CTR :
063832S 1074833E - 072418S 1084814E - 071300S 1085450E - 071441S 1090934E thence clockwise along the arc of a circle radius 75 NM centered at ANY VOR/DME to 061803S 1091938E - 060153S 1075519E thence clockwise along the arc of a circle radius 75 NM centered at 060700S 1064030E to 063832S 1074833E

ANY VOR/DME
06°58'28.9''S  110°22'48.4''E
"""


case_name = "Majalengka_CTR"

# Define fixed boundary points
fixed_points = [
    dms_to_decimal("063832S 1074833E"),
    dms_to_decimal("072418S 1084814E"),
    dms_to_decimal("071300S 1085450E"),
    dms_to_decimal("071441S 1090934E")
]

# Define ARP and VOR/DME centers for arcs
center_any_vor = dms_to_decimal("065829S 1102248E")  # ANY VOR/DME
center_secondary = dms_to_decimal("060700S 1064030E")

# Define arc radius in NM
arc_radius_nm = 75  # Convert to KM
arc_radius_km = arc_radius_nm * 1.852  

# Arc 1: From 071441S 1090934E to 061803S 1091938E, centered at ANY VOR/DME
arc1_start = dms_to_decimal("071441S 1090934E")
arc1_end = dms_to_decimal("061803S 1091938E")

bearing_start1 = util.initial_bearing_angle(center_any_vor.latitude, center_any_vor.longitude, arc1_start.latitude, arc1_start.longitude)
bearing_end1 = util.initial_bearing_angle(center_any_vor.latitude, center_any_vor.longitude, arc1_end.latitude, arc1_end.longitude)

arc1_points = util.generate_arc_points(
    arp=center_any_vor,
    bearing_start=bearing_start1,
    bearing_end=bearing_end1,
    distance_start_nm=arc_radius_nm,
    distance_end_nm=arc_radius_nm,
    step_degrees=min(5, abs(bearing_end1 - bearing_start1) / 10)
)

# Arc 2: From 060153S 1075519E to 063832S 1074833E, centered at 060700S 1064030E
arc2_start = dms_to_decimal("060153S 1075519E")
arc2_end = dms_to_decimal("063832S 1074833E")

bearing_start2 = util.initial_bearing_angle(center_secondary.latitude, center_secondary.longitude, arc2_start.latitude, arc2_start.longitude)
bearing_end2 = util.initial_bearing_angle(center_secondary.latitude, center_secondary.longitude, arc2_end.latitude, arc2_end.longitude)

arc2_points = util.generate_arc_points(
    arp=center_secondary,
    bearing_start=bearing_start2,
    bearing_end=bearing_end2,
    distance_start_nm=arc_radius_nm,
    distance_end_nm=arc_radius_nm,
    step_degrees=min(5, abs(bearing_end2 - bearing_start2) / 10)
)

# Convert points to tuples
arc1_tuples = [(point.longitude, point.latitude) for point in arc1_points]
arc2_tuples = [(point.longitude, point.latitude) for point in arc2_points]
fixed_tuples = [(point.longitude, point.latitude) for point in fixed_points]

# Combine all points
boundary_points = fixed_tuples + arc1_tuples + [(arc1_end.longitude, arc1_end.latitude)] + [(arc2_start.longitude, arc2_start.latitude)] + arc2_tuples 

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
plt.plot(lons, lats, marker='o', linestyle='-', label='Majalengka CTR')
plt.scatter(center_any_vor.longitude, center_any_vor.latitude, color='red', label='ANY VOR/DME', s=100)
plt.scatter(center_secondary.longitude, center_secondary.latitude, color='blue', label='060700S 1064030E', s=100)
plt.scatter([arc1_start.longitude, arc1_end.longitude], [arc1_start.latitude, arc1_end.latitude], color='green', label='Arc 1 Start/End', s=150, edgecolors='black', linewidths=1.5)
plt.scatter([arc2_start.longitude, arc2_end.longitude], [arc2_start.latitude, arc2_end.latitude], color='orange', label='Arc 2 Start/End', s=150, edgecolors='black', linewidths=1.5)

plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title(f"{case_name} Boundary and Arcs")
plt.legend()
plt.grid()
plt.show()
