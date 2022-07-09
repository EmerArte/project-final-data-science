"""Universidad de Córdoba"""


from fastapi import FastAPI

from typing import List
from clases import OutputModelo, InputModelo, APIModelBackEnd

# Creamos el objeto app
app = FastAPI(title="API de Machine Learning del Diplomado", version="1.0.0")
"""Objeto FastAPI usado para el deployment de la API :)"""

 #response_model=List[OutputModelo]

@app.post("/predict")
async def predict_proba(inputs: List[InputModelo]):
    """Endpoint de predicción de la API"""
    # Creamos una lista vacía con las respuestas
    response = list()
    # Iteramos por todas las entradas que damos
    for Input in inputs:
        # Usamos nuestra Clase en el backend para predecir con nuestros inputs.
        # Esta sería la línea que cambiamos en este archivo, podemos los inputs que necesitemos.
        # Esto es, poner Input.Nombre_Atributo
        model = APIModelBackEnd(
            Input.departamento,
            Input.genero,
            Input.grupo_etario,
            Input.armas_medio,
            Input.fecha
        )
        print(model.predecir())
        response.append(model.predecir()[0])
    # Retorna  la lista con todas las predicciones hechas.
    return response