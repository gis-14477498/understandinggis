# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#import files
from geopandas import read_file, GeoSeries
world = read_file("../../data/natural-earth/ne_10m_admin_0_countries.shp")
print(world.columns)



