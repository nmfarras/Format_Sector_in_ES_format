from geopy.distance import geodesic
import util

## Data define in this section is based on the characteristic of the boundary
# Given start and end points of the polygon
start_lat = 6.0000  # 06°00'00"N → Decimal Degrees
start_lon = 95 + 32/60 + 57/3600  # 095°32'57"E → Decimal Degrees
start_point = (start_lat, start_lon)
end_lat = 6.0000  # 06°00'00"N
end_lon = 95 + 17/60 + 27/3600  # 095°17'27"E
end_point = (end_lat, end_lon)

# ----------- Arc parameter definition -------------------------
# Define ARP (Banda Aceh Airport Reference Point), will be used as center of arc 1
arp_lat = 5 + 31/60 + 1/3600   # 5°31'01"N → Decimal Degrees
arp_lon = 95 + 25/60 + 12/3600  # 95°25'12"E → Decimal Degrees
arp = (arp_lat, arp_lon)


# Calculate bearings
bearing_angle_to_start = util.initial_bearing_angle(arp_lat, arp_lon, start_lat, start_lon)
bearing_angle_to_end = util.initial_bearing_angle(arp_lat, arp_lon, end_lat, end_lon)


# Calculate the distance in nautical miles (1 NM = 1852 meters)
distance_start_nm = geodesic(arp, start_point).meters / 1852

distance_end_nm = geodesic(arp, end_point).meters / 1852

# print(f"start: {distance_start_nm} nm, end: {distance_end_nm}")

# Generate arc points using calculated bearings and distances
arc_points_1 = util.generate_arc_points(arp, bearing_angle_to_start, bearing_angle_to_end, distance_start_nm, distance_end_nm)

boundary_points = [(start_lon, start_lat)] + [(p.longitude, p.latitude) for p in arc_points_1] + [(end_lon, end_lat), (start_lon, start_lat)]
kml_path = util.create_kml_polygon("banda_aceh_ctr_fixed.kml", boundary_points)

# Example usage
formatted_output = util.format_arc_points(arc_points_1, "Bandar_Aceh_CTR")
# print(formatted_output)

# Save to file
with open("Bandar_Aceh_CTR.txt", "w") as f:
    f.write(formatted_output)
