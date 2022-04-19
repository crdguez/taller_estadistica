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
        col1, col2 = st.columns(2)

        with col1 :
            st.subheader("Tabla de Frecuencias:")
            dic['tabla'].index=dic['tabla'].index.astype(str)
            tabla_formateada=dic['tabla'].astype({"x_i":int,
                "f_i":int,"F_i":int}).style.format({'h_i':"{:,.2f}",
                'H_i':"{:,.2f}",'%_i':"{:,.2f}%",
                '%A_i':"{:,.2f}%",'xf':"{:,.2f}",
                'x2f':"{:,.2f}"})
            # tabla_formateada=dic['tabla']
            # tabla_formateada.rename(columns={'x_i':r'$x^2$'}, inplace = True)
            st.table(tabla_formateada)
            # st.dataframe(tabla_formateada)
            # st.latex(tabla_formateada.to_latex())
        with col2 :
            st.pyplot(dic['figure'])

        st.subheader('Parámetros de centralización:')
        # tabla=dic['tabla']
        # media=r'$\overline{x}=\dfrac{\Sigma{x_i f_i}}{N}=' \
        #     +r'\dfrac{'+ str(tabla.iloc[:-1,7].sum()) \
        #     +r'}{'+str(tabla.iloc[:-1,1].sum())+r'}='+ \
        #     str(tabla.iloc[:-1,7].sum()/tabla.iloc[:-1,1].sum())+r'$'
        st.markdown('* Media: {} \
            \n * Moda:{} \
            \n * Mediana: {} \
            '.format(dic['texto_media'], dic['texto_moda'], \
            dic['texto_mediana'],))
        st.subheader('Párametros de posición')
        # st.markdown('**Percentiles**')
        k=st.slider('Selecciona percentil:',0,100,value=50,step=5)
        st.write('Percentil $P_{'+str(k)+'}$= '+str(percentil(dic['tabla'][:-1],k)))
        kk=st.radio('Selecciona cuartil: ',(25,50,75),format_func= lambda x: 'Q'+str(int(x/25)))
        st.write('Cuartil Q'+str(int(kk/25))+'='+str(percentil(dic['tabla'][:-1],kk)))
        st.subheader('Párametros de dispersión')
        st.write('Rango: '+str(dic['rango']))
        # st.write('Desviación: '+str(dic['desviacion']))
        st.write('Desviación típica:  '+dic['texto_desviacion'])
        st.write('Varianza:  $Var='+str(dic['desviacion'])+'^2='+str(dic['varianza'])+'$')



def agrupada() :
    st_datos=''
    n_intervalos=0
    st.title("Estadística agrupada")
    st.sidebar.markdown("""---""")
    st.warning(':fire: En construccion :fire:')
    st.header("Datos de análisis:")
    opciones = st.selectbox("Selecciona:", ('ejemplo1','entrada manual', 'entrada manual por intervalos'),index=0)
    if opciones == 'ejemplo1' :
        st_datos = """174 157 168 166 169 168 173 184 176 171 172 168 167 162 162 163
                166 166 167 167 174 159 170 172 173 164 161 163 176 177"""
        datos = np.loadtxt(st_datos.split())
        st.write('Datos:')
        st.write(', '.join(map(str,datos)))
        # rango=(155,185)
        n_intervalos=st.slider('Número de intervalos',2,10,value=3,step=1)
        frecs, intervalos, intervalos_latex = agrupar_por_intervalos(datos,n_intervalos)

    elif opciones == 'entrada manual' :
        st_datos = st.text_input('Introduce los datos separados por espacios', '')
        st_datos = st_datos.replace(',',' ')
        if st_datos != '' :
            datos = np.loadtxt(st_datos.split())
            n_intervalos=st.slider('Número de intervalos',2,10,value=3,step=1)
            frecs, intervalos, intervalos_latex = agrupar_por_intervalos(datos,n_intervalos)
    else:
        st_intervalos = st.text_input('Introduce la lista de límites de los intervalos:', '')
        st_intervalos = st_intervalos.replace(',',' ')
        intervalos = np.loadtxt(st_intervalos.split())
        intervalos_latex="$"+r", ".join([latex(Interval.Ropen(intervalos[i],intervalos[i+1])) for i in range(len(intervalos)-1)])+"$"
        n_intervalos=len(intervalos)-1
        # st.write(n_intervalos)
        st.write(intervalos_latex)
        if st_intervalos != '' :
            st_frecs = st.text_input('Introduce las frecuencias:', '')
            st_frecs = st_frecs.replace(',',' ')
            frecs=np.loadtxt(st_frecs.split())
            if len(intervalos) != len(frecs) + 1 :
                st.write("Reecuerda que tiene que haber un dato menos que la lista de intervalos")
            else :
                st.write(", ".join(map(str,frecs)))



    # if st_datos != '' :
    if n_intervalos != 0 :
        dic=analisis_agrupado(frecs, intervalos)
        st.write("**Datos agrupados:**")
        st.write(dic)
        st.write(np.cumsum(dic['frecs']))
        st.write((intervalos[:-1]+intervalos[1:])/2)
        # st.write(", ".join(map(str,datos)))
        # st.write("**Intervalos:**")
        # st.write(intervalos_latex)
        #
        # # st.write(dic)
        col1, col2 = st.columns(2)

        with col1 :
            st.subheader("Tabla de Frecuencias:")
            dic['tabla'].index=dic['tabla'].index.astype(str)
        #     tabla_formateada=dic['tabla'].astype({"x_i":int,
        #         "f_i":int,"F_i":int}).style.format({'h_i':"{:,.2f}",
        #         'H_i':"{:,.2f}",'%_i':"{:,.2f}%",
        #         '%A_i':"{:,.2f}%",'xf':"{:,.2f}",
        #         'x2f':"{:,.2f}"})
            # tabla_formateada=dic['tabla']
        #     # tabla_formateada.rename(columns={'x_i':r'$x^2$'}, inplace = True)
        #     st.table(tabla_formateada)
            st.table(dic['tabla'])

        #     # st.dataframe(tabla_formateada)
        #     # st.latex(tabla_formateada.to_latex())
        with col2 :
            st.write('Aquí irá el Diagrama')
        #     st.pyplot(dic['figure'])
        #
        st.subheader('Parámetros de centralización:')
        # # tabla=dic['tabla']
        # # media=r'$\overline{x}=\dfrac{\Sigma{x_i f_i}}{N}=' \
        # #     +r'\dfrac{'+ str(tabla.iloc[:-1,7].sum()) \
        # #     +r'}{'+str(tabla.iloc[:-1,1].sum())+r'}='+ \
        # #     str(tabla.iloc[:-1,7].sum()/tabla.iloc[:-1,1].sum())+r'$'
        # st.markdown('* Media: {} \
        #     \n * Moda:{} \
        #     \n * Mediana: {} \
        #     '.format(dic['texto_media'], dic['texto_moda'], \
        #     dic['texto_mediana'],))
        # st.subheader('Párametros de posición')
        # # st.markdown('**Percentiles**')
        # k=st.slider('Selecciona percentil:',0,100,value=50,step=5)
        # st.write('Percentil $P_{'+str(k)+'}$= '+str(percentil(dic['tabla'][:-1],k)))
        # kk=st.radio('Selecciona cuartil: ',(25,50,75),format_func= lambda x: 'Q'+str(int(x/25)))
        # st.write('Cuartil Q'+str(int(kk/25))+'='+str(percentil(dic['tabla'][:-1],kk)))
        # st.subheader('Párametros de dispersión')
        # st.write('Rango: '+str(dic['rango']))
        # # st.write('Desviación: '+str(dic['desviacion']))
        # st.write('Desviación típica:  '+dic['texto_desviacion'])
        # st.write('Varianza:  $Var='+str(dic['desviacion'])+'^2='+str(dic['varianza'])+'$')

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
