"""
demo.py
Spring 2022 PJW

Demonstrate use of Voronoi polygons and nearest feature
calculations. Requires QGIS for some operations.
"""

import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import os

plt.rcParams['figure.dpi'] = 300

out_file = 'demo-output.gpkg'

#
#  Set up the store input file, the CRS used by the store file,
#  which is WGS 84, and the CRS that will be used for projected
#  data, which is UTM 18N
#

store_file = 'Retail_Food_Stores.csv'

wgs84 = 4326
utm18n = 26918

#
#  Read the store file, filter down to Onondaga County, and
#  filter out records with no coordinates
#

raw = pd.read_csv(store_file)

trim = raw.query("County == 'Onondaga'")
trim = trim.dropna(subset='Georeference').copy()

#%%
#
#  Filter store data down to large stores
#

big_stores = [
    'ALDI',
    'BJS WHOLESALE',
    'COSTCO',
    'PRICE CHOPPER',
    'TARGET',
    'TOPS',
    'TRADER JOES',
    'WAL-MART',
    'WALMART',
    'WEGMANS'
    ]

trim['big'] = False

for store in big_stores:

    is_big = trim['DBA Name'].str.startswith(store)
    is_gas = trim['DBA Name'].str.contains('XPRESS')

    this_store = (is_big == True) & (is_gas == False)

    trim['big'] = trim['big'] | this_store

big = trim[ trim['big'] ]

#%%
#
#  Now build a GeoSeries from the georeference column,
#  which uses the Well-Known Text representation of
#  store coordinates. Then build a full GeoDataFrame
#  using it.
#

coords = gpd.GeoSeries.from_wkt(big['Georeference'])

data_only = big.drop(columns='Georeference')
geo = gpd.GeoDataFrame( data=data_only, geometry=coords, crs=wgs84)

#
#  Now convert the data to UTM 18N
#

geo = geo.to_crs(utm18n)

#%%
#
#  Load the county and city polygons for convenience, then plot
#  a figure
#

county = gpd.read_file('demo.gpkg',layer='county')
syr = gpd.read_file('demo.gpkg',layer='city')

fig,ax1 = plt.subplots()
county.plot(color='gray',ax=ax1)
syr.plot(color='tan',ax=ax1)
geo.plot(color='blue',markersize=1,ax=ax1)
ax1.axis('off')

#%%
#
#  Build a geopackage for use with QGIS in building Voronoi
#  polygons. Start by removing any existing version of the
#  output file, then write the layers.
#

if os.path.exists(out_file):
    os.remove(out_file)

county.to_file(out_file,layer='county')
syr.to_file(out_file,layer='city')
geo.to_file(out_file,layer='stores')

#%%
#
#  Copy a couple of other layers across that will be convenient
#  in demonstrating features of QGIS. Also, build a layer
#  of tract centroids in the process.
#

roads = gpd.read_file('demo.gpkg',layer='roads')
roads.to_file(out_file,layer='roads')

tracts = gpd.read_file('demo.gpkg',layer='tracts')
tracts.to_file(out_file,layer='tracts')

centroids = tracts.copy()
centroids['geometry'] = tracts.centroid
centroids.to_file(out_file,layer='centroids')

#%%
#
#  Find the distance from each tract centroid to the nearest store.
#

served_by = centroids.sjoin_nearest(geo,how='left',distance_col='dist')

#
#  What tracts does each serve?
#

grouped = served_by.groupby(['DBA Name','Street Number','Street Name'])

serves = grouped.size()
print( serves.sort_values(ascending=False).head(10) )

#
#  Now join the distance onto the tracts for plotting.
#

dist_to_store = served_by[['GEOID','dist']]

tracts = tracts.merge(dist_to_store,on='GEOID',validate='1:1',indicator=True)
print( tracts['_merge'].value_counts() )
tracts = tracts.drop(columns='_merge')

fig,ax1 = plt.subplots()
tracts.plot('dist',ax=ax1,legend=True)
geo.plot(color='red',markersize=0.5,ax=ax1)
ax1.axis('off')
fig.tight_layout()
