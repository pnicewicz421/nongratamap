# Purpose: convert csv to geojson file
# take the latitude and longitude columns in a csv file and encode as a Feature Point with coordinates in geojson format
# additionally, convert the other columns in the csv file to properties of the feature
# 
# used with converting criminalization events in csv format to geojson for visualization  

import pandas as pd
import numpy as np

def df_to_geojson(df, properties, lat='latitude', lon='longitude'):
    # create a new python dict to contain our geojson data, using geojson format
    geojson = {'type':'FeatureCollection', "name": "crim_data", "crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:OGC:1.3:CRS84" } },'features':[]}

    # loop through each row in the dataframe and convert each row to geojson format
    for _, row in df.iterrows():
        # create a feature template to fill in
        feature = {'type':'Feature',
                   'properties':{},
                   'geometry':{'type':'Point',
                               'coordinates':[]}}

        # fill in the coordinates
        feature['geometry']['coordinates'] = [row[lon],row[lat]]

        # for each column, get the value and add it as a new feature property
        for prop in properties:
            feature['properties'][prop] = row[prop]
        
        # add this feature (aka, converted dataframe row) to the list of features inside our dict
        geojson['features'].append(feature)
    
    return geojson

data = pd.read_csv('crim_data_with_state.csv')
data = data.replace(np.nan, '', regex=True)
geojson = df_to_geojson(data, data.columns)
eventDataScript = 'var eventData = ' + str(geojson)

eventDataFile = open("eventData.js", "w", encoding="utf-8")
eventDataFile.write(eventDataScript)
eventDataFile.close()

