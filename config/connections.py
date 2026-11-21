import mysql
import mysql.connector
from dotenv import load_dotenv
load_dotenv()
import os

class DatabaseConnection:
    def __init__(self, host:str, user:str, password: str, database:str):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.mydb = None

    async def get_db_connection(self):
        if self.mydb is None:
            self.mydb = mysql.connector.connect(
                host=os.getenv("DB_HOST", "127.0.0.1"),
                user=os.getenv("DB_USER", "admin"),
                password=os.getenv("DB_PASS", "1234567890"),
                database=os.getenv("DB_NAME", "myDB"),
                port=int(os.getenv("DB_PORT", "3306")),
                )
        return self.mydb
        