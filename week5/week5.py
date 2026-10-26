from math import radians, sin, cos	# IMPORT NECESSARY FUNCTIONS HERE

def compute_offset(origin, distance, direction):
    """
    Compute the location of a point at a given distance and direction from a specified location using trigonometry
    """
    offset_x = origin[0] + (cos(radians(direction))) * distance  # COMPLETE THIS LINE
    offset_y = origin[1] + (sin(radians(direction))) * distance  # COMPLETE THIS LINE 
    return (offset_x, offset_y)

from geopandas import read_file
world = read_file("../../data/natural-earth/ne_10m_admin_0_countries.shp")
iceland = world.loc[world.ISO_A3 == "ISL"]
land_cover = read_file("../../data/iceland/gis_osm_natural_a_free_1.shp")
ice = land_cover.loc[land_cover.fclass == "glacier"]
print (ice.head())
# get the bounds of the country
minx, miny, maxx, maxy = iceland.total_bounds
print(iceland.total_bounds)