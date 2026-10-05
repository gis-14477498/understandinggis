from geopandas import read_file, GeoSeries #import files
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