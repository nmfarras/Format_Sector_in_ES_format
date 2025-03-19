from geopy import Point
from geopy.distance import geodesic
import re
import util

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

case_name = "Jambi_CTR"

fixed_points = [
    dms_to_decimal("001743S 1040042E"),
    dms_to_decimal("010206S 1043536E"),
    dms_to_decimal("015241S 1041550E")  # Last fixed point before arc
]

arp_jambi = dms_to_decimal("013808S 1033835E")  # Arc center
arc_start = fixed_points[-1]  # Start of the arc
arc_end = dms_to_decimal("020928S 1031344E")  # End of the arc
print(arc_end.latitude, arc_end.longitude)


distance_start_nm = geodesic(arp_jambi, arc_start).meters / 1852
distance_end_nm = geodesic(arp_jambi, arc_end).meters / 1852

# Generate the arc (clockwise, 40 NM)
arc_points = util.generate_arc_points(
    arp=arp_jambi,
    bearing_start=util.initial_bearing_angle(arp_jambi.latitude, arp_jambi.longitude, arc_start.latitude, arc_start.longitude),
    bearing_end=util.initial_bearing_angle(arp_jambi.latitude, arp_jambi.longitude, arc_end.latitude, arc_end.longitude),
    distance_start_nm=distance_start_nm,
    distance_end_nm=distance_end_nm,
    step_degrees=10  # Clockwise
)

# Convert geopy points to (lon, lat) tuples
arc_points_tuples = [(point.longitude, point.latitude) for point in arc_points]

# Additional fixed points after the arc
additional_points = [
    dms_to_decimal("012715S 1024828E"),
    dms_to_decimal("001743S 1040042E")  # Closing point
]

# Combine everything into boundary points
boundary_points = (
    [(point.longitude, point.latitude) for point in fixed_points] +
    arc_points_tuples +
    [(point.longitude, point.latitude) for point in [arc_end, *additional_points]]
)

# Create KML
poly_coor = util.create_kml_polygon(f"{case_name}.kml", boundary_points)

# Save as .txt with format
formatted_output = util.format_coor_points(boundary_points, case_name)
print(formatted_output)

# Save to file
with open(f"{case_name}.txt", "w") as f:
    f.write(formatted_output)
    
print(f"{case_name} Bearings:")
print(f"  Bearing Start: {util.initial_bearing_angle(arp_jambi.latitude, arp_jambi.longitude, arc_start.latitude, arc_start.longitude)}")
print(f"  Bearing End: {util.initial_bearing_angle(arp_jambi.latitude, arp_jambi.longitude, arc_end.latitude, arc_end.longitude)}")

print(f"{case_name} Distances:")
print(f"  Distance Start (NM): {distance_start_nm}")
print(f"  Distance End (NM): {distance_end_nm}")

print(f"{case_name} Arc Points (Lon, Lat):")
for pt in arc_points_tuples:
    print(f"  {pt}")

import matplotlib.pyplot as plt

# Extracting longitude and latitude from boundary points
lons, lats = zip(*boundary_points)

# Save points to a text file
with open(f"{case_name}_points.txt", "w") as f:
    f.write("# Longitude, Latitude\n")
    f.write("# Boundary Points\n")
    for lon, lat in zip(lons, lats):
        f.write(f"{lon}, {lat}\n")
    
    f.write("\n# ARP Sultan Thaha\n")
    f.write(f"{arp_jambi.longitude}, {arp_jambi.latitude}\n")
    
    f.write("\n# Arc Start\n")
    f.write(f"{arc_start.longitude}, {arc_start.latitude}\n")
    
    f.write("\n# Arc End\n")
    f.write(f"{arc_end.longitude}, {arc_end.latitude}\n")

# Plotting
plt.figure(figsize=(8, 8))
plt.plot(lons, lats, marker='o', linestyle='-', label='Boundary')
plt.scatter(arp_jambi.longitude, arp_jambi.latitude, color='red', label='ARP Sultan Thaha', s=100)
plt.scatter([arc_start.longitude, arc_end.longitude], [arc_start.latitude, arc_end.latitude], color='green', label='Arc Start/End', s=150, edgecolors='black', linewidths=1.5)

# Labels and styling
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title(f"{case_name} Boundary and Arc")
plt.legend()
plt.grid()
plt.show()
