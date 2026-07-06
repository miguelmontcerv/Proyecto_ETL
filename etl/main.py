from pathlib import Path

from parser import Parser
from validator import Validator
from transformer import Transformer
from database import Database
from sftp_client import SFTPClient
from backup import Backup
from logger import Logger

from config import (
    HOST,
    PORT,
    USERNAME,
    PASSWORD,
    REMOTE_PATH,
    BACKUP_PATH,
    DOWNLOAD_PATH,
    MYSQL_HOST,
    MYSQL_DATABASE,
    MYSQL_USER,
    MYSQL_PASSWORD
)


def main():

    sftp = SFTPClient(
        HOST,
        PORT,
        USERNAME,
        PASSWORD
    )

    database = Database(
        MYSQL_HOST,
        MYSQL_DATABASE,
        MYSQL_USER,
        MYSQL_PASSWORD
    )

    parser = Parser()
    validator = Validator()
    transformer = Transformer()
    backup = Backup()
    logger = Logger()
    archivos_procesados = []

    # Conectamos con la base de datos y el sftp
    database.connect()
    sftp.connect()

    logger.info("Buscando archivos...")

    archivos = sftp.list_files(REMOTE_PATH)

    logger.info(f"{len(archivos)} encontrados.\n")

    for archivo in archivos:

        # Solo archivos válidos
        if not archivo.startswith("report_"):
            continue

        if not archivo.endswith(".txt"):
            continue

        # Verifica si ya fue procesado
        if database.file_processed(archivo):

            logger.warning(f"{archivo} ya fue procesado. Se omite.\n")
            continue

        logger.info(f"Procesando: {archivo}")

        # Descargamos el archivo en la carpeta local
        Path(DOWNLOAD_PATH).mkdir(
            parents=True,
            exist_ok=True
        )

        remote_file = f"{REMOTE_PATH}/{archivo}"
        local_file = Path(DOWNLOAD_PATH) / archivo

        sftp.download_file(
            remote_file,
            str(local_file)
        )

        # Lo convertimos en un dataframe (con la estructura solicitada -jyv-)
        dataframe = parser.parse(local_file)

        
        # Validamos el email y la fecha por cada registro del dataframe
        valid_df, error_df = validator.validate(dataframe)

        logger.info(f"Registros válidos : {len(valid_df)}")
        logger.info(f"Registros error   : {len(error_df)}")

        # Generamos los dataframes a vaciar en las tablas 'visitante' y 'estadistica' con los formatos y datos correspondientes
        visitante_df, estadistica_df = transformer.transform(valid_df)

        # Insertamos estadisticas en su tabla de la BD
        database.insert_estadistica(
            estadistica_df
        )

        # Insertamos visitante en su tabla de la BD
        database.upsert_visitante(
            visitante_df
        )

        # Si hubieron errores, los registramos en la BD
        if not error_df.empty:
            database.insert_errores(
                archivo,
                error_df
            )
        
        # Registramos que el archivo ya fue procesado y cuantos registros fueron validos e invalidos
        database.register_file(
            archivo,
            len(valid_df),
            len(error_df)
        )

        # Agregamos el archivo en la lista de procesados
        archivos_procesados.append(local_file)

        # Eliminamos el archivo remoto
        sftp.delete_file(remote_file)

        logger.info("-" * 60)

    # Comprimimos los archivos del día, los eliminamos remota y localmente, y guardamos el zip local
    if archivos_procesados:
        backup.compress(
            archivos_procesados,
            BACKUP_PATH
        )

        for archivo in archivos_procesados:
            archivo.unlink()
            logger.info(f"Archivo local eliminado: {archivo}")

    # Cerramos las conexiones
    sftp.disconnect()
    database.disconnect()


if __name__ == "__main__":
    main()