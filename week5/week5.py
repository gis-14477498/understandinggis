from math import radians, sin, cos, hypot	# IMPORT NECESSARY FUNCTIONS HERE

def compute_offset(origin, distance, direction):
    """
    Compute the location of a point at a given distance and direction from a specified location using trigonometry
    """
    offset_x = origin[0] + (cos(radians(direction))) * distance  # COMPLETE THIS LINE
    offset_y = origin[1] + (sin(radians(direction))) * distance  # COMPLETE THIS LINE 
    return (offset_x, offset_y)

from numpy.random import uniform
from numpy import arange
from shapely.geometry import Polygon

def evaluate_distortion(g, transformer, minx, miny, maxx, maxy, minr, maxr, sample_number, vertices=16):
    # calculate the required number of random locations (x and y separately) plus radius
    xs = uniform(low=minx, high=maxx, size=sample_number)        
    ys = uniform(low=miny, high=maxy, size=sample_number)
    rs = uniform(low=minr, high=maxr, size=sample_number)
    
    # offset distances
    forward_azimuths = arange(0, 360, 360 / vertices)
    
    area_indices = []
    shape_indices = []
    distance_indices = []
    for x,y,r in zip(xs,ys,rs):
        # construct a circle around the centre point on the ellipsoid
        lons, lats = g.fwd([x]*vertices, [y]*vertices, forward_azimuths, [r]*vertices)[:2]
        # project the result, calculate area, append to the list
        e_coords = [ transformer.transform(lon, lat, direction='FORWARD') for lon, lat in zip(lons, lats) ]

        # get the area of the resulting circle
        ellipsoidal_area = Polygon(e_coords).area
        # transform the centre point to the projected CRS
        centre_x, centre_y = transformer.transform(x, y, direction='FORWARD')

        # construct a circle around the projected point on a plane, calculate area
        planar_area = Polygon([ compute_offset((centre_x, centre_y), r, az) for az in forward_azimuths ]).area
        
        # calculate area distortion
        area_indices.append(abs(ellipsoidal_area - planar_area) / abs(ellipsoidal_area + planar_area))
       
        # get radial distances from the centre to each of the 16 points on the circle
        ellipsoidal_radial_distances = [ hypot(centre_x - ex, centre_y - ey) for ex, ey in e_coords ]

        # get the absolute proportional difference between the expected and actual radial distance for each 'spoke'
        shape_distortion = [abs((1 / vertices) - (d / sum(ellipsoidal_radial_distances))) for d in ellipsoidal_radial_distances]

    shape_indices.append(sum(shape_distortion))
        
    # check the number of samples
    print(len(area_indices), len(shape_indices))

    # calculate overall distortion
    Ea = sum(area_indices) / len(area_indices)
    Es = sum(shape_indices) / len(shape_indices)

    print(Ea, Es)
    
    for _ in range(sample_number):
        xs = uniform(low=minx, high=maxx, size=2)
        ys = uniform(low=miny, high=maxy, size=2)

        ellipsoidal_distance = g.line_length(xs, ys)

        origin = transformer.transform(xs[0], ys[0])
        destination = transformer.transform(xs[1], ys[1])

        planar_distance = hypot(
            destination[0] - origin[0],
            destination[1] - origin[1]
        )

        distance_indices.append(
            abs(ellipsoidal_distance - planar_distance)
            / abs(ellipsoidal_distance + planar_distance)
        )

    Ep = sum(distance_indices) / len(distance_indices)
    return Ep, Es, Ea
          
from geopandas import read_file
world = read_file("../../data/natural-earth/ne_10m_admin_0_countries.shp")
iceland = world[world.ISO_A3 == "ISL"]
land_cover = read_file("../../data/iceland/gis_osm_natural_a_free_1.shp")
ice = land_cover[land_cover.fclass == "glacier"]

# get the bounds of the country
minx, miny, maxx, maxy = iceland.total_bounds


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

    # calculate the distortion
    Ep, Es, Ea = evaluate_distortion(
    g, transformer, minx, miny, maxx, maxy,
    10000, 1000000, 1000
)
    

