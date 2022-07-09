from pydantic import BaseModel as BM
from datetime import datetime
from pydantic import Field
from typing import Literal
import joblib
import pandas as pd


class InputModelo(BM):
    """
    Clase que define las entradas del modelo según las verá el usuario.
    """

    departamento: Literal[
        'ATLÁNTICO', 'BOYACÁ', 'CAQUETÁ', 'CASANARE', 'CUNDINAMARCA', 'SUCRE',
        'VALLE', 'HUILA', 'ANTIOQUIA', 'ARAUCA', 'BOLÍVAR', 'CALDAS', 'CAUCA',
        'CESAR', 'CHOCÓ', 'CÓRDOBA', 'MAGDALENA', 'META', 'NARIÑO', 'NORTE DE SANTANDER',
        'PUTUMAYO', 'RISARALDA', 'SANTANDER', 'TOLIMA', 'VAUPÉS', 'GUAVIARE', 'GUAJIRA',
        'QUINDÍO', 'AMAZONAS', 'VICHADA', 'GUAINÍA', 'SAN ANDRÉS']

    genero: Literal['MASCULINO', 'FEMENINO', 'NO REPORTA']

    grupo_etario: Literal["ADULTOS", "MENORES", "ADOLECENTES"]

    armas_medio: Literal[
        'ARMA BLANCA / CORTOPUNZANTE', 'ARMA DE FUEGO',
        'CONTUNDENTES', 'SIN EMPLEO DE ARMAS', 'ESCOPOLAMINA']

    fecha: datetime = Field(ge=datetime.date(2010, 1, 1), le=datetime.date(2021, 7, 31))

    class Config:
        schema_extra = {
            "example": {
                "departamento": 'ANTIOQUIA',
                "genero": 'MASCULINO',
                "grupo_etario": "ADULTOS",
                "armas_medio": 'ARMA BLANCA / CORTOPUNZANTE',
                "fecha": datetime.date(2010, 1, 1)
            }
        }


class OutputModelo(BM):
    """
    Clase que define la salida del modelo según la verá el usuario.
    """

    cantidad_violentados: float = Field(ge=1, le=130)

    class Config:
        scheme_extra = {
            "example": {
                "cantidad_violentados": 90,
            }
        }


class APIModelBackEnd:
    def __init__(
            self,
            departamento,
            genero,
            grupo_etario,
            armas_medio,
            fecha

    ):
        self.departamento = departamento
        self.genero = genero
        self.grupo_etario = grupo_etario
        self.armas_medio = armas_medio
        self.fecha = datetime.datetime.strptime(fecha, "%Y-%m-%d %H:%M:%S")

    def _cargar_modelo(self, model_name: str = "cambiar nombre de modelo"):
        self.model = joblib.load(model_name)

    def _preparar_datos(self):
        departamento = self.departamento
        genero = self.genero
        grupo_etario = self.grupo_etario
        armas_medio = self.armas_medio
        departamento = [0] * 33
        genero = [0] * 3
        grupo_etario = [0] * 3
        armas_medio = [0] * 6
        fecha = self.fecha
        anio = fecha.year
        mes = fecha.month
        dia = fecha.day.strftime('%A')
        dia = [0]*7
        # Crea el DataFrame en el mismo orden las columnas del X_train

        data_predict = pd.DataFrame(
            columns=['Año', 'Mes', 'DEPARTAMENTO_AMAZONAS', 'DEPARTAMENTO_ANTIOQUIA',
                     'DEPARTAMENTO_ARAUCA', 'DEPARTAMENTO_ATLÁNTICO',
                     'DEPARTAMENTO_BOLÍVAR', 'DEPARTAMENTO_BOYACÁ',
                     'DEPARTAMENTO_CALDAS', 'DEPARTAMENTO_CAQUETÁ',
                     'DEPARTAMENTO_CASANARE', 'DEPARTAMENTO_CAUCA',
                     'DEPARTAMENTO_CESAR', 'DEPARTAMENTO_CHOCÓ',
                     'DEPARTAMENTO_CUNDINAMARCA', 'DEPARTAMENTO_CÓRDOBA',
                     'DEPARTAMENTO_GUAINÍA', 'DEPARTAMENTO_GUAJIRA',
                     'DEPARTAMENTO_GUAVIARE', 'DEPARTAMENTO_HUILA',
                     'DEPARTAMENTO_MAGDALENA', 'DEPARTAMENTO_META',
                     'DEPARTAMENTO_NARIÑO', 'DEPARTAMENTO_NORTE DE SANTANDER',
                     'DEPARTAMENTO_PUTUMAYO', 'DEPARTAMENTO_QUINDÍO',
                     'DEPARTAMENTO_RISARALDA', 'DEPARTAMENTO_SAN ANDRÉS',
                     'DEPARTAMENTO_SANTANDER', 'DEPARTAMENTO_SUCRE',
                     'DEPARTAMENTO_TOLIMA', 'DEPARTAMENTO_VALLE', 'DEPARTAMENTO_VAUPÉS',
                     'DEPARTAMENTO_VICHADA', 'GENERO_FEMENINO', 'GENERO_MASCULINO',
                     'GENERO_NO REPORTA', 'GRUPO ETARIO_ADOLESCENTES',
                     'GRUPO ETARIO_ADULTOS', 'GRUPO ETARIO_MENORES',
                     'ARMAS MEDIOS_ARMA BLANCA / CORTOPUNZANTE',
                     'ARMAS MEDIOS_ARMA DE FUEGO', 'ARMAS MEDIOS_CONTUNDENTES',
                     'ARMAS MEDIOS_ESCOPOLAMINA', 'ARMAS MEDIOS_NO REPORTA',
                     'ARMAS MEDIOS_SIN EMPLEO DE ARMAS', 'Dia de la semana_Friday',
                     'Dia de la semana_Monday', 'Dia de la semana_Saturday',
                     'Dia de la semana_Sunday', 'Dia de la semana_Thursday',
                     'Dia de la semana_Tuesday', 'Dia de la semana_Wednesday'],
            data=[[anio, mes, *departamento, *genero, *grupo_etario, *armas_medio, *dia]],
        )

        # Pone el 1 en la columna que debe ir el 1

        data_predict[
            [
                x
                for x in data_predict.columns
                if ((str(departamento) in x) and (x.startswith("DEPARTAMENTO_")))
            ]
        ] = 1
        data_predict[
            [
                x
                for x in data_predict.columns
                if ((str(genero) in x) and (x.startswith("GENERO_")))
            ]
        ] = 1
        data_predict[
            [
                x
                for x in data_predict.columns
                if ((str(grupo_etario) in x) and (x.startswith("GRUPO ETARIO_")))
            ]
        ] = 1
        data_predict[
            [
                x
                for x in data_predict.columns
                if ((str(armas_medio) in x) and (x.startswith("ARMAS MEDIOS_")))
            ]
        ] = 1
        data_predict[
            [
                x
                for x in data_predict.columns
                if ((str(dia) in x) and (x.startswith("Dia de la semana_")))
            ]
        ] = 1

        return data_predict

    def predecir(self, y_name="employee_left"):
        self._cargar_modelo()
        x = self._preparar_datos()
        prediction = pd.DataFrame(self.model.predict_proba(x)[:, 1]).rename(
            columns={0: y_name}
        )
        return prediction.to_dict(orient="records")
