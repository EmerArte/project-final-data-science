# This is a sample Python script.

# Press Mayús+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
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


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

def grafica_cantidad_sobre_tiempo(df):
    df_grp = df.groupby(['Año'])['CANTIDAD'].sum().reset_index()
    return px.line(df_grp, x='Año', y="CANTIDAD", height =650, title='CANTIDAD DE CASOS DE VIOLENCIA INTRAFAMILIAR POR AÑO', width=1000)

@st.cache(allow_output_mutation=True)
def cargar_datos():
    return pd.read_csv("Violencia_Intrafamiliar_Colombia_Clear.csv")

# Press the green button in the gutter to run the script.

st.set_page_config(page_title='Violencia intrafamiliar', layout='wide')
df=cargar_datos();
col1, col2 = st.columns([1, 3])


with st.sidebar:
    choose = option_menu("DASHBOARD", ["Home", "Más detalles", "Predecir", "Contacto"],
                         icons=['house', 'kanban', 'book','person lines fill'],
                         menu_icon="app-indicator", default_index=0,
                         styles={
        "container": {"padding": "5!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "25px"}, 
        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#02ab21"},
    }
    )

if choose == "Más detalles":
    with col1:
        st.markdown('Hola, aqui va una info grafica')
    with col2:
        st.markdown('Hola, aqui va una info grafica')    
    
elif choose == "Contacto":
    with col1:              
        st.markdown(""" <style> .font {
        font-size:20px ; font-family: 'Cooper Black'; color: #FF9633;} 
        </style> """, unsafe_allow_html=True)
        st.markdown('<p class="font">Acerca de los creadores</p>', unsafe_allow_html=True)    
    with col2:              
       st.markdown(""" <style> .font {
        font-size:20px ; font-family: 'Cooper Black'; color: #FF9633;} 
        </style> """, unsafe_allow_html=True)
    st.write("Somos unos estudiantes de ingeniería de sistemas que queremos que puedas conocernos y nos ayudes a mejorar, si tienes alguna duda o sugerencia puedes contactarnos en el siguiente correo: fktcg99@gmail.com, tambien puedes aportar a nuestro proyecto en github: https://github.com/Cgalvispadilla/project-final-data-science")    
    

elif choose == "Predecir":
    with col1:
        st.markdown('Hola, aqui va una info grafica')
    with col2:
        st.markdown('Hola, aquí va una info grafica')
elif choose == "Home":
    with col1:
        st.markdown(""" <style> .font {
        font-size:20px ; font-family: 'Cooper Black'; color: #FF9633;} 
        </style> """, unsafe_allow_html=True)
        st.markdown('<p class="font"> Conclusiones de la grafica iran aquí</p>', unsafe_allow_html=True)
    with col2:
        st.title('Hola, bienvenido a la plataforma de predicción de violencia intrafamiliar')
        st.markdown(""" <style> .font {
        font-size:20px ; font-family: 'Cooper Black'; color: #000000;} 
        </style> """, unsafe_allow_html=True)
        st.plotly_chart(grafica_cantidad_sobre_tiempo(df), use_container_width=False)            

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
