import streamlit as st
import plotly.express as px
from database import cargar_y_limpiar_datos
import os

# 1. Configuración de la Página
st.set_page_config(
    page_title="Monitoreo de Trayectoria Estudiantil",
    page_icon="🎓",
    layout="wide"
)

# 2. Carga de CSS con Tailwind para el Tema Oscuro
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

st.title("Sistema de Monitoreo de Trayectoria Estudiantil")
st.markdown("Análisis institucional de matrícula, permanencia y progresión académica de pregrado.")

# 3. Contexto de Negocio en HTML
st.markdown("""
<div class="bg-slate-800 border-l-4 border-blue-500 rounded-r-lg p-5 mb-5 shadow-lg border border-slate-700">
    <h3 class="text-blue-400 font-bold text-lg mb-1">Objetivo del Proyecto</h3>
    <p class="text-slate-300 text-sm leading-relaxed">
        Monitorear la trayectoria académica de los estudiantes desde su ingreso hasta la titulación,
        detectando riesgos académicos y oportunidades de mejora a través de indicadores de retención y matrícula.
    </p>
</div>
""", unsafe_allow_html=True)

# 3. Contexto
st.markdown("""
<div class="bg-slate-800 border-l-4 border-blue-500 rounded-r-lg p-5 mb-5 shadow-lg border border-slate-700">
    <h3 class="text-blue-400 font-bold text-lg mb-1">Contexto</h3>
    <p class="text-slate-300 text-sm leading-relaxed">Una institución de educación superior necesita contar con información 
    confiable y oportuna para monitorear la trayectoria de sus estudiantes, desde la matrícula hasta la titulación. 
    Actualmente, los registros provienen de distintas fuentes y requieren validación antes de convertirse en reportes útiles 
    para la gestión académica.
    </p>
        <p class="text-slate-300 text-sm leading-relaxed">Este proyecto simula el trabajo de un Analista de Datos 
        y Procesos Académicos. Su propósito es integrar, validar y analizar datos académicos para identificar patrones de matrícula, permanencia, rendimiento, progresión y titulación.
    </p>
        </p>
        <p class="text-slate-300 text-sm leading-relaxed">Los datos utilizados serán sintéticos: no representan estudiantes
        reales y fueron diseñados con fines demostrativos y de portafolio. Esto permite aplicar prácticas de calidad, 
        trazabilidad y confidencialidad sin comprometer información personal.
    </p>
</div>
""", unsafe_allow_html=True)

# 4. Preguntas de negocio
st.markdown("""
<div class="bg-slate-800 border-l-4 border-blue-500 rounded-r-lg p-5 mb-5 shadow-lg border border-slate-700">
    <h3 class="text-blue-400 font-bold text-lg mb-1">Preguntas de Negocio</h3>
    <p class="text-slate-300 text-sm leading-relaxed">Las principales preguntas que vamos a responder con este análisis son:
    </p>
        <p class="text-slate-300 text-sm leading-relaxed">1. ¿Cómo ha evolucionado la matrícula total, nueva 
        y de continuidad por período, sede y carrera?
    </p>
        </p>
        <p class="text-slate-300 text-sm leading-relaxed">2. ¿Qué carreras, cohortes o sedes presentan menor retención estudiantil?
    </p>
        </p>
        </p>
        <p class="text-slate-300 text-sm leading-relaxed">3. ¿Qué factores académicos se asocian con una mayor probabilidad 
        de abandono o atraso en la progresión?
    </p>
        </p>
        </p>
        <p class="text-slate-300 text-sm leading-relaxed">4. ¿Qué porcentaje de estudiantes completa su plan de estudios 
        y cuánto tiempo tarda en egresar o titularse?
    </p>
        </p>
        </p>
        <p class="text-slate-300 text-sm leading-relaxed">5. ¿Existen inconsistencias o problemas de calidad que 
        puedan afectar los indicadores institucionales?
    </p>
        </p>
        </p>
        <p class="text-slate-300 text-sm leading-relaxed">6. ¿Qué acciones puede tomar la institución para mejorar la permanencia, 
        la progresión y la calidad de sus registros?
    </p>
    
</div>
""", unsafe_allow_html=True)

# 4. Modelo de datos y diccionario de variables
st.markdown("""
<div class="bg-slate-800 border-l-4 border-blue-500 rounded-r-lg p-5 mb-3 shadow-lg border border-slate-700">
    <h3 class="text-blue-400 font-bold text-lg mb-1">Modelo de datos y diccionario de variables</h3>
    <p class="text-slate-300 text-sm leading-relaxed">
        El modelo se basa en una estructura relacional. <br>
        Cada estudiante puede tener una o más matrículas a lo largo del tiempo, 
        cursar varias asignaturas por período y eventualmente registrar un egreso o titulación[cite: 2].
    </p>   
</div>
""", unsafe_allow_html=True)

# Definir la ruta relativa
ruta_imagen = "data/diccionario.png" # Asegúrate de que coincida exactamente con el nombre de tu archivo

# Verificar si el archivo existe antes de renderizarlo
if os.path.exists(ruta_imagen):
    st.image(
        ruta_imagen, 
        caption="Modelo Entidad-Relación (MER) - Trayectoria Estudiantil", 
        use_container_width=True
    )
else:
    st.warning(f"No se encontró la imagen en la ruta: {ruta_imagen}. Por favor, guarda la imagen dentro de la carpeta 'data/'.")


# 4. Modelo de datos y diccionario de variables

# MER
ruta_imagen = "data/MER.jpg" # Asegúrate de que coincida exactamente con el nombre de tu archivo

# Verificar si el archivo existe antes de renderizarlo
if os.path.exists(ruta_imagen):
    st.image(
        ruta_imagen, 
        caption="Modelo Entidad-Relación (MER) - Trayectoria Estudiantil", 
        use_container_width=True
    )
else:
    st.warning(f"No se encontró la imagen en la ruta: {ruta_imagen}. Por favor, guarda la imagen dentro de la carpeta 'data/'.")


# Variables claves
ruta_imagen = "data/variables_claves.png" # Asegúrate de que coincida exactamente con el nombre de tu archivo

# Verificar si el archivo existe antes de renderizarlo
if os.path.exists(ruta_imagen):
    st.image(
        ruta_imagen, 
        caption="Variables Claves - Trayectoria Estudiantil", 
        use_container_width=True
    )
else:
    st.warning(f"No se encontró la imagen en la ruta: {ruta_imagen}. Por favor, guarda la imagen dentro de la carpeta 'data/'.")


# 4. Cargar Datos Procesados
@st.cache_data
def obtener_datos():
    return cargar_y_limpiar_datos()

df = obtener_datos()

if not df.empty:
    # Barra Lateral: Filtros
    st.sidebar.header("Filtros Institucionales")
    
    sedes = ["Todas"] + list(df["sede"].unique())
    sede_sel = st.sidebar.selectbox("Seleccionar Sede", sedes)
    
    if sede_sel != "Todas":
        df_filtrado = df[df["sede"] == sede_sel]
    else:
        df_filtrado = df.copy()

    # Indicadores Clave (KPIs)
    st.subheader("📊 Indicadores Generales")
    col1, col2, col3 = st.columns(3)
    
    total_estudiantes = df_filtrado["id_estudiante"].nunique()
    total_matriculas = len(df_filtrado[df_filtrado["estado_matricula"] == "vigente"])
    tasa_retirados = (len(df_filtrado[df_filtrado["estado_matricula"] == "retirada"]) / len(df_filtrado)) * 100

    col1.metric("Estudiantes Únicos", f"{total_estudiantes:,}")
    col2.metric("Matrículas Vigentes", f"{total_matriculas:,}")
    col3.metric("Tasa de Retiro", f"{tasa_retirados:.1f}%")

    st.markdown("<br>", unsafe_allow_html=True)

    # Gráficos
    tab1, tab2 = st.tabs(["📈 Evolución de Matrícula", "🏢 Análisis por Sede y Carrera"])

    with tab1:
        # Evolución por período académico
        df_periodo = (
            df_filtrado.groupby(["nombre_periodo", "tipo_matricula"])["id_matricula"]
            .count()
            .reset_index()
        )
        
        fig_evol = px.bar(
            df_periodo,
            x="nombre_periodo",
            y="id_matricula",
            color="tipo_matricula",
            title="Evolución de Matrícula Total (Nuevas vs Continuidad)",
            labels={"id_matricula": "Cantidad de Matrículas", "nombre_periodo": "Período Académico"},
            template="plotly_dark"
        )
        fig_evol.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_evol, use_container_width=True)

    with tab2:
        # Estado de matrícula por carrera
        df_carrera = (
            df_filtrado.groupby(["nombre_carrera", "estado_matricula"])["id_estudiante"]
            .count()
            .reset_index()
        )
        
        fig_carrera = px.bar(
            df_carrera,
            x="nombre_carrera",
            y="id_estudiante",
            color="estado_matricula",
            title="Distribución de Estado de Matrícula por Carrera",
            barmode="group",
            template="plotly_dark"
        )
        fig_carrera.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_carrera, use_container_width=True)

    # Conclusiones del informe
    st.markdown("---")
    st.markdown("""
    <div class="bg-slate-800 border-l-4 border-emerald-500 rounded-r-lg p-5 mt-5 shadow-lg border border-slate-700">
        <h3 class="text-emerald-400 font-bold text-lg mb-2">💡 Hallazgos Principales</h3>
        <ul class="list-disc list-inside text-slate-300 text-sm space-y-1">
            <li><b>Validación de Registros:</b> Se estandarizaron los valores en la variable <code>estado_matricula</code> y se eliminaron registros duplicados.</li>
            <li><b>Tendencia:</b> Permite identificar la proporción de alumnos nuevos frente a los de continuidad por cohorte y sede.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
else:
    st.error("No se pudieron cargar las tablas CSV. Revisa la ruta especificada.")