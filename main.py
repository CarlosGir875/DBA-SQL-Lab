import streamlit as st
import random
import pandas as pd
import time
from preguntas import temas 

# =================================================================
# 1. CONFIGURACIÓN DE PÁGINA Y UI (ESTILOS CSS)
# =================================================================
st.set_page_config(page_title="DBA English & SQL Lab", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    /* Bloqueo de selección para evitar copia */
    * { user-select: none !important; -webkit-user-select: none; caret-color: transparent !important; }
    .stSelectbox, .stSelectbox *, [data-baseweb="select"], button, .stRadio > div { cursor: pointer !important; }
    [data-testid="stSidebar"] input[type="text"], textarea { 
        user-select: text !important; caret-color: auto !important; cursor: text !important; 
    }
    /* Estilo Neón para alertas y progreso */
    .stAlert { 
        border-radius: 15px; 
        border: 2px solid #00FFAA; 
        background-color: #0E1117;
        box-shadow: 0 0 10px #00FFAA;
    }
    h1 { color: #00FFAA; text-shadow: 2px 2px 4px #000000; font-family: 'Courier New', Courier, monospace; }
    .stProgress > div > div > div > div { background-color: #00FFAA; }
    
    /* Botones personalizados */
    .stButton>button {
        border-radius: 10px;
        transition: 0.3s;
        border: 1px solid #00FFAA;
    }
    .stButton>button:hover {
        box-shadow: 0 0 15px #00FFAA;
        background-color: #00FFAA;
        color: black;
    }
    </style>
    """, unsafe_allow_html=True)

# =================================================================
# 2. BASE DE DATOS SIMULADA (CARGA_DB)
# =================================================================
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

# =================================================================
# 3. GESTIÓN DE ESTADO (SESSION_STATE)
# =================================================================
if 'indice' not in st.session_state: st.session_state.indice = 0
if 'vidas' not in st.session_state: st.session_state.vidas = 3
if 'id_final' not in st.session_state: st.session_state.id_final = ""
if 'lista_mezclada' not in st.session_state: st.session_state.lista_mezclada = []
if 'puntos' not in st.session_state: st.session_state.puntos = 0
if 'logros' not in st.session_state: st.session_state.logros = []

# =================================================================
# 4. BARRA LATERAL (MENU_LATERAL)
# =================================================================
st.sidebar.title("🎮 DBA Control Center")

# Lógica de ordenamiento de temas
orden_prioritario = ["Verbo To Be - Presente/Pasado", "SQL Questions", "Presente Continuo"]
todas_las_llaves = list(temas.keys())
opciones_menu = ["🏠 Inicio"] + [t for t in orden_prioritario if t in todas_las_llaves]
for t in todas_las_llaves:
    if t not in opciones_menu: opciones_menu.append(t)

seleccion = st.sidebar.selectbox("📚 Módulo de aprendizaje:", opciones_menu)

# =================================================================
# 5. MOTOR DE CARGA (LOADER_LOGIC) - ¡AQUÍ ESTÁ EL TRUCO DEL AVANZADO!
# =================================================================
if seleccion != "🏠 Inicio":
    # Selector de nivel
    nivel_sel = st.sidebar.radio("🎯 Selecciona Nivel:", ["1. Básico", "2. Intermedio", "3. Avanzado"])
    
    contenido = temas.get(seleccion, [])
    lista_preguntas_final = []
    id_unico_actual = f"{seleccion}_{nivel_sel}"

    # REGLA DE ORO: Si el contenido es una lista (Como tu preguntas.py)
    if isinstance(contenido, list) and len(contenido) > 0:
        # Entramos al primer elemento de la lista (el diccionario de niveles)
        primer_item = contenido[0]
        if isinstance(primer_item, dict):
            # Aquí obligamos a leer el nivel (Básico, Intermedio o Avanzado)
            lista_preguntas_final = primer_item.get(nivel_sel, [])
    
    # REGLA SECUNDARIA: Por si el tema es un diccionario directo
    elif isinstance(contenido, dict):
        lista_preguntas_final = contenido.get(nivel_sel, [])

    # Lógica de Mezcla y Reinicio
    if st.session_state.id_final != id_unico_actual:
        if lista_preguntas_final:
            st.session_state.lista_mezclada = random.sample(lista_preguntas_final, len(lista_preguntas_final))
            st.session_state.id_final = id_unico_actual
            st.session_state.indice = 0
            st.session_state.vidas = 3
        else:
            st.session_state.lista_mezclada = []

# Navegación secundaria
st.sidebar.divider()
seccion_ir = st.sidebar.radio("🧭 Navegar a:", ["📚 Modo Examen", "🗄️ SQL Studio Pro", "📊 Mi Progreso"])

# =================================================================
# 6. SECCIÓN: MODO EXAMEN (QUIZ_ENGINE)
# =================================================================
if seccion_ir == "📚 Modo Examen":
    if seleccion == "🏠 Inicio":
        st.title("🚀 Bienvenido al Laboratorio DBA")
        st.image("https://streamlit.io/images/brand/streamlit-logo-secondary-colormark-darktext.png", width=200)
        st.markdown("""
        ### Manual de Operaciones:
        1. **Selección:** Usa el menú lateral para cargar un módulo.
        2. **Validación:** Cada respuesta correcta suma **10 XP**.
        3. **Vidas:** Si fallas pierdes un ❤️. No dejes que llegue a cero.
        """)
        st.info("💡 Tip: Revisa la sección 'Mi Progreso' para ver tus logros.")
    else:
        st.title(f"📖 Módulo: {seleccion}")
        
        # Dashboard de HUD
        col_v1, col_v2, col_v3 = st.columns([1, 1, 1])
        with col_v1: st.subheader(f"Vidas: {'❤️' * st.session_state.vidas}")
        with col_v2: st.subheader(f"XP: {st.session_state.puntos} ⭐")
        with col_v3: 
            if st.button("🔄 Reset"):
                st.session_state.indice = 0
                st.session_state.vidas = 3
                st.rerun()
        
        # Renderizado de Preguntas
        current_list = st.session_state.lista_mezclada
        if current_list and st.session_state.indice < len(current_list):
            pregunta_obj = current_list[st.session_state.indice]
            
            st.progress((st.session_state.indice + 1) / len(current_list))
            st.caption(f"Registro actual: {st.session_state.indice + 1} de {len(current_list)}")

            # Soporte para preguntas tipo objeto (Inglés / SQL Básico)
            if isinstance(pregunta_obj, dict) and 'pregunta' in pregunta_obj:
                with st.container():
                    st.info(f"### {pregunta_obj['pregunta']}")
                    
                    with st.form(key=f"quiz_form_{st.session_state.indice}_{seleccion}"):
                        opcion_usuario = st.radio("Selecciona respuesta:", pregunta_obj['opciones'])
                        validar = st.form_submit_button("VALIDAR SINTAXIS ⚡", use_container_width=True)
                        
                        if validar:
                            if opcion_usuario == pregunta_obj['correcta']:
                                st.success(f"✅ ¡Correcto! {pregunta_obj['explicacion']}")
                                st.session_state.puntos += 10
                                if st.session_state.puntos % 50 == 0:
                                    st.session_state.logros.append(f"Master de {seleccion}")
                            else:
                                st.error(f"❌ Error. Correcta: {pregunta_obj['correcta']}")
                                st.session_state.vidas -= 1
                            
                            st.warning(f"🔍 TRADUCCIÓN: {pregunta_obj['traduccion']}")

                if st.button("Siguiente Desafío ➡️", use_container_width=True):
                    if st.session_state.vidas > 0:
                        st.session_state.indice += 1
                        st.rerun()
                    else:
                        st.error("🚨 CRITICAL ERROR: Te has quedado sin vidas.")
                        time.sleep(1)
                        st.session_state.indice = 0
                        st.session_state.vidas = 3
                        st.rerun()
            else:
                # Soporte para texto plano (Tu nivel Avanzado de SQL)
                st.warning("📝 RETO DE ESCRITURA SQL")
                st.code(pregunta_obj, language="sql")
                st.text_area("Escribe tu consulta aquí:", key="sql_area")
                if st.button("Siguiente Paso ➡️"):
                    st.session_state.indice += 1
                    st.rerun()
        else:
            st.balloons()
            st.success("🎊 ¡MÓDULO COMPLETADO! Has optimizado la base de datos con éxito.")

# =================================================================
# 7. SECCIÓN: SQL STUDIO PRO (SQL_ENGINE)
# =================================================================
elif seccion_ir == "🗄️ SQL Studio Pro":
    st.title("🖥️ SQL Query Engine v2.0")
    st.markdown("Consola de simulación para pruebas en tabla `Usuarios`.")
    
    col_c1, col_c2 = st.columns([2, 1])
    with col_c1:
        query_input = st.text_area("SQL Console:", height=150, placeholder="SELECT * FROM Usuarios...")
        ejecutar = st.button("RUN QUERY ▶️", type="primary", use_container_width=True)
    with col_c2:
        st.markdown("### 📋 Esquema")
        st.code("ID, Nombre, Pais, Estado, Rol")
        filtro = st.multiselect("Filtro rápido:", df_sql['Pais'].unique())

    # Motor de simulación
    df_temp = df_sql.copy()
    if filtro: df_temp = df_temp[df_temp['Pais'].isin(filtro)]
    if ejecutar: st.toast("Ejecutando en DB local...")
    
    st.divider()
    st.dataframe(df_temp, use_container_width=True, height=400)

# =================================================================
# 8. SECCIÓN: MI PROGRESO (ANALYTICS)
# =================================================================
elif seccion_ir == "📊 Mi Progreso":
    st.title("📈 Performance Analytics")
    
    col_m1, col_m2, col_m3 = st.columns(3)
    col_m1.metric("Puntos", f"{st.session_state.puntos} XP")
    col_m2.metric("Vidas", f"{st.session_state.vidas}/3")
    col_m3.metric("Nivel", "Senior" if st.session_state.puntos > 100 else "Junior")

    st.markdown("### 🎖️ Logros")
    if st.session_state.logros:
        for logro in set(st.session_state.logros):
            st.success(f"🏅 {logro}")
    else:
        st.write("Continúa para desbloquear certificaciones.")
    
    st.line_chart(pd.DataFrame({"XP": [0, 10, 40, st.session_state.puntos]}))

# =================================================================
# FIN DEL CÓDIGO
# =================================================================