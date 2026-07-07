# config.py

# ---------- SFTP ----------
HOST = "sftp"
PORT = 22
USERNAME = "usuario"
PASSWORD = "password"
REMOTE_PATH = "data"

# ---------- Carpetas locales ----------
DOWNLOAD_PATH = "downloads"
BACKUP_PATH = "backup"
LOG_PATH = "logs"

# ---------- Validación del layout de los CSV ----------
EXPECTED_COLUMNS = [
    "email",
    "jyv",
    "Badmail",
    "Baja",
    "Fecha envio",
    "Fecha open",
    "Opens",
    "Opens virales",
    "Fecha click",
    "Clicks",
    "Clicks virales",
    "Links",
    "IPs",
    "Navegadores",
    "Plataformas"
]

# ---------- Conectar MySQL ----------
MYSQL_HOST = "mysql"
MYSQL_DATABASE = "visitas"
MYSQL_USER = "etl"
MYSQL_PASSWORD = "etl"