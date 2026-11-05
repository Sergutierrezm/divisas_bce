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

    # Cadena de conexión estándar para PostgreSQL con psycopg2
    cadena = f"postgresql+psycopg2://{usuario}:{contrasena}@{host}:{puerto}/{base}"
    return create_engine(cadena)

def cargar_a_postgres(df, nombre_tabla):
    """
    Recibe un DataFrame procesado y lo guarda en PostgreSQL.
    """
    
    # 1. Defensa: No intentar conectar a BD si no hay datos
    if df is None or df.empty:
        print("Error en Carga: El DataFrame recibido está vacío.")
        return False
        
    try:
        print(f"Conectando a PostgreSQL para insertar en '{nombre_tabla}'...")
        engine = obtener_motor_bd()
        
        # 2. Inserción de datos
        # if_exists='replace': Borra la tabla si existe y la crea de nuevo con los datos frescos.
        # En un sistema de precios actualizados al minuto, 'replace' es útil para tener siempre "la foto actual".
        # Si quisieras un histórico, usarías 'append' (pero habría que añadir una columna con la fecha de extracción).
        df.to_sql(
            name=nombre_tabla, 
            con=engine, 
            if_exists='replace', 
            index=False # Crucial: Evita crear una columna inútil con los índices numéricos (0, 1, 2...) de Pandas
        )
        
        print(f"Éxito: {len(df)} gasolineras guardadas en la tabla '{nombre_tabla}'.")
        return True
        
    except Exception as e:
        print(f"Error crítico en la base de datos: {e}")
        return False