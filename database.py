import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return psycopg.connect(
        host = os.getenv("DB_HOST", "localhost"),
        port = os.getenv("DB_PORT", "5432"),
        dbname = os.getenv("DB_NAME", "atm_db"),
        user = os.getenv("DB_USER", "postgres"),
        password = os.getenv("DB_PASSWORD", "")
    )

