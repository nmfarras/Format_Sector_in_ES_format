from geopy import Point
from geopy.distance import geodesic
import util
import matplotlib.pyplot as plt

# Define ARP coordinates
arp_bengkulu = Point(-3.86111, 102.33944)  # Fatmawati Soekarno ARP (03°51'40"S 102°20'22"E)
arc_radius_nm = 30  # Radius in nautical miles
arc_radius_km = arc_radius_nm * 1.852  # Convert to kilometers

# Generate circle points
arc_points = util.generate_arc_points(
    arp=arp_bengkulu,
    bearing_start=0,
    bearing_end=360,
    distance_start_nm=arc_radius_nm,
    distance_end_nm=arc_radius_nm,
    step_degrees=10
)

# Convert points to tuples
boundary_points = [(point.longitude, point.latitude) for point in arc_points]
boundary_points.append(boundary_points[0])  # Close the circle

# Export KML
case_name = "Bengkulu_CTR"
util.create_kml_polygon(f"{case_name}.kml", boundary_points)

# Format output
formatted_output = util.format_coor_points(boundary_points, case_name)
print(formatted_output)

with open(f"{case_name}.txt", "w") as f:
    f.write(formatted_output)

# Plot
lons, lats = zip(*boundary_points)
plt.figure(figsize=(8, 8))
plt.plot(lons, lats, marker='o', linestyle='-', label='Bengkulu CTR')
plt.scatter(arp_bengkulu.longitude, arp_bengkulu.latitude, color='red', label='ARP Bengkulu', s=100)

plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title(f"{case_name} Boundary")
plt.legend()
plt.grid()
plt.show()
