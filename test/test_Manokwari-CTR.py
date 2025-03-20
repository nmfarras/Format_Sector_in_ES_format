from geopy import Point
from geopy.distance import geodesic
import util
import matplotlib.pyplot as plt

"""
MANOKWARI CTR :
A circle with radius of 25 NM centered at ARP

Sendani ARP
005338S 1340301E
"""

case_name = "Manokwari_CTR"

# Define ARP (Aerodrome Reference Point) as center
arp_manokwari = util.dms_to_decimal("005338S 1340301E")
arc_radius_nm = 25  # Nautical miles
arc_radius_km = arc_radius_nm * 1.852  # Convert to kilometers

# Generate circle points
arc_points = util.generate_arc_points(
    arp=arp_manokwari,
    bearing_start=0,
    bearing_end=360,
    distance_start_nm=arc_radius_nm,
    distance_end_nm=arc_radius_nm,
    step_degrees=10
)

# Convert to tuples
circle_tuples = [(point.longitude, point.latitude) for point in arc_points]
boundary_points = circle_tuples + [circle_tuples[0]]  # Closing the polygon

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
plt.plot(lons, lats, marker='o', linestyle='-', label='Manokwari CTR')
plt.scatter(arp_manokwari.longitude, arp_manokwari.latitude, color='red', label='ARP Manokwari', s=100)

plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title(f"{case_name} Boundary")
plt.legend()
plt.grid()
plt.show()
