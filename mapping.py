import geopandas as gpd
import pyproj
import streamlit as st
import smart_open
from shapely.ops import cascaded_union

class Mapper:

    def __init__(self):

        # aws_key = st.secrets['AWS_ACCESS_KEY_ID']
        # aws_secret = st.secrets['AWS_SECRET_ACCESS_KEY']
        aws_key = "AKIAYK4RUY66NFIIHU4U"
        aws_secret = "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"

        GEO_FILE = 'full_new.geojson'
        BUCKET = 'neighborhoodscout'

        geo_path = 's3://{}:{}@{}/{}'.format(aws_key, aws_secret, BUCKET, GEO_FILE)

        self.data = gpd.read_file(smart_open.smart_open(geo_path))
        self.data.to_crs(pyproj.CRS.from_epsg(4326), inplace=True)

        self.city_groups = self.data.groupby('city').aggregate({'geometry': list}).reset_index()
        self.city_groups['union'] = self.city_groups['geometry'].apply(lambda x: cascaded_union(x))
        self.city_groups = self.city_groups.drop('geometry', axis=1).rename(columns={'union': 'geometry'})
