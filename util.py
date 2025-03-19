from geopy.distance import geodesic
import numpy as np
import math
import simplekml
from geopy.point import Point

def initial_bearing_angle(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])  # Convert to radians
    delta_lon = lon2 - lon1

    x = math.sin(delta_lon) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(delta_lon)

    bearing = math.atan2(x, y)
    bearing = math.degrees(bearing)
    return (bearing + 360) % 360  # Normalize to 0-360 degrees

def decimal_to_dms(lat, lon):
    """Convert decimal degrees to DMS format"""
    def to_dms(value, is_lat=True):
        degrees = int(abs(value))
        minutes = int((abs(value) - degrees) * 60)
        seconds = (abs(value) - degrees - minutes / 60) * 3600
        direction = ('N' if value >= 0 else 'S') if is_lat else ('E' if value >= 0 else 'W')
        return f"{direction}{degrees:03d}.{minutes:02d}.{seconds:06.3f}"

    return to_dms(lat, True), to_dms(lon, False)
  
def format_coor_points(boundary_points, name="Data"):
    """Convert boundary points to formatted string with DMS coordinates."""

    def decimal_to_dms(lat, lon):
        """Convert decimal degrees to DMS format."""
        def to_dms(value, is_lat=True):
            degrees = int(abs(value))
            minutes = int((abs(value) - degrees) * 60)
            seconds = (abs(value) - degrees - minutes / 60) * 3600
            direction = ('N' if value >= 0 else 'S') if is_lat else ('E' if value >= 0 else 'W')
            return f"{direction}{degrees:03d}.{minutes:02d}.{seconds:06.3f}"

        return to_dms(lat, True), to_dms(lon, False)

    lines = []

    # First line with header
    first_lon, first_lat = boundary_points[0]  # Unpack tuple (lon, lat)
    second_lon, second_lat = boundary_points[1]
    first_lat_dms, first_lon_dms = decimal_to_dms(first_lat, first_lon)
    lat2_dms, lon2_dms = decimal_to_dms(second_lat, second_lon)
    (len(name) + 1)
    lines.append(f"{name}{' ' * (43 - (len(name) + 1))} {first_lat_dms} {first_lon_dms} {lat2_dms} {lon2_dms} COLOR_AirspaceC")

    # Remaining lines
    for i in range(1, len(boundary_points) - 1):
        lon1, lat1 = boundary_points[i]
        lon2, lat2 = boundary_points[i + 1]
        lat1_dms, lon1_dms = decimal_to_dms(lat1, lon1)
        lat2_dms, lon2_dms = decimal_to_dms(lat2, lon2)
        lines.append(f"{' ' * 43}{lat1_dms} {lon1_dms} {lat2_dms} {lon2_dms} COLOR_AirspaceC")

    # Closing the polygon if necessary
    if len(boundary_points) > 2:
        last_lon, last_lat = boundary_points[-1]
        if boundary_points[-1] != boundary_points[0]:
          lat_last_dms, lon_last_dms = decimal_to_dms(last_lat, last_lon)
          lines.append(f"{' ' * 43}{lat_last_dms} {lon_last_dms} {first_lat_dms} {first_lon_dms} COLOR_AirspaceC")

    return "\n".join(lines)

def format_arc_points(arc_points, name="Data"):
    """Convert arc points to formatted string with DMS coordinates."""

    lines = []
    
    # First line with header
    first_lat_dms, first_lon_dms = decimal_to_dms(arc_points[0].latitude, arc_points[0].longitude)
    lat2_dms, lon2_dms = decimal_to_dms(arc_points[1].latitude, arc_points[1].longitude)
    lines.append(f"{name} {first_lat_dms} {first_lon_dms} {lat2_dms} {lon2_dms} COLOR_AirspaceC")

    # Remaining lines
    for i in range(1, len(arc_points) - 1):
        lat1_dms, lon1_dms = decimal_to_dms(arc_points[i].latitude, arc_points[i].longitude)
        lat2_dms, lon2_dms = decimal_to_dms(arc_points[i + 1].latitude, arc_points[i + 1].longitude)
        lines.append(f"{' ' * 40}{lat1_dms} {lon1_dms} {lat2_dms} {lon2_dms} COLOR_AirspaceC")

    # Closing the arc
    lat_last_dms, lon_last_dms = decimal_to_dms(arc_points[-1].latitude, arc_points[-1].longitude)
    lines.append(f"{' ' * 40}{lat_last_dms} {lon_last_dms} {first_lat_dms} {first_lon_dms} COLOR_AirspaceC")

    return "\n".join(lines)

def generate_arc_points(arp, bearing_start, bearing_end, distance_start_nm, distance_end_nm, step_degrees=5):
    """Generate points along an arc, ensuring the last point is exactly arc_end."""
    # Adjust bearings based on direction
    clockwise = step_degrees > 0
    is_circle = False
    
    if bearing_start == bearing_end or (bearing_start == 0 and bearing_end == 360) or (bearing_start == 360 and bearing_end == 0):
        is_circle = True
    
    stop_space = 10 ** max(0, math.floor(math.log10(abs(step_degrees))))
    
    if clockwise:
        bearing_start += stop_space
        bearing_end -= stop_space
    else:
        bearing_start -= stop_space
        bearing_end += stop_space
    
    bearing_start %= 360
    bearing_end %= 360

    # Handle wrap-around angles
    if clockwise and bearing_end < bearing_start:
        bearing_end += 360
    elif not clockwise and bearing_start < bearing_end:
        bearing_start += 360

    # Generate bearings using np.linspace
    angles = np.linspace(bearing_start, bearing_end, int(abs(bearing_end - bearing_start) / abs(step_degrees))) % 360
    
    print(is_circle)
    
    if is_circle:
        angles = np.append(angles,360)
    
    print(angles)

    # Interpolate radius between start and end distances
    arc_points = []
    for i, angle in enumerate(angles[:-1]):  # Exclude the last auto-generated point
        radius_nm = np.interp(i, [0, len(angles) - 1], [distance_start_nm, distance_end_nm])
        radius_km = radius_nm * 1.852  # Convert NM to KM
        point = geodesic(kilometers=radius_km).destination(arp, angle)
        arc_points.append(point)

    if is_circle:
        arc_points.append(geodesic(kilometers=distance_end_nm * 1.852).destination(arp, 360))
        arc_points.append(arc_points[0])
    else:
        # Ensure last point is exactly arc_end
        arc_points.append(geodesic(kilometers=distance_end_nm * 1.852).destination(arp, bearing_end % 360))

    return arc_points

def create_kml_polygon(file_name, boundary_points, color="red", alpha="50"):
    """
    Creates a KML file with a polygon using the given boundary points.
    
    Args:
        file_name (str): The name of the KML file to save.
        boundary_points (list of tuples): List of (longitude, latitude) coordinates forming the polygon.
        color (str): Color of the polygon outline (default: red).
        alpha (str): Transparency of the polygon fill (default: '50').
    
    Returns:
        str: The saved KML file path.
    """
    kml = simplekml.Kml()

    polygon = kml.newpolygon()
    polygon.outerboundaryis = boundary_points
    polygon.style.linestyle.color = simplekml.Color.red if color == "red" else color
    polygon.style.linestyle.width = 2
    polygon.style.polystyle.color = simplekml.Color.changealpha(alpha, simplekml.Color.blue)

    kml.save(file_name)
    print(f"File has been saved as {file_name}")
    
    return file_name
