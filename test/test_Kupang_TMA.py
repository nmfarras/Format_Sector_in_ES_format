from geopy import Point
from geopy.distance import geodesic
import util
import matplotlib.pyplot as plt
import re


#########################################################################################################

# Given reference points
pixel_kikem = (1314, -464)
pixel_smthg = (1156, -160)
latlon_kikem = (-9 - 52/60 - 54.001/3600, 126 + 7/60 + 23.998/3600)  # S009.52.54.001 E126.07.23.998
latlon_smthg = (-8 - 13/60 - 44/3600, 125 + 15/60 + 1/3600)  # S008.13.44S 125.15.01E
latlon_mubra = (-8 - 33/60 - 37.299/3600, 125 + 6/60 + 29.199/3600)  # S008.33.37.299 E125.06.29.199

# Compute scaling factors
scale_x = (latlon_kikem[1] - latlon_smthg[1]) / (pixel_kikem[0] - pixel_smthg[0])
scale_y = (latlon_kikem[0] - latlon_smthg[0]) / (pixel_kikem[1] - pixel_smthg[1])

# Compute offset
offset_x = latlon_kikem[1] - pixel_kikem[0] * scale_x
offset_y = latlon_kikem[0] - pixel_kikem[1] * scale_y

# New boundary in pixel coordinates
new_boundary_pixels = [ 
    (1156, -160), (1142, -177), 
    (1133, -196), (1130, -211), 
    (1129, -385), (1314, -464)
]

# Convert to lat/lon using scaling and offset
converted_boundary = [(y * scale_y + offset_y, x * scale_x + offset_x) for x, y in new_boundary_pixels]

# Extract latitude and longitude
lats, lons = zip(*converted_boundary)

# Close the polygon
lats += (lats[0],)
lons += (lons[0],)

# # Plot the converted boundary
# plt.figure(figsize=(8, 8))
# plt.plot(lons, lats, color='red', linewidth=2, marker='o', markersize=4)

# # Label key points
# plt.scatter([latlon_kikem[1], latlon_smthg[1], latlon_mubra[1]], [latlon_kikem[0], latlon_smthg[0], latlon_mubra[0]], color='blue', marker='x', s=100, label='Reference Points')
# plt.text(latlon_kikem[1], latlon_kikem[0], 'KIKEM', fontsize=12, verticalalignment='bottom', horizontalalignment='right')
# plt.text(latlon_smthg[1], latlon_smthg[0], 'SMTHG', fontsize=12, verticalalignment='top', horizontalalignment='right')
# plt.text(latlon_mubra[1], latlon_mubra[0], 'MUBRA', fontsize=12, verticalalignment='top', horizontalalignment='right')

# # Title and labels
# plt.title("Converted Kupang TMA Boundary (Lat/Lon)")
# plt.xlabel("Longitude")
# plt.ylabel("Latitude")
# plt.grid(True)
# plt.gca().set_aspect('equal', adjustable='box')
# plt.legend()
# plt.show()



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

"""
Kupang (TMA):
120000S 1223015E thence clockwise along the circle of 130 NM radius centered at 
KPG VOR/DME to 081344S 1224138E (point where the circle crosses A464) then 
straight line to 081344S 1251501E then along the Timor Leste – Indonesia Boundary and 
along Brisbane FIR Boundary to 120000S 1223015E

KPG VOR/DME
101000S 1234130E
"""

case_name = "Kupang_TMA"

# Define fixed boundary points
point_start = dms_to_decimal("120000S 1223015E")
point_arc_end = dms_to_decimal("081344S 1224138E")
point_straight = dms_to_decimal("081344S 1251501E")

# Define arc center and radius
kpg_vor = dms_to_decimal("101000S 1234130E")
arc_radius_nm = 130  # Convert to KM
arc_radius_km = arc_radius_nm * 1.852  

# Compute bearing angles
bearing_start = util.initial_bearing_angle(kpg_vor.latitude, kpg_vor.longitude, point_start.latitude, point_start.longitude)
bearing_end = util.initial_bearing_angle(kpg_vor.latitude, kpg_vor.longitude, point_arc_end.latitude, point_arc_end.longitude)

# Generate arc points
arc_points = util.generate_arc_points(
    arp=kpg_vor,
    bearing_start=bearing_start,
    bearing_end=bearing_end,
    distance_start_nm=arc_radius_nm,
    distance_end_nm=arc_radius_nm,
    step_degrees=5
)

# Convert points to tuples
arc_tuples = [(point.longitude, point.latitude) for point in arc_points]
fixed_tuples = [(point_start.longitude, point_start.latitude), (point_arc_end.longitude, point_arc_end.latitude), (point_straight.longitude, point_straight.latitude)]

# Combine all points
# boundary_points = fixed_tuples + arc_tuples + [fixed_tuples[0]]  # Closing the polygon
boundary_points =  ([(point_start.longitude, point_start.latitude)] +  
                    arc_tuples + 
                    [(point_arc_end.longitude, point_arc_end.latitude)] + 
                    [(point_straight.longitude, point_straight.latitude)] +
                    [(point[1], point[0]) for point in converted_boundary] +
                    [(point_start.longitude, point_start.latitude)]
                    # Closing the polygon

)
# Export KML
util.create_kml_polygon(f"{case_name}.kml", boundary_points)

# Format output
formatted_output = util.format_coor_points(boundary_points, case_name, "B")
print(formatted_output)

with open(f"{case_name}.txt", "w") as f:
    f.write(formatted_output)

# Plot
lons, lats = zip(*boundary_points)

plt.figure(figsize=(8, 8))
plt.plot(lons, lats, marker='o', linestyle='-', label='Kupang TMA')
plt.scatter(kpg_vor.longitude, kpg_vor.latitude, color='red', label='KPG VOR/DME', s=100)
plt.scatter(point_start.longitude, point_start.latitude, color='yellow', label='StartPoint', s=450, edgecolors='black', linewidths=1.5)
plt.scatter([point_start.longitude, point_arc_end.longitude], [point_start.latitude, point_arc_end.latitude], color='green', label='Arc Start/End', s=250, edgecolors='black', linewidths=1.5)
plt.scatter([point_arc_end.longitude, point_straight.longitude], [point_arc_end.latitude, point_straight.latitude], color='orange', label='Key Points', s=150, edgecolors='black', linewidths=1.5)

plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title(f"{case_name} Boundary and Arc")
plt.legend()
plt.grid()
plt.show()
