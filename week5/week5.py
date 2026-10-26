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
iceland = world[world.ISO_A3 == "ISL"]
land_cover = read_file("../../data/iceland/gis_osm_natural_a_free_1.shp")
ice = land_cover[land_cover.fclass == "glacier"]
print (ice.head())
# get the bounds of the country
minx, miny, maxx, maxy = iceland.total_bounds
print(iceland.total_bounds)

from pyproj import Geod, CRS, Transformer
# set the geographical proj string and ellipsoid (should be the same)
geo_string = "+proj=longlat +datum=WGS84 +no_defs"
g = Geod(ellps='WGS84')

# create a list of dictionaries for the projected CRS' to evaluate for distortion
projections = [
    {'name':"Web Mercator", 'description':"Global Conformal",   'proj':"+proj=merc +a=6378137 +b=6378137 +lat_ts=0 +lon_0=0 +x_0=0 +y_0=0 +k=1 +units=m +nadgrids=@null +wktext +no_defs"},
    {'name':"Eckert IV",    'description':"Global Equal Area",  'proj':"+proj=eck4 +lon_0=0 +x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs +type=crs"},
    {'name':"Iceland Lambert Azimuthal Equal Area", 'description':"Local Equal Area",   'proj':"+proj=laea +lon_0=-18.984375 +lat_0=64.6305525 +datum=WGS84 +units=m +no_defs"}
]
# loop through each CRS
for ax_num, projection in enumerate(projections):
    print(ax_num, projection)
    
# initialise a PyProj Transformer to transform coordinates
transformer = Transformer.from_crs(CRS.from_proj4(geo_string), CRS.from_proj4(projection['proj']), always_xy=True)
