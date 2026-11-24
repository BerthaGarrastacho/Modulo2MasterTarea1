import os
from pathlib import Path

import mysql.connector
from dotenv import load_dotenv

# Lee el .env de la raíz del proyecto, sin importar desde dónde se ejecute el servicio
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

VARIABLES_REQUERIDAS = ["DB_HOST", "DB_USER", "DB_PASS", "DB_NAME", "DB_PORT"]


class DatabaseConnection:
    def __init__(self):
        # Falla al iniciar, con un mensaje claro, si falta alguna variable en .env
        faltantes = [v for v in VARIABLES_REQUERIDAS if not os.getenv(v)]
        if faltantes:
            raise RuntimeError(
                "Faltan variables en .env: " + ", ".join(faltantes)
            )
        self.mydb = None

    async def get_db_connection(self):
        if self.mydb is None:
            self.mydb = mysql.connector.connect(
                host=os.environ["DB_HOST"],
                user=os.environ["DB_USER"],
                password=os.environ["DB_PASS"],
                database=os.environ["DB_NAME"],
                port=int(os.environ["DB_PORT"]),
            )
        return self.mydb
