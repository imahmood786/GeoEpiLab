import numpy as np
import os
import geopandas as gpd
import pandas as pd
import plotly.express as px
import  plotly as py
import os

path = os.path.join(os.path.dirname(os.getcwd()), 'GeoEpiLab', 'VE', 'GIS','landuse.geojson')
LU = gpd.read_file(path)

land = LU[['PARCELNO', 'DOR_UC', 'PHY_ZIPCD', 'Shape_Leng', 'Shape_Area', 'geometry']]
land = land.to_crs("EPSG:3857")
land['x'] = land['geometry'].centroid.x
land['y'] = land['geometry'].centroid.y

house = ['000', '001', '002', '003', '004', '005', '006', '007', '008', '009', '012']
workplace = ['012', '017', '018', '019', '040', '041', '042', '043', '044', '045', '046', '047', '048', '049']
restaurant = ['021', '022', '033', '077']
worship = ['071', '076', '033']
grocery = ['011', '013', '014']
mall = ['015', '016']
school = ['072', '083', '084']
outdoor = ['020', '025', '026', '027', '028', '029', '030', '031', '032', '034', '035', '037', '038', '039', '082', '097']
bank = ['023', '024']
C = ['000', '001', '002', '003', '004', '005', '006', '007', '008', '009', '010', '011', '012', '013', '014', '015', '016', '017', '018', '019', '020', '021', '022', '023', '024', '025', '026', '027', '028', '029', '030', '031', '032', '033', '034', '035', '036', '037', '038', '039', '040', '041', '042', '043', '044', '045', '046', '047', '048', '049', '050', '051', '052', '053', '054', '055', '056', '057', '058', '059', '060', '061', '062', '063', '064', '065', '066', '067', '068', '069', '070', '071', '072', '073', '074', '075', '076', '077', '078', '079', '080', '081', '082', '083', '084', '085', '086', '087', '088', '089', '090', '091', '092', '093', '094', '095', '096', '097', '098', '099']
D = house + workplace + restaurant + worship + grocery + mall + outdoor + bank
other = [x for x in C if not x in D or D.remove(x)]

houses = land[land["DOR_UC"].isin(house)]
houses['type'] = 'house'

workplaces = land[land["DOR_UC"].isin(workplace)]
workplaces['type'] = 'workplaces'

restaurants = land[land["DOR_UC"].isin(restaurant)]
restaurants['type'] = 'restaurants'

worship_places = land[land["DOR_UC"].isin(worship)]
worship_places['type'] = 'worship_places'

grocery_places = land[land["DOR_UC"].isin(grocery)]
grocery_places['type'] = 'grocery_places'

malls = land[land["DOR_UC"].isin(mall)]
malls['type'] = 'malls'

schools = land[land["DOR_UC"].isin(school)]
schools['type'] = 'schools'

outdoors = land[land["DOR_UC"].isin(outdoor)]
outdoors['type'] = 'outdoors'

banks = land[land["DOR_UC"].isin(bank)]
banks['type'] = 'banks'

others = land[land["DOR_UC"].isin(other)]
others['type'] = 'others'

list = [houses, workplaces, restaurants, worship_places, grocery_places, malls, schools, outdoors, banks, others]

df = pd.DataFrame()
df = pd.concat(list)

print(df.columns)
# df.to_file(os.path.dirname(os.getcwd()), 'GeoEpiLab', 'VE', 'GIS','locationgraph.geojson', driver="GeoJSON")
df.to_file(os.path.join(os.path.dirname(os.getcwd()), 'GeoEpiLab', 'VE', 'GIS','landuse.geojson'), driver="GeoJSON")
# # land = land.sort_values(by=['DOR_UC'])
# fig = px.scatter_mapbox(df, lat="y", lon="x",
#                         color_discrete_sequence=px.colors.qualitative.G10,
#                         color="type",
#                         hover_name='PARCELNO',
#                         zoom=10)
# fig.update_layout(mapbox_style="open-street-map", title= "Hillsborough" + ' Location Graph', width=1000, height=800, legend=dict(x=0, y=0, orientation ="h"))
# # fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
# py.offline.plot(fig, filename= "Pointcloud.html")
# fig.show()