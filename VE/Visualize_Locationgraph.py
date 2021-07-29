import numpy as np
import os
import geopandas as gpd
import plotly.express as px
import  plotly as py

LG = gpd.read_file(os.path.join(os.getcwd(), 'SimulationEngine', 'GIS', 'hillsborough_LG.geojson'))

fig = px.scatter_mapbox(LG, lat="y", lon="x",
                        color_discrete_sequence=px.colors.qualitative.G10,
                        color="type",
                        hover_name='id',
                        zoom=10)
fig.update_layout(mapbox_style="open-street-map", title= "Hillsborough" + ' Location Graph', width=1000, height=800, legend=dict(x=0, y=0, orientation ="h"))
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
py.offline.plot(fig, filename= "Pointcloud.html")
fig.show()
