from geopy import Point
from geopy.distance import geodesic
import util
import re
import matplotlib.pyplot as plt

# Convert DMS to Decimal Degrees
def dms_to_decimal(dms_str):
    """Convert DMS (Degrees Minutes Seconds) format to decimal degrees."""
    match = re.match(r"(\d{2})(\d{2})(\d{2})([NS])\s*(\d{3})(\d{2})(\d{2})([EW])", dms_str)
    if not match:
        raise ValueError(f"Invalid DMS format: {dms_str}")

    lat_sign = -1 if match.group(4) == 'S' else 1
    lat = lat_sign * (int(match.group(1)) + int(match.group(2)) / 60 + int(match.group(3)) / 3600)

    lon_sign = -1 if match.group(8) == 'W' else 1
    lon = lon_sign * (int(match.group(5)) + int(match.group(6)) / 60 + int(match.group(7)) / 3600)

    return Point(lat, lon)

# Case Name
case_name = "Tanjung_Pandan_CTR"

arp_pangkal = dms_to_decimal("024443S 1074511E")  # Arc Center
arc_start = dms_to_decimal("022206S 1072522E")  # Arc starts from last fixed point
arc_end = dms_to_decimal("024817S 1071525E")  # Arc ends here

# Calculate distances
distance_start_nm = geodesic(arp_pangkal, arc_start).meters / 1852
distance_end_nm = geodesic(arp_pangkal, arc_end).meters / 1852

# Generate the Arc in Counterclockwise Order
arc_points_1 = util.generate_arc_points(
    arp=arp_pangkal,
    bearing_start=util.initial_bearing_angle(arp_pangkal.latitude, arp_pangkal.longitude, arc_start.latitude, arc_start.longitude),
    bearing_end=util.initial_bearing_angle(arp_pangkal.latitude, arp_pangkal.longitude, arc_end.latitude, arc_end.longitude),
    distance_start_nm=30,
    distance_end_nm=30,
    step_degrees=-5  # Counterclockwise direction
)

# Convert geopy points to (lon, lat) tuples
arc_points_tuples_1 = [(point.longitude, point.latitude) for point in arc_points_1]

# Generate the Arc in Clockwise Order
arc_points_2 = util.generate_arc_points(
    arp=arp_pangkal,
    bearing_start=util.initial_bearing_angle(arp_pangkal.latitude, arp_pangkal.longitude, arc_start.latitude, arc_start.longitude),
    bearing_end=util.initial_bearing_angle(arp_pangkal.latitude, arp_pangkal.longitude, arc_end.latitude, arc_end.longitude),
    distance_start_nm=30,
    distance_end_nm=30,
    step_degrees=5  # Clockwise direction
)

# Convert geopy points to (lon, lat) tuples
arc_points_tuples_2 = [(point.longitude, point.latitude) for point in arc_points_2]

# Combine everything into boundary points
boundary_points = (
    [(point.longitude, point.latitude) for point in [arc_end]] +
    arc_points_tuples_1[::-1] +
    [(point.longitude, point.latitude) for point in [arc_start]]+
    arc_points_tuples_2 
)

arc_points_tuples = [*arc_points_tuples_1, *arc_points_tuples_1]

# Create KML
util.create_kml_polygon(f"{case_name}.kml", boundary_points)

# Save as .txt with formatted coordinates
formatted_output = util.format_coor_points(boundary_points, case_name)
print(formatted_output)

with open(f"{case_name}.txt", "w") as f:
    f.write(formatted_output)

# Debugging Info
print(f"{case_name} Bearings:")
print(f"  Bearing Start: {util.initial_bearing_angle(arp_pangkal.latitude, arp_pangkal.longitude, arc_start.latitude, arc_start.longitude)}")
print(f"  Bearing End: {util.initial_bearing_angle(arp_pangkal.latitude, arp_pangkal.longitude, arc_end.latitude, arc_end.longitude)}")

print(f"{case_name} Distances:")
print(f"  Distance Start (NM): {distance_start_nm}")
print(f"  Distance End (NM): {distance_end_nm}")

print(f"{case_name} Arc Points (Lon, Lat):")
for pt in arc_points_tuples:
    print(f"  {pt}")

# Visualization
lons, lats = zip(*boundary_points)

plt.figure(figsize=(8, 8))
plt.plot(lons, lats, marker='o', linestyle='-', label='Boundary')
plt.scatter(arp_pangkal.longitude, arp_pangkal.latitude, color='red', label='ARP Pangkal Pinang', s=100)
plt.scatter([arc_start.longitude, arc_end.longitude], [arc_start.latitude, arc_end.latitude], color='green', label='Arc Start/End', s=150, edgecolors='black', linewidths=1.5)

plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title(f"{case_name} Boundary and Arc")
plt.legend()
plt.grid()
plt.show()
