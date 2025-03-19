# import matplotlib.pyplot as plt

# # Extracted coordinates from the new path data
# new_boundary = [
#     (656, 858), (651, 857), (611, 828), (581, 799), (549, 761), (529, 732), (515, 707), (495, 662),
#     (479, 608), (472, 567), (470, 539), (470, 504), (476, 448), (482, 420), (490, 393), (505, 354),
#     (514, 335), (528, 311), (547, 282), (583, 239), (619, 206), (665, 174), (691, 160), (1156, 160),
#     (1142, 177), (1133, 196), (1130, 211), (1129, 385), (1314, 464)
# ]

# # Extract x and y coordinates
# x_vals, y_vals = zip(*new_boundary)

# # Flip Y-axis to match map orientation
# y_vals_flipped = [-y for y in y_vals]

# # Close the polygon by appending the first point at the end
# x_vals = list(x_vals) + [x_vals[0]]
# y_vals_flipped = list(y_vals_flipped) + [y_vals_flipped[0]]

# # Plot the new boundary
# plt.figure(figsize=(8, 8))
# plt.plot(x_vals, y_vals_flipped, color='red', linewidth=2)
# plt.scatter(x_vals, y_vals_flipped, color='red', linewidth=2)

# # Adding labels and title
# plt.title('Kupang TMA Boundary (Y-Axis Flipped)')
# plt.xlabel('Longitude (Approx.)')
# plt.ylabel('Latitude (Approx.)')

# # Set aspect ratio and grid
# plt.gca().set_aspect('equal', adjustable='box')
# plt.grid(True)
# plt.show()

##################################################################################################################################

# import numpy as np
# import matplotlib.pyplot as plt

# # Given reference points
# pixel_kikem = (1314, -464)
# pixel_mubra = (1133, -196)
# latlon_kikem = (-9 - 52/60 - 54.001/3600, 126 + 7/60 + 23.998/3600)  # S009.52.54.001 E126.07.23.998
# latlon_mubra = (-8 - 33/60 - 37.299/3600, 125 + 6/60 + 29.199/3600)  # S008.33.37.299 E125.06.29.199

# # Compute scaling factors
# scale_x = (latlon_kikem[1] - latlon_mubra[1]) / (pixel_kikem[0] - pixel_mubra[0])
# scale_y = (latlon_kikem[0] - latlon_mubra[0]) / (pixel_kikem[1] - pixel_mubra[1])

# # Compute offset
# offset_x = latlon_kikem[1] - pixel_kikem[0] * scale_x
# offset_y = latlon_kikem[0] - pixel_kikem[1] * scale_y

# # New boundary in pixel coordinates
# new_boundary_pixels = [
#     (656, -858), (651, -857), (611, -828), (581, -799), (549, -761), (529, -732), (515, -707), (495, -662),
#     (479, -608), (472, -567), (470, -539), (470, -504), (476, -448), (482, -420), (490, -393), (505, -354),
#     (514, -335), (528, -311), (547, -282), (583, -239), (619, -206), (665, -174), (691, -160), (1156, -160),
#     (1142, -177), (1133, -196), (1130, -211), (1129, -385), (1314, -464)
# ]

# # Convert to lat/lon using scaling and offset
# converted_boundary = [(y * scale_y + offset_y, x * scale_x + offset_x) for x, y in new_boundary_pixels]

# # Extract latitude and longitude
# lats, lons = zip(*converted_boundary)

# # Close the polygon
# lats += (lats[0],)
# lons += (lons[0],)

# # Plot the converted boundary
# plt.figure(figsize=(8, 8))
# plt.plot(lons, lats, color='red', linewidth=2, marker='o', markersize=4)

# # Label key points
# plt.scatter([latlon_kikem[1], latlon_mubra[1]], [latlon_kikem[0], latlon_mubra[0]], color='blue', marker='x', s=100, label='Reference Points')
# plt.text(latlon_kikem[1], latlon_kikem[0], 'KIKEM', fontsize=12, verticalalignment='bottom', horizontalalignment='right')
# plt.text(latlon_mubra[1], latlon_mubra[0], 'MUBRA', fontsize=12, verticalalignment='top', horizontalalignment='right')

# # Title and labels
# plt.title("Converted Kupang TMA Boundary (Lat/Lon)")
# plt.xlabel("Longitude")
# plt.ylabel("Latitude")
# plt.grid(True)
# plt.gca().set_aspect('equal', adjustable='box')
# plt.legend()
# plt.show()

####################################################################################################################################################

import matplotlib.pyplot as plt

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
    (656, -858), (651, -857), (611, -828), (581, -799), (549, -761), (529, -732), (515, -707), (495, -662),
    (479, -608), (472, -567), (470, -539), (470, -504), (476, -448), (482, -420), (490, -393), (505, -354),
    (514, -335), (528, -311), (547, -282), (583, -239), (619, -206), (665, -174), (691, -160), (1156, -160),
    (1142, -177), (1133, -196), (1130, -211), (1129, -385), (1314, -464)
]

# Convert to lat/lon using scaling and offset
converted_boundary = [(y * scale_y + offset_y, x * scale_x + offset_x) for x, y in new_boundary_pixels]

# Extract latitude and longitude
lats, lons = zip(*converted_boundary)

# Close the polygon
lats += (lats[0],)
lons += (lons[0],)

# Plot the converted boundary
plt.figure(figsize=(8, 8))
plt.plot(lons, lats, color='red', linewidth=2, marker='o', markersize=4)

# Label key points
plt.scatter([latlon_kikem[1], latlon_smthg[1], latlon_mubra[1]], [latlon_kikem[0], latlon_smthg[0], latlon_mubra[0]], color='blue', marker='x', s=100, label='Reference Points')
plt.text(latlon_kikem[1], latlon_kikem[0], 'KIKEM', fontsize=12, verticalalignment='bottom', horizontalalignment='right')
plt.text(latlon_smthg[1], latlon_smthg[0], 'SMTHG', fontsize=12, verticalalignment='top', horizontalalignment='right')
plt.text(latlon_mubra[1], latlon_mubra[0], 'MUBRA', fontsize=12, verticalalignment='top', horizontalalignment='right')

# Title and labels
plt.title("Converted Kupang TMA Boundary (Lat/Lon)")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.grid(True)
plt.gca().set_aspect('equal', adjustable='box')
plt.legend()
plt.show()

