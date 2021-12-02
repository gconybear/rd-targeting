import streamlit as st
import pandas as pd
import numpy as np
from geocoding import parse_address_string
from helpers import slider_printout
from valid_cols import VALID_COLS
from metric_means import MEANS
from mapping import Mapper
import geopandas as gpd
import pyproj

import folium
from folium import Marker
from folium.plugins import MarkerCluster
from zscore_slider_vals import SLIDER_Z_SCORES

TILES = {
    'cartodbdark_matter': 'cartodbdark_matter',
    'cartodbpositron': 'cartodbpositron',
    'OpenStreetMap': 'OpenStreetMap',
    'Stamen Toner': 'Stamen Toner',
    'Stamen Terrain': 'Stamen Terrain',
    # 'stadia': 'https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png'
}

# these are the default z score slider settings
LOW_Z = -3.0
UPPER_Z = 3.0

st.set_page_config(layout='centered', page_icon='🎯')

@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

@st.cache
def get_data():

    return pd.read_csv('data/dat.csv'), Mapper()

df, mapper = get_data()
DISPLAY_COLS = [x for x in df.columns if x != 'Unnamed: 0']

def blank(): return st.text("")


def main():



    st.title("Targeting App")

    blank()


    with st.form(key='form'):

        st.markdown("**Cluster 1 Filter**")
        blank()
        # c1_col, c2_col= st.columns(2)
        c1 = st.slider(
            'minimum average cluster 1 probability',
            min_value=0.0,
            max_value=1.0,
            value=0.5,
            step=0.025
            )

        num_neighborhoods = st.slider(
            'minimum number of neighborhoods within market',
            min_value=0,
            max_value=20,
            value=1,
            step=1
            )

        blank()

        st.markdown("**Demographic Filters**")
        blank()

        # region_filter = st.multiselect(
        #     "choose region(s)",
        #     ['South', 'West', 'Midwest', 'Northeast', 'All'],
        #     ['All']
        # )

        state_filter = st.multiselect(
            "choose state(s)",
            ['All'] + sorted(list(df['state'].unique())),
            ['All']
        )

        blank()

        with st.expander("Housing and Economic filters"):
            hpa_m, hpa_sd = MEANS['hpa']['mean'], MEANS['hpa']['sd']
            mn, mx = SLIDER_Z_SCORES['hpa_3yr_pred_scaled']
            hpa = st.slider(
                f'Predicted 3 yr Home Price Appreciation % Z-Score --- (mean: {hpa_m * 100}%, sd: {hpa_sd * 100}%)',
                min_value=mn,
                max_value=mx,
                value=(mn, mx),
                step=0.1
            )

        # hpa_b = slider_printout(hpa, m=0.146, sd=0.134)
        # st.write(f"HPA between {hpa_b['low']*100}% and {hpa_b['up']*100}%")
            hv_m, hv_sd = MEANS['mhv']['mean'], MEANS['mhv']['sd']
            mn, mx = SLIDER_Z_SCORES['mhv_scaled']
            hv_z = st.slider(
                f'Median Home Value Z-Score --- (mean: {hv_m}, sd: {hv_sd})',
                min_value=mn,
                max_value=mx,
                value=(mn, mx),
                step=0.1
            )

            hcol_m, hcol_sd = MEANS['income_to_rent']['mean'], MEANS['income_to_rent']['sd']
            mn, mx = SLIDER_Z_SCORES['inc. to rent scaled']
            hcol_z = st.slider(
                f"Income to Rent Ratio Z-Score --- (mean: {hcol_m}, sd: {hcol_sd})",
                min_value=mn,
                max_value=mx,
                value=(mn, mx),
                step=0.1,
                help="""Defined as monthly per capita income / average monthly rent"""
            )

            ho_m, ho_sd = MEANS['home_own']['mean'], MEANS['home_own']['sd']
            mn, mx = SLIDER_Z_SCORES['home ownership scaled']
            ho_z = st.slider(
                f"Home Ownership % Z-Score --- (mean: {ho_m}, sd: {ho_sd})",
                min_value=mn,
                max_value=mx,
                value=(mn, mx),
                step=0.1,
                help="""Defined as % of population that owns a home"""
            )


        with st.expander("Population filters"):
            p_m, p_sd = MEANS['pop5']['mean'], MEANS['pop5']['sd']
            mn, mx = SLIDER_Z_SCORES['pop_est_5mile_scaled']
            pop5_z = st.slider(
                f'Population within 5 miles Z-Score --- (mean: {p_m}, sd: {p_sd})',
                min_value=mn,
                max_value=mx,
                value=(mn, mx),
                step=0.1
            )

            p_m, p_sd = MEANS['pop25']['mean'], MEANS['pop25']['sd']
            mn, mx = SLIDER_Z_SCORES['pop_est_25mile_scaled']
            pop25_z = st.slider(
                f'Population within 25 miles Z-Score --- (mean: {p_m}, sd: {p_sd})',
                min_value=mn,
                max_value=mx,
                value=(mn, mx),
                step=0.1
            )

            pc_m, pc_sd = MEANS['popch5']['mean'], MEANS['popch5']['sd']
            mn, mx = SLIDER_Z_SCORES['pop_ch_5mile_scaled']
            pop_ch5_z = st.slider(
                f'Population Change 5 miles Z-Score --- (mean: {pc_m}, sd: {pc_sd})',
                min_value=mn,
                max_value=mx,
                value=(mn, mx),
                step=0.1
            )

            pc_m, pc_sd = MEANS['popch25']['mean'], MEANS['popch25']['sd']
            mn, mx = SLIDER_Z_SCORES['pop_ch_25mile_scaled']
            pop_ch25_z = st.slider(
                f'Population Change 25 miles Z-Score --- (mean: {pc_m}%, sd: {pc_sd}%)',
                min_value=mn,
                max_value=mx,
                value=(mn, mx),
                step=0.1
            )

        with st.expander("Tax filters"):
            rtx_m, rtx_sd = MEANS['retax']['mean'], MEANS['retax']['sd']
            mn, mx = SLIDER_Z_SCORES['md_retax_scaled']
            tax_z = st.slider(
                f'Median Real Estate Tax Z-Score --- (mean: {rtx_m}, sd: {rtx_sd})',
                min_value=mn,
                max_value=mx,
                value=(mn, mx),
                step=0.1
            )


        with st.expander("Crime filters"):
            crime_m, crime_sd = MEANS['crime']['mean'], MEANS['crime']['sd']
            mn, mx = SLIDER_Z_SCORES['density_total_scaled']
            crime_z = st.slider(
                f"Crime Density Z-Score --- (mean: {crime_m}, sd: {crime_sd})",
                min_value=mn,
                max_value=mx,
                value=(mn, mx),
                step=0.1,
                help="Defined as average number of crimes per sq. mile"
            )



        blank()
        num_results = st.number_input(
            "choose how many results to show",
            min_value=5,
            max_value=50,
            step=5,
            value=15
        )

        cols_to_show = st.multiselect(
            "choose which columns to show in dataframe" ,
            DISPLAY_COLS, ['city', 'cluster 1 probability']
        )

        map_bool = st.radio(
            'show points on map?',
            ['yes', 'no'], index=1
        )

        submit_button = st.form_submit_button(label='Search')


    if submit_button:
        blank()


        # hpa = hpa / 100
        hpa_lower, hpa_upper = hpa
        pz5_lower, pz5_upper = pop5_z
        pz25_lower, pz25_upper = pop25_z
        pz_ch5_lower, pz_ch5_upper = pop_ch5_z
        pz_ch25_lower, pz_ch25_upper = pop_ch25_z
        hv_lower, hv_upper = hv_z
        tax_lower, tax_upper = tax_z
        hcol_lower, hcol_upper = hcol_z
        ho_lower, ho_upper = ho_z
        crime_lower, crime_upper = crime_z

        # 'Vail, CO' in df['city'].values
        # st.dataframe(df[df['city'] == 'Vail, CO'])

        data = df[
            (df['cluster 1 probability'] >= c1) & \
            (df['pop_est_5mile_scaled'] >= pz5_lower) & \
            (df['pop_est_5mile_scaled'] <= pz5_upper) & \
            (df['pop_est_25mile_scaled'] >= pz25_lower) & \
            (df['pop_est_25mile_scaled'] <= pz25_upper) & \
            (df['pop_ch_5mile_scaled'] >= pz_ch5_lower) & \
            (df['pop_ch_5mile_scaled'] <= pz_ch5_upper) & \
            (df['pop_ch_25mile_scaled'] >= pz_ch25_lower) & \
            (df['pop_ch_25mile_scaled'] <= pz_ch25_upper) & \
            (df['hpa_3yr_pred_scaled'] >= hpa_lower) & \
            (df['hpa_3yr_pred_scaled'] <= hpa_upper) & \
            (df['mhv_scaled'] >= hv_lower) & \
            (df['mhv_scaled'] <= hv_upper) & \
            (df['md_retax_scaled'] >= tax_lower) & \
            (df['md_retax_scaled'] <= tax_upper) & \
            (df['inc. to rent scaled'] >= hcol_lower) & \
            (df['inc. to rent scaled'] <= hcol_upper) & \
            (df['home ownership scaled'] >= ho_lower) & \
            (df['home ownership scaled'] <= ho_upper) & \
            (df['density_total_scaled'] >= crime_lower) & \
            (df['density_total_scaled'] <= crime_upper) & \
            (df['num. neighborhoods'] >= num_neighborhoods)
            ]


        if 'All' in state_filter:
            pass
        else:
            data = data[data['state'].isin(state_filter)]

        data = data.sort_values('cluster 1 probability', ascending=False)

        st.markdown(f"**{data.shape[0]}** markets match these filters")
        display_df = data.head(num_results).drop('Unnamed: 0', axis=1)
        if map_bool == 'yes':
            # coords = [parse_address_string(a) for a in display_df['city'].values]
            # map_df = pd.DataFrame({
            #     'lat': [x['lat'] for x in coords],
            #     'lon': [x['long'] for x in coords]
            # })
            #
            # st.map(map_df)

            blank()

            # cdf = mapper.city_groups
            # cdf = gpd.GeoDataFrame(cdf[cdf['city'].isin(display_df['city'].values)])
            # cdf.to_crs(pyproj.CRS.from_epsg(4326), inplace=True)

            gdf = mapper.data
            gdf = gdf[gdf['city'].isin(display_df['city'].values)]
            gdf = gpd.GeoDataFrame(gdf)

            m = folium.Map([39.112701, -94.626801], zoom_start=3.5)

            style_function = lambda x: {
                'fillColor': 'red',
                'color': 'red',
                'fillOpacity': 0,
                'weight': 3.0,
            }

            highlight_function = lambda x: {'fillColor': '#ef4036',
                                'color':'#ef4036',
                                'fillOpacity': 0.4,
                                'weight': 0.5}

            folium.GeoJson(gdf, style_function=style_function, highlight_function=highlight_function,
                tooltip=folium.GeoJsonTooltip(
                fields=['city'],
                localize=True
            )).add_to(m)



            for sty in TILES:
                folium.raster_layers.TileLayer(TILES[sty]).add_to(m)

            folium.LayerControl().add_to(m)
            st.markdown(m._repr_html_(), unsafe_allow_html=True)

            blank()
            st.download_button(
                label='Download map',
                data=m._repr_html_(),
                file_name='targeting_map.html',
                mime='text/html'
            )


        blank()
        blank()
        st.write("Data ranked by cluster 1 probability")
        display_df = display_df[cols_to_show].reset_index().drop('index', axis=1).round(2)
        display_df.index = np.arange(1, len(display_df) + 1)
        st.dataframe(display_df)

        blank()
        st.download_button(
            label='Download data',
            data=convert_df(display_df),
            file_name='target_markets.csv',
            mime='text/csv'
        )






main()
