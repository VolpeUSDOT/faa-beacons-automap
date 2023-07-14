import rasterio
from rasterio.plot import show
from shapely.geometry import Polygon
from rasterio.mask import mask
import geopandas as gpd
import json
import pandas

#tutorial used: https://automating-gis-processes.github.io/CSC18/lessons/L6/clipping-raster.html

def download_cropped_map(source_url, dest_path, lat, lon):
    #read raster
    img = rasterio.open(source_url)

    #create bounding box
    def bbox(lat,lng,margin):                                                                                                                  
        return Polygon([[lng-margin, lat-margin],[lng-margin, lat+margin],
        [lng+margin,lat+margin],[lng+margin,lat-margin]])
    bbox_shp = gpd.GeoDataFrame(pandas.DataFrame(['p1'], columns = ['geom']),
        crs = {'init':'epsg:4326'},
        geometry = [bbox(lat,lon,0.12)])

    #convert bounding box to projection of original tif
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
                    "crs": img.meta['crs']})

    #write to disk
    with rasterio.open(dest_path, "w", **out_meta) as dest:
        dest.write(out_img)