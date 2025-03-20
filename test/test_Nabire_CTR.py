from geopy import Point
from geopy.distance import geodesic
import util
import matplotlib.pyplot as plt

"""
Nabire CTR :
A circle with radius of 25 NM centred at ARP

Douw ARP
032353S 1352350E
"""

case_name = "Nabire_CTR"

# Define ARP center
arp_nabire = util.dms_to_decimal("032353S 1352350E")
arc_radius_nm = 25  # Convert to KM
arc_radius_km = arc_radius_nm * 1.852

# Generate circle points
arc_points = util.generate_arc_points(
    arp=arp_nabire,
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
plt.plot(lons, lats, marker='o', linestyle='-', label='Nabire CTR')
plt.scatter(arp_nabire.longitude, arp_nabire.latitude, color='red', label='ARP Nabire', s=100)

plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title(f"{case_name} Boundary")
plt.legend()
plt.grid()
plt.show()