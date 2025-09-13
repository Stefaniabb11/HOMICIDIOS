import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px 
import geopandas as gpd
import numpy as np
from pathlib import Path
from matplotlib.colors import LinearSegmentedColormap


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

#intento depto
dept = data.groupby("nombre_dpto")["total_homicidios"].sum().reset_index()

fig_dept = px.bar(
    dept.sort_values("total_homicidios", ascending=False),
    x="nombre_dpto",
    y="total_homicidios",
    color="total_homicidios",
    color_continuous_scale="Pinkyl",  # Paleta púrpura-naranja
    labels={
        "total_homicidios": "Homicidios Totales",
        "nombre_dpto": "Departamento"
    },
    title="Distribución de Homicidios por Departamento"
)

st.plotly_chart(fig_dept, use_container_width=True)

#grafico mun
fig_tasa = px.bar(
    data.sort_values("tasa_homicidios", ascending=False).head(30),  # Top 30 municipios
    x="municipio",
    y="tasa_homicidios",
    color="tasa_homicidios",
    color_continuous_scale="Mint",  # escala rojo-púrpura
    labels={
        "tasa_homicidios": "Tasa de Homicidios (por 100k)",
        "municipio": "Municipio"
    },
    title="Tasa de homicidios por municipio (2024)"
)

st.plotly_chart(fig_tasa, use_container_width=True)

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
        <div style="{card_style.format(bg='#f67c78')}">
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
        <div style="{card_style.format(bg='#63a6a0')}">
            <p style="color:white; font-size:16px; margin:0;">Tasa promedio (100k)</p>
            <p style="color:white; font-size:22px; font-weight:bold; margin:0;">
                {promedio_tasa:.2f}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

#Grafico de eso 

# Top 10

#st.subheader("Top 10 municipios con más homicidios")
top_mas = data.sort_values("tasa_homicidios", ascending=False).head(10)
#st.dataframe(top_mas[["municipio", "cod_dpto", "tasa_homicidios"]])

#st.subheader("Top 10 municipios con menos homicidios")
top_menos = data.sort_values("tasa_homicidios", ascending=True).head(10)
#st.dataframe(top_menos[["municipio", "cod_dpto", "tasa_homicidios"]])

st.subheader("Comparación de municipios")

# Datos
top_mas = data.sort_values("tasa_homicidios", ascending=False).head(10)
top_menos = data.sort_values("tasa_homicidios", ascending=True).head(10)

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 🔴 Top 10 con más homicidios")
    fig_mas = px.bar(
        top_mas.sort_values("tasa_homicidios",ascending= True),  # ordenado de menor a mayor para que se vea mejor
        x="tasa_homicidios",
        y="municipio",
        orientation="h",
        text="tasa_homicidios",
        color="tasa_homicidios",
        color_continuous_scale="Pinkyl"
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
        top_menos.sort_values("tasa_homicidios"), 
        x="tasa_homicidios",
        y="municipio",
        orientation="h",
        text="tasa_homicidios",
        color="tasa_homicidios",
        color_continuous_scale="Mint"
    )
    fig_menos.update_layout(
        xaxis_title="Homicidios",
        yaxis_title="",
        height=500,
        margin=dict(l=20, r=20, t=30, b=20)
    )
    st.plotly_chart(fig_menos, use_container_width=True)

st.subheader("Mapa de tasa de tasa de homicidios")



# Creamos el colormap Pinkyl a partir de Plotly

# Dibujar el mapa


# Definir Pinkyl como gradiente
pinkyl_colors = ["#edd597", "#ca7185", "#d94f6d"]
custom_cmap = LinearSegmentedColormap.from_list("Pinkyl", pinkyl_colors)

fig, ax = plt.subplots(1, 1, figsize=(4,4))

gdf.plot(
    column="tasa_homicidios",   # 👈 ajusté al nombre real de tu columna
    ax=ax,
    legend=True,
    cmap=custom_cmap,
    missing_kwds={
        "color": "lightgrey",
        "edgecolor": "white",
        "hatch": "///",
        "label": "Sin datos"
    }
)

# Quitar fondo blanco
ax.set_facecolor("none")
fig.patch.set_alpha(0)

ax.axis("off")
st.pyplot(fig)




