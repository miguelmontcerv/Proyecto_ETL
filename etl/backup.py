from pathlib import Path
import zipfile
from datetime import datetime


class Backup:

    def compress(self, files, backup_folder):

        Path(backup_folder).mkdir(
            parents=True,
            exist_ok=True
        )

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

        print(f"\nBackup creado: {zip_path}")