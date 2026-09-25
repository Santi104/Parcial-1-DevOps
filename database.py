import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()


def obtener_conexion():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )


def obtener_productos():
    conexion = obtener_conexion()

    cursor = conexion.cursor()

    cursor.execute(
        "SELECT * FROM productos ORDER BY id;"
    )

    productos = cursor.fetchall()

    cursor.close()
    conexion.close()

    return productos