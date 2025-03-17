from geopy import Point
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
