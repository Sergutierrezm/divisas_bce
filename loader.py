import pandas as pd
import os
from sqlalchemy import create_engine, text, inspect
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

def existen_datos_fecha(fecha, nombre_tabla):
    """Comprueba si ya existen registros para una fecha concreta en PostgreSQL."""
    try:
        engine = obtener_motor_bd()
        
        # Si la tabla todavía no existe, devolvemos False directamente
        if not inspect(engine).has_table(nombre_tabla):
            return False

        query = text(f"SELECT COUNT(*) FROM {nombre_tabla} WHERE fecha_actualizacion = :fecha")
        with engine.connect() as conn:
            cantidad = conn.execute(query, {"fecha": fecha}).scalar()
            return cantidad > 0

    except Exception as e:
        print(f"Error al consultar la base de datos: {e}")
        return False

def cargar_a_postgres(df, nombre_tabla):
    """Recibe un DataFrame procesado y lo añade (append) al histórico en PostgreSQL."""
    if df is None or df.empty:
        print("Error en Carga: El DataFrame recibido está vacío.")
        return False
        
    try:
        print(f"Conectando a PostgreSQL para insertar en '{nombre_tabla}'...")
        engine = obtener_motor_bd()
        
        # if_exists='append' añade los nuevos registros sin borrar los días anteriores
        df.to_sql(
            name=nombre_tabla, 
            con=engine, 
            if_exists='append', 
            index=False
        )
        
        print(f"Éxito: {len(df)} tipos de cambio añadidos a la tabla '{nombre_tabla}'.")
        return True
        
    except Exception as e:
        print(f"Error crítico en la base de datos: {e}")
        return False