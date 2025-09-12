import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px 
import geopandas as gpd
import numpy as np
from pathlib import Path

data = pd.read_csv("data_3.csv")          # homicidios, población, etc.
gdf = gpd.read_parquet("data_3.parquet")

st.set_page_config(
    page_title="Homicidios/Departamento-Municipio",
    page_icon="☠",
    layout="wide")

# Normalizamos los códigos
data["codigo_mun"] = data["codigo_mun"].astype(str)
gdf["codigo_mun"] = gdf["codigo_mun"].astype(str)

gdf = gdf.merge(data, on="codigo_mun", how="left")

# Corregimos columnas duplicadas
gdf = gdf.rename(columns={
    "municipio_x": "municipio",
    "departamento_x": "departamento",
    "total_homicidios_x": "total_homicidios",
    "poblacion_x": "poblacion",
    "tasa_homicidios_x": "tasa_homicidios"
})
cols_drop = [c for c in gdf.columns if c.endswith("_y")]
gdf = gdf.drop(columns=cols_drop)

total_homicidios = int(data["total_homicidios"].sum())
promedio_tasa = data["tasa_homicidios"].mean()

st.title("🔎 Homicidios en Colombia — 2024")
st.markdown("Visualización de homicidios a nivel municipal y departamental.")

#INTENTOOO
card_style = """
    background-color:{bg};
    padding:15px;
    border-radius:10px;
    text-align:center;
    box-shadow: 1px 1px 6px rgba(0,0,0,0.15);
    height:120px;
    display:flex;
    flex-direction:column;
    justify-content:center;
"""

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        f"""
        <div style="{card_style.format(bg='#e74c3c')}">
            <p style="color:white; font-size:16px; margin:0;">Total homicidios</p>
            <p style="color:white; font-size:22px; font-weight:bold; margin:0;">
                {total_homicidios:,}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div style="{card_style.format(bg='#2980b9')}">
            <p style="color:white; font-size:16px; margin:0;">Tasa promedio (100k)</p>
            <p style="color:white; font-size:22px; font-weight:bold; margin:0;">
                {promedio_tasa:.2f}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )


#Mapa 
st.subheader("Mapa de las tasas de homicidio")
fig_map = px.choropleth_mapbox(
    gdf,
    geojson=gdf.geometry,
    locations=gdf.index,
    color="tasa_homicidios",
    hover_name="municipio",
    hover_data={
    "nombre_dpto_x": True,
    "total_homicidios": True,
    "poblacion": True,
    "tasa_homicidios":':.2f'},
    mapbox_style="carto-positron",
    center={"lat": 4.5, "lon": -74},
    zoom=5,
    opacity=0.7,
    color_continuous_scale="Reds",
    height=600
)
#st.plotly_chart(fig_map, use_container_width=True)


# Top 10

#st.subheader("Top 10 municipios con más homicidios")
top_mas = data.sort_values("total_homicidios", ascending=False).head(10)
#st.dataframe(top_mas[["municipio", "cod_dpto", "total_homicidios", "tasa_homicidios"]])

#st.subheader("Top 10 municipios con menos homicidios")
top_menos = data.sort_values("total_homicidios", ascending=True).head(10)
#st.dataframe(top_menos[["municipio", "cod_dpto", "total_homicidios", "tasa_homicidios"]])

st.subheader("Comparación de municipios")

# Datos
top_mas = data.sort_values("total_homicidios", ascending=False).head(10)
top_menos = data.sort_values("total_homicidios", ascending=True).head(10)

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 🔴 Top 10 con más homicidios")
    fig_mas = px.bar(
        top_mas.sort_values("total_homicidios"),  # ordenado de menor a mayor para que se vea mejor
        x="total_homicidios",
        y="municipio",
        orientation="h",
        text="total_homicidios",
        color="total_homicidios",
        color_continuous_scale="Reds"
    )
    fig_mas.update_layout(
        xaxis_title="Homicidios",
        yaxis_title="",
        height=500,
        margin=dict(l=20, r=20, t=30, b=20)
    )
    st.plotly_chart(fig_mas, use_container_width=True)

with col2:
    st.markdown("#### 🟢 Top 10 con menos homicidios")
    fig_menos = px.bar(
        top_menos.sort_values("total_homicidios"), 
        x="total_homicidios",
        y="municipio",
        orientation="h",
        text="total_homicidios",
        color="total_homicidios",
        color_continuous_scale="Greens"
    )
    fig_menos.update_layout(
        xaxis_title="Homicidios",
        yaxis_title="",
        height=500,
        margin=dict(l=20, r=20, t=30, b=20)
    )
    st.plotly_chart(fig_menos, use_container_width=True)



#distrubuir por departamento 
st.subheader("Distribución por departamento")
dep = data.groupby("nombre_dpto").agg(
    homicidios_total=("total_homicidios", "sum"),
    poblacion_total=("poblacion", "sum")
).reset_index()
dep["tasa_100k"] = (dep["homicidios_total"] / dep["poblacion_total"]) * 100000

fig_dep = px.bar(
    dep.sort_values("homicidios_total", ascending=False),
    x="homicidios_total",
    y="nombre_dpto",
    orientation="h",
    color="tasa_100k",
    color_continuous_scale="Blues",
    labels={"homicidios_total": "Homicidios", "nombre_dpto": "Departamento"},
    title="Homicidios totales y tasa por departamento"
)
#st.plotly_chart(fig_dep, use_container_width=True)

#treemap
fig_treemap = px.treemap(
    gdf, 
    path=["nombre_dpto_x"],       # Jerarquía: por departamento
    values="total_homicidios",   # El tamaño es el número absoluto de homicidios
    color="tasa_homicidios",     # Color según tasa (opcional, puedes cambiar a 'total_homicidios')
    color_continuous_scale="Reds",
    title="Distribución de homicidios por departamento (2024)"
)

st.plotly_chart(fig_treemap, use_container_width=True)


#
st.subheader("Distribución de tasas municipales")
fig, ax = plt.subplots(figsize=(8, 4))
ax.hist(data["tasa_homicidios"].dropna(), bins=40, color="darkred", edgecolor="black")
ax.set_xlabel("Tasa por 100k")
ax.set_ylabel("Número de municipios")
ax.set_title("Histograma de tasas municipales")
st.pyplot(fig)

