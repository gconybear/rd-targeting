import requests
import json
import streamlit as st

API_KEY = st.secrets['GEOCODE_KEY']

def parse_address_string(addy):
    headers = {
  "apikey": API_KEY}

    params = (
       ("text", addy),
    )

    response = requests.get('https://app.geocodeapi.io/api/v1/search', headers=headers, params=params)

    if response.status_code == 200:
        dat = json.loads(response.content)
        long, lat = dat['features'][0]['geometry']['coordinates']

        return {'lat': lat, 'long': long}
