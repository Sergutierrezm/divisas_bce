import pandas as pd

def procesar_silver(df):
    """Filtra las divisas estratégicas y redondea a 2 decimales para la capa Silver."""
    if df is None or df.empty:
        return None

    try:
        divisas_top = ['USD', 'JPY', 'GBP', 'CHF']
        df_silver = df[df['moneda_destino'].isin(divisas_top)].copy()
        df_silver['tasa_cambio'] = df_silver['tasa_cambio'].round(2)

        columnas = ['fecha_actualizacion', 'moneda_base', 'moneda_destino', 'tasa_cambio']
        df_silver = df_silver[columnas].sort_values(by='moneda_destino')

        print(f"Transformación Silver completada: {len(df_silver)} divisas listas.")
        return df_silver
    except Exception as e:
        print(f"Error en transformación Silver: {e}")
        return None

def procesar_gold(df_silver_hist):
    """Calcula la variación diaria porcentual por moneda para la capa Gold."""
    if df_silver_hist is None or df_silver_hist.empty:
        return None

    try:
        df_gold = df_silver_hist.copy()
        df_gold['tasa_cambio'] = df_gold['tasa_cambio'].astype(float)

        # Ordenamos por moneda y fecha para que pct_change compare con el día anterior correcto
        df_gold = df_gold.sort_values(by=['moneda_destino', 'fecha_actualizacion'])

        df_gold['variacion_diaria_pct'] = (
            df_gold.groupby('moneda_destino')['tasa_cambio']
            .pct_change() * 100
        ).round(2)

        print(f"Transformación Gold completada: {len(df_gold)} registros con variación diaria.")
        return df_gold
    except Exception as e:
        print(f"Error en transformación Gold: {e}")
        return None
