import json
import math
import re
import numpy as np
import pandas as pd
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

def filter_by_bounding_box(df, ref_lat, ref_lon, lat_offset=0.05, lon_offset=0.05):
    """
    Filters DataFrame to rows within a bounding box around a reference point.
    
    Args:
        df: DataFrame with 'latitude' and 'longitude' columns
        ref_lat: Reference latitude (center point)
        ref_lon: Reference longitude (center point)
        lat_offset: ± degrees latitude (default: ±0.05)
        lon_offset: ± degrees longitude (default: ±0.05)
        
    Returns:
        Filtered DataFrame
    """
    # Define bounding box
    min_lat = ref_lat - lat_offset
    max_lat = ref_lat + lat_offset
    min_lon = ref_lon - lon_offset
    max_lon = ref_lon + lon_offset
    
    # Filter rows within the box
    filtered_df = df[
        (df['latitude'].between(min_lat, max_lat)) & 
        (df['longitude'].between(min_lon, max_lon))
    ]
    
    return filtered_df

def coordcheck(c1s,c2,distance_threshold):
    for c1 in c1s:
        distance = haversine(c1[0],c1[1],c2[0],c2[1])
        if distance < distance_threshold:
            return [True, [c1[0],c2[0]]]
    return [False, []]