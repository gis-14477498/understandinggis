from geopandas import read_file, GeoSeries #import files
from matplotlib_scalebar.scalebar import ScaleBar
from matplotlib.pyplot import subplots, savefig, title
from pyproj import Geod
from matplotlib.lines import Line2D
from matplotlib.patches import Patch 
world = read_file("../../data/natural-earth/ne_10m_admin_0_countries.shp")
print(world.columns)

usa = world.loc[(world.ISO_A3 == 'USA')] # extract the country rows as a GeoDataFrame object with 1 row
print(type(usa))
usa_col = usa.geometry # extract the geometry columns as a GeoSeries object
print(type(usa_col))
usa_geom = usa_col.iloc[0] # extract the geometry objects themselves from the GeoSeries
print(type(usa_geom))

mex = world.loc[(world.ISO_A3 == 'MEX')]
print(type(mex))
mex_col = mex.geometry
print(type(mex_col))
mex_geom = mex_col.iloc[0]
print(type(mex_geom))

border = usa_geom.intersection(mex_geom) # calculate the intersection of the geometry objects


my_fig, my_ax = subplots(1, 1, figsize=(16, 10)) # create map axis object
my_ax.axis('off') # remove axes
GeoSeries(border).plot(
  ax = my_ax
	)            # plot the border
savefig('./out/first-border.png')# save the image


# set which ellipsoid you would like to use
g = Geod(ellps='WGS84')

# initialise a variable to hold the cumulative length
cumulative_length = 0

# loop through each segment in the line
for segment in border.geoms:

	# THIS LINE NEEDS COMPLETING
	distance = g.inv(segment.coords[0][0], segment.coords[0][1], segment.coords[1][0], segment.coords[1][1])[2] 

	# add the distance to our cumulative total
	cumulative_length += distance
print(cumulative_length)

# open the graticule dataset
graticule = read_file("../../data/natural-earth/ne_110m_graticules_5.shp")

# create map axis object
my_fig, my_ax = subplots(1, 1, figsize=(16, 10))
lambert_conic='+proj=lcc +lon_0=-99.84375 +lat_1=2.3879563 +lat_2=30.2091988 +lat_0=16.2985775 +datum=WGS84 +units=m +no_defs'
# remove axes
my_ax.axis('off')

# set title
title(f"The wall would have been {cumulative_length / 1000:.2f} km long.")

# project border
border_series = GeoSeries(border, crs=world.crs).to_crs(lambert_conic)

# extract the bounds from the (projected) GeoSeries Object
minx, miny, maxx, maxy = border_series.geometry.iloc[0].bounds

# set bounds (10000m buffer around the border itself, to give us some context)
buffer = 10000
my_ax.set_xlim([minx - buffer, maxx + buffer])
my_ax.set_ylim([miny - buffer, maxy + buffer])

# plot data
usa.to_crs(lambert_conic).plot(
    ax = my_ax,
    color = '#ccebc5',
    edgecolor = '#4daf4a',
    linewidth = 0.5,
    )
mex.to_crs(lambert_conic).plot(
    ax = my_ax,
    color = '#fed9a6',
    edgecolor = '#ff7f00',
    linewidth = 0.5,
    )
border_series.plot(     # note that this has already been projected above!
    ax = my_ax,
    color = '#984ea3',
    linewidth = 2,
    )
graticule.to_crs(lambert_conic).plot(
    ax=my_ax,
    color='grey',
    linewidth = 1,
    )

# save the result
savefig('out/2.png', bbox_inches='tight')


# add north arrow
x, y, arrow_length = 0.98, 0.99, 0.1
my_ax.annotate('N', xy=(x, y), xytext=(x, y-arrow_length),
	arrowprops=dict(facecolor='black', width=5, headwidth=15),
	ha='center', va='center', fontsize=20, xycoords=my_ax.transAxes)

# add scalebar
my_ax.add_artist(ScaleBar(dx=1, units="m", location="lower left", length_fraction=0.25))

# add legend
my_ax.legend(handles=[
        Patch(facecolor='#ccebc5', edgecolor='#4daf4a', label='USA'),
        Patch(facecolor='#fed9a6', edgecolor='#ff7f00', label='Mexico'),
        Line2D([0], [0], color='#984ea3',  lw=0.6, label='Border')
    ],loc='lower right')

print("done!")