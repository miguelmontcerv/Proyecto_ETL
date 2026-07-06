import pandas as pd
from email_validator import validate_email, EmailNotValidError


class Validator:

    def validate(self, df: pd.DataFrame):

        df = df.copy()

        df["email_valid"] = df["email"].apply(self._validate_email)
        df["fecha_valid"] = df["Fecha envio"].apply(self._validate_date)
        df["motivo"] = ""

        df.loc[(~df["email_valid"]) & (df["fecha_valid"]), "motivo"] = "Email invalido"

        df.loc[(df["email_valid"]) & (~df["fecha_valid"]), "motivo"] = "Fecha invalida"

        df.loc[(~df["email_valid"]) & (~df["fecha_valid"]), "motivo"] = "Email y fecha invalidos"

        valid_df = df[(df["email_valid"]) & (df["fecha_valid"])].copy()
        error_df = df[~(df["email_valid"] & df["fecha_valid"])].copy()

        return valid_df, error_df
    
    def _validate_email(self, email):
        try:
            validate_email(email)
            return True
        except EmailNotValidError:
            return False
    
    def _validate_date(self, date_str):
        parsed = pd.to_datetime(
            date_str,
            format="%d/%m/%Y %H:%M",
            errors="coerce"
        )

        return not pd.isna(parsed)