from geopy import Point
from geopy.distance import geodesic
import util
import re
import matplotlib.pyplot as plt
import math

# def dms_to_decimal(dms_str):
#     match = re.match(r"(\d{2})(\d{2})(\d{2})([NS])\s*(\d{3})(\d{2})(\d{2})([EW])", dms_str)
#     if not match:
#         raise ValueError(f"Invalid DMS format: {dms_str}")

#     lat_sign = -1 if match.group(4) == 'S' else 1
#     lat = lat_sign * (int(match.group(1)) + int(match.group(2)) / 60 + int(match.group(3)) / 3600)

#     lon_sign = -1 if match.group(8) == 'W' else 1
#     lon = lon_sign * (int(match.group(5)) + int(match.group(6)) / 60 + int(match.group(7)) / 3600)

#     return Point(lat, lon)

"""
Prompt

Bandung CTR :
064716S 1074346E - 064716S 1065700E - 074960S 1065700E - 074960S 1082933E - 072418S 1084814E - 063832S 1074833E then an arc center on 060700S 1064030E from 064716S 1074346E to 063832S 1074833E
"""

case_name = "Bandung_CTR"

# Define fixed points
fixed_points = [
    util.dms_to_decimal("064716S 1074346E"),
    util.dms_to_decimal("064716S 1065700E"),
    util.dms_to_decimal("074960S 1065700E"),
    util.dms_to_decimal("074960S 1082933E"),
    util.dms_to_decimal("072418S 1084814E"),
    util.dms_to_decimal("063832S 1074833E")
]

# Arc center and start/end points
arp_bandung = util.dms_to_decimal("060700S 1064030E")  # Arc center
arc_start = util.dms_to_decimal("064716S 1074346E")
arc_end = util.dms_to_decimal("063832S 1074833E")

# Arc radius (approximate)
distance_nm = geodesic((arp_bandung.latitude, arp_bandung.longitude), (arc_start.latitude, arc_start.longitude)).nautical

# Compute bearings
bearing_start = util.initial_bearing_angle(arp_bandung.latitude, arp_bandung.longitude, arc_start.latitude, arc_start.longitude)
bearing_end = util.initial_bearing_angle(arp_bandung.latitude, arp_bandung.longitude, arc_end.latitude, arc_end.longitude)

# Generate arc points
arc_points = util.generate_arc_points(
    arp=arp_bandung,
    bearing_start=bearing_start,
    bearing_end=bearing_end,
    distance_start_nm=distance_nm,
    distance_end_nm=distance_nm,
    step_degrees=-min(5, abs(bearing_end - bearing_start) / 10)  # Adjust dynamically
)

arc_points_tuples = [(point.longitude, point.latitude) for point in arc_points[::-1]]

# Construct the full boundary
boundary_points = (
    [(point.longitude, point.latitude) for point in fixed_points] +
    arc_points_tuples
    + [(point.longitude, point.latitude) for point in [arc_start]]
)

# Export KML
util.create_kml_polygon(f"{case_name}.kml", boundary_points)

# Format and save output
formatted_output = util.format_coor_points(boundary_points, case_name)
print(formatted_output)

with open(f"{case_name}.txt", "w") as f:
    f.write(formatted_output)

# boundary_points.append(*[(point.longitude, point.latitude) for point in [arc_start]])

# Plot the boundary
lons, lats = zip(*boundary_points)

plt.figure(figsize=(8, 8))
plt.plot(lons, lats, marker='o', linestyle='-', label='Boundary')
plt.scatter(arp_bandung.longitude, arp_bandung.latitude, color='red', label='ARP Bandung', s=100)
plt.scatter([arc_start.longitude, arc_end.longitude], [arc_start.latitude, arc_end.latitude], color='green', label='Arc Start/End', s=150, edgecolors='black', linewidths=2.5)
plt.scatter(fixed_points[0].longitude, fixed_points[0].latitude, color='yellow', label='StartPoint', s=150, edgecolors='black', linewidths=1.5)

plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title(f"{case_name} Boundary and Arc")
plt.legend()
plt.grid()
plt.show()
