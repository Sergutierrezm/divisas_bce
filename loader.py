import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

def obtener_motor_bd():
    """Lee el archivo .env y crea el motor de conexión a PostgreSQL."""
    load_dotenv()
    cadena = (
        f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )
    return create_engine(cadena)

def cargar_bronze(df):
    """UPSERT de las 29 divisas crudas en bronze.tipos_cambio_raw."""
    if df is None or df.empty:
        return False

    query = text("""
        INSERT INTO bronze.tipos_cambio_raw (fecha_actualizacion, moneda_base, moneda_destino, tasa_cambio)
        VALUES (:fecha_actualizacion, :moneda_base, :moneda_destino, :tasa_cambio)
        ON CONFLICT (fecha_actualizacion, moneda_destino)
        DO UPDATE SET
            tasa_cambio = EXCLUDED.tasa_cambio,
            fecha_ingesta = CURRENT_TIMESTAMP;
    """)

    try:
        engine = obtener_motor_bd()
        with engine.begin() as conn:
            conn.execute(query, df.to_dict(orient="records"))
        print(f"Bronze actualizado: {len(df)} registros procesados (UPSERT).")
        return True
    except Exception as e:
        print(f"Error en carga Bronze: {e}")
        return False

def cargar_silver(df):
    """UPSERT de las divisas filtradas en silver.tipos_cambio_limpio."""
    if df is None or df.empty:
        return False

    query = text("""
        INSERT INTO silver.tipos_cambio_limpio (fecha_actualizacion, moneda_base, moneda_destino, tasa_cambio)
        VALUES (:fecha_actualizacion, :moneda_base, :moneda_destino, :tasa_cambio)
        ON CONFLICT (fecha_actualizacion, moneda_destino)
        DO UPDATE SET tasa_cambio = EXCLUDED.tasa_cambio;
    """)

    try:
        engine = obtener_motor_bd()
        with engine.begin() as conn:
            conn.execute(query, df.to_dict(orient="records"))
        print(f"Silver actualizado: {len(df)} registros procesados (UPSERT).")
        return True
    except Exception as e:
        print(f"Error en carga Silver: {e}")
        return False

def leer_silver():
    """Lee todo el histórico de Silver para calcular métricas de negocio en Gold."""
    try:
        engine = obtener_motor_bd()
        query = "SELECT fecha_actualizacion, moneda_base, moneda_destino, tasa_cambio FROM silver.tipos_cambio_limpio;"
        return pd.read_sql(query, engine)
    except Exception as e:
        print(f"Error al leer Silver: {e}")
        return None

def cargar_gold(df):
    """UPSERT de métricas de negocio en gold.resumen_divisas."""
    if df is None or df.empty:
        return False

    query = text("""
        INSERT INTO gold.resumen_divisas (fecha_actualizacion, moneda_base, moneda_destino, tasa_cambio, variacion_diaria_pct)
        VALUES (:fecha_actualizacion, :moneda_base, :moneda_destino, :tasa_cambio, :variacion_diaria_pct)
        ON CONFLICT (fecha_actualizacion, moneda_destino)
        DO UPDATE SET
            tasa_cambio = EXCLUDED.tasa_cambio,
            variacion_diaria_pct = EXCLUDED.variacion_diaria_pct;
    """)

    # Convertimos cualquier NaN de Pandas a None real de Python (NULL en PostgreSQL)
    registros = [
        {k: (None if pd.isna(v) else v) for k, v in fila.items()}
        for fila in df.to_dict(orient="records")
    ]

    try:
        engine = obtener_motor_bd()
        with engine.begin() as conn:
            conn.execute(query, registros)
        print(f"Gold actualizado: {len(registros)} registros procesados (UPSERT).")
        return True
    except Exception as e:
        print(f"Error en carga Gold: {e}")
        return False