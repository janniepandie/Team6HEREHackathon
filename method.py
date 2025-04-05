import json
import math
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from itertools import cycle

def validate_topology(topology_list):
    """
    Process topology list according to validation rules:
    1. If associated topology is motorway and pedestrian=True, correct pedestrian to False
    2. If associated topology ismotorway=False, find nearby motorway topology
    3. If no nearby motorway found, check probe data for pedestrians
    """
    
    # Case 3: Correct pedestrian flag for motorway segments
    for topo in topology_list:
        if topo['asscoiate'] and topo['ismotorway']:
            return 3 ,(f"Case 3: Corrected pedestrian to False for motorway segment {topo['topoid']}")
    
    # Case 2: Find nearby motorway for non-motorway segments
    for topo in topology_list:
        if topo['ismotorway'] and not topo['pedestrian']:
            return 2, (f"Case 2: Associated with the wrong road. The correct road {topo['topoid']}")
    
    return 4, 'correct association, correct attribution'

def find_matching_range_speedlimit(target_value, range_list):
    if range_list == None:
        return False
    for item in range_list:
        start = item['range']['startOffset']
        end = item['range']['endOffset']
        if start <= target_value <= end:
            return item['isUnlimited'] or item['valueKph'] >= 100
    return None 

def find_matching_range(target_value, range_list):
    if range_list == None:
        return False
    for item in range_list:
        start = item['range']['startOffset']
        end = item['range']['endOffset']
        if start <= target_value <= end:
            return item['value']
    return None 

from math import radians, cos, sin, asin, sqrt

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great-circle distance in meters between two points 
    on the Earth (specified in decimal degrees)
    """
    # Convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    
    # Haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    
    # Radius of Earth in meters (mean radius = 6,371km)
    r = 6371000
    return c * r

def filter_by_radius(df, ref_lat, ref_lon, radius_m=5.0,max_speed = 10):
    """
    Filters DataFrame to rows within a specified radius (km) of a reference point.
    
    Args:
        df: DataFrame with 'latitude' and 'longitude' columns
        ref_lat: Reference latitude (center point)
        ref_lon: Reference longitude (center point)
        radius_km: Radius in meter
        
    Returns:
        Filtered DataFrame with added 'distance_m' column
    """
    # Calculate distance for each row
    low_speed_df = df[df['speed'] < max_speed].copy()
    
    # Calculate distance for remaining points
    low_speed_df['distance_km'] = low_speed_df.apply(
        lambda row: haversine(ref_lat, ref_lon, row['latitude'], row['longitude']),
        axis=1
    )
    
    # Filter rows within radius
    filtered_df = low_speed_df[low_speed_df['distance_km'] <= radius_m].copy()
    
    return filtered_df

def coordcheck(c1s,c2,distance_threshold):
    for c1 in c1s:
        distance = haversine(c1[0],c1[1],c2[0],c2[1])
        if distance < distance_threshold:
            return [True, [c1[0],c1[1]]]
    return [False, []]

def solution(caseid):
    prefix = 'data_set/'+ caseid + '/' + caseid
    with open(prefix +'_validations.geojson', 'r') as f:
        geojson_data = json.load(f)
    with open(prefix +'_full_topology_data.geojson', 'r') as f:
        topojson_data = json.load(f)
    with open(prefix +'_signs.geojson', 'r') as f:
        signjson_data = json.load(f)

    probedf = pd.read_csv(prefix +'_probe_data.csv')
    res = []
    for i in range(0,len(geojson_data['features'])):
        resultdict = {}
        resultdict['Violation ID'] = geojson_data['features'][i]['properties']['Violation ID']
        resultdict['coordinates'] = geojson_data['features'][i]['geometry']['coordinates']
        case, message = solutionhelper(geojson_data,signjson_data,topojson_data,probedf,i)
        resultdict['scenario'] = case
        resultdict['message'] = message
        res.append(resultdict)
    return res

def solutionhelper(geojson_data,signjson_data,topojson_data,probedf,i):
    signid = geojson_data['features'][i]['properties']['Feature ID']
    ermes = geojson_data['features'][i]['properties']['Error Message']
    violationid = str(geojson_data['features'][i]['properties']['Partition ID']) + str(i)
    topo = re.search(r'urn:here::here:Topology:(\d+)', ermes).group(0)
    for j in range(0,len(signjson_data['features'])):
        c2 = signjson_data['features'][j]['properties']['id']
        if signjson_data['features'][j]['properties']['signType'] == 'MOTORWAY' and signid == c2:
            score_dict = signjson_data['features'][j]['properties']['confidence']['simpleScores'][0]
            existingscore = score_dict.get('existenceProbability', score_dict.get('score', None))
            observedict = signjson_data['features'][j]['properties']['observationCounts']
            observescore = int(observedict['NInputsObserved'])/int(observedict['NInputsObservable'])
    for x in range(0,len(topojson_data['features'])):
        c3 = topojson_data['features'][x]['properties']['id']
        if topo == c3:
            asscoiatedtopo = topojson_data['features'][x]
            asscoiatedindex = x

    signcord = geojson_data['features'][0]['geometry']['coordinates']

    color_cycle = cycle(['red', 'green', 'blue', 'orange', 'purple', 'cyan'])
    asscoiatecond, coord = coordcheck(asscoiatedtopo['geometry']['coordinates'],signcord,20)
    allpossibledict = []
    if existingscore < 0.5 and observescore<0.5:
        return 1, 'sign do not exsit since both existingscore and observescore are below 0.5'
    else:
        for i in range(0,len(topojson_data['features'])):
            condition, coord = coordcheck(topojson_data['features'][i]['geometry']['coordinates'],signcord,20)
            if condition:
                possibledict = {'asscoiate':False}
                temptopo = topojson_data['features'][i]
                if i == asscoiatedindex:
                    possibledict['asscoiate'] = True
                possibledict['index'] = i
                possibledict['pedestrian'] = temptopo['properties']['accessCharacteristics'][0]['pedestrian']
                # print(temptopo['properties']['accessCharacteristics'][0]['pedestrian'])
                coordinates = temptopo['geometry']['coordinates']

                totaldis = 0
                dis=0
                for c in range(1,len(coordinates)):
                    totaldis += haversine(coordinates[c-1][0], coordinates[c-1][1], coordinates[c][0], coordinates[c][1])
                    if coord == coordinates[c]:
                        dis = totaldis
                offsetindex = dis/totaldis

                ranges = temptopo['properties']['topologyCharacteristics']['isMotorway']
                speedlimitrange = temptopo['properties']['speedLimit']
                result = find_matching_range(offsetindex, ranges)
                speedlimithw = find_matching_range_speedlimit(offsetindex,speedlimitrange)
                # print(speedlimithw)
                filtered_probedf= filter_by_radius(probedf,coord[1],coord[0],20,10)
                # print(not (filtered_probedf['speed'] < 10).any())
                # print(result)
                possibledict['ismotorway'] = result or not (filtered_probedf['speed'] < 10).any() or speedlimithw
                possibledict['topoid'] = temptopo['properties']['id']
                x, y = zip(*coordinates)  # Unpack tuples into two lists
                allpossibledict.append(possibledict)
                # Plot
                plt.plot(x, y, 
                        color=next(color_cycle),
                        marker='o',      # Add markers at each point
                        linestyle='-',   # Solid line
                        linewidth=2,     # Thicker line
                        markersize=5,    # Size of markers
                        label='Path'+str(i))




        coordinates = asscoiatedtopo['geometry']['coordinates']
        x, y = zip(*coordinates)
        plt.plot(x, y, 
                        color='yellow', 
                        marker='o',      # Add markers at each point
                        linestyle='-',   # Solid line
                        linewidth=2,     # Thicker line
                        markersize=5,    # Size of markers
                        label='asscoiated')
        plt.plot(signcord[0],signcord[1],color='black',marker='o')
        # Customize the plot
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.title('Line Plot of Coordinates')
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend()
        plt.tight_layout()
        pngname = 'plot'+violationid+'.png'
        plt.savefig(pngname)
        plt.clf()

        return validate_topology(allpossibledict)
# cases = ['23608578','23608580','23608592','23612004','23612006','23612035']
# # for c in cases:
# #     print(solution(c))
