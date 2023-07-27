# faa-beacons-automap
Python tool for speeding up FAA light beacon location verification using USGS Historical Topo maps.

If you want to use this code to reproduce my results, run the batch_locating function in main.py.
If you want to input a different coordinate dataset, you'll probably have to change the way the csv is read/processed at the beginning of main.py.

main.py calls on three helper files:
- get_map_urls_at_coords.py - calls National Map API to get all of the historical topo download links at a point
- download_cropped_map.py - downloads a historical topo, crops it around the input point, and draws a point at the input point
- get_recognized_text.py - runs optical text recognition (OCR) on map file and resaves map with boxes around any instances of the word "BEACON"
