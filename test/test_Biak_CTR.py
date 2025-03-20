from geopy import Point
from geopy.distance import geodesic
import util
import matplotlib.pyplot as plt

"""
Biak CTR :
A circle with radius of 30 NM centred at ARP

Frans Kaisiepo ARP
011131S 1360636E
"""

case_name = "Biak_CTR"

# Define ARP location
arp_biak = util.dms_to_decimal("011131S 1360636E")
arc_radius_nm = 30  # Convert to KM
arc_radius_km = arc_radius_nm * 1.852  

# Generate circular boundary
arc_points = util.generate_arc_points(
    arp=arp_biak,
    bearing_start=0,
    bearing_end=360,
    distance_start_nm=arc_radius_nm,
    distance_end_nm=arc_radius_nm,
    step_degrees=10
)

# Convert points to tuples
arc_tuples = [(point.longitude, point.latitude) for point in arc_points]
boundary_points = arc_tuples + [arc_tuples[0]]  # Closing the circle

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
plt.plot(lons, lats, marker='o', linestyle='-', label='Biak CTR')
plt.scatter(arp_biak.longitude, arp_biak.latitude, color='red', label='ARP Biak', s=100)

plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title(f"{case_name} Boundary")
plt.legend()
plt.grid()
plt.show()