import logging
from pathlib import Path
from datetime import datetime

class Logger:

    def __init__(self):

        Path("logs").mkdir(
            parents=True,
            exist_ok=True
        )

        filename = datetime.now().strftime(
            "logs/etl_%Y%m%d.log"
        )

        logging.basicConfig(
            filename=filename,
            level=logging.INFO,
            format="%(asctime)s | %(levelname)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        self.logger = logging.getLogger("ETL")

    def info(self, message):
        print(message)
        self.logger.info(message)

    def warning(self, message):
        print(message)
        self.logger.warning(message)

    def error(self, message):
        print(message)
        self.logger.error(message)