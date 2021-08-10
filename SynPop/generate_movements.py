import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd
import numpy as np
import Utility.functions as fun
import matplotlib
import plotly.express as px
import os


def get_category(self, age):
    category = ""
    if age < 3:
        cateogry = 'infant'
    elif age >= 3 and age <= 12:
        category = 'child'
    elif age >= 13 and age < 19:
        category = 'teen'
    elif age >= 18 and age < 60:
        category = 'adult'
    else:
        category = 'senior'
    return category

pop = pd.read_csv(os.path.join(os.getcwd(), 'SynPop', 'hillsborough_pop33612.csv'))
pop = pop.sample(frac=1)

LG = gpd.read_file(os.path.join(os.path.dirname(os.getcwd()), 'GeoEpiLab', 'VE', 'GIS','location_graph33612.geojson'))
LG = LG.to_crs("EPSG:3857")

houses = LG[LG['type']=='house']
schools = LG[LG['type'] == 'schools']
work_places = LG[LG['type'] == 'workplace']
community_places = LG[LG['type'] == 'community']

