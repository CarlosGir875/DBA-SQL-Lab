import streamlit as st
import random
import pandas as pd  # <--- Agrega este si no lo tienes
from preguntas import temas  # Jala tus 6,600+ líneas de preguntas.py

st.markdown("""
    <style>
    /* 1. Bloqueo de selección y rayita global */
    * {
        user-select: none !important;
        -webkit-user-select: none;
        caret-color: transparent !important;
    }

    /* 2. FUERZA LA MANITA en todo el selector de temas */
    /* Usamos el contenedor principal para que no se pierda el puntero */
    .stSelectbox, .stSelectbox *, [data-baseweb="select"] {
        cursor: pointer !important;
    }

    /* 3. Bloqueo de escritura: Evita que el teclado interactúe con el menú */
    .stSelectbox input {
        pointer-events: none !important;
    }

    /* 4. Quita la "I" de los títulos y el panel */
    [data-testid="stSidebar"], h1, h2, h3, p, span {
        cursor: default !important;
    }

    /* 5. Fuerza manita en botones y radio buttons */
    button, [role="button"], [data-testid="stWidgetLabel"] p, .stRadio > div {
        cursor: pointer !important;
    }

    /* 6. EXCEPCIÓN: Buscador y Consola SQL (Aquí SÍ queremos escribir) */
    [data-testid="stSidebar"] input[type="text"], textarea {
        user-select: text !important;
        caret-color: auto !important;
        cursor: text !important;
        pointer-events: auto !important;
    }
    </style>
    """, unsafe_allow_html=True)
# --- CREACIÓN DE LA BASE DE DATOS (100 USUARIOS) ---
# Esto genera los datos para que la consola no tire error
# --- CREACIÓN DE LA BASE DE DATOS (300 USUARIOS) ---
data_usuarios = {
    'ID': range(1, 301), # 300 registros
    'Nombre': [
        "Carlos Giron", "Juan Perez", "Maria Lopez", "Ana Garcia", "Luis Martinez",
        "Elena Rodriguez", "Diego Sosa", "Carmen Ruiz", "Pablo Duarte", "Lucia Mendez"
    ] * 30, # 10 nombres * 30 = 300
    'Pais': ['Guatemala', 'Mexico', 'USA', 'España', 'El Salvador', 'Honduras'] * 50, # 6 países * 50 = 300
    'Estado': ['Activo', 'Inactivo', 'Pendiente'] * 100, # 3 estados * 100 = 300
    'Rol': ['DBA', 'Dev', 'Analista', 'Soporte', 'Manager'] * 60 # 5 roles * 60 = 300
}
# Esta línea ya no dará error porque todos miden 300
df_sql = pd.DataFrame(data_usuarios)

# 1. Configuración de la página
st.set_page_config(page_title="DBA English & SQL Lab", page_icon="⚡", layout="wide")

# 2. Inicialización de variables en el Session State
if 'indice' not in st.session_state:
    st.session_state.indice = 0
if 'vidas' not in st.session_state:
    st.session_state.vidas = 3
if 'tema_actual' not in st.session_state:
    st.session_state.tema_actual = ""

# --- BARRA LATERAL ---
st.sidebar.title("🎮 Panel de Control")

# Tu orden lógico de estudio
orden_logico = ["Verbo To Be", "Verbos Irregulares", "Verbos Regulares", "Presente Continuo", "SQL Questions"]

opciones_menu = ["🏠 Inicio"] + [t for t in orden_logico if t in temas]
for t in temas.keys():
    if t not in opciones_menu:
        opciones_menu.append(t)

# --- LÓGICA DE SELECCIÓN CON NIVELES (REEMPLAZO TOTAL) ---
seleccion = st.sidebar.selectbox("¿Qué módulo quieres dominar?", opciones_menu)

lista_preguntas = []
# --- LÓGICA DE SELECCIÓN CON NIVELES ---
if seleccion != "🏠 Inicio":
    # 1. Selector de Nivel
   # 1. Selector de Nivel (Solo se muestra si el tema tiene niveles)
    if isinstance(temas[seleccion], dict):
        nivel_elegido = st.radio("Dificultad:", list(temas[seleccion].keys()), horizontal=True)
        preguntas_finales = temas[seleccion][nivel_elegido]
        id_actual = f"{seleccion}_{nivel_elegido}"
    else:
        # Si es una lista vieja (sin niveles), lo usa directo
        preguntas_finales = temas[seleccion]
        id_actual = seleccion

    # 2. Reiniciamos si cambió el tema o el nivel
    if st.session_state.get("id_final") != id_actual:
        st.session_state.lista_mezclada = preguntas_finales.copy()
        random.shuffle(st.session_state.lista_mezclada)
        st.session_state.id_final = id_actual
        st.session_state.indice = 0
        st.session_state.vidas = 3

# --- BUSCADOR ACTUALIZADO (Para encontrar preguntas en los niveles) ---
st.sidebar.divider()
with st.sidebar.expander("🔍 Buscador de Conceptos"):
    termino = st.text_input("Buscar palabra o comando:")
    if termino:
        for cat, contenido in temas.items():
            if isinstance(contenido, dict):
                for sub, lista in contenido.items():
                    for p in lista:
                        if termino.lower() in p['pregunta'].lower():
                            st.caption(f"**{cat} ({sub}):** {p['pregunta']}")
                            st.write(f"R: {p['correcta']}")
            else:
                for p in contenido:
                    if termino.lower() in p['pregunta'].lower():
                        st.caption(f"**{cat}:** {p['pregunta']}")
                        st.write(f"R: {p['correcta']}")

# --- LÓGICA PRINCIPAL ---

# 1. Selector de Sección (Optimizado para pulgar en móvil)
st.sidebar.divider()
seccion = st.sidebar.radio("Ir a:", ["📚 Examen", "🗄️ Consola SQL"])

# --- SECCIÓN A: EXAMEN ---
if seccion == "📚 Examen":
    if seleccion == "🏠 Inicio":
        st.title("Welcome to DBA Lab! 📚")
        st.markdown(f"### ¡Welcome my app, I hope you can learn with my methods! 🚀\n Prepare for learn**.")
        st.info("Selecciona un tema a la izquierda para empezar.")
    else:
        # Lógica de preguntas (se mantiene igual pero optimizada)
        if st.session_state.tema_actual != seleccion:
            lista_shuffled = temas[seleccion].copy()
            random.shuffle(lista_shuffled)
            st.session_state.lista_mezclada = lista_shuffled
            st.session_state.tema_actual = seleccion
            st.session_state.indice = 0
            st.session_state.vidas = 3

        st.sidebar.subheader(f"Vidas: {'❤️' * st.session_state.vidas}")
        progreso_num = st.session_state.indice + 1
        total_p = len(st.session_state.lista_mezclada)
        
        st.title(f"🚀 {seleccion}")
        st.progress(progreso_num / total_p)

        pregunta_actual = st.session_state.lista_mezclada[st.session_state.indice]

        with st.form(key=f"quiz_{st.session_state.indice}"):
            st.markdown(f"### {pregunta_actual['pregunta']}")
            respuesta = st.radio("Elige la respuesta:", pregunta_actual['opciones'])
            # use_container_width hace que el botón sea grande en celular
            if st.form_submit_button("Comprobar ✅", use_container_width=True):
                if respuesta == pregunta_actual['correcta']:
                    st.success("✨ ¡Correcto!")
                else:
                    st.session_state.vidas -= 1
                    st.error(f"❌ Incorrecto.")
                st.info(f"💡 {pregunta_actual['explicacion']}")

        if st.button("Siguiente Pregunta ➡️", use_container_width=True):
            if st.session_state.indice < total_p - 1:
                st.session_state.indice += 1
                st.rerun()

# --- SECCIÓN B: CONSOLA SQL (Optimizado para Celular) ---
elif seccion == "🗄️ Consola SQL":
    st.title("🖥️ SQL Studio")
    
    # Cuadro grande para que quepa bien el código en el celular
    query_sql = st.text_area(
        label="", 
        placeholder="-- Escribe tu SELECT aquí...\nSELECT * FROM Usuarios WHERE Pais = 'Guatemala'",
        height=180 
    )
    
    # Botón principal ancho y llamativo
    ejecutar = st.button("Execute Query ▶️", use_container_width=True, type="primary")

    # Filtro rápido de apoyo
    paises = st.multiselect("Filtrar rápido:", ["Guatemala", "Mexico", "USA", "España", "El Salvador", "Honduras"])
    
    df_m = df_sql.copy() 
    
    # Simulación de motor SQL
    if ejecutar and query_sql:
        q_upper = query_sql.upper()
        if "GUATEMALA" in q_upper:
            df_m = df_m[df_m['Pais'] == 'Guatemala']
        elif "MEXICO" in q_upper:
            df_m = df_m[df_m['Pais'] == 'Mexico']
            
    if paises:
        df_m = df_m[df_m['Pais'].isin(paises)]

    # Resultados con scroll táctil
    st.markdown("#### Results:")
    st.dataframe(df_m, use_container_width=True, height=400)
    st.caption(f"Rows: {len(df_m)} | Database: Online ✅")