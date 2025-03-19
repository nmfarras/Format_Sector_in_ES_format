from geopy import Point
from geopy.distance import geodesic
import re
import util
import matplotlib.pyplot as plt

def dms_to_decimal(dms_str):
    """Convert DMS (Degrees Minutes Seconds) format to decimal degrees."""
    match = re.match(r"(\d{2})(\d{2})(\d{2})([NS])\s*(\d{3})(\d{2})(\d{2})([EW])", dms_str)
    if not match:
        raise ValueError(f"Invalid DMS format: {dms_str}")

    lat_sign = -1 if match.group(4) == 'S' else 1
    lat = lat_sign * (int(match.group(1)) + int(match.group(2)) / 60 + int(match.group(3)) / 3600)

    lon_sign = -1 if match.group(8) == 'W' else 1
    lon = lon_sign * (int(match.group(5)) + int(match.group(6)) / 60 + int(match.group(7)) / 3600)

    return Point(lat, lon)

case_name = "Curug_CTR"

fixed_points = [
    dms_to_decimal("060828S 1060230E"),
    dms_to_decimal("055546S 1061233E"),
    dms_to_decimal("060012S 1062100E"),
    dms_to_decimal("061627S 1062100E"),
    dms_to_decimal("061627S 1062409E"),
    dms_to_decimal("061325S 1063707E"),
    dms_to_decimal("061902S 1064123E")
]

arp_curug = dms_to_decimal("061558S 1065303E")  # Arc center
arc_start = dms_to_decimal("061902S 1064123E")
arc_end = dms_to_decimal("062141S 1064226E")

bearing_start=util.initial_bearing_angle(arp_curug.latitude, arp_curug.longitude, arc_start.latitude, arc_start.longitude)
bearing_end=util.initial_bearing_angle(arp_curug.latitude, arp_curug.longitude, arc_end.latitude, arc_end.longitude)

distance_nm = 12  # Arc radius in nautical miles

arc_end = geodesic(nautical=distance_nm).destination(arp_curug, bearing_end)  # Ensure arc_end lies on the circle

print(util.initial_bearing_angle(arp_curug.latitude, arp_curug.longitude, arc_end.latitude, arc_end.longitude))

arc_points = util.generate_arc_points(
    arp=arp_curug,
    bearing_start=util.initial_bearing_angle(arp_curug.latitude, arp_curug.longitude, arc_start.latitude, arc_start.longitude),
    bearing_end=util.initial_bearing_angle(arp_curug.latitude, arp_curug.longitude, arc_end.latitude, arc_end.longitude),
    distance_start_nm=distance_nm,
    distance_end_nm=distance_nm,
    step_degrees=-2  # Anticlockwise direction
)

arc_points_tuples = [(point.longitude, point.latitude) for point in arc_points]

additional_points = [
    dms_to_decimal("063000S 1062949E"),
    dms_to_decimal("063000S 1060230E"),
    dms_to_decimal("060828S 1060230E")  # Closing the polygon
]

boundary_points = (
    [(point.longitude, point.latitude) for point in fixed_points] +
    arc_points_tuples +
    [(point.longitude, point.latitude) for point in [arc_end, *additional_points]]
)

util.create_kml_polygon(f"{case_name}.kml", boundary_points)
formatted_output = util.format_coor_points(boundary_points, case_name)
# print(formatted_output)

with open(f"{case_name}.txt", "w") as f:
    f.write(formatted_output)

lons, lats = zip(*boundary_points)

plt.figure(figsize=(8, 8))
plt.plot(lons, lats, marker='o', linestyle='-', label='Boundary')
plt.scatter(arp_curug.longitude, arp_curug.latitude, color='red', label='ARP Curug', s=100)
plt.scatter([arc_start.longitude, arc_end.longitude], [arc_start.latitude, arc_end.latitude], color='green', label='Arc Start/End', s=150, edgecolors='black', linewidths=1.5)
plt.scatter(fixed_points[0].longitude, fixed_points[0].latitude, color='yellow', label='StartPoint', s=150, edgecolors='black', linewidths=1.5)

plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title(f"{case_name} Boundary and Arc")
plt.legend()
plt.grid()
plt.show()
