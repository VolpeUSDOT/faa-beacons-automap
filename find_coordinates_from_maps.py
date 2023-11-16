import cv2
import matplotlib
import matplotlib.pyplot as plt
import csv
import os
import datetime
import pandas
import rasterio
import geopandas as gpd
from shapely.geometry import Point

class MapImage():
    def __init__(self, filename):
        self.fname = filename
        self.img = cv2.imread(self.fname)
        self.shift_is_held = False

    def getCoord(self):
        fig = plt.figure()
        plt.imshow(self.img)
        cid = fig.canvas.mpl_connect('button_press_event', self.__onclick__)
        cid2 = fig.canvas.mpl_connect('key_press_event', self.on_key_press)
        cid3 = fig.canvas.mpl_connect('key_release_event', self.on_key_release)
        plt.show()

    def on_key_press(self, event):
        if event.key == 'shift':
            self.shift_is_held = True

    def on_key_release(self, event):
        if event.key == 'shift':
            self.shift_is_held = False

    def __onclick__(self,click):
        if self.shift_is_held:
            self.point = (click.xdata,click.ydata)
            with open('find_coordinates_from_maps_out.csv', 'a', encoding='Latin-1', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([str(datetime.datetime.now()), self.fname, self.point[0], self.point[1]])
            self.shift_is_held = False
            plt.close()

def open_maps_to_click_beacons():
    files = os.listdir("../beacons_maps/")
    recorded_files = pandas.read_csv('find_coordinates_from_maps_out.csv')['filename'].tolist()
    for i, file in enumerate(files):
        if "../beacons_maps/" + file not in recorded_files:
            print(file)
            image = MapImage("../beacons_maps/" + file)
            image.getCoord()

def convert_pixel_coords_geo_coords():
    recorded_files = pandas.read_csv('find_coordinates_from_maps_out.csv')
    for index, row in recorded_files.iterrows():
        #read csv row
        x, y, filename = float(row['x']), float(row['y']), row['filename']

        #find coordinates of pixel
        map = rasterio.open(filename)
        lon, lat = rasterio.transform.xy(map.transform, y, x)

        #convert to lat/lon from georaster coordinate system
        centerpoint_shp = gpd.GeoDataFrame(pandas.DataFrame(['p1'], columns=['geom']),
            crs = map.meta['crs'],
            geometry = [Point(lon, lat)])
        centerpoint_shp = centerpoint_shp.to_crs(4326)

        #write to output file
        pnt = centerpoint_shp.geometry

        substring = filename[filename.find("maps/")+5:filename.find("USGS")-1]
        site_num = substring[0:substring.find("_")]

        with open('convert_pixels_to_coordinates.csv', 'a', encoding='Latin-1', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([filename, site_num, pnt.x[0], pnt.y[0]])

#convert_pixel_coords_geo_coords()


def check_for_duplicate_coordinates():
    dupes = []
    
    first_read = pandas.read_csv('convert_pixels_to_coordinates.csv')
    for i1, r1 in first_read.iterrows():
    #read csv row
        lat1, lon1, site_id1 = float(r1['latitude']), float(r1['longitude']), r1['site_id']
        second_read = pandas.read_csv('convert_pixels_to_coordinates.csv')
        for i2, r2 in second_read.iterrows():
            lat2, lon2, site_id2 = float(r2['latitude']), float(r2['longitude']), r2['site_id']
            if site_id1 != site_id2 and abs(lat2-lat1) < .01 and abs(lon2-lon1) < .01:
                if (site_id2, site_id1) not in dupes:
                    dupes.append((site_id1, site_id2))
    print(dupes)

#check_for_duplicate_coordinates()