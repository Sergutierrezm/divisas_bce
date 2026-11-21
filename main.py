from extractor_api import extraer_datos
from procesador import procesar_datos
from loader import cargar_a_postgres, existen_datos_fecha

def ejecutar_pipeline():
    nombre_tabla = "tipos_cambio_bce"
    print("🚀 Iniciando Pipeline ETL de Divisas BCE...\n")
    
    # --- FASE 1: EXTRACCIÓN ---
    print(">>> FASE 1: Extracción")
    df_raw = extraer_datos()
    
    if df_raw is None:
        print("❌ Pipeline abortado.")
        return

    # Comprobamos si ya tenemos en BD la fecha que acaba de devolver el BCE
    fecha_datos = df_raw["fecha_actualizacion"].iloc[0]
    if existen_datos_fecha(fecha_datos, nombre_tabla):
        print(f"\nℹ️ Los datos del {fecha_datos} ya están guardados en '{nombre_tabla}'. No es necesario volver a cargarlos.")
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
    exito = cargar_a_postgres(df_clean, nombre_tabla)
    
    if exito:
        print("\n✅ Pipeline ETL completado. Histórico actualizado en PostgreSQL.")
    else:
        print("\n❌ Pipeline abortado.")

if __name__ == "__main__":
    ejecutar_pipeline()