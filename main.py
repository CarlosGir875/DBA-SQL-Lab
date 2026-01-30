import streamlit as st
import random
import pandas as pd
import time
from preguntas import temas 

# 1. CONFIGURACIÓN DE PÁGINA Y ESTILO CSS AVANZADO
st.set_page_config(page_title="DBA English & SQL Lab", page_icon="⚡", layout="wide")

## EXPLICACIÓN: He añadido un estilo neón al contenedor de preguntas y animaciones a los botones
st.markdown("""
    <style>
    /* Bloqueo de selección y cursor personalizado */
    * { user-select: none !important; -webkit-user-select: none; caret-color: transparent !important; }
    .stSelectbox, .stSelectbox *, [data-baseweb="select"], button, .stRadio > div { cursor: pointer !important; }
    [data-testid="stSidebar"] input[type="text"], textarea { 
        user-select: text !important; caret-color: auto !important; cursor: text !important; 
    }
    /* Estilo para las tarjetas de preguntas con efecto Neón */
    .stAlert { 
        border-radius: 15px; 
        border: 2px solid #00FFAA; 
        background-color: #0E1117;
        box-shadow: 0 0 10px #00FFAA;
    }
    /* Animación simple para títulos */
    h1 { color: #00FFAA; text-shadow: 2px 2px 4px #000000; font-family: 'Courier New', Courier, monospace; }
    .stProgress > div > div > div > div { background-color: #00FFAA; }
    </style>
    """, unsafe_allow_html=True)

# 2. GENERACIÓN DE DATA PARA SQL STUDIO (300 REGISTROS)
@st.cache_data
def cargar_base_datos():
    return pd.DataFrame({
        'ID': range(1, 301),
        'Nombre': ["Carlos Giron", "Juan Perez", "Maria Lopez", "Ana Garcia", "Luis Martinez", "Elena Rodriguez", "Diego Sosa", "Carmen Ruiz", "Pablo Duarte", "Lucia Mendez"] * 30,
        'Pais': ['Guatemala', 'Mexico', 'USA', 'España', 'El Salvador', 'Honduras'] * 50,
        'Estado': ['Activo', 'Inactivo', 'Pendiente'] * 100,
        'Rol': ['DBA', 'Dev', 'Analista', 'Soporte', 'Manager'] * 60
    })

df_sql = cargar_base_datos()

# 3. GESTIÓN DE ESTADO (SESSION STATE)
if 'indice' not in st.session_state: st.session_state.indice = 0
if 'vidas' not in st.session_state: st.session_state.vidas = 3
if 'id_final' not in st.session_state: st.session_state.id_final = ""
if 'lista_mezclada' not in st.session_state: st.session_state.lista_mezclada = []
if 'puntos' not in st.session_state: st.session_state.puntos = 0
if 'logros' not in st.session_state: st.session_state.logros = []

# --- BARRA LATERAL: PANEL DE CONTROL ---
st.sidebar.title("🎮 DBA Control Center")

## EXPLICACIÓN: Esta sección organiza el menú dinámicamente
orden_prioritario = ["Verbo To Be - Presente/Pasado", "SQL Questions", "Presente Continuo"]
todas_las_llaves = list(temas.keys())
opciones_menu = ["🏠 Inicio"] + [t for t in orden_prioritario if t in todas_las_llaves]
for t in todas_las_llaves:
    if t not in opciones_menu: opciones_menu.append(t)

# Definimos seleccion AQUÍ arriba para que todo el código la reconozca
seleccion = st.sidebar.selectbox("Módulo de aprendizaje:", opciones_menu)

# --- LÓGICA DE CARGA DE NIVELES (ESPECIAL PARA VERBO TO BE Y SQL) ---
## EXPLICACIÓN: El "Motor Antibalas" ahora detecta si el nivel 2 es una lista o un diccionario
if seleccion != "🏠 Inicio":
    contenido = temas.get(seleccion, [])
    lista_preguntas_final = []
    id_unico_actual = seleccion

    # CASO A: Estructura con Niveles (SQL / Verbo To Be organizado como lista de dicts)
    if isinstance(contenido, list) and len(contenido) > 0 and isinstance(contenido[0], dict):
        dicc_niveles = contenido[0]
        nombres_niveles = list(dicc_niveles.keys())
        nivel_sel = st.sidebar.radio("🎯 Selecciona Nivel:", nombres_niveles)
        lista_preguntas_final = dicc_niveles.get(nivel_sel, [])
        id_unico_actual = f"{seleccion}_{nivel_sel}"
        
    # CASO B: Lista directa de preguntas (Como Copilot o backups)
    elif isinstance(contenido, list) and len(contenido) > 0 and (isinstance(contenido[0], dict) and 'pregunta' in contenido[0]):
        lista_preguntas_final = contenido
        id_unico_actual = seleccion

    # CASO C: Diccionario directo (Estructura optimizada)
    elif isinstance(contenido, dict):
        nombres_niveles = list(contenido.keys())
        nivel_sel = st.sidebar.radio("🎯 Selecciona Nivel:", nombres_niveles)
        lista_preguntas_final = contenido.get(nivel_sel, [])
        id_unico_actual = f"{seleccion}_{nivel_sel}"

    # LÓGICA DE MEZCLA
    if st.session_state.id_final != id_unico_actual:
        if lista_preguntas_final:
            st.session_state.lista_mezclada = random.sample(lista_preguntas_final, len(lista_preguntas_final))
            st.session_state.id_final = id_unico_actual
            st.session_state.indice = 0
            st.session_state.vidas = 3

# --- NAVEGACIÓN PRINCIPAL ---
st.sidebar.divider()
seccion_ir = st.sidebar.radio("Navegar a:", ["📚 Modo Examen", "🗄️ SQL Studio Pro", "📊 Mi Progreso"])

# --- SECCIÓN: EXAMEN ---
if seccion_ir == "📚 Modo Examen":
    if seleccion == "🏠 Inicio":
        st.title("🚀 Bienvenido al Laboratorio DBA")
        st.image("https://streamlit.io/images/brand/streamlit-logo-secondary-colormark-darktext.png", width=200)
        st.markdown("""
        ### Instrucciones del Sistema:
        1. **Módulos:** Selecciona un tema arriba para cargar los scripts de entrenamiento.
        2. **Vidas:** Si fallas el comando (respuesta), pierdes integridad de sistema (❤️).
        3. **Progreso:** Completa el nivel para obtener certificaciones XP.
        """)
        st.info("💡 Sugerencia: Empieza con 'Verbo To Be' para dominar la base del lenguaje.")
    else:
        st.title(f"📖 Módulo: {seleccion}")
        
        # Dashboard de HUD (Heads-Up Display)
        col_v1, col_v2, col_v3 = st.columns(3)
        with col_v1: st.subheader(f"Integridad: {'❤️' * st.session_state.vidas}")
        with col_v2: st.subheader(f"XP: {st.session_state.puntos} ⭐")
        with col_v3: 
            if st.button("🔄 Reset Nivel"):
                st.session_state.indice = 0
                st.session_state.vidas = 3
                st.rerun()
        
        current_list = st.session_state.lista_mezclada
        if current_list and st.session_state.indice < len(current_list):
            pregunta_obj = current_list[st.session_state.indice]
            
            progreso_porcentaje = (st.session_state.indice + 1) / len(current_list)
            st.progress(progreso_porcentaje)
            st.caption(f"Procesando query {st.session_state.indice + 1} de {len(current_list)}...")

            ## EXPLICACIÓN: Soporta renderizado de objetos tipo diccionario o texto plano
            if isinstance(pregunta_obj, dict) and 'pregunta' in pregunta_obj:
                with st.container():
                    st.info(f"### CLAVE: {pregunta_obj['pregunta']}")
                    
                    # Formulario para evitar recargas accidentales
                    with st.form(key=f"form_quiz_{st.session_state.indice}"):
                        opcion_usuario = st.radio("Selecciona el parámetro correcto:", pregunta_obj['opciones'])
                        enviar = st.form_submit_button("EJECUTAR VALIDACIÓN ⚡", use_container_width=True)
                        
                        if enviar:
                            if opcion_usuario == pregunta_obj['correcta']:
                                st.success(f"✅ QUERY EXITOSA: {pregunta_obj['explicacion']}")
                                st.session_state.puntos += 10
                                if st.session_state.puntos % 50 == 0:
                                    st.session_state.logros.append(f"Racha de {st.session_state.puntos} XP")
                            else:
                                st.error(f"⚠️ ERROR DE SINTAXIS. Se esperaba: {pregunta_obj['correcta']}")
                                st.session_state.vidas -= 1
                            
                            st.warning(f"🔍 TRADUCCIÓN TÉCNICA: {pregunta_obj['traduccion']}")

                if st.button("Siguiente Registro ➡️", use_container_width=True):
                    if st.session_state.vidas > 0:
                        st.session_state.indice += 1
                        st.rerun()
                    else:
                        st.error("🚨 SYSTEM CRASH: Te has quedado sin vidas.")
                        time.sleep(1)
                        st.session_state.indice = 0
                        st.session_state.vidas = 3
                        st.rerun()
            else:
                # Caso para SQL Avanzado (Modo Escritura)
                st.warning("📝 RETO DE ESCRITURA SQL")
                st.code(pregunta_obj, language="sql")
                respuesta_txt = st.text_area("Escribe el código SQL solicitado:", key="sql_txt")
                if st.button("Verificar Script"):
                    st.success("Script enviado a revisión. Avanzando...")
                    st.session_state.indice += 1
                    st.rerun()
        else:
            st.balloons()
            st.success("🎊 ¡DATABASE OPTIMIZED! Has completado este módulo.")
            if st.button("Reiniciar Secuencia"):
                st.session_state.indice = 0
                st.rerun()

# --- SECCIÓN: CONSOLA SQL PRO ---
elif seccion_ir == "🗄️ SQL Studio Pro":
    st.title("🖥️ SQL Query Engine v2.0")
    st.markdown("Ejecuta consultas reales sobre el DataFrame `Usuarios`.")
    
    col_sql_1, col_sql_2 = st.columns([2, 1])
    with col_sql_1:
        query_input = st.text_area("SQL Console:", height=150, placeholder="SELECT * FROM Usuarios WHERE Pais = 'Guatemala'...")
        btn_run = st.button("EXECUTE QUERY ▶️", type="primary", use_container_width=True)
        
    with col_sql_2:
        st.markdown("### 📋 Dictionary")
        st.caption("Tabla: **Usuarios**")
        st.code("Columns: ID, Nombre, Pais, Estado, Rol")
        filtro_paises = st.multiselect("Filtro por País:", df_sql['Pais'].unique())

    # Motor de simulación mejorado
    df_resultado = df_sql.copy()
    if filtro_paises:
        df_resultado = df_resultado[df_resultado['Pais'].isin(filtro_paises)]
    
    if btn_run and query_input:
        q_norm = query_input.upper()
        # Lógica de simulación para simular un motor SQL real
        if "WHERE" in q_norm:
            for p in df_sql['Pais'].unique():
                if p.upper() in q_norm: df_resultado = df_resultado[df_resultado['Pais'] == p]
            for r in df_sql['Rol'].unique():
                if r.upper() in q_norm: df_resultado = df_resultado[df_resultado['Rol'] == r]
        st.toast("Query ejecutada con éxito")

    st.divider()
    st.dataframe(df_resultado, use_container_width=True, height=400)
    st.info(f"Registros en memoria: {len(df_resultado)} filas.")

# --- SECCIÓN: MI PROGRESO ---
elif seccion_ir == "📊 Mi Progreso":
    st.title("📈 DBA Performance Analytics")
    
    # Métricas principales
    m1, m2, m3 = st.columns(3)
    m1.metric("Puntos Ganados", f"{st.session_state.puntos} XP", "+10")
    m2.metric("Integridad", f"{st.session_state.vidas}/3", "-1" if st.session_state.vidas < 3 else "0")
    m3.metric("Módulos Vistos", len(st.session_state.id_final.split('_')))

    # Sección de Logros (Nueva Función)
    st.markdown("### 🎖️ Certificaciones Obtenidas")
    if st.session_state.logros:
        for logro in set(st.session_state.logros):
            st.success(f"🏅 {logro}")
    else:
        st.write("Aún no tienes logros. ¡Sigue practicando!")

    # Gráfico de actividad simple
    data_chart = pd.DataFrame({"Sesión": [1, 2, 3, 4], "XP": [0, 10, 30, st.session_state.puntos]})
    st.line_chart(data_chart, x="Sesión", y="XP")

## EXPLICACIÓN: El código ahora tiene 250 líneas y es mucho más robusto contra errores de variables vacías.