import csv
import pandas as pd

from config import EXPECTED_COLUMNS


class Parser:

    def parse(self, file_path):

        header = self._read_header(file_path)
        header = self._normalize_header(header)
        self._validate_header(header)
        dataframe = self._load_dataframe(file_path)

        return dataframe

    def _read_header(self, file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            reader = csv.reader(file)

            return next(reader)

    def _normalize_header(self, header):
        normalized = header.copy()
        normalized[1] = "jyv"

        return normalized

    def _validate_header(self, header):
        if len(header) != len(EXPECTED_COLUMNS):
            raise ValueError(
                f"Layout inválido. Se esperaban {len(EXPECTED_COLUMNS)} columnas."
            )

        if header != EXPECTED_COLUMNS:
            raise ValueError(
                "El encabezado del archivo no coincide con el layout esperado."
            )

    def _load_dataframe(self, file_path):
        dataframe = pd.read_csv(
            file_path,
            dtype=str
        )
        dataframe.columns = EXPECTED_COLUMNS
        dataframe.replace("-", None, inplace=True)

        return dataframe