import streamlit as st
from funciones_estadisticas import *
import matplotlib.pyplot as plt

st.set_page_config(
    page_title='Taller de Estadística',
    page_icon="🧊🧊",
    layout='wide')

# Funciones

def intro() :
    st.title("Taller de Estadística")
    st.markdown("---")
    st.header("🚧 :pick: En construcción  :pick: 🚧")
    st.markdown("---")
    st.write('Aquí irá la introducción')

    st.subheader('Sobre el proyecto')
    st.markdown('- Autor: *Carlos Rodríguez*  \n -   :exclamation: [Repo *Github*](https://github.com/crdguez/taller_estadistica)' )
    st.subheader('Licencia')
    st.write('Tanto el código como la aplicación se publican con **licencia libre**. \
      \n * En caso de uso, se agradece la atribución :+1: \
        \n * Así mismo, se agradecen sugerencias y contribuciones \
        a través de *pull requests* en el repositorio')


def unidimensional() :
    st.title("Estadística unidimensional")
    # st.write("Aquí irá la estadística unidimensional")

    st.sidebar.markdown("""---""")
    st.header("Datos de análisis:")
    opciones = st.selectbox("Selecciona:", ('ejemplo1','entrada manual'),index=0)
    if opciones == 'ejemplo1' :
        datos = """16 11 17 12 10 5 1 8 10 14 15 20 10 3 8 10 2 5 12 6 16 7 6 16 10 3 3 9 4 12"""
    else:
        datos = st.text_input('Introduce los datos separados por espacios', '')
        datos = datos.replace(',',' ')

    if datos != '' :
        dic=analisis_discreto(datos)
        st.write("Datos:")
        st.write(", ".join(map(str,dic['datos'])))

        # st.write(dic)
        st.subheader("Tabla de Frecuencias:")
        dic['tabla'].index=dic['tabla'].index.astype(str)
        st.table(dic['tabla'].astype({"x_i":int, "f_i":int, "F_i":int}).style.format({'h_i':"{:,.2f}",'H_i':"{:,.2f}",'%_i':"{:,.2f}%",'%A_i':"{:,.2f}%",'xf':"{:,.2f}%"}))
        st.pyplot(dic['figure'])




def agrupada() :
    st.title("Estadística agrupada")
    st.write("Aquí irá la estadística unidimensional agrupada")

def bidimensional() :
    st.title("Estadística bidimensinal y regresión lineal")
    st.write("Aquí irá la estadística unidimensional agrupada")

# Menú lateral

st.sidebar.title("""Taller de  Estadística
---
""")
PAGES = {
    "Introducción": intro,
    "E. unidimensional": unidimensional,
    "E. con datos agrupados": agrupada,
    "E. bidimensional": agrupada,
}

selection = st.sidebar.radio("Menú:", list(PAGES.keys()),index=0)
st.sidebar.markdown("""---""")

if selection == list(PAGES.keys())[1] :
    unidimensional()
elif selection == list(PAGES.keys())[2] :
    agrupada()
elif selection == list(PAGES.keys())[3] :
    bidimensional()
else :
    intro()
