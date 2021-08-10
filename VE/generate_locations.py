from pyrosm import OSM
from pyrosm import get_data
import geopandas
import numpy as np
import os
import matplotlib.pyplot as plt
from pyrosm.data import sources
import pyrosm
from shapely import geometry
from shapely.geometry import Polygon
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import plotly.express as px
import  plotly as py
from urllib.request import urlopen
import json
import pandas as pd
import folium
import sys
import xml.etree.ElementTree as ET
import pyproj
from shapely import ops
from functools import partial
from shapely.geometry import Polygon, Point

path = os.getcwd()
# Get County boundary in Geojson
# boundary = gpd.read_file(os.path.join(path, 'VE', 'GIS','County_Boundary.geojson'))
boundary = gpd.read_file(os.path.join(path, 'VE', 'GIS','Zip_Codes2.geojson'))
poly = boundary[(boundary['Zip_Code'] == '33612')].iloc[0].geometry
poly = boundary.iloc[0].geometry

osm = pyrosm.OSM(os.path.join(path, 'VE', 'GIS','florida-latest.osm.pbf'), bounding_box=poly)
buildings = osm.get_buildings()

buildings_yes = buildings.loc[(buildings['building'] == 'yes')]
# This code is to mark yes locations with random sampling
house_rand = buildings_yes.sample(frac = 0.75)
buildings_yes = buildings_yes.drop(house_rand.index)

#remaining 70% (out of 25%) to work
work_rand = buildings_yes.sample(frac = 0.70)
buildings_yes = buildings_yes.drop(work_rand.index)

#remaining 30% to community
community_rand = buildings_yes #remaining rows
buildings_yes = buildings_yes.drop(community_rand.index)

house_rand['type'] = 'house'
work_rand['type'] = 'workplace'
community_rand['type'] = 'community'

# Reading houses [Ref: https://wiki.openstreetmap.org/wiki/Buildings#Accommodation]
house_filter = {"building": ['apartments', 'bungalow', 'cabin', 'hut', 'detached', 'dormitory', 'farm', 'ger', 'hotel', 'house', 'houseboat',
                             'residential', 'semidetached_house', 'static_caravan', 'terrace']}

work_filter = {"building": ['commercial', 'construction', 'farm_auxiliary', 'government', 'garage', 'garages', 'industrial', 'kiosk',
                            'office', 'post_office', 'service', 'train_station', 'yes;office', 'warehouse']}

community_filter = {"building": ['cathedral', 'chapel', 'church', 'monastery', 'mosque', 'presbytery', 'religious', 'shrine', 'synagogue', 'temple',
                                 'civic', 'government', 'hospital', 'public', 'toilets', 'train_station', 'transportation', 'barn', 'conservatory',
                                 'cowshed', 'farm_auxiliary', 'greenhouse', 'slurry_tank', 'stable', 'sty', 'grandstand', 'pavilion', 'riding_hall',
                                 'sports_hall', 'stadium', 'Storage', 'hangar', 'hut', 'shed', 'carport', 'garage', 'garages', 'parking', 'service',
                                 'marquee', 'gatehouse', 'roof'],
                    "Shop": True,
                    "Amenity": ['bar', 'biergarten', 'cafe', 'fast_food', 'food_court', 'ice_cream', 'pub', 'restaurant',
                                'bus_station', 'car_sharing', 'ferry_terminal', 'fuel', 'parking',
                                'atm', 'bank', 'Healthcare', 'clinic', 'dentist', 'doctors', 'hospital', 'nursing_home', 'pharmacy',
                                'social_facility', 'veterinary', 'arts_centre', 'brothel', 'casino', 'cinema', 'community_centre',
                                'conference_centre', 'events_venue', 'gambling', 'love_hotel', 'nightclub', 'planetarium', 'public_bookcase',
                                'social_centre', 'stripclub', 'studio', 'swingerclub', 'theatre', 'Public Service', 'courthouse', 'embassy',
                                'fire_station', 'police', 'post_box', 'post_depot', 'post_office', 'prison', 'ranger_station', 'townhall',
                                'bbq', 'bench', 'dog_toilet', 'drinking_water', 'give_box', 'shelter', 'shower', 'telephone', 'toilets',
                                'sanitary_dump_station', 'recycling', 'waste_basket', 'waste_disposal', 'waste_transfer_station',
                                'childcare', 'clock', 'crematorium', 'dive_centre', 'funeral_hall', 'grave_yard', 'gym', 'hunting_stand',
                                'internet_cafe', 'kitchen', 'kneipp_water_cure', 'lounger', 'marketplace', 'monastery', 'photo_booth',
                                'place_of_mourning', 'place_of_worship', 'public_bath', 'public_building', 'refugee_site', 'vending_machine'
                                ]}
school_filter = {"building": ['kindergarten', 'school', 'university', 'college'],
                 "Amenity": ['college', 'driving_school', 'kindergarten', 'language_school', 'library', 'music_school', 'school', 'university']}

houses = osm.get_buildings(custom_filter=house_filter)
workplaces = osm.get_buildings(custom_filter=work_filter)
communityplaces = osm.get_buildings(custom_filter=community_filter)
schools = osm.get_buildings(custom_filter=school_filter)

houses['type'] = 'house'
workplaces['type'] = 'workplace'
communityplaces['type'] = 'community'
schools['type'] = 'school'

places = [houses, workplaces, communityplaces, schools, house_rand,  work_rand, community_rand]

LG = pd.concat(places)
print(len(LG))
# LG['x'] = LG['geometry'].centroid.x
# LG['y'] = LG['geometry'].centroid.y


# buildings['x'] = buildings['geometry'].centroid.x
# buildings['y'] = buildings['geometry'].centroid.y
# fig = px.scatter_mapbox(LG2, lat="y", lon="x",
#                         color_discrete_sequence=px.colors.qualitative.G10,
#                         color="type",
#                         hover_name='id',
#                         zoom=10)
# fig.update_layout(mapbox_style="open-street-map", title= "Hillsborough" + ' Location Graph', width=1000, height=800, legend=dict(x=0, y=0, orientation ="h"))
# # fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
# py.offline.plot(fig, filename= "Pointcloud.html")
# fig.write_image(os.getcwd() +"\\" + borough + ".png",  width=1024, height=768, scale=1)
# fig.show()

LG.drop_duplicates(subset=['id'],keep = False, inplace = True)
LG.duplicated(subset='id', keep='first').sum()
print(LG.columns)
# LG = LG[[]]
LG.to_file(os.path.join(path, 'VE', '../SimulationEngine/GIS/hillsborough_LG_33612.geojson'), driver="GeoJSON")
# LG.to_csv(os.path.join(path, 'VE', '../SimulationEngine/GIS/hillsborough_LG.csv'))
print(len(LG[LG['type']=='house']))
print(len(LG[LG['type']=='workplace']))
print(len(LG[LG['type']=='community']))
print(len(LG[LG['type']=='school']))