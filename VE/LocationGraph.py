# Import libraries
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from matplotlib.colors import ListedColormap
import geopandas as gpd
import plotly.express as px
import  plotly as py

# flordia_state = gpd.read_file('./florida/gis_osm_buildings_a_free_1.shp')
hillsborough = gpd.read_file('hillsborough.shp')
zipcodes = gpd.read_file('Zip_Codes.geojson')

LG = gpd.sjoin(hillsborough, zipcodes, how="inner", op='intersects')
LG = LG[LG['Zip_Code']=='33612']
LG =  LG[['osm_id', 'code', 'fclass', 'name', 'type', 'Zip_Code', 'Name', 'Shape__Area', 'geometry']]
groups = LG.groupby('type')
for name,group in groups:
    print(name, group.size)

LG.loc[(LG['type'] == 'apartments'),'type']='house'
LG.loc[(LG['type'] == 'detached'),'type']='house'
LG.loc[(LG['type'] == 'dormitory'),'type']='house'
LG.loc[(LG['type'] == 'house'),'type']='house'
LG.loc[(LG['type'] == 'hut'),'type']='house'
LG.loc[(LG['type'] == 'residential'),'type']='house'


LG.loc[(LG['type'] == 'commercial'),'type']='office'
LG.loc[(LG['type'] == 'construction'),'type']='office'
LG.loc[(LG['type'] == 'farm_auxiliary'),'type']='office'
LG.loc[(LG['type'] == 'garage'),'type']='office'
LG.loc[(LG['type'] == 'garages'),'type']='office'
LG.loc[(LG['type'] == 'industrial'),'type']='office'
LG.loc[(LG['type'] == 'office'),'type']='office'
LG.loc[(LG['type'] == 'post_office'),'type']='office'
LG.loc[(LG['type'] == 'service'),'type']='office'
LG.loc[(LG['type'] == 'train_station'),'type']='office'
LG.loc[(LG['type'] == 'yes;office'),'type']='office'
LG.loc[(LG['type'] == 'warehouse'),'type']='office'

LG.loc[(LG['type'] == 'college'),'type']='school'
LG.loc[(LG['type'] == 'kindergarten'),'type']='school'
LG.loc[(LG['type'] == 'school'),'type']='school'
LG.loc[(LG['type'] == 'university'),'type']='school'

LG.loc[(LG['type'] == 'church'),'type']='leisure'
LG.loc[(LG['type'] == 'public'),'type']='leisure'
LG.loc[(LG['type'] == 'stadium'),'type']='leisure'
LG.loc[(LG['type'] == 'barn'),'type']='leisure'

LG.loc[(LG['type'] == 'mall'),'type']='shops'
LG.loc[(LG['type'] == 'supermarket'),'type']='shops'
LG.loc[(LG['type'] == 'retail'),'type']='shops'

LG['type'].fillna('house', inplace=True)

groups = LG.groupby('type')
for name,group in groups:
    print(name, group.size)
# LG.to_file("output.geojson", driver="GeoJSON")

LG['x'] = LG['geometry'].centroid.x
LG['y'] = LG['geometry'].centroid.y

fig = px.scatter_mapbox(LG, lat="y", lon="x",
                        color_discrete_sequence=px.colors.qualitative.G10,
                        color="type",
                        zoom=10)
fig.update_layout(mapbox_style="open-street-map", title= "Hillsborough" + ' Location Graph', width=1000, height=800, legend=dict(x=0, y=0, orientation ="h"))
# fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
py.offline.plot(fig, filename= "Pointcloud.html")
# fig.write_image(os.getcwd() +"\\" + borough + ".png",  width=1024, height=768, scale=1)
fig.show()