from helpers.get_map_urls_at_coords import get_map_urls_at_coords
from helpers.download_cropped_map import download_cropped_map
from helpers.get_recognized_text import get_recognized_text

#INPUTS
lat = 34.500880266090036 #x
lon = -118.2829927423854 #y
url1 = 'https://prd-tnm.s3.amazonaws.com/StagedProducts/Maps/HistoricalTopo/GeoTIFF/CA/CA_Los%20Angeles_299820_1975_250000_geo.tif'
url2 = 'https://prd-tnm.s3.amazonaws.com/StagedProducts/Maps/HistoricalTopo/GeoTIFF/CA/CA_Los%20Angeles_299817_1966_250000_geo.tif'


#function testing
#maps = get_map_urls_at_coords(lat, lon)

#download_cropped_map(url2, "beacon_example.tif", lat, lon)

#get_recognized_text("beacon_example.tif", "beacon_example_annotated.tif")
get_recognized_text("text recognition test image 1.png", "text recognition test image 1 out.png")


#large-scale processing
#LOAD OCR READER AT THIS LEVEL
# for title, data in maps.items():
#     data['downloadUrl']
#     download_cropped_map(url, "crop_output.tif", lat, lon)