from geopandas import read_file

# open a dataset of all countries in the world
world = read_file("../../data/natural-earth/ne_10m_admin_0_countries.shp")

# extract the UK, project, and extract the geometry
uk = world[(  )].to_crs(  ).geometry.iloc[0]	# COMPLETE THIS LINE

# report geometry type
print(f"geometry type: {uk.geom_type}")


from sys import exit
# quit the analysis if we are dealing with any geometry but a MultiPolygon
if uk.geom_type != 'MultiPolygon':
  print("Geometry is not a MultiPolygon, exiting...")
  exit()
  
  # initialise variables to hold the coordinates and area of the largest polygon
biggest_area = 0
coord_list = []

# loop through each polygon in the multipolygon and find the biggest (mainland Great Britain)
for poly in uk.geoms:

	# if it is the biggest so far
	if 	# COMPLETE THIS LINE
    
		# store the new value for biggest area
		biggest_area = poly.area
        
     # store the coordinates of the polygon
		          = list(poly.boundary.coords)	# COMPLETE THIS LINE (look at the variables that you defined before the loop)

# set the percentage of nodes that you want to remove
SIMPLIFICATION_PERC = 98

# how many nodes do we need?
n_nodes = int(len(coord_list) / 100.0 * (100 - SIMPLIFICATION_PERC))

# ensure that there are at least 3 nodes (minimum for a polygon)
if n_nodes < 3:
	n_nodes = 3 
    
    def get_effective_area(a, b, c):
	"""
	* Calculate the area of a triangle made from the points a, b and c using Heron's formula
	* 	https://en.wikipedia.org/wiki/Heron%27s_formula
	"""
	# calculate the length of each side
	side_a = distance(b[0], b[1], c[0], c[1])
	side_b = distance(a[0], a[1], c[0], c[1])
	side_c = distance(a[0], a[1], b[0], b[1])

	# calculate semi-perimeter of the triangle (perimeter / 2)
	s = (side_a + side_b + side_c) / 2

	# apply Heron's formula and return
	return sqrt(s * (s - side_a) * (s - side_b) * (s - side_c))
# loop through each node, excluding the end points
areas = []
for i in range(1, len(node_list)-1):

  # get the effective area
  area = get_effective_area(  , node_list[i],  )	# COMPLETE THIS LINE

  # append the node and effective area to the list
  areas.append({"point": node_list[i], "area": area})
  
  # add the end points back in at the start (0) and end (len(areas))
areas.insert(0, {"point": node_list[0], "area": 0})
areas.insert(len(areas), {"point": node_list[len(node_list)-1], "area": 0})

# remove one node and overwrite it with the new, shorter list
simplified_nodes = visvalingam_whyatt(coord_list, n_nodes)

# take a copy of the list so that we don't edit the original
nodes = areas.copy()

# keep going as long as the number of nodes is greater than the desired number
while len(nodes) > n_nodes:
    
    # remove the current point from the list
nodes.pop(node_to_delete)

# if there is a node to the left of the deleted node, recalculate the effective area
if node_to_delete > 1:
	nodes[node_to_delete-1]['area'] = get_effective_area(   , nodes[node_to_delete-1]['point'],    )	# COMPLETE THIS LINE

# if there is a node to the right of the deleted node, recalculate the effective area
if node_to_delete < len(nodes)-1:
	nodes[node_to_delete]['area'] = get_effective_area(   , nodes[node_to_delete]['point'],   )		# COMPLETE THIS LINE
    
    # extract the nodes and return
return [ node['point'] for node in nodes ]

# extract the nodes and return
out = []
for node in nodes:
  out.append(node['point'])

return out

from shapely.geometry import LineString

# make a linestring out of the coordinates
before_line = LineString(coord_list)
print(f"original node count: {len(coord_list)}")
print(f"original length: {before_line.length / 1000:.2f}km\n")

# make the resulting list of coordinates into a line
after_line = LineString(simplified_nodes)
print(f"simplified node count: {len(simplified_nodes)}")
print(f"simplified length: {after_line.length / 1000:.2f}km\n")

from geopandas import GeoSeries # THIS ONE CAN BE COMBINED WITH AN EXISTING IMPORT STATEMENT
from matplotlib_scalebar.scalebar import ScaleBar
from matplotlib.pyplot import subplots, savefig, subplots_adjust

# create map axis object, with two axes (maps)
fig, my_axs = subplots(1, 2, figsize=(16, 10))

# get the proj string definition for British National Grid (OSGB)
osgb = "+proj=tmerc +lat_0=49 +lon_0=-2 +k=0.9996012717 +x_0=400000 +y_0=-100000 +ellps=airy +towgs84=446.448,-125.157,542.06,0.15,0.247,0.842,-20.489 +units=m +no_defs"

# set titles
fig.suptitle("The Length of the Coastline of Mainland Great Britain")
my_axs[0].set_title(f"Original: {before_line.length / 1000:.0f}km, {len(coord_list)} nodes.")
my_axs[1].set_title(f"{SIMPLIFICATION_PERC}% Simplified: {after_line.length / 1000:.0f}km, {len(simplified_nodes)} nodes.")

# reduce the gap between the subplots
subplots_adjust(wspace=0)

# add the original coastline
GeoSeries(before_line, crs=osgb).plot(
    ax=my_axs[0],
    color='blue',
    linewidth = 0.6,
	)

# add the new coastline
GeoSeries(after_line, crs=osgb).plot(
    ax=my_axs[1],
    color='red',
    linewidth = 0.6,
	)

# edit individual axis
for my_ax in my_axs:

	# remove axes
	my_ax.axis('off')

	# add north arrow
	x, y, arrow_length = 0.95, 0.99, 0.1
	my_ax.annotate('N', xy=(x, y), xytext=(x, y-arrow_length),
		arrowprops=dict(facecolor='black', width=5, headwidth=15),
		ha='center', va='center', fontsize=20, xycoords=my_ax.transAxes)

	# add scalebar
	my_ax.add_artist(ScaleBar(dx=1, units="m", location="lower right"))

# save the result
savefig(f'out/4.png', bbox_inches='tight')
print("done!")

# eliminate polygons that are too small
if poly.area > 500000000:
    # init counter variables
original_nodes = 0
original_len = 0
simplified_nodes = 0
simplified_len = 0

# init lists to hold the results
original_lines = []
simplified_lines = []