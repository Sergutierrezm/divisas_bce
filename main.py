from extractor_api import extraer_datos
from procesador import procesar_datos
from loader import cargar_a_postgres

def ejecutar_pipeline():
    print("🚀 Iniciando Pipeline ETL de Divisas BCE...\n")
    
    # --- FASE 1: EXTRACCIÓN ---
    print(">>> FASE 1: Extracción")
    df_raw = extraer_datos()
    
    if df_raw is None:
        print("❌ Pipeline abortado.")
        return
        
    print("-" * 50)
    
    # --- FASE 2: TRANSFORMACIÓN ---
    print(">>> FASE 2: Transformación")
    df_clean = procesar_datos(df_raw)
    
    if df_clean is None:
        print("❌ Pipeline abortado.")
        return
        
    print("-" * 50)
    
    # --- FASE 3: CARGA ---
    print(">>> FASE 3: Carga")
    # Guardamos el DataFrame limpio en la BD 'divisas_bce'
    exito = cargar_a_postgres(df_clean, "tipos_cambio_bce")
    
    if exito:
        print("\n✅ Pipeline ETL completado. Datos listos en PostgreSQL.")
    else:
        print("\n❌ Pipeline abortado.")

if __name__ == "__main__":
    ejecutar_pipeline()