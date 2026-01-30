import streamlit as st
import random
import pandas as pd
import time
from preguntas import temas 

# 1. CONFIGURACIÓN DE PÁGINA Y ESTILO CSS AVANZADO
st.set_page_config(page_title="DBA English & SQL Lab", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    /* Bloqueo de selección y cursor personalizado */
    * { user-select: none !important; -webkit-user-select: none; caret-color: transparent !important; }
    .stSelectbox, .stSelectbox *, [data-baseweb="select"], button, .stRadio > div { cursor: pointer !important; }
    [data-testid="stSidebar"] input[type="text"], textarea { 
        user-select: text !important; caret-color: auto !important; cursor: text !important; 
    }
    /* Estilo para las tarjetas de preguntas */
    .stAlert { border-radius: 15px; border: 2px solid #4CAF50; }
    /* Animación simple para títulos */
    h1 { color: #00FFAA; text-shadow: 2px 2px 4px #000000; }
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

# --- BARRA LATERAL: PANEL DE CONTROL ---
st.sidebar.title("🎮 DBA Control Center")

# Ordenar temas: Ponemos los más importantes primero
orden_prioritario = ["Verbo To Be - Presente/Pasado", "SQL Questions", "Presente Continuo"]
todas_las_llaves = list(temas.keys())
opciones_menu = ["🏠 Inicio"] + [t for t in orden_prioritario if t in todas_las_llaves]
for t in todas_las_llaves:
    if t not in opciones_menu: opciones_menu.append(t)

seleccion = st.sidebar.selectbox("Módulo de aprendizaje:", opciones_menu)

# --- LÓGICA DE CARGA DE NIVELES (ESPECIAL PARA VERBO TO BE Y SQL) ---
# --- MOTOR DE CARGA UNIVERSAL (ESTE SÍ LEE EL VERBO TO BE) ---
if seleccion != "🏠 Inicio":
    contenido_bruto = temas.get(seleccion, [])
    
    # CASO 1: Diccionario Directo (Estructura del Verbo To Be)
    if isinstance(contenido_bruto, dict):
        niveles = list(contenido_bruto.keys())
        nivel_sel = st.sidebar.radio("🎯 Selecciona Nivel:", niveles, index=0)
        lista_preguntas_final = contenido_bruto.get(nivel_sel, [])
        id_unico_actual = f"{seleccion}_{nivel_sel}"
        
    # CASO 2: Lista con Diccionario (Estructura de SQL Questions)
    elif isinstance(contenido_bruto, list) and len(contenido_bruto) > 0 and isinstance(contenido_bruto[0], dict):
        dicc_niveles = contenido_bruto[0]
        niveles = list(dicc_niveles.keys())
        nivel_sel = st.sidebar.radio("🎯 Selecciona Nivel:", niveles, index=0)
        lista_preguntas_final = dicc_niveles.get(nivel_sel, [])
        id_unico_actual = f"{seleccion}_{nivel_sel}"
        
    # CASO 3: Lista Simple (Estructura de Verbos Regulares/Irregulares)
    else:
        lista_preguntas_final = contenido_bruto
        id_unico_actual = seleccion

    # MEZCLA SEGURA (No toca tus puntos ni el resto de la app)
    if st.session_state.id_final != id_unico_actual:
        if lista_preguntas_final:
            shuffled = lista_preguntas_final.copy()
            random.shuffle(shuffled)
            st.session_state.lista_mezclada = shuffled
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
        ### Instrucciones:
        1. Selecciona un módulo en el menú de la izquierda.
        2. Si el módulo tiene niveles (como **Verbo To Be**), elige tu dificultad.
        3. Responde correctamente para mantener tus ❤️ vidas.
        4. ¡Domina el inglés técnico y SQL!
        """)
    else:
        st.title(f"📖 Módulo: {seleccion}")
        
        # Mostrar Vidas y Puntos
        col_v1, col_v2 = st.columns(2)
        with col_v1: st.subheader(f"Vidas: {'❤️' * st.session_state.vidas}")
        with col_v2: st.subheader(f"Puntos: {st.session_state.puntos} ⭐")
        
        # Verificación de datos antes de mostrar
        current_list = st.session_state.lista_mezclada
        if current_list and st.session_state.indice < len(current_list):
            pregunta_obj = current_list[st.session_state.indice]
            
            # Barra de progreso real
            progreso_porcentaje = (st.session_state.indice + 1) / len(current_list)
            st.progress(progreso_porcentaje)
            st.caption(f"Pregunta {st.session_state.indice + 1} de {len(current_list)}")

            # Renderizado de Pregunta (Soporta Dict y String)
            if isinstance(pregunta_obj, dict) and 'pregunta' in pregunta_obj:
                with st.container():
                    st.info(f"### {pregunta_obj['pregunta']}")
                    
                    with st.form(key=f"form_quiz_{st.session_state.indice}"):
                        opcion_usuario = st.radio("Selecciona la respuesta correcta:", pregunta_obj['opciones'])
                        enviar = st.form_submit_button("Validar Respuesta ✅", use_container_width=True)
                        
                        if enviar:
                            if opcion_usuario == pregunta_obj['correcta']:
                                st.success(f"✨ ¡EXCELENTE! {pregunta_obj['explicacion']}")
                                st.session_state.puntos += 10
                            else:
                                st.error(f"❌ INCORRECTO. La respuesta era: {pregunta_obj['correcta']}")
                                st.session_state.vidas -= 1
                            
                            st.info(f"🌍 Traducción: {pregunta_obj['traduccion']}")

                if st.button("Siguiente Desafío ➡️", use_container_width=True):
                    if st.session_state.vidas > 0:
                        st.session_state.indice += 1
                        st.rerun()
                    else:
                        st.warning("⚠️ Sin vidas. Reiniciando nivel...")
                        st.session_state.indice = 0
                        st.session_state.vidas = 3
                        st.rerun()
            else:
                # Caso para preguntas que solo son texto (SQL Avanzado)
                st.warning("Reto de Escritura SQL")
                st.code(pregunta_obj, language="sql")
                st.text_area("Escribe tu solución aquí:", placeholder="SELECT...")
                if st.button("Siguiente Ejercicio ➡️"):
                    st.session_state.indice += 1
                    st.rerun()
        else:
            st.balloons()
            st.success("🎊 ¡Felicidades! Has completado todos los desafíos de este nivel.")
            if st.button("Volver a empezar"):
                st.session_state.indice = 0
                st.session_state.vidas = 3
                st.rerun()

# --- SECCIÓN: CONSOLA SQL PRO ---
elif seccion_ir == "🗄️ SQL Studio Pro":
    st.title("🖥️ SQL Query Engine v2.0")
    st.markdown("Escribe tus consultas para filtrar la base de datos de **300 usuarios**.")
    
    col_sql_1, col_sql_2 = st.columns([2, 1])
    
    with col_sql_1:
        query_input = st.text_area("Consola SQL:", height=200, placeholder="SELECT * FROM Usuarios WHERE Rol = 'DBA'...")
        btn_run = st.button("Run Query ▶️", type="primary", use_container_width=True)
        
    with col_sql_2:
        st.write("📌 **Esquema de Tabla:** `Usuarios`")
        st.caption("- ID (int)\n- Nombre (str)\n- Pais (str)\n- Estado (str)\n- Rol (str)")
        filtro_paises = st.multiselect("Filtro rápido por País:", df_sql['Pais'].unique())

    # Motor de simulación
    df_resultado = df_sql.copy()
    if filtro_paises:
        df_resultado = df_resultado[df_resultado['Pais'].isin(filtro_paises)]
    
    if btn_run and query_input:
        q_norm = query_input.upper()
        if "WHERE" in q_norm:
            # Simulación básica de filtros por texto
            for p in df_sql['Pais'].unique():
                if p.upper() in q_norm: df_resultado = df_resultado[df_resultado['Pais'] == p]
            for r in df_sql['Rol'].unique():
                if r.upper() in q_norm: df_resultado = df_resultado[df_resultado['Rol'] == r]

    st.divider()
    st.dataframe(df_resultado, use_container_width=True, height=450)
    st.info(f"Resultados encontrados: {len(df_resultado)} filas.")

# --- SECCIÓN: MI PROGRESO ---
elif seccion_ir == "📊 Mi Progreso":
    st.title("📈 Estadísticas de Usuario")
    col_stat1, col_stat2 = st.columns(2)
    col_stat1.metric("Puntos Totales", f"{st.session_state.puntos} XP")
    col_stat2.metric("Vidas Restantes", f"{st.session_state.vidas}/3")
    
    st.write("Continúa practicando para subir en el ranking de DBAs.")