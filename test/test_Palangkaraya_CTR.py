from geopy import Point
from geopy.distance import geodesic
import util
import matplotlib.pyplot as plt
import re

# Function to convert DMS to decimal degrees
def dms_to_decimal(dms_str):
    match = re.match(r"(\d{2})(\d{2})(\d{2})([NS])\s*(\d{3})(\d{2})(\d{2})([EW])", dms_str)
    if not match:
        raise ValueError(f"Invalid DMS format: {dms_str}")
    
    lat_sign = -1 if match.group(4) == 'S' else 1
    lat = lat_sign * (int(match.group(1)) + int(match.group(2)) / 60 + int(match.group(3)) / 3600)
    
    lon_sign = -1 if match.group(8) == 'W' else 1
    lon = lon_sign * (int(match.group(5)) + int(match.group(6)) / 60 + int(match.group(7)) / 3600)
    
    return Point(lat, lon)

"""
Palangka Raya CTR :
014538S 1134908E - 015130S 1132722E - 022057S 1132722E - 025525S 1132056E - 024335S 1140444E thence anti-clockwise along the circle of 30 NM radius centered at PKY VOR/DME to 014538S 1134908E

PKY VOR/DME
02°13'34.6''S 113°56'46.2''E
"""

case_name = "Palangkaraya_CTR"

# Define fixed boundary points
fixed_points = [
    dms_to_decimal("014538S 1134908E"),
    dms_to_decimal("015130S 1132722E"),
    dms_to_decimal("022057S 1132722E"),
    dms_to_decimal("025525S 1132056E"),
    dms_to_decimal("024335S 1140444E")
]

# Define arc center and radius
arc_center = dms_to_decimal("021452S 1135704E")  # PKY VOR/DME
arc_radius_nm = 30  # Convert to KM
arc_radius_km = arc_radius_nm * 1.852  

# Compute bearing angles
bearing_start = util.initial_bearing_angle(arc_center.latitude, arc_center.longitude, fixed_points[-1].latitude, fixed_points[-1].longitude)
bearing_end = util.initial_bearing_angle(arc_center.latitude, arc_center.longitude, fixed_points[0].latitude, fixed_points[0].longitude)

# Generate arc points (anti-clockwise)
arc_points = util.generate_arc_points(
    arp=arc_center,
    bearing_start=bearing_start,
    bearing_end=bearing_end,
    distance_start_nm=arc_radius_nm,
    distance_end_nm=arc_radius_nm,
    step_degrees=-10  # Negative for anti-clockwise
)

# Convert points to tuples
arc_tuples = [(point.longitude, point.latitude) for point in arc_points]
fixed_tuples = [(point.longitude, point.latitude) for point in fixed_points]

# Combine all points
boundary_points = fixed_tuples + arc_tuples + [fixed_tuples[0]]  # Closing the polygon

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
plt.plot(lons, lats, marker='o', linestyle='-', label='Palangka Raya CTR')
plt.scatter(arc_center.longitude, arc_center.latitude, color='red', label='PKY VOR/DME', s=100)
plt.scatter(fixed_points[0].longitude, fixed_points[0].latitude, color='yellow', label='StartPoint', s=450, edgecolors='black', linewidths=1.5)
plt.scatter([p.longitude for p in fixed_points], [p.latitude for p in fixed_points], color='green', label='Boundary Points', s=150, edgecolors='black', linewidths=1.5)

plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title(f"{case_name} Boundary and Arc")
plt.legend()
plt.grid()
plt.show()
