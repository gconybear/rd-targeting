import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(layout='centered', page_icon='🎯')

@st.cache
def get_data():

    return pd.read_csv('data/dat.csv')

df = get_data()

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
            step=0.1
            )

        blank()

        st.markdown("**Demographic Filters**")
        blank()

        region_filter = st.multiselect(
            "choose region(s)",
            ['South', 'West', 'Midwest', 'Northeast', 'All'],
            ['All']
        )

        blank()

        hpa = st.slider(
            'Min. Predicted 3 yr Home Price Appreciation Z-Score',
            min_value=-3.0,
            max_value=3.0,
            value=(-1.0, 1.0),
            step=0.1
        )

        pop_z = st.slider(
            'Population Z-Score',
            min_value=-3.0,
            max_value=3.0,
            value=(-1.0, 1.0),
            step=0.1
        )

        pop_ch_z = st.slider(
            'Population Change Z-Score',
            min_value=-3.0,
            max_value=3.0,
            value=(-1.0, 1.0),
            step=0.1
        )

        hv_z = st.slider(
            'Median Home Value Z-Score',
            min_value=-3.0,
            max_value=3.0,
            value=(-1.0, 1.0),
            step=0.1
        )

        tax_z = st.slider(
            'Median Real Estate Tax Z-Score',
            min_value=-3.0,
            max_value=3.0,
            value=(-1.0, 1.0),
            step=0.1
        )

        # rd_col, wealth_col = st.columns(2)
        #
        # rd_match = rd_col.selectbox(
        #     'Red Dot demographic similarity',
        #     ['low', 'medium', 'high']
        # )
        #
        # wealth = wealth_col.slider(
        #     'Min. Predicted 3 yr Home Price Appreciation %',
        #     min_value=0.0,
        #     max_value=3.0,
        #     value=0.0,
        #     step=0.1
        # )
        #
        # home_val_col, crime_col = st.columns(2)
        #
        # home_val = home_val_col.selectbox(
        #     'Home value growth',
        #     ['low', 'medium', 'high']
        # )
        #
        # crime = crime_col.selectbox(
        #     'Crime level',
        #     ['low', 'medium', 'high']
        # )

        blank()
        submit_button = st.form_submit_button(label='Search')


    if submit_button:
        blank()

        # hpa = hpa / 100
        hpa_lower, hpa_upper = hpa
        pz_lower, pz_upper = pop_z
        pz_ch_lower, pz_ch_upper = pop_ch_z
        hv_lower, hv_upper = hv_z
        tax_lower, tax_upper = tax_z

        data = df[
            (df['cluster 1 probability'] >= c1) & \
            (df['pop_est_25mile_scaled'] >= pz_lower) & \
            (df['pop_est_25mile_scaled'] <= pz_upper) & \
            (df['pop_ch_25mile_scaled'] >= pz_ch_lower) & \
            (df['pop_ch_25mile_scaled'] <= pz_ch_upper) & \
            (df['hpa_3yr_pred'] >= hpa_lower) & \
            (df['hpa_3yr_pred'] <= hpa_upper) & \
            (df['mhv_scaled'] >= hv_lower) & \
            (df['mhv_scaled'] <= hv_upper) & \
            (df['md_retax_scaled'] >= tax_lower) & \
            (df['md_retax_scaled'] <= tax_upper)
            ]

        if 'All' in region_filter:
            pass
        else:
            data = data[data['region'].isin(region_filter)]

        data = data.sort_values('cluster 1 probability', ascending=False)

        st.markdown(f"**{data.shape[0]}** markets match these filters")

        st.dataframe(data)




main()
