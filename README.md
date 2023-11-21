# faa-beacons-automap
Python tool for speeding up FAA light beacon location verification using USGS Historical Topo maps.

If you want to use this code to reproduce my results, run the batch_locating function in main.py.
If you want to input a different coordinate dataset, you'll probably have to change the way the csv is read/processed at the beginning of main.py.

main.py calls on three helper files:
- get_map_urls_at_coords.py - calls National Map API to get all of the download links for historical topo containing the input coordinates
- download_cropped_map.py - downloads a historical topo, crops it around the input coordinates, and draws a little icon at the input coordinates
- get_recognized_text.py - runs optical text recognition (OCR) on map file and resaves map with boxes around any instances of the word "BEACON"
