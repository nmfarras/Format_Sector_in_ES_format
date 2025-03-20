# import numpy as np

# def dms_to_decimal(dms):
#     """Converts DMS (Degrees, Minutes, Seconds) to Decimal Degrees."""
#     d, m, s, direction = int(dms[:2]), int(dms[2:4]), int(dms[4:6]), dms[-1]
#     decimal = d + m / 60 + s / 3600
#     if direction in ['S', 'W']:
#         decimal = -decimal
#     return decimal

# # Given Points
# point_start = (-2.1139, 141.0000)
# arp_sentani = (-2.5720, 140.5117)  # Center of the arc
# point_end = (-3.0614, 141.0000)

# # Convert Arc Radius to Degrees
# nm_to_km = 1.852
# radius_nm = 40
# radius_km = radius_nm * nm_to_km
# km_to_deg = 1 / 111.32  # Approximate conversion for latitude degrees
# radius_deg = radius_km * km_to_deg

# # Solve for Latitude where Longitude = 141.0000
# lon_fixed = 141.0000

# delta_x = lon_fixed - arp_sentani[1]
# delta_x_squared = delta_x ** 2
# radius_squared = radius_deg ** 2

# delta_y_squared = radius_squared - delta_x_squared

# if delta_y_squared < 0:
#     print("No intersection found (arc does not reach the line).")
# else:
#     delta_y = np.sqrt(delta_y_squared)
#     lat1 = arp_sentani[0] + delta_y  # Upper intersection
#     lat2 = arp_sentani[0] - delta_y  # Lower intersection
    
#     # Choose the valid intersection within the range
#     if point_end[0] <= lat1 <= point_start[0]:
#         intersection_point = (lat1, lon_fixed)
#     else:
#         intersection_point = (lat2, lon_fixed)
    
#     print(f"Intersection Point: {intersection_point}")

from math import radians, degrees, sin, cos, acos
import re
from geopy import Point

def dms_to_decimal(dms_str):
    """Convert DMS (Degrees, Minutes, Seconds) to decimal degrees."""
    match = re.match(r"(\d{2})(\d{2})(\d{2})([NS])\s*(\d{3})(\d{2})(\d{2})([EW])", dms_str)
    if not match:
        raise ValueError(f"Invalid DMS format: {dms_str}")

    lat_sign = -1 if match.group(4) == 'S' else 1
    lat = lat_sign * (int(match.group(1)) + int(match.group(2)) / 60 + int(match.group(3)) / 3600)

    lon_sign = -1 if match.group(8) == 'W' else 1
    lon = lon_sign * (int(match.group(5)) + int(match.group(6)) / 60 + int(match.group(7)) / 3600)

    return Point(lat, lon)

def find_end_points(arc_center, arc_radius_nm, target_longitude):
    """Finds the two possible points that are arc_radius_nm away from arc_center and fall on target_longitude."""
    radius_km = arc_radius_nm * 1.852  # Convert NM to KM
    R = 6371  # Earth's radius in km
    lat_center, lon_center = map(radians, arc_center)  # Convert to radians
    target_longitude = radians(target_longitude)
    delta_lambda = target_longitude - lon_center
    
    # Compute latitude using the spherical law of cosines
    cos_lat = (cos(radius_km / R) - sin(lat_center) * sin(lat_center)) / (cos(lat_center) * cos(delta_lambda))
    
    if abs(cos_lat) > 1:
        return []  # No valid intersection (numerical error or arc too small)
    
    lat1 = degrees(acos(cos_lat))  # First intersection
    lat2 = -lat1  # Second intersection (mirrored)
    
    return [(lat1, degrees(target_longitude)), (lat2, degrees(target_longitude))]

# Given Points
arp_sentani = [(point.latitude, point.longitude) for point in [dms_to_decimal("023419S 1403042E")]] # Center of the arc

arc_radius_nm = 40
fixed_longitude = 141.0000

# Find the endpoints
endpoints = find_end_points(*arp_sentani, arc_radius_nm, fixed_longitude)
print(f"Endpoints on Longitude {fixed_longitude}: {endpoints}")


