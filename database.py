import pandas as pd
import os

# Ruta hacia la carpeta con los CSV
DATA_DIR = "data"

def cargar_y_limpiar_datos():
    # Cargar archivos usando os.path.join para evitar problemas entre Windows/Linux
    df_estudiantes = pd.read_csv(os.path.join(DATA_DIR, "estudiantes.csv"))
    df_carreras = pd.read_csv(os.path.join(DATA_DIR, "carreras.csv"))
    df_periodos = pd.read_csv(os.path.join(DATA_DIR, "periodos_academicos.csv"))
    df_matriculas = pd.read_csv(os.path.join(DATA_DIR, "matriculas.csv"))
    
    # Resto de la lógica de limpieza y merge...
    df_matriculas["estado_matricula"] = df_matriculas["estado_matricula"].str.strip().str.lower()
    df_matriculas = df_matriculas.sort_values("id_matricula").drop_duplicates(
        subset=["id_estudiante", "id_carrera", "id_periodo"], keep="first"
    )

    df_merged = df_matriculas.merge(df_estudiantes, on="id_estudiante", how="inner")
    df_merged = df_merged.merge(df_carreras, on="id_carrera", how="inner")
    df_merged = df_merged.merge(df_periodos, on="id_periodo", how="inner")

    return df_merged