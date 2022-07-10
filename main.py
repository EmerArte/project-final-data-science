import streamlit as st
import pandas as pd
import datetime
import plotly.express as px
from streamlit_option_menu import option_menu
import plotly.graph_objects as go
import streamlit.components.v1 as html
from PIL import Image
import numpy as np
import io


def graphy_case_anio(df):
    df_grp = df.groupby(['Año'])['CANTIDAD'].sum().reset_index()
    return px.bar(df_grp, x='Año', y="CANTIDAD", title='CANTIDAD DE CASOS DE VIOLENCIA INTRAFAMILIAR POR AÑO',
    color_discrete_sequence=['#fb8501'])

def graphy_case_depto(df):
    df_grp1 = df.groupby(['DEPARTAMENTO'])['CANTIDAD'].sum().reset_index()
    fig = px.bar(df_grp1.sort_values(by='CANTIDAD', ascending=False), x='DEPARTAMENTO', y='CANTIDAD',
                 title='CANTIDAD DE CASOS DE VIOLENCIA INTRAFAMILIAR POR DEPARTAMENTO')
    fig.update_xaxes(tickangle=-90)
    return fig

def graphy_case_top5_depto(df):
    df_grp7 = df.groupby(['DEPARTAMENTO', 'ARMAS MEDIOS'])['CANTIDAD'].sum().reset_index()
    df_grp7 = df_grp7[(df_grp7['DEPARTAMENTO'] == 'CUNDINAMARCA') | (df_grp7['DEPARTAMENTO'] == 'ANTIOQUIA') | (
                df_grp7['DEPARTAMENTO'] == 'VALLE') | (df_grp7['DEPARTAMENTO'] == 'SANTANDER') | (
                                  df_grp7['DEPARTAMENTO'] == 'BOYACÁ')]
    df_grp7 = df_grp7.sort_values(['DEPARTAMENTO', 'CANTIDAD'], ascending=False).groupby(
        ['DEPARTAMENTO', 'ARMAS MEDIOS']).head(5)
    fig = px.bar(df_grp7.sort_values(by='CANTIDAD', ascending=False), x="DEPARTAMENTO", y='CANTIDAD',
                 color="ARMAS MEDIOS",
                 title="NUMERO DE CASOS POR DÍA EN LOS 5 DEPARTAMENTOS CON MÁS VIOLENCIA INTRAFAMILIAR",
                 barmode='group',
                 color_discrete_map={"SIN EMPLEO DE ARMAS": "#273746",
                                     "CONTUNDENTES": "#28B463",
                                     "ARMA BLANCA / CORTOPUNZANTE": "#F1C40F",
                                     "ESCOPOLAMINA": "#138D75",
                                     "NO REPORTA": "#3498DB",
                                     "ARMA DE FUEGO": "red"
                                     })
    return fig
@st.cache(allow_output_mutation=True)
def cargar_datos():
    return pd.read_csv("Violencia_Intrafamiliar_Colombia_Clear.csv")


st.set_page_config(page_title='Violencia intrafamiliar', layout='wide')
df = cargar_datos()
#styles
st.markdown(
    """
    <style type="text/css">
        li.nav-item a.active i.icon {
            color: var(--text-color) !important;
            background-color: #007bff !important;
        }
        i.icon{
            color: var(--text-color);
        }
        
    </style>
    """, unsafe_allow_html=True)

with st.sidebar:
    choose = option_menu("DASHBOARD", ["Home", "Más detalles", "Predecir", "Contacto"],
                         icons=['house', 'kanban',
                                'graph-up', 'person lines fill'],
                         menu_icon="app-indicator", default_index=0,
                         styles={
        "container": {"padding": "5! important", "font-family": "sans-serif", "font-weight": "bold", "background-color": "var(--background-color)"},
        "icon": {"font-size": "25px", "font-family": "sans-serif", "font-weight": "bold"},
        "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px", "--hover-color": "var(--secondary-background-color)", "font-family": "sans-serif"},
        "nav-link-selected": {"background-color": "var(--primary-color)"},
    })

if choose == "Home":
    with st.container():
        st.title(
                'Saludos, bienvenido a la plataforma de predicción de violencia intrafamiliar en Colombia')
        st.markdown("""
        <p class ="fw-semibold fs-5 text-danger">
        Este estudio fue realizado con la informacion recolectada durante la ultima decada, y tiene como objetivo predecir la cantidad de casos de violencia intrafamiliar que se presentan en el pais.
        <br>
        A continuacion encontrará información general acerca del panorama de casos de violencia intrafamiliar en Colombia, y una breve descripcion de cada uno de los datos que se recolectan.
        </p>
        """, unsafe_allow_html=True)   
        col1, col2 = st.columns(2)
        col1.plotly_chart(graphy_case_anio(df),
                            use_container_width=False)

elif choose == "Más detalles":
    with st.container():
        st.markdown('Hola, aqui va una info grafica')
        st.multiselect("Seleccione", ["HOLA"], default=None, key=None,
                       help=None, on_change=None, args=None, kwargs=None, disabled=False)
        st.markdown('Hola, aqui va una info grafica')

elif choose == "Contacto":
    with st.container():
        st.markdown('<p class="font">Acerca de los creadores</p>',
                    unsafe_allow_html=True)
        st.write("Somos unos estudiantes de ingeniería de sistemas que queremos que puedas conocernos y nos ayudes a mejorar, si tienes alguna duda o sugerencia puedes contactarnos en el siguiente correo: fktcg99@gmail.com, tambien puedes aportar a nuestro proyecto en github: https://github.com/Cgalvispadilla/project-final-data-science")


elif choose == "Predecir":
    with st.container():
        st.markdown('Hola, aqui va una info grafica')
        st.markdown('Hola, aquí va una info grafica')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
