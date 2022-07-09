# This is a sample Python script.

# Press Mayús+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import streamlit as st
import pandas as pd
import datetime
import plotly.express as px
import plotly.graph_objects as go



def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

def grafica_cantidad_sobre_tiempo(df):
    df_grp = df.groupby(['Año'])['CANTIDAD'].sum().reset_index()
    fig = px.line(df_grp, x='Año', y="CANTIDAD", height =650, title='CANTIDAD DE CASOS DE VIOLENCIA INTRAFAMILIAR POR AÑO')
    return fig.show()

@st.cache(allow_output_mutation=True)
def cargar_datos():
    return pd.read_csv("Violencia_Intrafamiliar_Colombia_Clear.csv")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    st.set_page_config(page_title='Diplomado UniCor', layout='wide')
    df=cargar_datos();
    col1, col2 = st.columns([1, 3])
    col1.markdown('''
    # Soy un header en markdown
    Queda bonito :) 
    **Poner en negrilla**
    ''')
    col1, col2 = st.columns([1, 3])
    col2.plotly_chart(grafica_cantidad_sobre_tiempo(df), use_container_width=True)
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
