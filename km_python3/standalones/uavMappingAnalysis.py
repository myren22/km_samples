'''
Created on Mar 21, 2019

@author: kmyren
'''
# import os
# 
# #install with "pip install pandas geojson Pillow ipyleaflets
# import pandas as pd
# import geojson
# from PIL import ImageOps, Image
# from ipyleaflet import Map,basemaps,basemap_to_tiles,Marker,MeasureControl,GeoJSON,LayersControl,Circle,Polyline,Rectangle,ImageOverlay
# from ipywidgets import Layout
# 
# m = Map(center=(35.0774, -84.9865), zoom=13)
# 
# print("hello world!")

#%matplotlib inline
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
 
fig = plt.figure(figsize=(8, 8))
m = Basemap(projection='ortho', resolution=None,
            lat_0=35.0595, lon_0=-84.9645)
draw_map(m);