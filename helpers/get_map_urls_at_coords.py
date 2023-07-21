import requests
import sys

def get_map_urls_at_coords(lat, lon):
    """  
    returns: dictionary of maps at inputted lat/lon
        keys: name of map
        values: dictionary with keys sourceId, boundingBox, downloadURL, publicationYear, and scale
    """

    #form api requests
    api_base_url = "https://tnmaccess.nationalmap.gov/api/v1/products?"
    api_format = "prodFormats=GeoTIFF&"
    api_extents = ["prodExtents=7.5%20x%207.5%20minute&", "prodExtents=7.5%20x%2015%20minute&", "prodExtents=30%20x%2060%20minute&", "prodExtents=30%20x%2030%20minute&", "prodExtents=3.75%20x%203.75%20minute&", "prodExtents=2%20x%201%20degree&", "prodExtents=15%20x%2015%20minute&", "prodExtents=1%20x%202%20degree&"]
    api_dataset = "datasets=Historical%20Topographic%20Maps&"
    api_bbox = f'bbox={lon},{lat},{lon},{lat},&'
    
    api_requests = []
    for api_extent in api_extents:
        api_requests.append(api_base_url + api_format + api_extent + api_dataset + api_bbox)

    #make api requests and log in maps dict
    maps = {}
    for api_request in api_requests: 
        try:
            res = requests.get(api_request).json() #make API call
            
            if 'items' in res.keys():
                #save non-repeating maps to dict with important attributes only
                for map in res['items']:
                    title = map['title']
                    if title not in maps:
                        maps[title] = {'sourceId': map['sourceId'], 
                                            'boundingBox': map['boundingBox'], 
                                            'downloadURL': map['downloadURL'], 
                                            'publicationYear': map['publicationDate'][0:4],
                                            'scale': int(title[title.find(":")+1:title.find("-")]),
                                            }
        except Exception as e:
            print("***ERROR***")
            print (e, file=sys.stderr) #TODO: error handling here could be improved - usually a timeout, should try 2x before moving on


    return maps
