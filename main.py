import streamlit as st
import random
import pandas as pd
import time
from preguntas import temas 

# =================================================================
# 1. CONFIGURACIÓN DE PÁGINA Y UI (ESTILOS CSS AVANZADOS)
# =================================================================
st.set_page_config(page_title="DBA English & SQL Lab", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    /* Bloqueo de selección */
    * { user-select: none !important; -webkit-user-select: none; caret-color: transparent !important; }
    
    /* Estilo del Sidebar (Menú Lateral) */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0E1117 0%, #1a1c24 100%);
        border-right: 2px solid #00FFAA;
    }
    
    /* Cursor personalizado */
    .stSelectbox, .stSelectbox *, [data-baseweb="select"], button, .stRadio > div { cursor: pointer !important; }
    [data-testid="stSidebar"] input[type="text"], textarea { 
        user-select: text !important; caret-color: auto !important; cursor: text !important; 
    }

    /* Estilo Neón para alertas y tarjetas */
    .stAlert { 
        border-radius: 15px; 
        border: 2px solid #00FFAA; 
        background-color: #0E1117;
        box-shadow: 0 0 15px rgba(0, 255, 170, 0.3);
    }

    /* Títulos y fuentes Cyberpunk */
    h1, h2, h3 { 
        color: #00FFAA; 
        text-shadow: 0 0 10px #00FFAA; 
        font-family: 'Courier New', Courier, monospace; 
    }
    
    /* Barra de progreso Neón */
    .stProgress > div > div > div > div { 
        background-image: linear-gradient(to right, #00FFAA, #0088ff); 
    }

    /* Botones Pro */
    .stButton>button {
        border-radius: 8px;
        transition: all 0.4s ease;
        border: 1px solid #00FFAA;
        background-color: transparent;
        color: #00FFAA;
        font-weight: bold;
    }
    .stButton>button:hover {
        box-shadow: 0 0 20px #00FFAA;
        background-color: #00FFAA;
        color: #000;
        transform: scale(1.02);
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
st.sidebar.title("🎮 DBA CONTROL PANEL")

# Orden dinámico de temas
orden_prioritario = ["Verbo To Be - Presente/Pasado", "SQL Questions", "Presente Continuo"]
todas_las_llaves = list(temas.keys())
opciones_menu = ["🏠 Inicio"] + [t for t in orden_prioritario if t in todas_las_llaves]
for t in todas_las_llaves:
    if t not in opciones_menu: opciones_menu.append(t)

seleccion = st.sidebar.selectbox("📂 Módulo de aprendizaje:", opciones_menu)

# Lógica de Rangos (Función Nueva)
def obtener_rango(xp):
    if xp < 50: return "Novato (Trainee)"
    if xp < 150: return "Junior DBA"
    if xp < 300: return "Senior DBA"
    return "SQL Master Elite"

# =================================================================
# 5. MOTOR DE CARGA (LOADER_LOGIC) - ¡NO BUGS!
# =================================================================
# =================================================================
# 5. MOTOR DE CARGA (LOADER_LOGIC) - ¡EL BUSCADOR ANTIFALLOS!
# =================================================================
if seleccion != "🏠 Inicio":
    # El usuario elige esto en la UI
    nivel_sel = st.sidebar.radio("🎯 Selecciona Nivel:", ["1. Básico", "2. Intermedio", "3. Avanzado"])
    
    contenido = temas.get(seleccion, [])
    lista_preguntas_final = []
    id_unico_actual = f"{seleccion}_{nivel_sel}"

    # --- BUSCADOR INTELIGENTE ---
    if isinstance(contenido, list):
        for bloque in contenido:
            if isinstance(bloque, dict):
                # Esto busca si la palabra "Avanzado" está en alguna llave, 
                # no importa si dice "3. Avanzado" o "Avanzado" a secas.
                for llave in bloque.keys():
                    if nivel_sel.split(". ")[-1] in llave or llave in nivel_sel:
                        lista_preguntas_final = bloque[llave]
                        break
    
    # Lógica de Mezcla y Reset
    if st.session_state.id_final != id_unico_actual:
        if lista_preguntas_final:
            st.session_state.lista_mezclada = random.sample(lista_preguntas_final, len(lista_preguntas_final))
            st.session_state.id_final = id_unico_actual
            st.session_state.indice = 0
            st.session_state.vidas = 3
        else:
            # Si llega aquí, es que de verdad no encontró nada
            st.session_state.lista_mezclada = []
            st.session_state.id_final = id_unico_actual

st.sidebar.divider()
seccion_ir = st.sidebar.radio("🧭 Navegación:", ["📚 Modo Examen", "🗄️ SQL Studio Pro", "📊 Mi Progreso"])
st.sidebar.caption(f"Rango actual: {obtener_rango(st.session_state.puntos)}")

# =================================================================
# 6. SECCIÓN: MODO EXAMEN (QUIZ_ENGINE)
# =================================================================
if seccion_ir == "📚 Modo Examen":
    if seleccion == "🏠 Inicio":
        st.title("🚀 DBA English & SQL Lab")
        st.markdown("---")
        st.info("SISTEMA ONLINE. Por favor, selecciona un módulo en el menú lateral para comenzar el despliegue.")
        st.image("https://streamlit.io/images/brand/streamlit-logo-secondary-colormark-darktext.png", width=200)
    else:
        st.title(f"📖 Módulo: {seleccion}")
        
        # HUD de Integridad
        hud_1, hud_2, hud_3 = st.columns(3)
        hud_1.markdown(f"### Vidas: {'❤️' * st.session_state.vidas}")
        hud_2.markdown(f"### XP: {st.session_state.puntos} ⭐")
        with hud_3:
            if st.button("🔄 Reset Total"):
                st.session_state.indice = 0
                st.session_state.vidas = 3
                st.rerun()

        # Validación de banco de datos
        if not st.session_state.lista_mezclada:
            st.warning("⚠️ Sin datos en este nivel. Intenta con otro.")
        
        elif st.session_state.indice < len(st.session_state.lista_mezclada):
            pregunta_obj = st.session_state.lista_mezclada[st.session_state.indice]
            
            # Progreso visual
            prog = (st.session_state.indice + 1) / len(st.session_state.lista_mezclada)
            st.progress(prog)
            st.caption(f"Pregunta {st.session_state.indice + 1} de {len(st.session_state.lista_mezclada)}")

            # Caso A: Preguntas con Opciones (Básico / Intermedio)
            if isinstance(pregunta_obj, dict) and 'pregunta' in pregunta_obj:
                with st.container():
                    st.info(f"#### {pregunta_obj['pregunta']}")
                    
                    with st.form(key=f"form_{st.session_state.indice}"):
                        opc = st.radio("Selecciona la sintaxis correcta:", pregunta_obj['opciones'])
                        validar = st.form_submit_button("EJECUTAR SCRIPT ⚡")
                        
                        if validar:
                            if opc == pregunta_obj['correcta']:
                                st.success(f"✅ COMPILADO EXITOSO: {pregunta_obj['explicacion']}")
                                st.session_state.puntos += 10
                                st.toast("¡XP Ganada!", icon="⭐")
                            else:
                                st.error(f"❌ ERROR DE SINTAXIS. Correcta: {pregunta_obj['correcta']}")
                                st.session_state.vidas -= 1
                                st.toast("Integridad comprometida", icon="⚠️")
                            
                            st.warning(f"💡 TRADUCCIÓN TÉCNICA: {pregunta_obj['traduccion']}")

                if st.button("Siguiente Registro ➡️", use_container_width=True):
                    if st.session_state.vidas > 0:
                        st.session_state.indice += 1
                        st.rerun()
                    else:
                        st.error("🚨 DATABASE CRASH: Te has quedado sin vidas.")
                        time.sleep(2)
                        st.session_state.indice = 0
                        st.session_state.vidas = 3
                        st.rerun()

            # Caso B: Retos de Escritura (Avanzado SQL)
            else:
                st.warning("📝 RETO DE ESCRITURA SQL (Nivel Avanzado)")
                st.code(pregunta_obj, language="sql")
                respuesta = st.text_area("Consola SQL:", placeholder="Escribe tu query aquí...", key=f"sql_{st.session_state.indice}")
                
                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    if st.button("Validar y Seguir ➡️"):
                        st.session_state.indice += 1
                        st.session_state.puntos += 15
                        st.rerun()
                with col_btn2:
                    if st.button("🆘 Pánico (Pista)"):
                        st.toast("Revisa los comandos CREATE o TRIGGER en la documentación.", icon="📖")

        else:
            st.balloons()
            st.success("🎊 ¡SISTEMA OPTIMIZADO! Has completado el módulo con éxito.")
            if st.button("Volver a Empezar"):
                st.session_state.indice = 0
                st.rerun()

# =================================================================
# 7. SECCIÓN: SQL STUDIO PRO
# =================================================================
elif seccion_ir == "🗄️ SQL Studio Pro":
    st.title("🖥️ SQL Management Studio Simulator")
    st.markdown("Prueba tus queries sobre la tabla `Usuarios`.")
    
    query = st.text_area("SQL Editor:", height=100, placeholder="SELECT * FROM Usuarios WHERE Pais = 'Guatemala'...")
    
    col_run, col_clear = st.columns([1, 4])
    if col_run.button("EXECUTE ▶️", type="primary"):
        st.toast("Ejecutando consulta...")
        st.dataframe(df_sql, use_container_width=True)
    
    st.divider()
    st.caption("Diccionario de datos: ID (int), Nombre (string), Pais (string), Estado (string), Rol (string)")

# =================================================================
# 8. SECCIÓN: MI PROGRESO (ANALYTICS)
# =================================================================
elif seccion_ir == "📊 Mi Progreso":
    st.title("📈 Performance Analytics")
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Puntos Totales", f"{st.session_state.puntos} XP", "+10")
    m2.metric("Nivel de Acceso", obtener_rango(st.session_state.puntos))
    m3.metric("Integridad Sistema", f"{st.session_state.vidas}/3")

    # Gráfico de XP simple
    st.write("### Historial de Rendimiento")
    chart_data = pd.DataFrame({"Sesión": range(1, 6), "XP": [0, 20, 50, 100, st.session_state.puntos]})
    st.line_chart(chart_data, x="Sesión", y="XP")

# =================================================================
# FIN DEL CÓDIGO (Carlos Giron - DBA Lab 2026)
# =================================================================