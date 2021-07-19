import geopandas as gpd
import os
import matplotlib.pyplot as plt


# Filepath to the addresses Shapefile
fp = os.path.join(os.getcwd(),'SimulationEngine', 'shape', 'County_Boundary.shp')
data = gpd.read_file(fp)
data.crs
print(data['geometry'].head())
data_proj = data.copy()
data_proj['geometry'] = data_proj['geometry'].to_crs(epsg=3857)

print(data_proj['geometry'].head())
