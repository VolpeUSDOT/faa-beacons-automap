import requests

def get_map_urls_at_coords(lat, lon):
    """  
    returns: dictionary of maps at inputted lat/lon
        key: name of map
        value: dictionary with keys sourceId, boundingBox, downloadURL, and publicationYear
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
        response = requests.get(api_request)

        response_maps = response.json()['items']
        for map in response_maps:
            if map['title'] not in maps:
                maps[map['title']] = {'sourceId': map['sourceId'], 
                                      'boundingBox': map['boundingBox'], 
                                      'downloadURL': map['downloadURL'], 
                                      'publicationYear': map['publicationDate'][0:4]}

    return maps
