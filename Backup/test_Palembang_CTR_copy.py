from geopy import Point
from geopy.distance import geodesic
import re
import util

def dms_to_decimal(dms_str):
    """Convert DMS (Degrees Minutes Seconds) format to decimal degrees."""
    match = re.match(r"(\d{2})(\d{2})(\d{2})([NS])\s*(\d{3})(\d{2})(\d{2})([EW])", dms_str)
    if not match:
        raise ValueError(f"Invalid DMS format: {dms_str}")

    lat_sign = -1 if match.group(4) == 'S' else 1
    lat = lat_sign * (int(match.group(1)) + int(match.group(2)) / 60 + int(match.group(3)) / 3600)

    lon_sign = -1 if match.group(8) == 'W' else 1
    lon = lon_sign * (int(match.group(5)) + int(match.group(6)) / 60 + int(match.group(7)) / 3600)

    return Point(lat, lon)  # Return (lon, lat) to match GIS conventions


case_name = "Palembang_CTR"

fixed_points = [
    dms_to_decimal("010206S 1043536E"),
    dms_to_decimal("025930S 1060612E"),
    dms_to_decimal("043200S 1043900E"),
    dms_to_decimal("020928S 1031344E")  # Last fixed point before arc
]

arp_sultan_thaha = dms_to_decimal("013808S 1033835E")  # Arc center
arc_start = fixed_points[-1]  # Start of the arc
arc_end = dms_to_decimal("015241S 1041550E")  # End of the arc

distance_start_nm = geodesic(arp_sultan_thaha, arc_start).meters / 1852

distance_end_nm = geodesic(arp_sultan_thaha, arc_end).meters / 1852

# Generate the arc (counterclockwise, 40 NM)
arc_points = util.generate_arc_points(
    arp=arp_sultan_thaha,
    bearing_start=util.initial_bearing_angle(arp_sultan_thaha.latitude,arp_sultan_thaha.longitude, arc_start.latitude,arc_start.longitude),
    bearing_end=util.initial_bearing_angle(arp_sultan_thaha.latitude,arp_sultan_thaha.longitude, arc_end.latitude,arc_end.longitude),
    distance_start_nm=distance_start_nm,
    distance_end_nm=distance_end_nm,
    step_degrees=-10
)

# Convert geopy points to (lon, lat) tuples
arc_points_tuples = [(point.longitude, point.latitude) for point in arc_points]

# Combine everything into boundary points
boundary_points = [(point.longitude, point.latitude) for point in fixed_points] + arc_points_tuples + [(point.longitude, point.latitude) for point in  [arc_end, fixed_points[0]] ] # Close loop

# print(boundary_points)


# Create KML
poly_coor = util.create_kml_polygon(f"{case_name}.kml", boundary_points)

# Save as .txt with format
formatted_output = util.format_coor_points(boundary_points, case_name)
print(formatted_output)

# Save to file
with open(f"{case_name}.txt", "w") as f:
    f.write(formatted_output)