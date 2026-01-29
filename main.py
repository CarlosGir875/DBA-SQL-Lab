import streamlit as st
import random
import pandas as pd
from preguntas import temas 

# 1. CONFIGURACIÓN INICIAL
st.set_page_config(page_title="DBA English & SQL Lab", page_icon="⚡", layout="wide")

# 2. TU CSS (Intacto)
st.markdown("""<style>
    * { user-select: none !important; -webkit-user-select: none; caret-color: transparent !important; }
    .stSelectbox, .stSelectbox *, [data-baseweb="select"] { cursor: pointer !important; }
    .stSelectbox input { pointer-events: none !important; }
    button, [role="button"], [data-testid="stWidgetLabel"] p, .stRadio > div { cursor: pointer !important; }
    [data-testid="stSidebar"] input[type="text"], textarea { 
        user-select: text !important; caret-color: auto !important; cursor: text !important; pointer-events: auto !important; 
    }
</style>""", unsafe_allow_html=True)

# 3. DATOS SQL (Intacto)
df_sql = pd.DataFrame({
    'ID': range(1, 301),
    'Nombre': ["Carlos Giron", "Juan Perez", "Maria Lopez"] * 100,
    'Pais': ['Guatemala', 'Mexico', 'USA', 'España', 'El Salvador', 'Honduras'] * 50,
    'Estado': ['Activo', 'Inactivo', 'Pendiente'] * 100,
    'Rol': ['DBA', 'Dev', 'Analista', 'Soporte', 'Manager'] * 60
})

# 4. SESSION STATE
if 'indice' not in st.session_state: st.session_state.indice = 0
if 'vidas' not in st.session_state: st.session_state.vidas = 3
if 'id_final' not in st.session_state: st.session_state.id_final = ""
if 'lista_mezclada' not in st.session_state: st.session_state.lista_mezclada = []

# --- BARRA LATERAL ---
st.sidebar.title("🎮 Panel de Control")
opciones_menu = ["🏠 Inicio"] + list(temas.keys())
seleccion = st.sidebar.selectbox("Módulo:", opciones_menu)

# --- MOTOR DE CARGA UNIVERSAL (El arreglo de los errores) ---
lista_preguntas = []
id_actual = seleccion

if seleccion != "🏠 Inicio":
    contenido = temas.get(seleccion, [])
    
    # CASO A: Es una lista que contiene un diccionario (SQL y Verbo To Be)
    if isinstance(contenido, list) and len(contenido) > 0 and isinstance(contenido[0], dict):
        diccionario_niveles = contenido[0]
        niveles = list(diccionario_niveles.keys())
        nivel_elegido = st.sidebar.radio("Dificultad:", niveles, index=0)
        lista_preguntas = diccionario_niveles.get(nivel_elegido, [])
        id_actual = f"{seleccion}_{nivel_elegido}"
    # CASO B: Es una lista directa de preguntas (Verbos)
    else:
        lista_preguntas = contenido
        id_actual = seleccion

    # Mezclar solo si cambiamos de tema/nivel
    if st.session_state.id_final != id_actual:
        if lista_preguntas:
            temp = lista_preguntas.copy()
            random.shuffle(temp)
            st.session_state.lista_mezclada = temp
            st.session_state.id_final = id_actual
            st.session_state.indice = 0
            st.session_state.vidas = 3

# --- SECCIONES ---
st.sidebar.divider()
seccion = st.sidebar.radio("Ir a:", ["📚 Examen", "🗄️ Consola SQL"])

if seccion == "📚 Examen":
    if seleccion == "🏠 Inicio":
        st.title("Welcome to DBA Lab! 🚀")
        st.info("Selecciona un tema a la izquierda.")
    else:
        st.title(f"🚀 {seleccion}")
        st.sidebar.subheader(f"Vidas: {'❤️' * st.session_state.vidas}")
        
        # ESCUDO: Solo muestra si hay preguntas cargadas
        if st.session_state.lista_mezclada and st.session_state.indice < len(st.session_state.lista_mezclada):
            preg = st.session_state.lista_mezclada[st.session_state.indice]
            
            st.progress((st.session_state.indice + 1) / len(st.session_state.lista_mezclada))
            
            with st.form(key=f"q_{st.session_state.id_final}_{st.session_state.indice}"):
                st.markdown(f"### {preg.get('pregunta', 'Pregunta no encontrada')}")
                resp = st.radio("Elige:", preg.get('opciones', []))
                
                if st.form_submit_button("Comprobar ✅", use_container_width=True):
                    if resp == preg.get('correcta'):
                        st.success("✨ ¡Correcto!")
                    else:
                        st.session_state.vidas -= 1
                        st.error("❌ Incorrecto.")
                    st.info(f"💡 {preg.get('explicacion', '')}")
                    st.write(f"🌍 {preg.get('traduccion', '')}")

            if st.button("Siguiente ➡️", use_container_width=True):
                if st.session_state.vidas > 0:
                    st.session_state.indice += 1
                    st.rerun()
                else:
                    st.session_state.indice = 0; st.session_state.vidas = 3; st.rerun()
        else:
            st.warning("Cargando o nivel completado.")
            if st.button("Reiniciar"):
                st.session_state.indice = 0; st.rerun()

elif seccion == "🗄️ Consola SQL":
    st.title("🖥️ SQL Studio")
    st.dataframe(df_sql, use_container_width=True)