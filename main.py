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
#ocr_reader = easyocr.Reader(['en'], verbose=False)
#get_recognized_text("detection_outputs_22_N_beacons_kml_USGS_1_250000_scale_Quadrangle_for_Douglas__AZ_1959_5a8a3eeee4b00f54eb3eadcc.tif", "test_inputs_outputs/site_22_test.tif", ocr_reader)


def batch_locating(start_site_id, end_site_id):
    """
    Given a starting site and ending site, this function pulls all of the other functions together by doing the following for each site:
        (STEP 1) reads the light beacons csv and finds the best data point to use coordinates for
        (STEP 2) uses get_map_urls_at_coords to call the National Map api to find download links for topos at those coordinates
        (STEP 3) uses download_cropped_map to download and crop each map
        (STEP 4) uses get_recognized_text to run a text recognition model on the map, 
            saving a map with all found instances of the word "beacon" highlighted if any are found, deleting the original downloaded map
    """

    #(STEP 1)
    #open csv
    BEACONS_CSV = "LightBeacons_Supplemental_July17_Datatable.csv"
    beacons_df = pandas.read_csv(BEACONS_CSV, encoding='Latin-1')
    beacons_df = beacons_df.reset_index()

    best_centerpoints = {} #keys: site_id, values: {latitude, longitude, source}
    def write_centerpoint(site_id, lat, lon, source):
        best_centerpoints[site_id] = (lat, lon, source)

    for index, row in beacons_df.iterrows(): #iterating over a dataframe but it's fine-ish because the ocr is the real bottleneck
        site_id = row['site_id']

        if site_id < start_site_id: #don't process and data for sites before start_site_id
            continue
        if site_id > end_site_id: #stop collecting coordinates for entries after end_site_id
            print(f"Progress: best centerpoints found for {len(best_centerpoints.keys())} sites.")
            break
        
        #if site number is within start and end site numbers, check to see if this entry is the best centerpoint
        lat, lon, source = row['latitude'],  row['longitude'],  row['source_lay']
        if site_id in best_centerpoints.keys():
            if source == "beacons_kml": #most preferred
                write_centerpoint(site_id, lat, lon, source)
            elif source == "beacons_ksn": #second most preferred
                write_centerpoint(site_id, lat, lon, source)
        else:
            write_centerpoint(site_id, lat, lon, source)
    
    #load the text recgnition model into memory once
    print('Progress: loading ocr model')
    ocr_reader = easyocr.Reader(['en'], verbose=False) 

    #now that there is one best centerpoint for each site, iterate through each site to download and process
    for site_id, site_info in best_centerpoints.items():
        lat, lon, source = site_info

        #(STEP 2)
        print(f'Progress: site {site_id}: finding map download urls at coordinates')
        map_urls = get_map_urls_at_coords(lat, lon)
        print(f'    {len(map_urls.keys())} map urls found')

        for map_title, map_info in map_urls.items(): #TODO: want to have this block in some sort of try/except block in case download/crop/recognition fails
            def get_filename(type):            
                filename = f'{site_id}_{type}_{source}_{map_title}_{map_info["sourceId"]}'
                filename = "".join(x if x.isalnum() else "_" for x in filename) + ".tif" #clean filename - alphanumeric characters only
                return 'detection outputs/' + filename
            
            try:
                #(STEP 3)
                print(f'Progress: site {site_id}: downloading map "{map_title}"')
                download_cropped_map(map_info["downloadURL"], get_filename('N'), lat, lon)

                #(STEP 4)
                print(f'Progress: site {site_id}: running ocr for map "{map_title}"')
                get_recognized_text(get_filename('N'), get_filename('Y'), ocr_reader)
            except:
                print(Exception)
            
        print(f"Progress: all maps processed and saved for site {site_id}.")


batch_locating(1, 22)