from geopy import Point
from matplotlib import pyplot as plt
import util

## Data define in this section is based on the characteristic of the boundary
"""
    Creates a KML and txt file with a polygon using the given boundary points.
    Method that usually used is creating arch, the rest should be the same
    
    Methods:
        initial_bearing_angle (float): The name of the KML file to save.
        generate_arc_points (list of tuples): List of (longitude, latitude) coordinates forming the arc.
        color (str): Color of the polygon outline (default: red).
        alpha (str): Transparency of the polygon fill (default: '50').
    
    Returns:
        str: The saved KML file path.
"""
# Define case
case_name = "Bandar_Aceh_CTR"

# Define ARP
arp = Point(5.51694, 95.42000)  # Converted from DMS to decimal

# Define start and end points
start_point = Point(6.00000, 95.54917)
end_point = Point(6.00000, 95.29083)

# Compute bearings
bearing_start = util.initial_bearing_angle(arp.latitude, arp.longitude, start_point.latitude, start_point.longitude)
bearing_end = util.initial_bearing_angle(arp.latitude, arp.longitude, end_point.latitude, end_point.longitude)

# Generate arc points
arc_points = util.generate_arc_points(arp, bearing_start, bearing_end, 30, 30)

# Convert arc points to KML format
boundary_points = [(p.longitude, p.latitude) for p in arc_points]
boundary_points.append(boundary_points[0])  # Close the polygon

# Create KML
poly_coor = util.create_kml_polygon(f"{case_name}.kml", boundary_points)

# Save as .txt with format
formatted_output = util.format_coor_points(boundary_points, case_name)

# Save to file
with open(f"{case_name}.txt", "w") as f:
    f.write(formatted_output)
    
    
# Extracting longitude and latitude from boundary points
lons, lats = zip(*boundary_points)

# Save points to a text file
with open(f"{case_name}_points.txt", "w") as f:
    f.write("# Longitude, Latitude\n")
    f.write("# Boundary Points\n")
    for lon, lat in zip(lons, lats):
        f.write(f"{lon}, {lat}\n")
    
    f.write("\n# ARP Banda Aceh\n")
    f.write(f"{arp.longitude}, {arp.latitude}\n")
    
    f.write("\n# Arc Start\n")
    f.write(f"{start_point.longitude}, {start_point.latitude}\n")
    
    f.write("\n# Arc End\n")
    f.write(f"{end_point.longitude}, {end_point.latitude}\n")

# Plotting
plt.figure(figsize=(8, 8))
plt.plot(lons, lats, marker='o', linestyle='-', label='Boundary')
plt.scatter(arp.longitude, arp.latitude, color='red', label='ARP Banda Aceh', s=100)
plt.scatter([start_point.longitude, end_point.longitude], [start_point.latitude, end_point.latitude], color='green', label='Arc Start/End', s=150, edgecolors='black', linewidths=1.5)

# Labels and styling
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title(f"{case_name} Boundary and Arc")
plt.legend()
plt.grid()
plt.show()
