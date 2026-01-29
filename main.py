import streamlit as st
import random
import pandas as pd
from preguntas import temas 

# 1. CONFIGURACIÓN PÁGINA (De primero para evitar errores)
st.set_page_config(page_title="DBA English & SQL Lab", page_icon="⚡", layout="wide")

# 2. CSS (Tu estilo intacto)
st.markdown("""
    <style>
    * { user-select: none !important; -webkit-user-select: none; caret-color: transparent !important; }
    .stSelectbox, .stSelectbox *, [data-baseweb="select"] { cursor: pointer !important; }
    .stSelectbox input { pointer-events: none !important; }
    button, [role="button"], [data-testid="stWidgetLabel"] p, .stRadio > div { cursor: pointer !important; }
    [data-testid="stSidebar"] input[type="text"], textarea { 
        user-select: text !important; caret-color: auto !important; cursor: text !important; pointer-events: auto !important; 
    }
    </style>
    """, unsafe_allow_html=True)

# 3. BASE DE DATOS (Intacta)
df_sql = pd.DataFrame({
    'ID': range(1, 301),
    'Nombre': ["Carlos Giron", "Juan Perez", "Maria Lopez"] * 100,
    'Pais': ['Guatemala', 'Mexico', 'USA', 'España', 'El Salvador', 'Honduras'] * 50,
    'Estado': ['Activo', 'Inactivo', 'Pendiente'] * 100,
    'Rol': ['DBA', 'Dev', 'Analista', 'Soporte', 'Manager'] * 60
})

# 4. INICIALIZACIÓN SEGURA DEL ESTADO
if 'indice' not in st.session_state: st.session_state.indice = 0
if 'vidas' not in st.session_state: st.session_state.vidas = 3
if 'id_final' not in st.session_state: st.session_state.id_final = ""
if 'lista_mezclada' not in st.session_state: st.session_state.lista_mezclada = []

# --- BARRA LATERAL ---
st.sidebar.title("🎮 Panel de Control")
opciones_menu = ["🏠 Inicio"] + list(temas.keys())
seleccion = st.sidebar.selectbox("¿Qué módulo quieres dominar?", opciones_menu)

# --- MOTOR DE CARGA CON SENSOR DE DICCIONARIOS (Arregla SQL y Verbo To Be) ---
if seleccion != "🏠 Inicio":
    contenido = temas.get(seleccion, [])
    
    # Sensor: ¿Es lista de niveles o lista de preguntas?
    if isinstance(contenido, list) and len(contenido) > 0 and isinstance(contenido[0], dict):
        niveles_dict = contenido[0]
        nivel_elegido = st.sidebar.radio("Nivel:", list(niveles_dict.keys()), index=0)
        preguntas_seleccionadas = niveles_dict.get(nivel_elegido, [])
        id_actual = f"{seleccion}_{nivel_elegido}"
    else:
        preguntas_seleccionadas = contenido
        id_actual = seleccion

    # Solo si el ID cambió, reseteamos todo
    if st.session_state.id_final != id_actual:
        if preguntas_seleccionadas:
            temp_list = preguntas_seleccionadas.copy()
            random.shuffle(temp_list)
            st.session_state.lista_mezclada = temp_list
            st.session_state.id_final = id_actual
            st.session_state.indice = 0
            st.session_state.vidas = 3
        else:
            st.session_state.lista_mezclada = []

# --- NAVEGACIÓN ---
st.sidebar.divider()
seccion = st.sidebar.radio("Ir a:", ["📚 Examen", "🗄️ Consola SQL"])

if seccion == "📚 Examen":
    if seleccion == "🏠 Inicio":
        st.title("Welcome to DBA Lab! 🚀")
        st.info("Selecciona un tema a la izquierda para empezar.")
    else:
        st.title(f"🚀 {seleccion}")
        st.sidebar.subheader(f"Vidas: {'❤️' * st.session_state.vidas}")
        
        # EL ESCUDO DEFINITIVO: Solo corre si la lista existe y tiene la pregunta
        if st.session_state.lista_mezclada and st.session_state.indice < len(st.session_state.lista_mezclada):
            pregunta_actual = st.session_state.lista_mezclada[st.session_state.indice]
            
            # Verificación de llaves (Evita KeyError 'pregunta')
            if isinstance(pregunta_actual, dict) and 'pregunta' in pregunta_actual:
                st.progress((st.session_state.indice + 1) / len(st.session_state.lista_mezclada))
                
                with st.form(key=f"f_{st.session_state.id_final}_{st.session_state.indice}"):
                    st.markdown(f"### {pregunta_actual['pregunta']}")
                    res = st.radio("Respuesta:", pregunta_actual['opciones'])
                    if st.form_submit_button("Comprobar ✅", use_container_width=True):
                        if res == pregunta_actual['correcta']:
                            st.success("✨ ¡Correcto!")
                        else:
                            st.session_state.vidas -= 1
                            st.error("❌ Incorrecto.")
                        st.info(f"💡 {pregunta_actual['explicacion']}")
                        st.write(f"🌍 {pregunta_actual['traduccion']}")

                if st.button("Siguiente Pregunta ➡️", use_container_width=True):
                    if st.session_state.vidas > 0:
                        st.session_state.indice += 1
                        st.rerun()
                    else:
                        st.session_state.indice = 0
                        st.session_state.vidas = 3
                        st.rerun()
            else:
                st.error("Error en el formato de la pregunta. Revisa preguntas.py")
        else:
            st.warning("Cargando preguntas o nivel completado...")
            if st.button("Reiniciar"):
                st.session_state.indice = 0
                st.rerun()

elif seccion == "🗄️ Consola SQL":
    st.title("🖥️ SQL Studio")
    query = st.text_area("SQL Query:", placeholder="SELECT * FROM Usuarios...")
    if st.button("Execute ▶️", use_container_width=True):
        st.dataframe(df_sql, use_container_width=True)