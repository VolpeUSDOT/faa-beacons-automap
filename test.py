import os
import pandas
import openpyxl
import shutil
#import geopy
from geopy.geocoders import Nominatim
import csv

BEACONS_CSV_PATH = "LightBeacons_Supplemental_November_Datatable.csv"
beacons_df = pandas.read_csv(BEACONS_CSV_PATH, encoding='Latin-1')
beacons_df = beacons_df.reset_index()


# counting num of grouped sites and finding false positives

# sites_with_groupings = set()

# for index, row in beacons_df.iterrows():
#     if str(row['clustered']) == "Y":
#         if row['site_id'] not in sites_with_groupings:
#             sites_with_groupings.add(row['site_id'])

# print(len(sites_with_groupings))


source_for_grouped_points = {"topo": 0, "beacon_ksn": 0, "beacons_kml": 0, "web_docs": 0, "Aeronautical Charts": 0}

for index, row in beacons_df.iterrows():
    if str(row['clustered']) == "Y":
        if row['source_lay'] in source_for_grouped_points:
            source_for_grouped_points[row['source_lay']] += 1
        else:
            source_for_grouped_points["Aeronautical Charts"] += 1

print(source_for_grouped_points)


source_counts = {"topo": 0, "beacon_ksn": 0, "beacons_kml": 0, "web_docs": 0, "Aeronautical Charts": 0}
for index, row in beacons_df.iterrows():
    if row['source_lay'] in source_counts:
        source_counts[row['source_lay']] += 1
    else:
        source_counts["Aeronautical Charts"] += 1

print(source_counts)



# site_group_sizes = dict()

# for index, row in beacons_df.iterrows():
#     if str(row['clustered']) == "Y":
#         if row['site_id'] not in site_group_sizes:
#             site_group_sizes[row['site_id']] = 1
#         else:
#             site_group_sizes[row['site_id']] += 1

# print(site_group_sizes)

# for key, value in site_group_sizes.items():
#     if value == 1:
#         print(key)

# copying good maps

# count = 0

# for index, row in beacons_df.iterrows():
#     filename = str(row['topo_file'])
#     files = os.listdir("../beacons_maps/")
#     if filename not in files and len(filename) > 3:
#         print(filename)

#     # if len(filename) > 3:
#     #     count += 1 
#     #     #shutil.copy2("../detection outputs/" + filename, "../beacons_maps/" + filename)

# # print(count)




#remark which data source was checked for each site

# best_centerpoints = {}
# def write_centerpoint(site_id, source, index):
#     best_centerpoints[site_id] = (source, index)

# for index, row in beacons_df.iterrows():
#         site_id = row['site_id']
#         source = row['source_lay']
#         if site_id in best_centerpoints.keys():
#             if source == "beacons_kml": #most preferred
#                 write_centerpoint(site_id, source, index)
#             elif source == "beacons_ksn": #second most preferred
#                 write_centerpoint(site_id, source, index)
#         else:
#             write_centerpoint(site_id, source, index)

# for site_id, data in best_centerpoints.items():
#     source, index = data[0], data[1]
#     beacons_df.loc[index, "auto"] = source

# beacons_df.to_excel("validation_out_2.xlsx", 'Sheet1', index=False)   



#go through nums at start of files

# files = os.listdir("../detection outputs/")
# for i, file in enumerate(files):
#     first_us = file.index("_")
#     files[i] = int(file[:first_us])



#testing for multiple kmls

# best_centerpoints = {} #keys: site_id, values: {latitude, longitude, source}
# def write_centerpoint(site_id):
#     if site_id not in best_centerpoints.keys():
#         best_centerpoints[site_id] = 1
#     else:
#         best_centerpoints[site_id] += 1

# for index, row in beacons_df.iterrows():
#     site_id = row['site_id']
#     source = row['source_lay']
#     if source == "beacons_kml": #most preferred
#         write_centerpoint(site_id)

# print(best_centerpoints)

# for id, num in best_centerpoints.items():
#     if num > 1:
#         print(id)



#counting successful detections or something

# answers = {}

# for file in files:
#     first_us = file.index("_")
#     num = file[:first_us]
#     answers[num] = 0

# for file in files:
#     first_us = file.index("_")
#     if file[first_us+1:file.index("_", first_us+1)] == "Y":
#         answers[num] = 1

# print(len(answers.keys()))
# print(sum(answers.values()))

# lats = [
#     33.5924526,
#     33.4496389,
#     33.0032494,
#     32.7188757,
#     31.92026291,
#     31.76463827,
#     31.4890323,
#     31.3453181,
#     31.9912811,
#     35.20014333,
#     35.1529359,
#     35.1077301,
#     35.0696723,
#     35.0220215,
#     35.0269002,
#     35.0257467,
#     35.0283917,
#     34.9359791,
#     35.0295132,
#     35.0398155,
#     35.0347516,
#     34.7351787,
#     35.1362107,
#     31.4179039,
#     31.5804639,
#     34.4448934,
#     35.077562,
#     35.3996152,
#     37.7874936,
#     37.9026412,
#     41.7284959,
#     41.8577441,
#     38.953245,
#     39.3085044,
#     39.3109661,
#     39.321809,
#     41.4396195,
#     42.0110134,
#     42.5413192,
#     43.2459378,
#     43.3659175,
#     43.5034451,
#     44.1689282,
#     37.1519812,
#     37.2550105,
#     37.3504557,
#     37.5346275,
#     44.81904,
#     41.2141871,
#     35.9532762,
#     36.6853789,
#     36.79682844,
#     39.5100593,
#     39.57867606,
#     40.295974,
#     40.075346,
#     40.3452483,
#     41.0073428,
#     40.9250811,
#     40.9094561,
#     40.8466095,
#     40.7401133,
#     41.1027371,
#     40.851688,
#     40.9278663,
#     31.9282997,
#     31.9186511,
#     31.824869,
#     31.8030278,
#     35.1664605,
#     35.362591,
#     35.4269433,
#     35.5294609,
#     35.0562112,
#     35.1664197,
#     31.8178724,
#     31.8065474,
#     31.7802715,
#     31.7460427,
#     31.8532922,
#     31.8337302,
#     31.8143433,
#     31.8182373,
#     32.0775834,
#     32.4572305,
#     37.3959264,
#     40.4582811,
#     41.7082638,
#     40.7501114,
#     40.8859409,
#     41.5621331,
#     41.6716969,
#     41.6574491,
#     41.8170756,
#     41.8870672,
#     41.445701,
#     41.2262195,
#     41.1969737,
#     41.1647949,
#     41.1814176,
#     41.439669,
#     34.417009,
#     35.853758,
#     38.202465,
#     38.550538,
#     36.279004,
#     35.077582,
#     35.399638,
#     35.740175,
#     35.953291,
#     36.540803,
#     36.685313,
#     36.796807,
#     37.065031,
#     37.117443,
#     37.180577,
#     37.395882,
#     40.458392,
#     41.339137,
#     41.708251,
#     42.01097,
#     42.415687,
#     42.541296,
#     42.991293,
#     43.065376,
#     43.245908,
#     43.365799,
#     43.503414,
#     45.493944,
#     41.543336,
#     41.728455,
#     41.857716,
#     42.447933,
#     42.451566,
#     42.730083,
#     43.014163,
#     43.210943,
#     43.802045,
#     44.8189,
#     39.914748,
#     39.906933,
#     37.902652,
#     39.310921,
#     39.321803,
#     39.510018,
#     39.578623,
#     40.295988,
#     40.075377,
#     40.757958,
#     40.345212,
#     41.007369,
#     40.925068,
#     40.909402,
#     40.846553,
#     40.740119,
#     40.596104,
#     41.102691,
#     40.851696,
#     40.851722,
#     40.826505,
#     40.750015,
#     40.704553,
#     41.598768,
#     41.562086,
#     41.671638,
#     41.678992,
#     41.657424,
#     41.817054,
#     41.850283,
#     41.887107,
#     41.445629,
#     41.267873,
#     41.226232,
#     41.196869,
#     41.164781,
#     41.181378,
#     41.214164,
#     41.786497,
#     34.820876,
#     30.811407,
#     39.506896,
#     39.540298,
#     39.57679,
#     41.543358,
#     42.724449,
#     44.168858,
#     34.137539,
#     47.415312,
#     31.928343,
#     31.91861,
#     31.82481,
#     31.803015,
#     31.817888,
#     31.806444,
#     31.780141,
#     31.745964,
#     31.853277,
#     31.833647,
#     31.814212,
#     31.789974,
#     31.818195,
#     31.914223,
#     32.077499,
#     32.457054,
#     32.573874,
#     35.52939,
#     35.362562,
#     35.426752,
#     35.166517,
#     35.061033,
#     35.048712,
#     34.984756,
#     35.030487,
#     35.056165,
#     35.135861,
#     35.107036,
#     36.360148,
#     37.151884,
#     37.255016,
#     37.350424,
#     37.534602,
#     40.022605,
#     40.421633,
#     41.0930601,
#     43.245908,
#     40.846553,
#     44.318433,
#     46.974158,
#     35.115041,
#     35.13017,
#     35.166305,
#     35.18627,
#     35.195588
# ]

# lons = [
# -114.3476921,
# -112.6003241,
# -111.6748466,
# -111.4004962,
# -110.3696104,
# -110.1455669,
# -109.699084,
# -109.5111641,
# -109.3007636,
# -112.2049246,
# -111.4704445,
# -111.2163118,
# -110.9835657,
# -110.7159068,
# -110.5982933,
# -110.3478482,
# -110.1182916,
# -110.1401439,
# -109.5256093,
# -109.3050182,
# -109.2606677,
# -112.0395719,
# -111.6772258,
# -110.8521163,
# -110.3306928,
# -118.4396102,
# -116.3918868,
# -115.8312924,
# -122.1449375,
# -122.0780573,
# -122.5398759,
# -122.5117885,
# -121.074593,
# -120.5624156,
# -120.4657263,
# -120.336121,
# -72.9923254,
# -113.20586,
# -113.4559697,
# -115.8076882,
# -115.9567522,
# -116.1278339,
# -112.2243529,
# -98.0769308,
# -97.9109944,
# -97.747938,
# -97.4199078,
# -92.911915,
# -103.2521957,
# -115.1793603,
# -114.5176792,
# -114.2465698,
# -119.92238,
# -119.4901681,
# -118.351789,2
# -118.1815336,
# -117.3474476,
# -117.5927274,
# -117.3981292,
# -117.285645,
# -117.1935924,
# -117.0636083,
# -115.0905509,
# -114.440156,
# -114.294407,
# -108.9953572,
# -108.3284987,
# -107.6321733,
# -107.0651936,
# -107.8983252,
# -108.0460227,
# -108.3032467,
# -108.6064902,
# -106.7945774,
# -103.8549974,
# -105.7822255,
# -105.6278804,
# -105.3512311,
# -105.0816605,
# -104.548977,
# -104.2914788,
# -104.0295046,
# -102.8697077,
# -101.9481212,
# -100.290662,
# -113.2571934,
# -112.3638193,
# -112.919841,
# -112.6481616,
# -111.9493189,
# -109.6780392,
# -108.941221,
# -108.5630812,
# -106.676839,
# -106.1898458,
# -105.6403126,
# -105.2431009,
# -105.0478486,
# -104.6745859,
# -104.503775,
# -72.99229,
# -97.149813,
# -97.418648,
# -96.304156,
# -95.546084,
# -86.553375,
# -116.391882,
# -115.831278,
# -115.352343,
# -115.179291,
# -114.710304,
# -114.517653,
# -114.246536,
# -113.595362,
# -113.487642,
# -113.400438,
# -113.257308,
# -112.363756,
# -112.506011,
# -112.919707,
# -113.205818,
# -113.399801,
# -113.455847,
# -115.374181,
# -115.558363,
# -115.8076,
# -115.956761,
# -116.127834,
# -118.401832,
# -122.503685,
# -122.5399,
# -122.511756,
# -123.056588,
# -123.297969,
# -123.384333,
# -123.324792,
# -123.357337,
# -123.038882,
# -92.911797,
# -77.957221,
# -77.436393,
# -122.078105,
# -120.465714,
# -120.336218,
# -119.922404,
# -119.490192,
# -118.351783,
# -118.181521,
# -118.022663,
# -117.347564,
# -117.592923,
# -117.398107,
# -117.285699,
# -117.193631,
# -117.063519,
# -116.507807,
# -115.09043,
# -114.440217,
# -114.440248,
# -112.905742,
# -112.648235,
# -112.253627,
# -109.982662,
# -109.678035,
# -108.941306,
# -108.771934,
# -108.56307,
# -106.676753,
# -106.440292,
# -106.189908,
# -105.640333,
# -105.433681,
# -105.243206,
# -105.047817,
# -104.674513,
# -104.503735,
# -103.252222,
# -89.020658,
# -82.097825,
# -97.519463,
# -85.515725,
# -85.658862,
# -85.799683,
# -112.065553,
# -112.534296,
# -112.22435,
# -84.728844,
# -117.738502,
# -108.995529,
# -108.328478,
# -107.632151,
# -107.065224,
# -105.782222,
# -105.627861,
# -105.351197,
# -105.081636,
# -104.549017,
# -104.29152,
# -104.029324,
# -103.570748,
# -102.869852,
# -102.364019,
# -101.948084,
# -100.290639,
# -88.455853,
# -108.606407,
# -108.046007,
# -108.303248,
# -107.89827,
# -107.725418,
# -107.546137,
# -107.148956,
# -106.97625,
# -106.794388,
# -105.084748,
# -104.408078,
# -99.592261,
# -98.076937,
# -97.910973,
# -97.747956,
# -97.420016,
# -82.464253,
# -78.1682,
# -78.8796449,
# -115.8076,
# -117.193631,
# -123.051314,
# -118.592392,
# -105.06571,
# -104.806993,
# -103.855028,
# -103.410014,
# -102.986494
# ]


#states = []
#geolocator = Nominatim(user_agent="airwaybeacons")
#for i in range(len(lats)):
#    state = geolocator.reverse(str(lats[i])+","+str(lons[i])).raw['address']['state']
#    states.append(state)

# states = ['Arizona', 'Arizona', 'Arizona', 'Arizona', 'Arizona', 'Arizona', 'Arizona', 'Arizona', 'Arizona', 'Arizona', 'Arizona', 'Arizona', 'Arizona', 'Arizona', 'Arizona', 'Arizona', 'Arizona', 'Arizona', 'Arizona', 'Arizona', 'Arizona', 'Arizona', 'Arizona', 'Arizona', 'Arizona', 'California', 'California', 'California', 'California', 'California', 'California', 'California', 'California', 'California', 'California', 'California', 'Connecticut', 'Idaho', 'Idaho', 'Idaho', 'Idaho', 'Idaho', 'Idaho', 'Kansas', 'Kansas', 'Kansas', 'Kansas', 'Minnesota', 'Nebraska', 'Nevada', 'Nevada', 'Nevada', 'Nevada', 'Nevada', 'Nevada', 'Nevada', 'Nevada', 'Nevada', 'Nevada', 'Nevada', 'Nevada', 'Nevada', 'Nevada', 'Nevada', 'Nevada', 'New Mexico', 'New Mexico', 'New Mexico', 'New Mexico', 'New Mexico', 'New Mexico', 'New Mexico', 'New Mexico', 'New Mexico', 'New Mexico', 'Texas', 'Texas', 'Texas', 'Texas', 'Texas', 'Texas', 'Texas', 'Texas', 'Texas', 'Texas', 'Utah', 'Utah', 'Utah', 'Utah', 'Utah', 'Wyoming', 'Wyoming', 'Wyoming', 'Wyoming', 'Wyoming', 'Wyoming', 'Wyoming', 'Wyoming', 'Wyoming', 'Wyoming', 'Connecticut', 'Oklahoma', 'Oklahoma', 'Kansas', 'Kansas', 'Tennessee', 'California', 'California', 'Nevada', 'Nevada', 'Nevada', 'Nevada', 'Nevada', 'Utah', 'Utah', 'Utah', 'Utah', 'Utah', 'Utah', 'Utah', 'Idaho', 'Idaho', 'Idaho', 'Idaho', 'Idaho', 'Idaho', 'Idaho', 'Idaho', 'Oregon', 'California', 'California', 'California', 'Oregon', 'Oregon', 'Oregon', 'Oregon', 'Oregon', 'Oregon', 'Minnesota', 'Pennsylvania', 'Pennsylvania', 'California', 'California', 'California', 'Nevada', 'Nevada', 'Nevada', 'Nevada', 'Nevada', 'Nevada', 'Nevada', 'Nevada', 'Nevada', 'Nevada', 'Nevada', 'Nevada', 'Nevada', 'Nevada', 'Nevada', 'Utah', 'Utah', 'Utah', 'Wyoming', 'Wyoming', 'Wyoming', 'Wyoming', 'Wyoming', 'Wyoming', 'Wyoming', 'Wyoming', 'Wyoming', 'Wyoming', 'Wyoming', 'Wyoming', 'Wyoming', 'Wyoming', 'Nebraska', 'Illinois', 'South Carolina', 'Texas', 'Indiana', 'Indiana', 'Indiana', 'Utah', 'Idaho', 'Idaho', 'Georgia', 'Washington', 'New Mexico', 'New Mexico', 'New Mexico', 'New Mexico', 'Texas', 'Texas', 'Texas', 'Texas', 'Texas', 'Texas', 'Texas', 'Texas', 'Texas', 'Texas', 'Texas', 'Texas', 'Mississippi', 'New Mexico', 'New Mexico', 'New Mexico', 'New Mexico', 'New Mexico', 'New Mexico', 'New Mexico', 'New Mexico', 'New Mexico', 'New Mexico', 'New Mexico', 'Oklahoma', 'Kansas', 'Kansas', 'Kansas', 'Kansas', 'Ohio', 'Pennsylvania', 'Pennsylvania', 'Idaho', 'Nevada', 'Oregon', 'Washington', 'New Mexico', 'New Mexico', 'New Mexico', 'New Mexico', 'Texas']   

# statename_to_abbr = {
#     # Other
#     'District of Columbia': 'DC',

#     # States
#     'Alabama': 'AL',
#     'Montana': 'MT',
#     'Alaska': 'AK',
#     'Nebraska': 'NE',
#     'Arizona': 'AZ',
#     'Nevada': 'NV',
#     'Arkansas': 'AR',
#     'New Hampshire': 'NH',
#     'California': 'CA',
#     'New Jersey': 'NJ',
#     'Colorado': 'CO',
#     'New Mexico': 'NM',
#     'Connecticut': 'CT',
#     'New York': 'NY',
#     'Delaware': 'DE',
#     'North Carolina': 'NC',
#     'Florida': 'FL',
#     'North Dakota': 'ND',
#     'Georgia': 'GA',
#     'Ohio': 'OH',
#     'Hawaii': 'HI',
#     'Oklahoma': 'OK',
#     'Idaho': 'ID',
#     'Oregon': 'OR',
#     'Illinois': 'IL',
#     'Pennsylvania': 'PA',
#     'Indiana': 'IN',
#     'Rhode Island': 'RI',
#     'Iowa': 'IA',
#     'South Carolina': 'SC',
#     'Kansas': 'KS',
#     'South Dakota': 'SD',
#     'Kentucky': 'KY',
#     'Tennessee': 'TN',
#     'Louisiana': 'LA',
#     'Texas': 'TX',
#     'Maine': 'ME',
#     'Utah': 'UT',
#     'Maryland': 'MD',
#     'Vermont': 'VT',
#     'Massachusetts': 'MA',
#     'Virginia': 'VA',
#     'Michigan': 'MI',
#     'Washington': 'WA',
#     'Minnesota': 'MN',
#     'West Virginia': 'WV',
#     'Mississippi': 'MS',
#     'Wisconsin': 'WI',
#     'Missouri': 'MO',
#     'Wyoming': 'WY',
# }


# for state in states:
#     print(statename_to_abbr[state])



#print(states)

