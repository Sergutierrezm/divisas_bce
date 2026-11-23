from extractor_api import extraer_datos
from procesador import procesar_silver, procesar_gold
from loader import cargar_bronze, cargar_silver, leer_silver, cargar_gold

def ejecutar_pipeline():
    print("🚀 Iniciando Pipeline Medallion (Bronze -> Silver -> Gold)...\n")

    # --- CAPA BRONZE (Ingesta cruda) ---
    print(">>> 1. CAPA BRONZE")
    df_raw = extraer_datos()
    if df_raw is None or not cargar_bronze(df_raw):
        print("❌ Pipeline abortado en Bronze.")
        return
    print("-" * 50)

    # --- CAPA SILVER (Limpieza y filtrado) ---
    print(">>> 2. CAPA SILVER")
    df_silver = procesar_silver(df_raw)
    if df_silver is None or not cargar_silver(df_silver):
        print("❌ Pipeline abortado en Silver.")
        return
    print("-" * 50)

    # --- CAPA GOLD (Métricas de negocio) ---
    print(">>> 3. CAPA GOLD")
    df_silver_hist = leer_silver()
    df_gold = procesar_gold(df_silver_hist)
    if df_gold is None or not cargar_gold(df_gold):
        print("❌ Pipeline abortado en Gold.")
        return

    print("\n✅ Pipeline Medallion completado con éxito.")

if __name__ == "__main__":
    ejecutar_pipeline()