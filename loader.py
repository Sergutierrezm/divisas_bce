import pandas as pd
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

def obtener_motor_bd():
    """Lee el archivo .env y crea el motor de conexión a PostgreSQL."""
    load_dotenv()

    usuario = os.getenv("DB_USER")
    contrasena = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    puerto = os.getenv("DB_PORT")
    base = os.getenv("DB_NAME")

    cadena = f"postgresql+psycopg2://{usuario}:{contrasena}@{host}:{puerto}/{base}"
    return create_engine(cadena)

def cargar_a_postgres(df, nombre_tabla):
    """Recibe un DataFrame procesado y lo guarda en PostgreSQL."""
    if df is None or df.empty:
        print("Error en Carga: El DataFrame recibido está vacío.")
        return False
        
    try:
        print(f"Conectando a PostgreSQL para insertar en '{nombre_tabla}'...")
        engine = obtener_motor_bd()
        
        # if_exists='replace' mantiene solo la foto actual del último cierre.
        # Para guardar histórico diario, se cambiaría a 'append' con control de duplicados.
        df.to_sql(
            name=nombre_tabla, 
            con=engine, 
            if_exists='replace', 
            index=False
        )
        
        print(f"Éxito: {len(df)} tipos de cambio guardados en la tabla '{nombre_tabla}'.")
        return True
        
    except Exception as e:
        print(f"Error crítico en la base de datos: {e}")
        return False