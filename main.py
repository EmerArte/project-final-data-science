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


def graphy_serie_time(df):
    df_grp = df.groupby(['FECHA HECHO'])['CANTIDAD'].sum().reset_index()
    fig = px.line(df_grp, x='FECHA HECHO', y="CANTIDAD", title='CANTIDAD DE CASOS DE VIOLENCIA INTRAFAMILIAR POR AÑO',
                  color_discrete_sequence=['#7BE583'])
    fig.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)', 'paper_bgcolor': 'rgba(0,0,0,0)'})
    fig.update_xaxes(rangeslider_visible=True,
                     rangeselector=dict(buttons=list(
                         [
                             dict(step='day', stepmode='backward', label='1 semana', count=7),
                             dict(step='month', stepmode='backward', label='1 mes', count=1),
                             dict(step='month', stepmode='backward', label='3 meses', count=3),
                             dict(step='year', stepmode='backward', label='1 año', count=1),
                             dict(label='Mostrar Todo', step='all')
                         ]
                     )))
    return fig

def graphy_porcentual_gender_increment(df):
    
    df_total_año = df.groupby(['Año'])['CANTIDAD'].sum().reset_index();
    df_h_año = df[df.GENERO == 'MASCULINO'].groupby(['Año'])['CANTIDAD'].sum().reset_index();
    df_f_año = df[df.GENERO == 'FEMENINO'].groupby(['Año'])['CANTIDAD'].sum().reset_index();
    df_h_año['cambio_porcentual'] = round((df_h_año['CANTIDAD'].pct_change()*100),0)
    df_f_año['cambio_porcentual'] = round((df_f_año['CANTIDAD'].pct_change()*100),0)
    df_h_año = df_h_año[df_h_año.Año < 2021]
    df_f_año = df_f_año[df_f_año.Año < 2021]
    df_f_año = df_f_año.dropna()
    df_h_año = df_h_año.dropna()


    title = 'Incremento porcentual por año'
    labels = ['Masculino', 'Femenino']
    colors = ['#7BE583', '#9EFFCA']

    mode_size = [8, 8]
    line_size = [2, 2]

    x_data = np.vstack((np.arange(2011, 2020),)*2)

    y_data = np.array([df_h_año['cambio_porcentual'],df_f_año['cambio_porcentual']])

    fig = go.Figure()

    for i in range(0, 2):
        fig.add_trace(go.Scatter(x=x_data[i], y=y_data[i], mode='lines',
            name=labels[i],
            line=dict(color=colors[i], width=line_size[i]),
            connectgaps=True,
        ))

        # endpoints
        fig.add_trace(go.Scatter(
            x=[x_data[i][0], x_data[i][-1]],
            y=[y_data[i][0], y_data[i][-1]],
            mode='markers',
            marker=dict(color=colors[i], size=mode_size[i])
        ))

    fig.update_layout(
        xaxis=dict(
            showline=True,
            showgrid=False,
            showticklabels=True,
            linecolor='rgb(204, 204, 204)',
            linewidth=2,
            ticks='outside',
            tickfont=dict(
                family='Arial',
                size=12,
                color='rgb(82, 82, 82)',
            ),
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=False,
            showticklabels=False,
        ),
        autosize=False,
        margin=dict(
            autoexpand=False,
            l=100,
            r=20,
            t=110,
        ),
        showlegend=False,
        plot_bgcolor='white'
        )
    annotations = []

    for i in range(0, 2):
        fig.add_trace(go.Scatter(x=x_data[i], y=y_data[i], mode='lines',
                name=labels[i],
                line=dict(color=colors[i], width=line_size[i]),
                connectgaps=True,
        ))

            # endpoints
        fig.add_trace(go.Scatter(
                x=[x_data[i][0], x_data[i][-1]],
                y=[y_data[i][0], y_data[i][-1]],
                mode='markers',
                marker=dict(color=colors[i], size=mode_size[i])
        ))

    fig.update_layout(
            xaxis=dict(
                showline=True,
                showgrid=False,
                showticklabels=True,
                linecolor='rgb(204, 204, 204)',
                linewidth=2,
                ticks='outside',
                tickfont=dict(
                    family='Arial',
                    size=12,
                    color='rgb(82, 82, 82)',
                ),
            ),
            yaxis=dict(
                showgrid=False,
                zeroline=False,
                showline=False,
                showticklabels=False,
            ),
            autosize=False,
            margin=dict(
                autoexpand=False,
                l=100,
                r=20,
                t=110,
            ),
            showlegend=False,
            plot_bgcolor='white'
        )

    annotations = []

    # Adding labels
    for y_trace, label, color in zip(y_data, labels, colors):
        # labeling the right_side of the plot
        annotations.append(dict(xref='paper', x=0.95, y=y_trace[9],
                                    xanchor='left', yanchor='middle',
                                    text='{}'.format(label),
                                    font=dict(family='Arial',
                                                size=10),
                                    showarrow=False))
    # Title
        annotations.append(dict(xref='paper', yref='paper', x=0.0, y=1.00,
                                xanchor='left', yanchor='bottom',
                                text='INCREMENTO PORCENTUAL ANUAL EN CASOS REPORTADOS POR GENERO',
                                font=dict(family='Arial',
                                            size=12,
                                            color='black'),
                                showarrow=False))
    fig.update_layout(annotations=annotations)
    return fig

def graphy_case_depto(df):
    df_grp1 = df.groupby(['DEPARTAMENTO'])['CANTIDAD'].sum().reset_index()
    fig = px.line(df_grp1.sort_values(by='CANTIDAD', ascending=False), x='DEPARTAMENTO', y='CANTIDAD',
                 title='CANTIDAD DE CASOS DE VIOLENCIA INTRAFAMILIAR POR DEPARTAMENTO',
                 color_discrete_sequence=['#7BE583'])
    fig.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)', 'paper_bgcolor': 'rgba(0,0,0,0)'})
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
                 color_discrete_map={"SIN EMPLEO DE ARMAS": "#9EFFCA",
                                     "CONTUNDENTES": "#26A18D",
                                     "ARMA BLANCA / CORTOPUNZANTE": "#004E64",
                                     "ESCOPOLAMINA": "#00A5CF",
                                     "NO REPORTA": "#8ECAE6",
                                     "ARMA DE FUEGO": "#3DECAF"
                                     })
    fig.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)', 'paper_bgcolor': 'rgba(0,0,0,0)'})
    return fig


def graphy_grupo_etario_top5_depto(df):
    df_grp9 = df.groupby(['DEPARTAMENTO', 'GRUPO ETARIO'])['CANTIDAD'].sum().reset_index()
    df_grp9 = df_grp9[(df_grp9['DEPARTAMENTO'] == 'CUNDINAMARCA') | (df_grp9['DEPARTAMENTO'] == 'ANTIOQUIA') | (
                df_grp9['DEPARTAMENTO'] == 'VALLE') | (df_grp9['DEPARTAMENTO'] == 'SANTANDER') | (
                                  df_grp9['DEPARTAMENTO'] == 'BOYACÁ')]

    fig = px.bar(df_grp9.sort_values(by='CANTIDAD', ascending=True), x="GRUPO ETARIO", y='CANTIDAD',
                 color="DEPARTAMENTO", title="CASOS POR GRUPO ETARIO - TOP 5 DEPARTAMENTOS MÁS VIOLENTOS",
                  barmode='group',
                 color_discrete_map={"CUNDINAMARCA": "#9EFFCA",
                                     "ANTIOQUIA": "#00A5CF",
                                     "VALLE": "#26A18D",
                                     "SANTANDER": "#004E64",
                                     "BOYACÁ": "#78E07C",
                                     })
    fig.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)', 'paper_bgcolor': 'rgba(0,0,0,0)'})
    return fig
def graphy_depto_gender(d):
    df_grp8 = df.groupby(['DEPARTAMENTO', 'ARMAS MEDIOS', 'GENERO'])['CANTIDAD'].sum().reset_index()
    df_grp8 = df_grp8[(df_grp8['ARMAS MEDIOS'] == 'ARMA DE FUEGO')]
    fig = px.bar(df_grp8.sort_values(by='CANTIDAD', ascending=False), x="DEPARTAMENTO", y="CANTIDAD", color="GENERO",
                 title="DEPARTAMENTOS CON MAYOR USO DE ARMAS DE FUEGO POR GENERO",
                 color_discrete_map={"FEMENINO": "#78E07C",
                                     "MASCULINO": "#00A5CF",
                                     })
    fig.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)', 'paper_bgcolor': 'rgba(0,0,0,0)'})
    fig.update_xaxes(tickangle=-90)
    return fig

def graphy_day_of_week_depto(df, week_day=1):
    df_grp5 = df.groupby(['DEPARTAMENTO', 'Dia de la semana'])['CANTIDAD'].sum().reset_index()
    df_grp5 = df_grp5[(df_grp5['DEPARTAMENTO'] == 'CUNDINAMARCA') | (df_grp5['DEPARTAMENTO'] == 'ANTIOQUIA') | (
                df_grp5['DEPARTAMENTO'] == 'VALLE') | (df_grp5['DEPARTAMENTO'] == 'SANTANDER') | (
                                  df_grp5['DEPARTAMENTO'] == 'BOYACÁ')]
    fig = px.bar(df_grp5.sort_values(by='CANTIDAD', ascending=False), x="Dia de la semana", y='CANTIDAD',
                 color="DEPARTAMENTO",
                 title="NUMERO DE CASOS POR DÍA EN LOS 5 DEPARTAMENTOS CON MÁS VIOLENCIA INTRAFAMILIAR", barmode='group',
                 color_discrete_map={"CUNDINAMARCA": "#78E07C",
                                     "ANTIOQUIA": "#004E64",
                                     "VALLE": "#00A5CF",
                                     "SANTANDER": "#26A18D",
                                     "BOYACÁ": "#9EFFCA",
                                     })
    fig.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)', 'paper_bgcolor': 'rgba(0,0,0,0)'})
    return fig
@st.cache(allow_output_mutation=True)
def cargar_datos():
    return pd.read_csv("Violencia_Intrafamiliar_Colombia.csv")


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
        <p>
        Este estudio fue realizado con la informacion recolectada durante la ultima decada, y tiene como objetivo predecir la cantidad de casos de violencia intrafamiliar que se presentan en el pais.
        <br>
        A continuacion encontrará información general acerca del panorama de casos de violencia intrafamiliar en Colombia, y una breve descripcion de cada uno de los datos que se recolectan.
        </p>
        """, unsafe_allow_html=True)   
        
        with st.container():
            st.plotly_chart(graphy_serie_time(df),use_container_width=True)
            st.markdown("""
            <p>
            Esta gráfica muestra la cantidad de casos de violencia intrafamiliar que se presentan en el pais en cada uno de los años de la historia.
            Observamos que la cantidad de casos de violencia intrafamiliar que se presentan en el pais aumenta progresivamente a medida que avanza el tiempo.
            Además, observamos que durante el transcurso de los años,comunmente se ve un aumento en la cantidad de casos de violencia intrafamiliar en el més de enero.
            <br>
            </p>
            """, unsafe_allow_html=True)
            st.plotly_chart(graphy_case_top5_depto(df), use_container_width=True)
            st.markdown("""
            <p>
            Esta gráfica muestra la cantidad de casos de violencia intrafamiliar que se presentan en cada uno de los 5 departamentos con más violencia intrafamiliar.
            <br>
            </p>
            """, unsafe_allow_html=True)


            st.plotly_chart(graphy_depto_gender(df), use_container_width=True)
            st.plotly_chart(graphy_day_of_week_depto(df), use_container_width=True)

elif choose == "Más detalles":
    with st.container():
        st.markdown('Hola, aqui va una info grafica')
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
