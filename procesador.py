import pandas as pd

def procesar_datos(df):
    """Filtra el DataFrame para quedarnos solo con las divisas estratégicas."""
    if df is None or df.empty:
        return None
        
    try:
        # 1. Filtramos solo las monedas que nos interesan para nuestro "negocio"
        divisas_top = ['USD', 'JPY', 'GBP', 'CHF']
        df_local = df[df['moneda_destino'].isin(divisas_top)].copy()
        
        # 2. Redondeamos la tasa de cambio a 2 decimales para que quede más limpio en SQL
        df_local['tasa_cambio'] = df_local['tasa_cambio'].round(2)
        
        # 3. Ordenamos las columnas para que queden bonitas en PostgreSQL
        columnas_ordenadas = ['fecha_actualizacion', 'moneda_base', 'moneda_destino', 'tasa_cambio']
        df_local = df_local[columnas_ordenadas]
        
        # 4. Ordenamos alfabéticamente por la moneda de destino
        df_local = df_local.sort_values(by='moneda_destino')
        
        print(f"Transformación completada: {len(df_local)} divisas estratégicas listas.")
        return df_local
        
    except Exception as e:
        print(f"Error inesperado en la transformación: {e}")
        return None
