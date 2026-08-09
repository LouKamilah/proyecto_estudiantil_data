import pandas as pd
import os

# Ruta hacia la carpeta con los archivos CSV
DATA_DIR = "data"

def cargar_y_limpiar_datos():
    """
    Carga y consolida las matrículas con la información de estudiantes,
    carreras y períodos académicos.
    """
    df_estudiantes = pd.read_csv(os.path.join(DATA_DIR, "estudiantes.csv"))
    df_carreras = pd.read_csv(os.path.join(DATA_DIR, "carreras.csv"))
    df_periodos = pd.read_csv(os.path.join(DATA_DIR, "periodos_academicos.csv"))
    df_matriculas = pd.read_csv(os.path.join(DATA_DIR, "matriculas.csv"))
    
    # Estandarización de estado de matrícula
    df_matriculas["estado_matricula"] = (
        df_matriculas["estado_matricula"]
        .str.strip()
        .str.lower()
    )
    
    # Eliminación de duplicados
    df_matriculas = (
        df_matriculas
        .sort_values("id_matricula")
        .drop_duplicates(subset=["id_estudiante", "id_carrera", "id_periodo"], keep="first")
    )

    # Conversión de fechas
    df_estudiantes["fecha_nacimiento"] = pd.to_datetime(df_estudiantes["fecha_nacimiento"], errors="coerce")
    df_estudiantes["fecha_ingreso"] = pd.to_datetime(df_estudiantes["fecha_ingreso"], errors="coerce")
    
    # Joins relacionales
    df_merged = df_matriculas.merge(df_estudiantes, on="id_estudiante", how="inner")
    df_merged = df_merged.merge(df_carreras, on="id_carrera", how="inner")
    df_merged = df_merged.merge(df_periodos, on="id_periodo", how="inner")

    return df_merged


def cargar_rendimiento_academico():
    """
    Carga el detalle de inscripciones de asignaturas junto con el catálogo de asignaturas.
    """
    df_inscripciones = pd.read_csv(os.path.join(DATA_DIR, "inscripciones_asignaturas.csv"))
    df_asignaturas = pd.read_csv(os.path.join(DATA_DIR, "asignaturas.csv"))
    
    # Estandarizar estado de la inscripción del estudiante
    df_inscripciones["estado_asignatura"] = (
        df_inscripciones["estado_asignatura"]
        .str.strip()
        .str.lower()
    )
    
    # Cruce relacional
    df_rendimiento = df_inscripciones.merge(df_asignaturas, on="id_asignatura", how="inner")
    
    # Corregir sufijo de Pandas (_x proviene de inscripciones)
    if "estado_asignatura_x" in df_rendimiento.columns:
        df_rendimiento.rename(columns={"estado_asignatura_x": "estado_asignatura"}, inplace=True)
        
    return df_rendimiento

def cargar_egresos_titulaciones():
    """
    Carga los registros de egreso y titulación con información de carreras y estudiantes.
    """
    df_egresos = pd.read_csv(os.path.join(DATA_DIR, "egresos_titulaciones.csv"))
    df_carreras = pd.read_csv(os.path.join(DATA_DIR, "carreras.csv"))
    df_estudiantes = pd.read_csv(os.path.join(DATA_DIR, "estudiantes.csv"))
    
    df_egresos["fecha_egreso"] = pd.to_datetime(df_egresos["fecha_egreso"], errors="coerce")
    df_egresos["fecha_titulacion"] = pd.to_datetime(df_egresos["fecha_titulacion"], errors="coerce")
    df_estudiantes["fecha_ingreso"] = pd.to_datetime(df_estudiantes["fecha_ingreso"], errors="coerce")
    
    df_full = df_egresos.merge(df_carreras, on="id_carrera", how="inner")
    df_full = df_full.merge(df_estudiantes, on="id_estudiante", how="inner")
    
    # Cálculo del tiempo hasta la titulación en años
    df_full["anios_titulacion"] = (
        (df_full["fecha_titulacion"] - df_full["fecha_ingreso"]).dt.days / 365.25
    )
    
    return df_full