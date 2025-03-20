from geopy import Point
from geopy.distance import geodesic
import util
import matplotlib.pyplot as plt

"""
Sorong CTR :
A circle with radius of 30 NM centred at ARP

Sorong ARP
005330S 1311713E
"""

case_name = "Sorong_CTR"

# Define the ARP (center of the circle)
arp_sorong = util.dms_to_decimal("005330S 1311713E")  # Sorong ARP
arc_radius_nm = 30  # Radius in nautical miles
arc_radius_km = arc_radius_nm * 1.852  # Convert to KM

# Generate circle points
circle_points = util.generate_arc_points(
    arp=arp_sorong,
    bearing_start=0,
    bearing_end=360,
    distance_start_nm=arc_radius_nm,
    distance_end_nm=arc_radius_nm,
    step_degrees=10
)

# Convert points to tuples
boundary_points = [(point.longitude, point.latitude) for point in circle_points] # Closing the circle

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
plt.plot(lons, lats, marker='o', linestyle='-', label='Sorong CTR')
plt.scatter(arp_sorong.longitude, arp_sorong.latitude, color='red', label='ARP Sorong', s=100)

plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title(f"{case_name} Boundary")
plt.legend()
plt.grid()
plt.show()
