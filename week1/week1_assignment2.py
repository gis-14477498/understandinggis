# -*- coding: utf-8 -*-
"""
Created on Wed Sep 30 21:25:43 2026

@author: 86391
"""

from geopandas import read_file
from matplotlib.pyplot import subplots, savefig

# read spatial datasets
world = read_file("../../data/natural-earth/ne_50m_admin_0_countries.shp")
graticule = read_file("../../data/natural-earth/ne_110m_graticules_15.shp")
bbox = read_file("../../data/natural-earth/ne_110m_wgs84_bounding_box.shp")

# define Equal Earth projection
ea_proj="+proj=eqearth +lon_0=0 +datum=WGS84 +units=m +no_defs"

# reproject all three layers to equal earth
world = world.to_crs(ea_proj)
graticule = graticule.to_crs(ea_proj)
bbox = bbox.to_crs(ea_proj)

# calculate GDP per Capita
world['GDP_per_Capita'] = world['GDP_MD_EST'] * 1000000 / world['POP_EST']

# create map axis object
my_fig, my_ax = subplots(1, 1, figsize=(16, 10))

# add map title
my_ax.set(title="GDP per Capita: Equal Earth Coordinate Reference System")

# add bounding box and graticule layers
bbox.plot(
    ax = my_ax,
    color = 'lightgrey',
    linewidth = 0,
    )

# plot the countries
world.plot(								# plot the world dataset
    ax = my_ax,						# specify the axis object to draw it to
    column = 'GDP_per_Capiita',  # specify the column used to style the dataset
    cmap = 'OrRd',				# specify the colour map used to style the dataset based on POP_EST
    scheme = 'quantiles',	# specify how the colour map will be mapped to the values in POP_EST
    linewidth = 0.5,			# specify the line width for the country outlines
    edgecolor = 'gray',		# specify the line colour for the country outlines
    legend = True,
    legend_kwds = {
        'loc': 'lower left',
        'title': 'GDP per Capiita'
        }
    )


# plot the graticule
graticule.plot(
    ax = my_ax,
    color = 'white',
    linewidth = 0.5,
    )

# turn off the visible axes on the map
my_ax.axis('off')

# save the result
savefig('./out/3.png')
print("done!")
