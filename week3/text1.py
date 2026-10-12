from geopandas import read_file
# read in shapefiles, ensure that they all have the same CRS
pop_points = read_file("../../data/gulu/pop_points.shp")
water_points = read_file("../../data/gulu/water_points.shp").to_crs(pop_points.crs)
gulu_district = read_file("../../data/gulu/district.shp").to_crs(pop_points.crs)
print(pop_points.crs.to_epsg())
print(water_points.crs.to_epsg())
print(gulu_district.crs.to_epsg())

print(pop_points.estimate_utm_crs(datum_name='Arc 1960'))
print(water_points.estimate_utm_crs(datum_name='Arc 1960'))
print(gulu_district.estimate_utm_crs(datum_name='Arc 1960'))


