import requests
import pandas as pd

def extraer_datos():
    """Conecta a la API de Frankfurter y obtiene los tipos de cambio del Euro."""
    url = "https://api.frankfurter.app/latest?from=EUR"
    
    try:
        print("Descargando tipos de cambio oficiales del Banco Central Europeo...")
        # Petición limpia y normal, sin trucos
        respuesta = requests.get(url, timeout=10)
        respuesta.raise_for_status()
        
        datos_json = respuesta.json()
        tasas = datos_json.get("rates", {})
        fecha = datos_json.get("date")
        
        # Convertimos el diccionario {'USD': 1.08, 'GBP': 0.85...} en un DataFrame de 2 columnas
        df = pd.DataFrame(list(tasas.items()), columns=["moneda_destino", "tasa_cambio"])
        
        # Le añadimos la fecha y la moneda base para tener el contexto completo
        df["moneda_base"] = "EUR"
        df["fecha_actualizacion"] = fecha
        
        print(f"Extracción completada: {len(df)} divisas obtenidas.")
        return df
        
    except Exception as e:
        print(f"Error en la extracción: {e}")
        return None