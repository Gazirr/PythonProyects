import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 1. Cargar datos
df = pd.read_csv(r"C:\Users\gabrielheralv\Desktop\Acceso a Datos\Matriculas_Alumnos(Gabriel Herrador)\WebScrapping\paises_poblacion.csv")

# Mostrar columnas y primeras filas para depurar
st.write("Columnas disponibles en el CSV:", df.columns.tolist())
st.write(df.head())

st.title("Análisis y Visualización de Datos de Población Mundial")

# Filtrado interactivo


df_filtrado = df

# Ajusta aquí el nombre correcto de la columna de población
col_poblacion = None
for col in df.columns:
    if 'popul' in col.lower():
        col_poblacion = col
        break

if col_poblacion:
    # Limpiar y convertir a entero
    df_filtrado[col_poblacion] = df_filtrado[col_poblacion].str.replace(',', '').astype(int)

    poblacion_min, poblacion_max = int(df_filtrado[col_poblacion].min()), int(df_filtrado[col_poblacion].max())
    rango_poblacion = st.slider("Rango de población:", poblacion_min, poblacion_max, (poblacion_min, poblacion_max))
    df_filtrado = df_filtrado[
        (df_filtrado[col_poblacion] >= rango_poblacion[0]) & (df_filtrado[col_poblacion] <= rango_poblacion[1])]

else:
    st.warning("No se encontró ninguna columna relacionada con población")

# Mostrar tabla
st.dataframe(df_filtrado)

# Visualización
col_pais = None
for col in df.columns:
    if 'country' in col.lower():
        col_pais = col
        break

if col_pais and col_poblacion:
    top10 = df_filtrado.sort_values(by=col_poblacion, ascending=False).head(10)

    fig, ax = plt.subplots()
    ax.barh(top10[col_pais], top10[col_poblacion])
    ax.set_xlabel("Población")
    ax.set_title("Top 10 Países por Población")
    st.pyplot(fig)
else:
    st.warning("No se encontraron las columnas necesarias para graficar")
