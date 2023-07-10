import matplotlib
import rasterio
from rasterio.plot import show
from shapely.geometry import box
from shapely.geometry import Polygon

from rasterio.plot import show_hist
from rasterio.mask import mask
import geopandas as gpd
from fiona.crs import from_epsg
#import pycrs
import json
import pandas

#tutorial used: https://automating-gis-processes.github.io/CSC18/lessons/L6/clipping-raster.html

#read raster
url = 'https://prd-tnm.s3.amazonaws.com/StagedProducts/Maps/HistoricalTopo/GeoTIFF/CA/CA_Los%20Angeles_299820_1975_250000_geo.tif'
img = rasterio.open(url)

#create bounding box
ycoord, xcoord = 34.500880266090036, -118.2829927423854 
def bbox(lat,lng,margin):                                                                                                                  
    return Polygon([[lng-margin, lat-margin],[lng-margin, lat+margin],
    [lng+margin,lat+margin],[lng+margin,lat-margin]])
bbox_shp = gpd.GeoDataFrame(pandas.DataFrame(['p1'], columns = ['geom']),
    crs = {'init':'epsg:4326'},
    geometry = [bbox(ycoord,xcoord,0.12)])

#convert bounding box to raster projection
bbox_shp = bbox_shp.to_crs(crs=img.meta['crs'])

#crop
bbox_shp = [json.loads(bbox_shp.to_json())['features'][0]['geometry']]
out_img, out_transform = mask(img, bbox_shp, crop=True)

#fix metadata
out_meta = img.meta.copy()
out_meta.update({"driver": "GTiff", 
                 "height": out_img.shape[1], 
                 "width": out_img.shape[2], 
                 "transform": out_transform, 
                 "crs": img.meta['crs'].to_dict()})


#!!! fix writing to disk w metadata
with rasterio.open(out_img, "w", **out_meta) as dest:
    dest.write(out_img)

clipped = rasterio.open(out_img)

show(out_img)

