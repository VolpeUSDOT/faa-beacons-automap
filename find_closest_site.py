import geopandas
import numpy as np
import pandas
from scipy.spatial import cKDTree
from shapely.geometry import Point

#tutorial used: https://gis.stackexchange.com/questions/222315/finding-nearest-point-in-other-geodataframe-using-geopandas

allpoints_df = pandas.read_csv('LightBeacons_Supplemental_November_Datatable.csv', encoding='Latin-1')
allpoints_gdf = geopandas.GeoDataFrame(allpoints_df, crs='epsg:4326', geometry=geopandas.points_from_xy(allpoints_df.longitude, allpoints_df.latitude))

newpoints_df = pandas.read_csv('web_docs.csv', encoding='Latin-1')
newpoints_gdf = geopandas.GeoDataFrame(newpoints_df, crs='epsg:4326', geometry=geopandas.points_from_xy(newpoints_df.web_longitude, newpoints_df.web_latitude))

def ckdnearest(gdA, gdB):
    nA = np.array(list(gdA.geometry.apply(lambda x: (x.x, x.y))))
    nB = np.array(list(gdB.geometry.apply(lambda x: (x.x, x.y))))
    btree = cKDTree(nB)
    dist, idx = btree.query(nA, k=1)
    gdB_nearest = gdB.iloc[idx].drop(columns="geometry").reset_index(drop=True)
    gdf = pandas.concat(
        [
            gdA.reset_index(drop=True),
            gdB_nearest,
            pandas.Series(dist, name='dist')
        ], 
        axis=1)

    return gdf

out_gdf = ckdnearest(newpoints_gdf, allpoints_gdf)
print(out_gdf.columns)
out_gdf.to_excel("find_closest_site_out.xlsx")