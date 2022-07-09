import streamlit as st
import pandas as pd
import datetime
import plotly.express as px
from streamlit_option_menu import option_menu
import plotly.graph_objects as go
import streamlit as st
import streamlit.components.v1 as html
from  PIL import Image
import numpy as np
import io 

def grafica_cantidad_sobre_tiempo(df):
    df_grp = df.groupby(['Año'])['CANTIDAD'].sum().reset_index()
    return px.line(df_grp, x='Año', y="CANTIDAD", height =650, title='CANTIDAD DE CASOS DE VIOLENCIA INTRAFAMILIAR POR AÑO', width=1000)

@st.cache(allow_output_mutation=True)
def cargar_datos():
    return pd.read_csv("Violencia_Intrafamiliar_Colombia_Clear.csv")

# Press the green button in the gutter to run the script.

st.set_page_config(page_title='Violencia intrafamiliar', layout='wide')
df=cargar_datos();


with st.sidebar:
    choose = option_menu("DASHBOARD", ["Home", "Más detalles", "Predecir", "Contacto"],
                         icons=['house', 'kanban', 'book','person lines fill'],
                         menu_icon="app-indicator", default_index=0,
                         styles={
        "container": {"padding": "5!important","font-family":"sans-serif","font-weight":"bold", "background-color":"#FFFFFF"},
        "icon": {"color": "#023047", "font-size": "25px","font-family":"sans-serif", "font-weight":"bold","color:hover": "#eee"}, 
        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee","font-family":"sans-serif"},
        "nav-link-selected": {"background-color": "#FB8500"},
    }
    )

if choose == "Más detalles":
    with st.container():
        st.markdown('Hola, aqui va una info grafica')
        st.multiselect("Seleccione", ["HOLA"], default=None, key=None, help=None, on_change=None, args=None, kwargs=None,disabled=False)
        st.markdown('Hola, aqui va una info grafica')    
    
elif choose == "Contacto":
    with st.container():              
        st.markdown('<p class="font">Acerca de los creadores</p>', unsafe_allow_html=True)    
        st.write("Somos unos estudiantes de ingeniería de sistemas que queremos que puedas conocernos y nos ayudes a mejorar, si tienes alguna duda o sugerencia puedes contactarnos en el siguiente correo: fktcg99@gmail.com, tambien puedes aportar a nuestro proyecto en github: https://github.com/Cgalvispadilla/project-final-data-science")    
    

elif choose == "Predecir":
    with st.container():
        st.markdown('Hola, aqui va una info grafica')
        st.markdown('Hola, aquí va una info grafica')
elif choose == "Home":
    with st.container():
        st.title('Hola, bienvenido a la plataforma de predicción de violencia intrafamiliar')
        st.plotly_chart(grafica_cantidad_sobre_tiempo(df), use_container_width=False)            

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
