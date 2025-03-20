from geopy import Point
from geopy.distance import geodesic
import util
import matplotlib.pyplot as plt

"""
Timika CTR :
A circle with radius 25 NM centred on ARP

Mozes Kilangin ARP
043152S 1365300E
"""

case_name = "Timika_CTR"

# Define ARP center
arp_timika = util.dms_to_decimal("043152S 1365300E")
arc_radius_nm = 25  # Convert to KM
arc_radius_km = arc_radius_nm * 1.852  

# Generate arc points (full circle)
arc_points = util.generate_arc_points(
    arp=arp_timika,
    bearing_start=0,
    bearing_end=360,
    distance_start_nm=arc_radius_nm,
    distance_end_nm=arc_radius_nm,
    step_degrees=10
)

# Convert points to tuples
arc_tuples = [(point.longitude, point.latitude) for point in arc_points]

# Closing the polygon
boundary_points = arc_tuples + [arc_tuples[0]]

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
plt.plot(lons, lats, marker='o', linestyle='-', label='Timika CTR')
plt.scatter(arp_timika.longitude, arp_timika.latitude, color='red', label='ARP Timika', s=100)

plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title(f"{case_name} Boundary")
plt.legend()
plt.grid()
plt.show()