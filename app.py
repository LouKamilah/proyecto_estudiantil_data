import streamlit as st
import plotly.express as px
import os
from database import (
    cargar_y_limpiar_datos,
    cargar_rendimiento_academico,
    cargar_egresos_titulaciones
)

# ==========================================
# 1. CONFIGURACIÓN DE PÁGINA
# ==========================================
st.set_page_config(
    page_title="Monitoreo de Trayectoria Estudiantil",
    page_icon="🎓",
    layout="wide"
)

# ==========================================
# 2. ESTILOS CSS CON TAILWIND (TEMA OSCURO)
# ==========================================
st.markdown("""
<script src="https://cdn.tailwindcss.com"></script>
<style>
    .stApp {
        background-color: #0f172a !important;
        color: #f8fafc !important;
    }
    section[data-testid="stSidebar"] {
        background-color: #1e293b !important;
        border-right: 1px solid #334155;
    }
</style>
""", unsafe_allow_html=True)

st.title("🎓 Sistema de Monitoreo de Trayectoria Estudiantil")
st.markdown("Análisis institucional secuencial de matrícula, retención, rendimiento y titulación.")

# ==========================================
# 3. CONTEXTO DE NEGOCIO Y MODELO DE DATOS
# ==========================================
st.markdown("""
<div class="bg-slate-800 border-l-4 border-blue-500 rounded-r-lg p-5 mb-5 shadow-lg border border-slate-700">
    <h3 class="text-blue-400 font-bold text-lg mb-1">📌 Objetivo del Proyecto</h3>
    <p class="text-slate-300 text-sm leading-relaxed">
        Integrar, validar y analizar datos académicos para identificar patrones de matrícula, permanencia, 
        rendimiento, progresión y titulación, apoyando las decisiones institucionales y detectando riesgos de abandono.
    </p>
</div>
""", unsafe_allow_html=True)

# Documentación desplegable del modelo de datos
with st.expander("📂 Ver Documentación del Modelo (MER y Variables)"):
    col_img1, col_img2 = st.columns(2)
    with col_img1:
        if os.path.exists("data/MER.jpg"):
            st.image("data/MER.jpg", caption="Modelo Entidad-Relación (MER)", use_container_width=True)
    with col_img2:
        if os.path.exists("data/variables_claves.png"):
            st.image("data/variables_claves.png", caption="Variables Claves", use_container_width=True)

# ==========================================
# 4. CARGA DE DATOS DESDE DATABASE.PY
# ==========================================
@st.cache_data
def obtener_todo():
    df_mat = cargar_y_limpiar_datos()
    df_rend = cargar_rendimiento_academico()
    df_egr = cargar_egresos_titulaciones()
    return df_mat, df_rend, df_egr

df_mat, df_rend, df_egr = obtener_todo()

if not df_mat.empty:
    # Filtro Lateral
    st.sidebar.header("Filtros Globales")
    sedes = ["Todas"] + list(df_mat["sede"].unique())
    sede_sel = st.sidebar.selectbox("Seleccionar Sede", sedes)
    
    if sede_sel != "Todas":
        df_mat_f = df_mat[df_mat["sede"] == sede_sel]
    else:
        df_mat_f = df_mat.copy()

    # Indicadores Clave (KPIs)
    st.subheader("📊 Indicadores Generales Institucionales")
    col1, col2, col3, col4 = st.columns(4)
    
    total_estudiantes = df_mat_f["id_estudiante"].nunique()
    total_vigentes = len(df_mat_f[df_mat_f["estado_matricula"] == "vigente"])
    retirados = len(df_mat_f[df_mat_f["estado_matricula"] == "retirada"])
    tasa_retencion = ((len(df_mat_f) - retirados) / len(df_mat_f)) * 100

    col1.metric("Estudiantes Totales", f"{total_estudiantes:,}")
    col2.metric("Matrículas Vigentes", f"{total_vigentes:,}")
    col3.metric("Estudiantes Retirados", f"{retirados:,}")
    col4.metric("Tasa de Retención", f"{tasa_retencion:.1f}%")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")

    # ==========================================
    # 5. ESTRUCTURA DE LISTA: PREGUNTAS Y GRÁFICOS
    # ==========================================

    # -------------------------------------------------------------
    # ITEM 1: EVOLUCIÓN DE MATRÍCULA
    # -------------------------------------------------------------
    st.markdown("""
    <div class="text-xl font-bold text-blue-400 mb-2">
        1. ¿Cómo ha evolucionado la matrícula total, nueva y de continuidad por período, sede y carrera?
    </div>
    """, unsafe_allow_html=True)

    df_evo = (
        df_mat_f.groupby(["nombre_periodo", "tipo_matricula"])["id_matricula"]
        .count()
        .reset_index()
    )

    fig_evo = px.bar(
        df_evo,
        x="nombre_periodo",
        y="id_matricula",
        color="tipo_matricula",
        title="Evolución de Matrícula por Período Académico (Nuevos vs Continuidad)",
        labels={"id_matricula": "Cantidad de Matrículas", "nombre_periodo": "Período"},
        template="plotly_dark",
        barmode="stack"
    )
    fig_evo.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_evo, use_container_width=True)

    st.markdown("""
    <div class="bg-slate-800 border-l-4 border-emerald-500 rounded-r-lg p-4 mb-8 shadow-lg border border-slate-700">
        <h4 class="text-emerald-400 font-bold text-base mb-1">💡 Conclusión del Gráfico de Matrícula</h4>
        <p class="text-slate-300 text-sm leading-relaxed">
            Se observa un volumen sostenido de alumnos de continuidad a lo largo de los semestres semestrales. 
            La relación entre alumnos nuevos y continuidad muestra ciclos regulares de ingreso en los primeros semestres de cada año, 
            lo que confirma la estabilidad de la demanda en las sedes analizadas.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # -------------------------------------------------------------
    # ITEM 2: RETENCIÓN POR CARRERA
    # -------------------------------------------------------------
    st.markdown("""
    <div class="text-xl font-bold text-blue-400 mb-2">
        2. ¿Qué carreras, cohortes o sedes presentan menor retención estudiantil?
    </div>
    """, unsafe_allow_html=True)

    df_ret = (
        df_mat_f.groupby(["nombre_carrera", "estado_matricula"])["id_estudiante"]
        .count()
        .reset_index()
    )

    fig_ret = px.bar(
        df_ret,
        x="nombre_carrera",
        y="id_estudiante",
        color="estado_matricula",
        title="Distribución del Estado de Matrícula por Carrera",
        labels={"id_estudiante": "Cantidad de Estudiantes", "nombre_carrera": "Carrera"},
        template="plotly_dark",
        barmode="group"
    )
    fig_ret.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_ret, use_container_width=True)

    st.markdown("""
    <div class="bg-slate-800 border-l-4 border-emerald-500 rounded-r-lg p-4 mb-8 shadow-lg border border-slate-700">
        <h4 class="text-emerald-400 font-bold text-base mb-1">💡 Conclusión del Gráfico de Retención</h4>
        <p class="text-slate-300 text-sm leading-relaxed">
            La mayor proporción de estudiantes retirados o suspendidos se concentra en programas técnicos y carreras de primer nivel curricular.
            Esto destaca la necesidad de implementar acompañamiento académico intensivo durante los primeros dos semestres.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # -------------------------------------------------------------
    # ITEM 3: RENDIMIENTO ACADÉMICO Y NOTAS
    # -------------------------------------------------------------
    st.markdown("""
    <div class="text-xl font-bold text-blue-400 mb-2">
        3. ¿Qué factores académicos se asocian con una mayor probabilidad de abandono o atraso?
    </div>
    """, unsafe_allow_html=True)

    if not df_rend.empty:
        col_a, col_b = st.columns(2)

        df_aprob = (
            df_rend.groupby(["estado_asignatura"])["id_inscripcion"]
            .count()
            .reset_index()
        )

        with col_a:
            fig_pie = px.pie(
                df_aprob,
                names="estado_asignatura",
                values="id_inscripcion",
                title="Tasa Global de Aprobación vs Reprobación",
                template="plotly_dark",
                hole=0.4
            )
            fig_pie.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_pie, use_container_width=True)

        with col_b:
            fig_hist = px.histogram(
                df_rend,
                x="nota_final",
                nbins=20,
                title="Distribución Histórica de Notas Finales",
                labels={"nota_final": "Nota Final"},
                template="plotly_dark",
                color_discrete_sequence=["#3b82f6"]
            )
            fig_hist.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_hist, use_container_width=True)

        st.markdown("""
        <div class="bg-slate-800 border-l-4 border-emerald-500 rounded-r-lg p-4 mb-8 shadow-lg border border-slate-700">
            <h4 class="text-emerald-400 font-bold text-base mb-1">💡 Conclusión sobre Rendimiento Académico</h4>
            <p class="text-slate-300 text-sm leading-relaxed">
                Existe un porcentaje significativo de reprobación acumulada en asignaturas clave del área de tecnología y ciencias básicas.
                La acumulación de notas finales por debajo del umbral mínimo de aprobación es el principal factor predictivo de suspensión y retiro de matrícula.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # -------------------------------------------------------------
    # ITEM 4: EGRESO Y TIEMPOS DE TITULACIÓN
    # -------------------------------------------------------------
    st.markdown("""
    <div class="text-xl font-bold text-blue-400 mb-2">
        4. ¿Qué porcentaje de estudiantes completa su plan de estudios y cuánto tarda en titularse?
    </div>
    """, unsafe_allow_html=True)

    if not df_egr.empty:
        col_e1, col_e2 = st.columns(2)

        with col_e1:
            df_mod = df_egr.groupby("modalidad_titulacion")["id_egreso_titulacion"].count().reset_index()
            fig_mod = px.bar(
                df_mod,
                x="modalidad_titulacion",
                y="id_egreso_titulacion",
                title="Distribución de Titulados por Modalidad",
                labels={"id_egreso_titulacion": "Cantidad de Titulados", "modalidad_titulacion": "Modalidad"},
                template="plotly_dark"
            )
            fig_mod.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_mod, use_container_width=True)

        with col_e2:
            fig_box = px.box(
                df_egr,
                x="nombre_carrera",
                y="anios_titulacion",
                title="Años de Duración Real hasta Titulación por Carrera",
                labels={"anios_titulacion": "Años", "nombre_carrera": "Carrera"},
                template="plotly_dark"
            )
            fig_box.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_box, use_container_width=True)

        st.markdown("""
        <div class="bg-slate-800 border-l-4 border-emerald-500 rounded-r-lg p-5 mb-8 shadow-lg border border-slate-700">
            <h4 class="text-emerald-400 font-bold text-base mb-1">💡 Conclusión sobre Egresos y Titulación</h4>
            <p class="text-slate-300 text-sm leading-relaxed">
                La <b>Práctica Profesional</b> es la modalidad preferida y más eficiente de titulación. 
                Los datos reflejan un sobretiempo promedio de entre 0.5 a 1.5 años respecto a la duración formal del plan de estudios, 
                causado principalmente por la reprobación de asignaturas en semestres intermedios.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # -------------------------------------------------------------
    # ITEM 5: CALIDAD DE DATOS Y ACCIONES
    # -------------------------------------------------------------
    st.markdown("""
    <div class="text-xl font-bold text-blue-400 mb-2">
        5. Calidad de Registros e Intervenciones Sugeridas
    </div>
    """, unsafe_allow_html=True)

    col_q1, col_q2 = st.columns(2)

    with col_q1:
        st.markdown("""
        <div class="bg-slate-800 p-5 rounded-lg border border-slate-700 text-sm text-slate-300 h-full">
            <h4 class="text-blue-400 font-bold text-base mb-2">🧹 Inconsistencias de Calidad Corregidas</h4>
            <ul class="list-disc list-inside space-y-2">
                <li><b>Normalización de Mayúsculas/Minúsculas:</b> Se corrigió la inconsistencia entre <code>VIGENTE</code> y <code>vigente</code> en matrículas.</li>
                <li><b>Tratamiento de Duplicados:</b> Se depuraron duplicados lógicos en la tabla de matrículas conservando la primera inscripción válida.</li>
                <li><b>Alineación de Columnas Duplicadas:</b> Se resolvió la colisión entre el estado de inscripción y el estado del catálogo de asignaturas en Pandas.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col_q2:
        st.markdown("""
        <div class="bg-slate-800 p-5 rounded-lg border border-slate-700 text-sm text-slate-300 h-full">
            <h4 class="text-emerald-400 font-bold text-base mb-2">🚀 Plan de Acción e Intervenciones Propuestas</h4>
            <ul class="list-disc list-inside space-y-2">
                <li><b>Alertas Tempranas:</b> Notificar a los coordinadores de carrera cuando un estudiante repruebe 2 o más módulos en su primer año.</li>
                <li><b>Tutorías Académicas:</b> Reforzar los módulos críticos con mayor tasa histórica de reprobación.</li>
                <li><b>Validaciones en Origen:</b> Incorporar reglas de validación en la base de datos para evitar variaciones de formato y duplicidad de matrículas.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

else:
    st.error("No se pudieron cargar los datos. Revisa la carpeta 'data/'.")