import simplekml
from geopy.distance import geodesic
import numpy as np
import util

# Define ARP (Banda Aceh Airport Reference Point)
arp_lat = 5 + 31/60 + 1/3600   # 5°31'01"N → Decimal Degrees
arp_lon = 95 + 25/60 + 12/3600  # 95°25'12"E → Decimal Degrees
arp = (arp_lat, arp_lon)

# Given start and end points of the arc
start_lat = 6.0000  # 06°00'00"N → Decimal Degrees
start_lon = 95 + 32/60 + 57/3600  # 095°32'57"E → Decimal Degrees
start_point = (start_lat, start_lon)
end_lat = 6.0000  # 06°00'00"N
end_lon = 95 + 17/60 + 27/3600  # 095°17'27"E
end_point = (end_lat, end_lon)

# Calculate bearings
bearing_angle_to_start = util.initial_bearing_angle(arp_lat, arp_lon, start_lat, start_lon)
bearing_angle_to_end = util.initial_bearing_angle(arp_lat, arp_lon, end_lat, end_lon)


# Calculate the distance in nautical miles (1 NM = 1852 meters)
distance_start_nm = geodesic(arp, start_point).meters / 1852

distance_end_nm = geodesic(arp, end_point).meters / 1852

print(f"start: {distance_start_nm} nm, end: {distance_end_nm}")

# Define arc parameters
radius_nm = 30  # Radius in nautical miles
radius_km = radius_nm * 1.852  # Convert NM to KM
num_points = 100  # Number of points in the arc

# Compute bearings for the arc
bearing_start = geodesic(kilometers=radius_km).destination(arp, 0).latitude
bearing_end = geodesic(kilometers=radius_km).destination(arp, 180).latitude

# Generate arc points with varying radius
# Ensure angles start after start point and stop before end point
angles = np.linspace(bearing_angle_to_start + 0.1, bearing_angle_to_end - 0.1, num_points)

arc_points = []
for i, angle in enumerate(angles):
    # Interpolate radius based on progress between start and end
    radius_nm = np.interp(i, [0, num_points - 1], [distance_start_nm, distance_end_nm])
    radius_km = radius_nm * 1.852  # Convert NM to KM

    # Compute the geodesic destination
    point = geodesic(kilometers=radius_km).destination(arp, angle)
    arc_points.append(point)

# Create KML file
kml = simplekml.Kml()

# Draw the arc without overlapping start/end points
linestring = kml.newlinestring()
linestring.coords = [(p.longitude, p.latitude) for p in arc_points]
linestring.style.linestyle.color = simplekml.Color.red
linestring.style.linestyle.width = 2

# Connect start and end points to close the polygon properly
polygon = kml.newpolygon()
polygon.outerboundaryis = [(start_lon, start_lat)] + [(p.longitude, p.latitude) for p in arc_points] + [(end_lon, end_lat), (start_lon, start_lat)]
polygon.style.linestyle.color = simplekml.Color.red
polygon.style.linestyle.width = 2
polygon.style.polystyle.color = simplekml.Color.changealpha('50', simplekml.Color.blue)

# Save KML file
kml_path = "banda_aceh_ctr_fixed.kml"
kml.save(kml_path)

kml_path

# Example usage
formatted_output = util.format_arc_points(arc_points, "Bandar_Aceh_CTR")
print(formatted_output)

# Save to file
with open("Bandar_Aceh_CTR.txt", "w") as f:
    f.write(formatted_output)
