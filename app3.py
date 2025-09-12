import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px 
import geopandas as gpd
import numpy as np


data = pd.read_csv('data_3.csv')
parquet = pd.read_parquet("data_3.parquet")

st.title("Homicidios a nivel municipal 2024")

st.set_page_config(
    page_title="Homicidios/municipios",
    page_icon="☠",
    layout="wide"
)

st.subheader("Tasa de homicidios por 100.000 habitantes en cada municipio")
# KPIs generales
total_homicidios = int(data['total_homicidios'].sum())
mean_tasa = data['tasa_homicidios'].mean()


col1, col2 = st.columns(2)
col1.metric("Total homicidios 2024 (suma municipal)", f"{total_homicidios:,}")
col2.metric("Tasa municipal promedio (100k)", f"{mean_tasa:.2f}")

# Mapa
st.subheader("Mapa municipal — tasa por 100.000 hab.")
if gpd is not None and not gpd.empty:
    fig_map = px.choropleth_mapbox(
        gpd,
        geojson=gpd.set_index('codigo_mun').geometry._geo_interface_,
        locations=gpd['codigo_mun'],
        color='tasa_homicidios',
        hover_name='municipio',
        hover_data=['nombre_dpto','tasa_homicidios','poblacion'],
        mapbox_style="carto-positron",
        center={"lat": 4.5, "lon": -74},
        zoom=5,
        opacity=0.6,
        color_continuous_scale="Reds"
    )
    st.plotly_chart(fig_map, use_container_width=True)
else:
    st.info("No se encontró municipios.parquet. Si lo tienes, colócalo en /mnt/data para ver el mapa.")



fig1 = px.scatter_mapbox(
    data,
    lat="latitud",
    lon="longitud",
    size="tasa_homicidios",              # tamaño según tasa
    color="tasa_homicidios",             # color según tasa
    hover_name="municipio",
    hover_data={"nombre_dpto": True, "total_homicidios": True, "poblacion": True, "tasa_homicidios": True},
    color_continuous_scale="Reds",
    zoom=4,
    height=600
)
fig1.update_layout(mapbox_style="carto-positron")  # estilo del mapa
st.plotly_chart(fig1)

