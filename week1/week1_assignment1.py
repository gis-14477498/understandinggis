# -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 12:08:30 2026

@author: 86391
"""

from geopandas import read_file
world = read_file("../../data/natural-earth/ne_50m_admin_0_countries.shp")
graticule = read_file("../../data/natural-earth/ne_110m_graticules_15.shp")
bbox = read_file("../../data/natural-earth/ne_110m_wgs84_bounding_box.shp")

