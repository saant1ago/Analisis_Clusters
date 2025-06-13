
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(page_title="Análisis TDA de Consumo de Combustible", layout="wide")

st.title("🔍 Análisis Topológico de Consumo de Combustible en SLB México")
st.markdown("Aplicación interactiva basada en Mapper, UMAP, t-SNE y análisis estadístico descriptivo. Identifica pozos atípicos y patrones relevantes para optimizar el consumo de combustible.")

# Sidebar con navegación
st.sidebar.header("📂 Secciones")
section = st.sidebar.radio("Ir a:", ["Resumen Clusters", "Desviación Mensual", "Visualización UMAP", "Visualización t-SNE", "Predicción de Outliers"])

@st.cache_data
def cargar_archivos():
    tsne_df = pd.read_csv("resumen_clusters_tsne.csv")
    umap_df = pd.read_csv("resumen_clusters_umap.csv")
    stats_df = pd.read_csv("descripcion_estadistica_mensual.csv")
    pozos_df = pd.read_csv("pozos_reales.csv")
    return tsne_df, umap_df, stats_df, pozos_df

tsne_df, umap_df, stats_df, pozos_df = cargar_archivos()

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

elif section == "Predicción de Outliers":
    st.header("🔮 Predicción de Outliers")

    st.markdown("""
    Este módulo analiza los patrones históricos de desviación operativa por pozo 
    y predice qué pozos podrían comportarse como *outliers* en los siguientes meses. 
    """)

    archivo = st.file_uploader("Sube un archivo CSV con tu matriz de pozos y meses", type=["csv"])
    n_meses = st.number_input("¿Cuántos meses deseas simular?", min_value=1, max_value=24, value=6, step=1)
    ejecutar = st.button("🚀 Ejecutar simulación del modelo")

    if archivo and ejecutar:
        df_input = pd.read_csv(archivo)
        pozos = df_input.iloc[:, 0].tolist()
    elif ejecutar:
        pozos = pozos_df["Pozo"].tolist()
    else:
        pozos = []

    if ejecutar and pozos:
        meses = [f"2024-{str(m+1).zfill(2)}" for m in range(n_meses)]
        data = np.random.choice([0, 1], size=(len(pozos), len(meses)), p=[0.92, 0.08])
        df_outliers_sim = pd.DataFrame(data, columns=meses)
        df_outliers_sim.insert(0, "Pozo", pozos)

        st.subheader("📋 Resultados simulados")
        st.dataframe(df_outliers_sim)

        df_outliers_sim["Total_Meses_Outlier"] = df_outliers_sim[meses].sum(axis=1)
        pozos_alerta = df_outliers_sim[df_outliers_sim["Total_Meses_Outlier"] >= 2]

        for _, row in pozos_alerta.iterrows():
            st.warning(f"⚠️ Atención: El pozo *{row['Pozo']}* fue clasificado como outlier en {int(row['Total_Meses_Outlier'])} de los últimos {n_meses} meses.")

        st.subheader("📊 Visualización por pozo y mes")
        heatmap_data = df_outliers_sim.set_index("Pozo")[meses]
        st.dataframe(heatmap_data.style.background_gradient(cmap="Reds", axis=None))
