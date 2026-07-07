from pathlib import Path
import zipfile
from datetime import datetime
from logger import Logger


class Backup:

    def compress(self, files, backup_folder):
        logger = Logger()

        Path(backup_folder).mkdir(
            parents=True,
            exist_ok=True
        )

        # Podemos cambiar al formato de fecha que queramos
        zip_name = datetime.now().strftime(
            "backup_%Y%m%d.zip"
        )

        zip_path = Path(backup_folder) / zip_name

        with zipfile.ZipFile(
            zip_path,
            "w",
            compression=zipfile.ZIP_DEFLATED
        ) as zip_file:

            for file in files:

                zip_file.write(
                    file,
                    arcname=file.name
                )

        logger.info(f"Backup creado: {zip_path}")