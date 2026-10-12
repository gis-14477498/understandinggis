from geopandas import read_file
# read in shapefiles, ensure that they all have the same CRS
pop_points = read_file("../../data/gulu/pop_points.shp")
water_points = read_file("../../data/gulu/water_points.shp")
gulu_district = read_file("../../data/gulu/district.shp")
print(pop_points.crs.to_epsg())
print(water_points.crs.to_epsg())
print(gulu_district.crs.to_epsg())

