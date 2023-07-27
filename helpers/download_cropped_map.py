import rasterio
from rasterio.plot import show
from shapely.geometry import Polygon, Point
from rasterio.mask import mask
import geopandas as gpd
import json
import pandas
from PIL import Image, ImageDraw

#whoops bad practice
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

#tutorial used: https://automating-gis-processes.github.io/CSC18/lessons/L6/clipping-raster.html

def download_cropped_map(source_url, dest_path, lat, lon, scale):
    """
    Downloads the topo map at source_url with centerpoint at given lat lon, clips a map 
    with width and height of 2xBUFFER degrees, and saves to dest_path
    """

    #read raster
    img = rasterio.open(source_url)

    def get_bounding_box(margin):
        #create geodataframe bounding box
        bbox = Polygon([[lon-margin, lat-margin],[lon-margin, lat+margin],[lon+margin, lat+margin],[lon+margin, lat-margin]])
        bbox_shp = gpd.GeoDataFrame(pandas.DataFrame(['p1'], columns=['geom']),
            crs = {'init':'epsg:4326'},
            geometry = [bbox])

        #convert bounding box to projection of original tif
        bbox_shp = bbox_shp.to_crs(crs=img.meta['crs'])

        #convert bounding box to json for rasterio function
        return [json.loads(bbox_shp.to_json())['features'][0]['geometry']]

    #crop
    if scale <= 62500:
        bbox_shp = get_bounding_box(0.025)
    else:
        bbox_shp = get_bounding_box(0.05)
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

    #find centerpoint
    cropped_image = rasterio.open(dest_path)
    
    centerpoint_shp = gpd.GeoDataFrame(pandas.DataFrame(['p1'], columns=['geom']),
        crs = {'init':'epsg:4326'},
        geometry = [Point(lon, lat)])
    centerpoint_shp = centerpoint_shp.to_crs(crs=img.meta['crs'])
    centerpoint_pixels = rasterio.transform.rowcol(cropped_image.transform, centerpoint_shp['geometry'].x, centerpoint_shp['geometry'].y)
    pixel_row, pixel_col = centerpoint_pixels[0][0], centerpoint_pixels[1][0]

    #draw centerpoint
    cropped_image = Image.open(dest_path)
    metadata = cropped_image.getexif()

    draw = ImageDraw.Draw(cropped_image)
    r = 15
    draw.ellipse([(pixel_col-r, pixel_row-r), (pixel_col+r, pixel_row+r)], outline=(255,0,0,150), width=4) #outer
    draw.ellipse([(pixel_col-1, pixel_row-1), (pixel_col+1, pixel_row+1)], outline=(255,0,0,150), width=4) #inner

    cropped_image.save(dest_path, exif=metadata)