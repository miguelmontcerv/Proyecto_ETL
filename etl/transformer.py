import pandas as pd
from datetime import datetime


class Transformer:

    def transform(self, df: pd.DataFrame):
        visitante_df = self._build_visitante(df)

        estadistica_df = self._build_estadistica(df)
        estadistica_df = self._convert_dates(estadistica_df)

        return visitante_df, estadistica_df
    
    def _build_visitante(self, df: pd.DataFrame):
        visitante = df.copy()

        visitante["Fecha envio"] = pd.to_datetime(
            visitante["Fecha envio"],
            format="%d/%m/%Y %H:%M"
        )

        current_year = datetime.now().year
        current_month = datetime.now().month

        visitas_anio = (
            visitante[visitante["Fecha envio"].dt.year == current_year]
            .groupby("email")
            .size()
        )

        visitas_mes = (
            visitante[
                (visitante["Fecha envio"].dt.year == current_year)
                &
                (visitante["Fecha envio"].dt.month == current_month)
            ]
            .groupby("email")
            .size()
        )

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

        visitante["visitasAnioActual"] = (
            visitante["email"]
            .map(visitas_anio)
            .fillna(0)
            .astype(int)
        )

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

        return estadistica
    
    def _convert_dates(self, dataframe):
        date_columns = [
            "Fecha envio",
            "Fecha open",
            "Fecha click"
        ]

        for column in date_columns:

            dataframe[column] = pd.to_datetime(
                dataframe[column],
                format="%d/%m/%Y %H:%M",
                errors="coerce"
            )

        return dataframe