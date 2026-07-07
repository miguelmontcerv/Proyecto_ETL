import pandas as pd
from datetime import datetime


class Transformer:

    def transform(self, df: pd.DataFrame):
        visitante_df = self._build_visitante(df)

        estadistica_df = self._build_estadistica(df)

        return visitante_df, estadistica_df
    
    def _build_visitante(self, df: pd.DataFrame):
        visitante = df.copy()

        visitante["Fecha envio"] = pd.to_datetime(
            visitante["Fecha envio"],
            format="%d/%m/%Y %H:%M"
        )

        current_year = datetime.now().year
        current_month = datetime.now().month

        # Calcula las visitas del año actual
        visitas_anio = (
            visitante[visitante["Fecha envio"].dt.year == current_year]
            .groupby("email")
            .size()
        )

        # Calcula las visitas del mes actual
        visitas_mes = (
            visitante[
                (visitante["Fecha envio"].dt.year == current_year)
                &
                (visitante["Fecha envio"].dt.month == current_month)
            ]
            .groupby("email")
            .size()
        )

        # Calcula la primera y ultima visita, asi como visitas totales
        visitante = (
            visitante
            .groupby("email")
            .agg(
                fechaPrimeraVisita=("Fecha envio", "min"),
                fechaUltimaVisita=("Fecha envio", "max"),
                visitasTotales=("email", "count")
            )
            .reset_index()
        )

        # Mapea las visitas del año en el dataframe, si no hay dato, pone cero
        visitante["visitasAnioActual"] = (
            visitante["email"]
            .map(visitas_anio)
            .fillna(0)
            .astype(int)
        )

        # Mapea las visitas del mes en el dataframe, si no hay dato, pone cero
        visitante["visitasMesActual"] = (
            visitante["email"]
            .map(visitas_mes)
            .fillna(0)
            .astype(int)
        )

        visitante["fechaPrimeraVisita"] = visitante["fechaPrimeraVisita"].dt.date
        visitante["fechaUltimaVisita"] = visitante["fechaUltimaVisita"].dt.date

        return visitante
    
    def _build_estadistica(self, df):
        estadistica = df.copy()

        date_columns = [
            "Fecha envio",
            "Fecha open",
            "Fecha click"
        ]

        for column in date_columns:
            estadistica[column] = pd.to_datetime(
                estadistica[column],
                format="%d/%m/%Y %H:%M",
                errors="coerce"
            )

        return estadistica
    