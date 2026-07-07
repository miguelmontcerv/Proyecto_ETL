import mysql.connector
import pandas as pd

from logger import Logger


class Database:

    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password

        self.connection = None
        self.cursor = None
        self.logger = Logger()

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )

            self.cursor = self.connection.cursor()
            self.logger.info("Conexión a MySQL exitosa.")

        except mysql.connector.Error as err:
            self.logger.error(f"Error al conectar a MySQL: {err}")

    def disconnect(self):
        try:
            if self.cursor:
                self.cursor.close()

            if self.connection and self.connection.is_connected():
                self.connection.close()

            self.logger.info("Conexión cerrada.")

        except mysql.connector.Error as err:
            self.logger.error(f"Error al cerrar la conexión: {err}")

    def file_processed(self, filename):
        try:
            query = """
                SELECT 1
                FROM control_cargas
                WHERE archivo = %s
                LIMIT 1
            """

            self.cursor.execute(query, (filename,))
            return self.cursor.fetchone() is not None

        except mysql.connector.Error as err:
            self.logger.error(f"Error consultando control_cargas: {err}")
            return False

    def register_file(self, filename, processed_records, error_records):
        try:
            query = """
                INSERT INTO control_cargas
                (
                    archivo,
                    registrosProcesados,
                    registrosError
                )
                VALUES
                (
                    %s,
                    %s,
                    %s
                )
            """

            self.cursor.execute(
                query,
                (
                    filename,
                    processed_records,
                    error_records
                )
            )

            self.connection.commit()
            self.logger.info(f"{filename} registrado en control_cargas.")

        except mysql.connector.Error as err:
            self.connection.rollback()
            if err.errno == 1062:
                self.logger.error(f"El archivo '{filename}' ya estaba registrado.")
            else:
                self.logger.error(f"Error registrando archivo: {err}")
    
    def insert_estadistica(self, dataframe):
        try:
            query = """
                INSERT INTO estadistica
                (
                    email,
                    jyv,
                    Badmail,
                    Baja,
                    FechaEnvio,
                    FechaOpen,
                    Opens,
                    OpensVirales,
                    FechaClick,
                    Clicks,
                    ClicksVirales,
                    Links,
                    IPs,
                    Navegadores,
                    Plataformas
                )
                VALUES
                (
                    %s,%s,%s,%s,%s,
                    %s,%s,%s,%s,%s,
                    %s,%s,%s,%s,%s
                )
            """

            for _, row in dataframe.iterrows():
                values = tuple(
                    None if pd.isna(value) else value
                    for value in (
                        row["email"],
                        row["jyv"],
                        row["Badmail"],
                        row["Baja"],
                        row["Fecha envio"],
                        row["Fecha open"],
                        row["Opens"],
                        row["Opens virales"],
                        row["Fecha click"],
                        row["Clicks"],
                        row["Clicks virales"],
                        row["Links"],
                        row["IPs"],
                        row["Navegadores"],
                        row["Plataformas"]
                    )
                )

                self.cursor.execute(query, values)

            self.connection.commit()
            self.logger.info(f"{len(dataframe)} registros insertados en estadistica.")

        except mysql.connector.Error as err:
            self.connection.rollback()
            self.logger.error(f"Error insertando estadistica: {err}")

    def upsert_visitante(self, dataframe):
        try:
            select_query = """
                SELECT
                    fechaUltimaVisita,
                    visitasTotales,
                    visitasAnioActual,
                    visitasMesActual
                FROM visitante
                WHERE email = %s
            """

            insert_query = """
                INSERT INTO visitante
                (
                    email,
                    fechaPrimeraVisita,
                    fechaUltimaVisita,
                    visitasTotales,
                    visitasAnioActual,
                    visitasMesActual
                )
                VALUES
                (
                    %s,%s,%s,%s,%s,%s
                )
            """

            update_query = """
                UPDATE visitante
                SET
                    fechaUltimaVisita = %s,
                    visitasTotales = %s,
                    visitasAnioActual = %s,
                    visitasMesActual = %s
                WHERE email = %s
            """

            inserts = 0
            updates = 0

            for _, row in dataframe.iterrows():

                # Buscar si el visitante ya existe
                self.cursor.execute(
                    select_query,
                    (row["email"],)
                )

                result = self.cursor.fetchone()

                if result is None:

                    self.cursor.execute(
                        insert_query,
                        (
                            row["email"],
                            row["fechaPrimeraVisita"],
                            row["fechaUltimaVisita"],
                            row["visitasTotales"],
                            row["visitasAnioActual"],
                            row["visitasMesActual"]
                        )
                    )

                    inserts += 1

                else:

                    fecha_bd = result[0]
                    total_bd = result[1]
                    anio_bd = result[2]
                    mes_bd = result[3]

                    nueva_fecha = max(
                        fecha_bd,
                        row["fechaUltimaVisita"]
                    )

                    nuevo_total = (
                        total_bd
                        + row["visitasTotales"]
                    )

                    # Debemos de validar que sea el mismo mes y mismo año
                    nuevo_anio = (
                        anio_bd
                        + row["visitasAnioActual"]
                    )

                    nuevo_mes = (
                        mes_bd
                        + row["visitasMesActual"]
                    )

                    self.cursor.execute(
                        update_query,
                        (
                            nueva_fecha,
                            nuevo_total,
                            nuevo_anio,
                            nuevo_mes,
                            row["email"]
                        )
                    )

                    updates += 1

            self.connection.commit()

            self.logger.info(f"Visitantes insertados : {inserts}")
            self.logger.info(f"Visitantes actualizados: {updates}")

        except mysql.connector.Error as err:
            self.connection.rollback()
            self.logger.error(f"Error haciendo upsert de visitante: {err}")

    def insert_errores(self, archivo, dataframe):
        try:
            query = """
                INSERT INTO errores
                (
                    archivo,
                    email,
                    motivo
                )
                VALUES
                (
                    %s,
                    %s,
                    %s
                )
            """

            for _, row in dataframe.iterrows():

                self.cursor.execute(
                    query,
                    (
                        archivo,
                        row["email"],
                        row["motivo"]
                    )
                )

            self.connection.commit()

            self.logger.info(f"{len(dataframe)} registros insertados en errores.")

        except mysql.connector.Error as err:
            self.connection.rollback()
            self.logger.error(f"Error insertando errores: {err}")