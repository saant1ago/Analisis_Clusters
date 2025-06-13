
import streamlit as st
import pandas as pd
import plotly.express as px

# Carga de archivos
tsne_df = pd.read_csv("resumen_clusters_tsne.csv")
umap_df = pd.read_csv("resumen_clusters_umap.csv")
stats_df = pd.read_csv("descripcion_estadistica_mensual.csv")

st.set_page_config(page_title="Análisis TDA de Consumo de Combustible", layout="wide")

st.title("🔍 Análisis Topológico de Consumo de Combustible en SLB México")
st.markdown("Aplicación interactiva basada en Mapper, UMAP, t-SNE y análisis estadístico descriptivo. Identifica pozos atípicos y patrones relevantes para optimizar el consumo de combustible.")

st.sidebar.header("📂 Secciones")
section = st.sidebar.radio("Ir a:", ["Resumen Clusters", "Desviación Mensual", "Visualización UMAP", "Visualización t-SNE"])

if section == "Resumen Clusters":
    st.header("📌 Resumen de Clusters por Técnica")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("UMAP")
        st.dataframe(umap_df)
    with col2:
        st.subheader("t-SNE")
        st.dataframe(tsne_df)

elif section == "Desviación Mensual":
    st.header("📊 Estadísticas Descriptivas Mensuales")
    st.dataframe(stats_df)

    fig = px.line(stats_df, x=stats_df.columns[0], y="mean", title="Promedio mensual de desviación operativa")
    st.plotly_chart(fig, use_container_width=True)

elif section == "Visualización UMAP":
    st.header("🌐 Visualización Clusters UMAP")
    fig = px.scatter(umap_df, x="Desviacion_Promedio_General_Cluster", y="Valor_Pico_Desviacion_Mes",
                     color="Descripcion_Cluster", size="Num_Pozos", hover_name="Cluster_ID",
                     title="Clusters UMAP - Desviación vs Pico")
    st.plotly_chart(fig, use_container_width=True)

elif section == "Visualización t-SNE":
    st.header("🌐 Visualización Clusters t-SNE")
    fig = px.scatter(tsne_df, x="Desviacion_Promedio_General_Cluster", y="Valor_Pico_Desviacion_Mes",
                     color="Descripcion_Cluster", size="Num_Pozos", hover_name="Cluster_ID",
                     title="Clusters t-SNE - Desviación vs Pico")
    st.plotly_chart(fig, use_container_width=True)
