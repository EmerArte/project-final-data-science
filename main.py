import streamlit as st
import pandas as pd
import datetime
import plotly.express as px
from streamlit_option_menu import option_menu
import plotly.graph_objects as go
import numpy as np
import requests
import json
import time



def graphy_serie_time(df):
    df_grp = df.groupby(['FECHA HECHO'])['CANTIDAD'].sum().reset_index()
    fig = px.line(df_grp, x='FECHA HECHO', y="CANTIDAD", title='CANTIDAD DE CASOS DE VIOLENCIA INTRAFAMILIAR POR DÍA',
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
    df_h_año = df[df.GENERO == 'MASCULINO'].groupby(['Año'])['CANTIDAD'].sum().reset_index()
    df_f_año = df[df.GENERO == 'FEMENINO'].groupby(['Año'])['CANTIDAD'].sum().reset_index()
    df_h_año['cambio_porcentual'] = round((df_h_año['CANTIDAD'].pct_change()*100),0)
    df_f_año['cambio_porcentual'] = round((df_f_año['CANTIDAD'].pct_change()*100),0)
    df_h_año = df_h_año[df_h_año.Año < 2021]
    df_f_año = df_f_año[df_f_año.Año < 2021]
    df_f_año = df_f_año.dropna()
    df_h_año = df_h_año.dropna()

    labels = ['Masculino', 'Femenino']
    colors = ['#90CAF9', '#F48FB1']

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
                                text='INCREMENTO PORCENTUAL ANUAL EN CASOS REPORTADOS POR GÉNERO',
                                font=dict(family='Arial',
                                            size=12,
                                            color='black'),
                                showarrow=False))
    fig.update_layout(annotations=annotations)
    return fig

def graphy_case_depto(df):
    df_grp1 = df.groupby(['DEPARTAMENTO'])['CANTIDAD'].sum().reset_index()
    fig = px.bar(df_grp1.sort_values(by='CANTIDAD', ascending=False), x='DEPARTAMENTO', y='CANTIDAD', title='CANTIDAD DE CASOS DE VIOLENCIA INTRAFAMILIAR POR DEPARTAMENTO', height =700)
    fig.update_xaxes(tickangle=-90)
    return fig
def graphy_grupo_etario(df, df_departament = "CÓRDOBA", df_grupo = "MENORES"):
    df_grp9 = df.groupby(['DEPARTAMENTO', 'ARMAS MEDIOS', 'GRUPO ETARIO'])['CANTIDAD'].sum().reset_index()
    df_grp9 = df_grp9[(df_grp9['DEPARTAMENTO'] == str(df_departament))]
    df_grp9 = df_grp9[(df_grp9['GRUPO ETARIO'] == str(df_grupo))]
    fig = px.bar(df_grp9.sort_values(by='CANTIDAD', ascending=True), x="GRUPO ETARIO", y='CANTIDAD',
                 color="ARMAS MEDIOS", title="CASOS DE VIOLENCIA INTRAFAMILIAR POR GRUPO ETARIO EN {}".format(df_departament),
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
def graphy_day_of_week_depto(df,df_departament):
    df_grp5 = df.groupby(['DEPARTAMENTO', 'Dia de la semana', 'GENERO'])['CANTIDAD'].sum().reset_index()
    df_grp5 = df_grp5[(df_grp5['DEPARTAMENTO'] == str(df_departament))]
    fig = px.bar(df_grp5.sort_values(by='CANTIDAD', ascending=False), x="Dia de la semana", y='CANTIDAD',
                 color="GENERO",
                 title="Número de casos de violencia intrafamiliar por día de la semana en el departamento '{}'".format(df_departament), barmode='group',
                 color_discrete_map={"MASCULINO": "#90CAF9",
                                     "FEMENINO": "#F48FB1",
                                     "NO REPORTA": "#00A5CF",
                                     })
    fig.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)', 'paper_bgcolor': 'rgba(0,0,0,0)'})
    return fig
@st.cache(allow_output_mutation=True)
def cargar_datos():
    return pd.read_csv("Violencia_Intrafamiliar_Colombia.csv")
def calcular_prediccion(departament, grupo_etario, genero, fecha, arma_medio):
    request_data = [{"departamento": departament,
                     "genero": genero,
                     "grupo_etario": grupo_etario,
                     "armas_medio": arma_medio,
                     "fecha": fecha}]
    data_cleaned = str(request_data).replace("'", '"')
    url_api = "https://backed-api-data-science.herokuapp.com/predict"
    pred = requests.post(url=url_api, json=json.loads(data_cleaned),headers={"Content-Type": "application/json"}).text
    pred_df = json.loads(pred)
    return pred_df[0]

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
        div.row-widget button{
            width: 100%;
        }
        .title_personalized{
            font-size: 1rem;
            font-weight: bold;
            text-color: var(--text-color) !important;
            color: var(--text-color) !important;
            text-decoration: none;
            margin: 0 0.4rem;
        }
        
    </style>
    """, unsafe_allow_html=True)

with st.sidebar:
    choose = option_menu("DASHBOARD", ["Home", "Predecir", "Contacto"],
                         icons=['house', 'graph-up', 'person lines fill'],
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
                'Saludos, bienvenidos a la plataforma de predicción de violencia intrafamiliar en Colombia')
        st.markdown("""
        <p>
        Este estudio fue realizado con la información recolectada durante la última década, y tiene como objetivo predecir la cantidad de casos de violencia intrafamiliar que se presentan en el país.        Este estudio fue realizado con la informacion recolectada durante la ultima decada, y tiene como objetivo predecir la cantidad de casos de violencia intrafamiliar que se presentan en el pais.
        <br>
        A continuación encontrará información general acerca del panorama de casos de violencia intrafamiliar en Colombia, y una breve descripción de cada uno de los datos que se recolectan.        </p>
        """, unsafe_allow_html=True)   
        
        with st.container():
            st.plotly_chart(graphy_serie_time(df),use_container_width=True)
            st.markdown("""
            <p>
            Esta gráfica muestra la cantidad de casos de violencia intrafamiliar que se presentan en el país en cada uno de los años de la historia.
            Observamos que la cantidad de casos de violencia intrafamiliar que se presentan en el país aumenta progresivamente a medida que avanza el tiempo. Además, observamos que durante el transcurso de los años, comúnmente se ve un aumento en la cantidad de casos de violencia intrafamiliar en el mes de enero, específicamente encontramos un mayor número de casos en año nuevo, probablemente esto esté relacionado con el alcohol y las fiestas de fin de año.
            <br>
            </p>
            <hr>
            """, unsafe_allow_html=True)
            with st.container():
                st.subheader("La violencia intrafamiliar por departamento")
                st.markdown("""
                <p>
                A continuación encontrará una gráfica con la información de detallada de cada uno de los departamentos, utilice los filtros para ver la información de cada departamento.
                </p>
                """, unsafe_allow_html=True)
                col1, col2 = st.columns(2)
                with col1:
                    option = st.selectbox(key="a",
                    label ='Departamento', options=tuple(pd.unique(df['DEPARTAMENTO'])))
                    
                with col2:
                    option2 = st.selectbox(
                    'Grupo etario', tuple(pd.unique(df['GRUPO ETARIO'])))
                st.plotly_chart(graphy_grupo_etario(df,option, option2),use_container_width=True)
                st.markdown("""
                <p>
                El común denominador en los casos de violencia intrafamiliar en la mayoria de departamentos es el
                 uso de armas contundentes, además vemos un aumento en el numero de casos de violencia intrafamiliar en los adultos y uno de los departamentos con mayor cantidad de casos de violencia intrafamiliar es Cundinamarca.
                </p>
                """, unsafe_allow_html=True)
            st.subheader("La violencia intrafamiliar por género")
            with st.container():
                option3 = st.selectbox(key="b",
                label ='Departamento', options=tuple(pd.unique(df['DEPARTAMENTO'])))
                st.plotly_chart(graphy_day_of_week_depto(df, option3), use_container_width=True)
                st.markdown("""
                <p>
                En este gráfico podemos observar que la violencia intrafamiliar afecta principalmente a las mujeres, y en la mayoria de departamentos existe un mayor número de casos los el día domingo.
                <br>
                En el siguiente gráfico nos enfocaremos en el incremento porcentual con respecto al año anterior.
                </p>
                """, unsafe_allow_html=True)
                st.plotly_chart(graphy_porcentual_gender_increment(df), use_container_width=True)
                st.markdown("""
                <p>
                Para entender esta gráfica tenemos que tener en cuenta los resultados globales en cuanto al número total de casos por año, ya que como hemos venido observando la cantidad de casos de violencia intrafamiliar aumenta progresivamente a medida que avanza el tiempo. Sin embargo, en este gráfico queremos observar cuál fue el cambio porcentual basándonos en el año anterior.
                <br>
                Una vez tenemos claro lo anterior, podemos observar como durante el periodo comprendido desde 2011 hasta 2015 se estaban presentando un incremento porcentual bastante marcado. Sin embargo, los periodos posteriores a este nos demuestran
                que el número de casos con respecto al anterior no subía con el mismo ritmo que lo había hecho en los años anteriores, hasta el punto que en 2018 para los casos de violencia intrafamiliar en las mujeres el incremento porcentual fue negativo '-11%'.
                <br>
                El número de casos sigue siendo preocupante, pero a lo largo de los años estos han bajado su ritmo de crecimiento, lo cual da esperanza de que este pueda llegar a disminuir en un largo plazo.</p>
                """, unsafe_allow_html=True)


elif choose == "Contacto":
    with st.container():
        st.title('Gupo desarrollador')
        st.write("Somos unos estudiantes de ingeniería de sistemas de la Universidad De Córdoba, si tienes alguna duda o sugerencia puedes contactarnos en el siguiente correo: fktcg99@gmail.com, también puedes aportar a nuestro proyecto en GitHub: https://github.com/Cgalvispadilla/project-final-data-science")
        st.markdown("""
        <a class = "title_personalized" href="https://www.linkedin.com/in/cgalvispadilla/">CARLOS ANDRES GALVIS PADILLA</a>
        <br>
        <a class = "title_personalized" href="https://www.linkedin.com/in/emerarteaga22/">EMER ELIAS ARTEAGA CAMARGO</a>
        <br>
        <a class = "title_personalized" href="https://www.linkedin.com/in/andr%C3%A9s-otero-670a61232/">ANDRES FELIPE OTERO LOBO</a>
        <br>
        <a class = "title_personalized" href="https://www.linkedin.com/in/andres-camilo-ortiz-cogollo-3560b2243/">ANDRES CAMILO ORTIZ COGOLLO</a>
        <br>
        <a class = "title_personalized" href="https://www.linkedin.com/in/carlos-alberto-del-castillo-maussa-a3b0aa245/">CARLOS ALBERTO DEL CASTILLO MAUSSA</a>
        """,unsafe_allow_html=True)
elif choose == "Predecir":
    with st.container():
        st.title(
                'Predicción de violencia intrafamiliar en Colombia')
        st.markdown('''<p>
                        Este modelo fue entrenado con una base de datos de violencia intrafamiliar en Colombia, y se utilizó el algoritmo de regresión llamado KNeighborsRegresor.<br>
                        Rellene el siguiente formulario para realizar una predicción.
                    </p>''', unsafe_allow_html=True)
        col_1, col_2, col_3 = st.columns(3)
        col_f, col_g = st.columns(2)

        with st.container():
            with col_1:
                departament = st.selectbox(key="departament",
                        label ='Seleccione un departamento', options=tuple(pd.unique(df['DEPARTAMENTO'])))
                
            with col_2:
                grupo_etario = st.selectbox(key="grupo_etario",
                        label ='Seleccione un grupo etario', options=tuple(pd.unique(df['GRUPO ETARIO'])))
            with col_3:
                genero = st.selectbox( key="genero", label ='Seleccione un género', options=tuple(pd.unique(df['GENERO'])))
            with col_f:
                fecha = st.date_input('Seleccione el día que desea predecir', value=datetime.date.today())
            with col_g:
                arma_medio = st.selectbox( key="arma_medio", label ='Seleccione el arma medio', options=tuple(pd.unique(df['ARMAS MEDIOS'])))
            
            predecir = st.button(label='Predecir')
            
            if predecir :
                my_bar = st.progress(0)
                res = calcular_prediccion(departament, grupo_etario, genero, str(fecha), arma_medio)
                for percent_complete in range(100):
                    time.sleep(0.01)
                    my_bar.progress(percent_complete + 1)
                
                st.subheader("El pronóstico de casos de violencia intrafamiliar para los filtros seleccionados es: {}".format(round(res['cantidad_violentados'])))
            