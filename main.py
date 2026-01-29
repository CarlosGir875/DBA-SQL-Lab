import streamlit as st
import random
import pandas as pd
from preguntas import temas 

# --- 1. CONFIGURACIÓN CSS (INTACTO) ---
st.markdown("""
    <style>
    * { user-select: none !important; -webkit-user-select: none; caret-color: transparent !important; }
    .stSelectbox, .stSelectbox *, [data-baseweb="select"] { cursor: pointer !important; }
    .stSelectbox input { pointer-events: none !important; }
    [data-testid="stSidebar"], h1, h2, h3, p, span { cursor: default !important; }
    button, [role="button"], [data-testid="stWidgetLabel"] p, .stRadio > div { cursor: pointer !important; }
    [data-testid="stSidebar"] input[type="text"], textarea { 
        user-select: text !important; caret-color: auto !important; cursor: text !important; pointer-events: auto !important; 
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. BASE DE DATOS SQL (INTACTO) ---
data_usuarios = {
    'ID': range(1, 301),
    'Nombre': ["Carlos Giron", "Juan Perez", "Maria Lopez", "Ana Garcia", "Luis Martinez", "Elena Rodriguez", "Diego Sosa", "Carmen Ruiz", "Pablo Duarte", "Lucia Mendez"] * 30,
    'Pais': ['Guatemala', 'Mexico', 'USA', 'España', 'El Salvador', 'Honduras'] * 50,
    'Estado': ['Activo', 'Inactivo', 'Pendiente'] * 100,
    'Rol': ['DBA', 'Dev', 'Analista', 'Soporte', 'Manager'] * 60
}
df_sql = pd.DataFrame(data_usuarios)

# --- 3. CONFIGURACIÓN PÁGINA Y STATE ---
st.set_page_config(page_title="DBA English & SQL Lab", page_icon="⚡", layout="wide")

if 'indice' not in st.session_state: st.session_state.indice = 0
if 'vidas' not in st.session_state: st.session_state.vidas = 3
if 'id_final' not in st.session_state: st.session_state.id_final = ""
if 'lista_mezclada' not in st.session_state: st.session_state.lista_mezclada = []

# --- 4. BARRA LATERAL (PANEL DE CONTROL) ---
st.sidebar.title("🎮 Panel de Control")

orden_logico = ["Verbos Irregulares", "Verbos Regulares", "Presente Continuo", "SQL Questions"]
opciones_menu = ["🏠 Inicio"] + [t for t in orden_logico if t in temas]
for t in temas.keys():
    if t not in opciones_menu: opciones_menu.append(t)

seleccion = st.sidebar.selectbox("¿Qué módulo quieres dominar?", opciones_menu)

# --- 5. LÓGICA DE SELECCIÓN DE NIVELES (EL MOTOR) ---
if seleccion != "🏠 Inicio":
    contenido = temas[seleccion]
    
    # Si el tema viene en una lista como [{'1. Básico': [...]}]
    if isinstance(contenido, list) and len(contenido) > 0 and isinstance(contenido[0], dict):
        diccionario_niveles = contenido[0]
        opciones_niveles = list(diccionario_niveles.keys())
        # index=0 para que cargue Básico automático y no tire error rojo
        nivel_elegido = st.sidebar.radio("Selecciona Nivel:", opciones_niveles, index=0)
        lista_preguntas = diccionario_niveles[nivel_elegido]
        id_actual = f"{seleccion}_{nivel_elegido}"
    else:
        # Si es una lista simple
        lista_preguntas = contenido
        id_actual = seleccion

    # Reinicio si cambia el tema
    if st.session_state.id_final != id_actual:
        st.session_state.lista_mezclada = lista_preguntas.copy()
        random.shuffle(st.session_state.lista_mezclada)
        st.session_state.id_final = id_actual
        st.session_state.indice = 0
        st.session_state.vidas = 3

# --- 6. BUSCADOR (INTACTO) ---
st.sidebar.divider()
with st.sidebar.expander("🔍 Buscador de Conceptos"):
    termino = st.text_input("Buscar palabra o comando:")
    if termino:
        for cat, contenido in temas.items():
            # (Lógica de búsqueda idéntica a la tuya...)
            if isinstance(contenido, list) and len(contenido) > 0 and isinstance(contenido[0], dict):
                for sub, lista in contenido[0].items():
                    for p in lista:
                        if termino.lower() in p['pregunta'].lower():
                            st.caption(f"**{cat} ({sub}):** {p['pregunta']}"); st.write(f"R: {p['correcta']}")
            elif isinstance(contenido, list):
                for p in contenido:
                    if termino.lower() in p['pregunta'].lower():
                        st.caption(f"**{cat}:** {p['pregunta']}"); st.write(f"R: {p['correcta']}")

# --- 7. NAVEGACIÓN PRINCIPAL ---
st.sidebar.divider()
seccion = st.sidebar.radio("Ir a:", ["📚 Examen", "🗄️ Consola SQL"])

if seccion == "📚 Examen":
    if seleccion == "🏠 Inicio":
        st.title("Welcome to DBA Lab! 📚")
        st.markdown(f"### ¡Welcome my app, I hope you can learn with my methods! 🚀\n Prepare for learn**.")
        st.info("Selecciona un tema a la izquierda para empezar.")
    else:
        # Título y Vidas
        st.title(f"🚀 {seleccion}")
        st.sidebar.subheader(f"Vidas: {'❤️' * st.session_state.vidas}")
        
        # ESCUDO ANTICRASH: Solo muestra si la lista tiene algo
        if st.session_state.lista_mezclada and st.session_state.indice < len(st.session_state.lista_mezclada):
            progreso = (st.session_state.indice + 1) / len(st.session_state.lista_mezclada)
            st.progress(progreso)
            
            pregunta_actual = st.session_state.lista_mezclada[st.session_state.indice]

            with st.form(key=f"quiz_{st.session_state.id_final}_{st.session_state.indice}"):
                st.markdown(f"### {pregunta_actual['pregunta']}")
                respuesta = st.radio("Elige la respuesta:", pregunta_actual['opciones'])
                
                if st.form_submit_button("Comprobar ✅", use_container_width=True):
                    if respuesta == pregunta_actual['correcta']:
                        st.success("✨ ¡Correcto!")
                    else:
                        st.session_state.vidas -= 1
                        st.error(f"❌ Incorrecto.")
                    st.info(f"💡 {pregunta_actual['explicacion']}")
                    st.write(f"🌍 {pregunta_actual['traduccion']}")

            if st.button("Siguiente Pregunta ➡️", use_container_width=True):
                if st.session_state.vidas > 0:
                    st.session_state.indice += 1
                    st.rerun()
                else:
                    st.warning("Te quedaste sin vidas. Reiniciando módulo...")
                    st.session_state.indice = 0
                    st.session_state.vidas = 3
                    st.rerun()
        else:
            st.balloons()
            st.success("¡Felicidades! Completaste este nivel.")
            if st.button("Reiniciar Nivel"):
                st.session_state.indice = 0
                st.session_state.vidas = 3
                st.rerun()

elif seccion == "🗄️ Consola SQL":
    # --- CONSOLA SQL (INTACTO) ---
    st.title("🖥️ SQL Studio")
    query_sql = st.text_area(label="", placeholder="SELECT * FROM Usuarios...", height=180)
    ejecutar = st.button("Execute Query ▶️", use_container_width=True, type="primary")
    paises = st.multiselect("Filtrar rápido:", ["Guatemala", "Mexico", "USA", "España", "El Salvador", "Honduras"])
    
    df_m = df_sql.copy()
    if ejecutar and query_sql:
        q_upper = query_sql.upper()
        if "GUATEMALA" in q_upper: df_m = df_m[df_m['Pais'] == 'Guatemala']
        elif "MEXICO" in q_upper: df_m = df_m[df_m['Pais'] == 'Mexico']
    if paises: df_m = df_m[df_m['Pais'].isin(paises)]

    st.markdown("#### Results:")
    st.dataframe(df_m, use_container_width=True, height=400)
    st.caption(f"Rows: {len(df_m)} | Database: Online ✅")