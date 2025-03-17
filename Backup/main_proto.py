import simplekml
from geopy.distance import geodesic
import numpy as np
import math

def initial_bearing_angle(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])  # Convert to radians
    delta_lon = lon2 - lon1

    x = math.sin(delta_lon) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(delta_lon)

    bearing = math.atan2(x, y)
    bearing = math.degrees(bearing)
    return (bearing + 360) % 360  # Normalize to 0-360 degrees

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
bearing_angle_to_start = initial_bearing_angle(arp_lat, arp_lon, start_lat, start_lon)
bearing_angle_to_end = initial_bearing_angle(arp_lat, arp_lon, end_lat, end_lon)


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

# Generate arc points
angles = np.linspace(bearing_angle_to_start, bearing_angle_to_end, num_points)  # Clockwise from East (90°) to West (270°)
arc_points = [geodesic(kilometers=radius_km).destination(arp, angle) for angle in angles]

# Create KML file
kml = simplekml.Kml()

# Draw the arc
linestring = kml.newlinestring()
linestring.coords = [(p.longitude, p.latitude) for p in arc_points]
linestring.style.linestyle.color = simplekml.Color.red
linestring.style.linestyle.width = 2

# Connect start and end points to close the polygon
polygon = kml.newpolygon()
polygon.outerboundaryis = [(start_lon, start_lat)] + [(p.longitude, p.latitude) for p in arc_points] + [(end_lon, end_lat), (start_lon, start_lat)]
polygon.style.linestyle.color = simplekml.Color.red
polygon.style.linestyle.width = 2
polygon.style.polystyle.color = simplekml.Color.changealpha('50', simplekml.Color.blue)

# Save KML file
kml_path = "banda_aceh_ctr.kml"
kml.save(kml_path)

kml_path
