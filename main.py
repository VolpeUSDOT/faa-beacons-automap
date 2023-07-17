from helpers.get_map_urls_at_coords import get_map_urls_at_coords
from helpers.download_cropped_map import download_cropped_map
from helpers.get_recognized_text import get_recognized_text

import easyocr
import pandas

#TEST INPUTS
test_lat = 34.500880266090036 #x
test_lon = -118.2829927423854 #y
test_url1 = 'https://prd-tnm.s3.amazonaws.com/StagedProducts/Maps/HistoricalTopo/GeoTIFF/CA/CA_Los%20Angeles_299820_1975_250000_geo.tif'
test_url2 = 'https://prd-tnm.s3.amazonaws.com/StagedProducts/Maps/HistoricalTopo/GeoTIFF/CA/CA_Los%20Angeles_299817_1966_250000_geo.tif' #has one instance of the word beacon
test_image = "Test_Inputs_Outputs/text recognition test image 1.png"
test_image_out = "Test_Inputs_Outputs/text recognition test image 1 out.png"

#FUNCTION TESTING
#maps = get_map_urls_at_coords(lat, lon)
#download_cropped_map(url2, "beacon_example.tif", lat, lon)
#get_recognized_text("beacon_example.tif", "beacon_example_annotated.tif")
#get_recognized_text("text recognition test image 1.png", "text recognition test image 1 out.png")


def batch_locating(start_site_id, end_site_id):
    """
    """

    # Open Beacons csv and iterate through each site to collect best coordinates
    BEACONS_CSV = "LightBeacons_Supplemental_July17_Datatable.csv"
    beacons_df = pandas.read_csv(BEACONS_CSV, encoding='Latin-1')
    beacons_df = beacons_df.reset_index()

    best_centerpoints = {} #keys: site_id, values: {latitude, longitude, source}
    def write_to_best_coordinates(site_id, lat, lon, source):
        best_centerpoints[site_id] = (lat, lon, source)

    for index, row in beacons_df.iterrows():
        site_id = row['site_id']

        if site_id < start_site_id: #don't process before start_site_id
            continue
        if site_id > end_site_id: #stop collecting coordinates for entries after end_site_id
            break
        
        #check to see if best centerpoint
        lat, lon, source = row['latitude'],  row['longitude'],  row['source_lay']
        if site_id in best_centerpoints.keys():
            if source == "beacons_kml":
                write_to_best_coordinates(site_id, lat, lon, source)
            elif source == "beacons_ksn":
                write_to_best_coordinates(site_id, lat, lon, source)
        else:
            write_to_best_coordinates(site_id, lat, lon, source)
        
    ocr_reader = easyocr.Reader(['en']) # load the text recgnition model into memory

    for site_id, site_info in best_centerpoints.items():
        lat, lon, source = site_info

        map_urls = get_map_urls_at_coords(lat, lon)

        for map_title, map_info in map_urls.items(): #will want to have this block in some sort of try/except block in case download/crop/recognition fails
            filename = f'{site_id}_{source}_{map_title}'
            download_cropped_map(map_info["downloadURl"], f'working downloads/{filename}', lat, lon) #will I have to wait for this to be done downloading / is downloading async?
            get_recognized_text(f'working downloads/{filename}', f'detection outputs/{filename}', ocr_reader) # Feed each cropped map into get_recognized_text, save maps with recognized text under site name
            # TO DO: Delete original cropped maps
    

#batch_locating(1, 15)