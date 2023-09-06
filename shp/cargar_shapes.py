from geo.Geoserver import Geoserver
import os
import glob
import zipfile
import geopandas as gpd
from sqlalchemy import *
from geoalchemy2 import Geometry, WKTElement

epsg=32719



# # For creating workspace
# #geo.create_workspace(workspace='demo1')

# # For uploading raster data to the geoserver
# #geo.create_coveragestore(layer_name='layer1', path=r'path\to\raster\file.tif', workspace='demo')

# # For creating postGIS connection and publish postGIS table
# geo.create_featurestore(store_name='geo_data', workspace='demo', db='postgres', host='localhost', pg_user='postgres',
#                         pg_password='admin')
# geo.publish_featurestore(workspace='demo', store_name='geo_data', pg_table='geodata_table_name')

# # For uploading SLD file and connect it with layer
# geo.upload_style(path=r'path\to\sld\file.sld', workspace='demo')
# geo.publish_style(layer_name='geoserver_layer_name', style_name='sld_file_name', workspace='demo')

# # For creating the style file for raster data dynamically and connect it with layer
# geo.create_coveragestyle(raster_path=r'path\to\raster\file.tiff', style_name='style_1', workspace='demo',
#                          color_ramp='RdYiGn')
# geo.publish_style(layer_name='geoserver_layer_name', style_name='raster_file_name', workspace='demo')

# # delete workspace
# geo.delete_workspace(workspace='demo')

# # delete layer
# geo.delete_layer(layer_name='agri_final_proj', workspace='demo')

# # delete style file
# geo.delete_style(style_name='kamal2', workspace='demo')

file = './capas/capa.zip'
file_format = os.path.basename(file).split('.')[-1]
file_name = os.path.basename(file).split('.')[0]
file_path = os.path.dirname(file)
nombre_capa = file_name

# SERver BD AWS Colcapirhua
conn_str = 'postgresql://postgres:acer56xxx@52.86.173.62:5432/ide_produccion'

print (file, 'archivo')
print (file_name)
print (file_path)

#extraer zip
with zipfile.ZipFile(file, 'r') as zip_ref:
    zip_ref.extractall(file_path)

os.remove (file)

shp = glob.glob(r'{}/**/*.shp'.format(file_path), recursive=True)[0] # obtener shp
print('---------------------')
print (shp, 'shape')
print('---------------------')

gdf = gpd.read_file(shp)


geom_type = gdf.geom_type[1]
print('----------GDF--------------')
print (gdf)
print('---------------------------')

engine = create_engine(conn_str) # crea  el SSQL Alchemy engine
gdf['geom'] = gdf['geometry'].apply (lambda x: WKTElement(x.wkt, srid=epsg)) ###### creamos nueva columna geom desde columna geometry
gdf.drop(axis='columns', columns=['geometry'], inplace = True)  #drop  the geometry column (since we already backup this column with geom)

print('----------GDF--------------')
print (gdf)
print('---------------------------')

##################################### REGISTRO EN BD POSTGIS ###############################################
gdf.to_sql(nombre_capa, engine, 'public', if_exists='replace', 
            index=false, dtype={'geom': Geometry('Geometry', srid=epsg)}) # post into  a postgres
############################################################################################################

###########################  Publicacion geoserver AWS Colcapirhua #########################################
# geo.create_featurestore(store_name='BDColcapirhuaTest', workspace='Colcapirhua', db='ide_produccion', host='52.86.173.62', pg_user='postgres',
#                    pg_password='acer56xxx', schema='public')
# geo.publish_featurestore(workspace='Colcapirhua', store_name='BDColcapirhuaTest', pg_table=nombre_capa)

geo = Geoserver('http://3.217.17.20:8080/geoserver', username='admin', password='4OYD7uX4a$h313Ry')
sql = 'SELECT * FROM ' + nombre_capa
geo.publish_featurestore_sqlview(store_name='BDColcapirhuaTest', name=nombre_capa, sql=sql, srid=epsg, workspace='Colcapirhua')

# geo.create_outline_featurestyle('estilo1',color='#3579b1', workspace='Colcapirhua')
# #geo.create_catagorized_featurestyle(style_name='categorizado', column_name='RSRP',column_distinct_values=[-120, -110, -105, -100, -94, -86,-80, -50, null],  workspace='nuevatel')
# #geo.create_classified_featurestyle(style_name='clasificado', column_name='SECTOR_ID', column_distinct_values=[1,2,3,4,5,6,7], workspace='nuevatel')
# geo.publish_style(layer_name=nombre_capa, style_name='estilo1', workspace='Colcapirhua')
############################################################################################################

