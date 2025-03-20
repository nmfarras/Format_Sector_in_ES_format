from geopy import Point
from geopy.distance import geodesic
import util
import matplotlib.pyplot as plt

"""
Pekanbaru CTR :
A circle with radius of 60 NM centred on PKU VOR/DME

PKU VOR/DME
002532.1N 1012629.8E
"""

case_name = "Pekanbaru_CTR"

# Define center point and radius
arp_pku = util.dms_to_decimal("002532.1N 1012629.8E")
radius_nm = 60  # Nautical miles
radius_km = radius_nm * 1.852  # Convert to kilometers

# Generate circle points
arc_points = util.generate_arc_points(
    arp=arp_pku,
    bearing_start=0,
    bearing_end=360,
    distance_start_nm=radius_nm,
    distance_end_nm=radius_nm,
    step_degrees=10
)

# Convert points to tuples
boundary_points = [(point.longitude, point.latitude) for point in arc_points]

# Close the polygon
boundary_points.append(boundary_points[0])

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
plt.plot(lons, lats, marker='o', linestyle='-', label='Pekanbaru CTR')
plt.scatter(arp_pku.longitude, arp_pku.latitude, color='red', label='PKU VOR/DME', s=100)

plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title(f"{case_name} Boundary")
plt.legend()
plt.grid()
plt.show()