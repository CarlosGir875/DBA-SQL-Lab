import streamlit as st
import random
import pandas as pd
import time
from preguntas import temas 

# =================================================================
# 1. CONFIGURACIÓN DE PÁGINA Y UI ENGINE (NEON SYSTEM)
# =================================================================
st.set_page_config(page_title="DBA English & SQL Lab 2026", page_icon="⚡", layout="wide")

# CSS PERSONALIZADO - DECORACIÓN EXTREMA Y LAYOUT DE TARJETAS
st.markdown("""
<style>
    /* IMPORTAR FUENTES CYBER */
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');

    .stApp { 
        background-color: #0D1117; 
        color: #C9D1D9; 
        font-family: 'Segoe UI', sans-serif; 
    }
    
    /* CURSOR POINTER SYSTEM */
    * { cursor: pointer !important; }
    input, textarea, [data-testid="stHeader"] { cursor: default !important; }

    /* CONTENEDOR DE TARJETAS (DASHBOARD) */
    .main-container {
        padding: 20px;
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 20px;
    }

    .card {
        background: linear-gradient(145deg, #161b22, #0d1117);
        border: 1px solid #30363d;
        border-radius: 15px;
        padding: 25px;
        text-align: center;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 5px 5px 15px rgba(0,0,0,0.3);
    }

    .card:hover {
        border-color: #00FFAA;
        transform: scale(1.03) translateY(-5px);
        box-shadow: 0 0 25px rgba(0, 255, 170, 0.2);
    }

    /* TÍTULOS NEON */
    h1, h2, h3 {
        font-family: 'JetBrains Mono', monospace;
        color: #00FFAA !important;
        text-shadow: 0 0 10px rgba(0, 255, 170, 0.3);
    }

    /* ESTILO DE BOTONES DE ACCIÓN */
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        border: 1px solid #00FFAA;
        background: transparent;
        color: #00FFAA;
        font-weight: bold;
        padding: 10px;
        transition: 0.3s;
    }

    .stButton>button:hover {
        background: #00FFAA;
        color: #0D1117;
        box-shadow: 0 0 20px #00FFAA;
    }

    /* SIDEBAR CUSTOM */
    [data-testid="stSidebar"] {
        background: #010409 !important;
        border-right: 1px solid #30363D;
    }

    .user-card {
        background: rgba(0, 255, 170, 0.1);
        padding: 15px;
        border-radius: 12px;
        border: 1px solid #00FFAA33;
        margin-bottom: 25px;
    }

    /* CONSOLA DE TELEMETRÍA */
    .console-box {
        background: #000;
        color: #00FFAA;
        font-family: 'JetBrains Mono', monospace;
        padding: 10px;
        border-radius: 5px;
        font-size: 0.75rem;
        border-left: 3px solid #00FFAA;
        height: 120px;
        overflow-y: auto;
    }

    /* STATUS LIGHT */
    .online-led {
        height: 8px;
        width: 8px;
        background-color: #00FFAA;
        border-radius: 50%;
        display: inline-block;
        box-shadow: 0 0 8px #00FFAA;
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0% { opacity: 0.4; }
        50% { opacity: 1; }
        100% { opacity: 0.4; }
    }

    /* REMOVER ELEMENTOS STREAMLIT */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# =================================================================
# 2. SISTEMA DE DATOS Y ESTADO (PERSISTENCIA)
# =================================================================
if 'page' not in st.session_state: st.session_state.page = "dashboard"
if 'indice' not in st.session_state: st.session_state.indice = 0
if 'vidas' not in st.session_state: st.session_state.vidas = 3
if 'puntos' not in st.session_state: st.session_state.puntos = 0
if 'logs' not in st.session_state: st.session_state.logs = [f"[{time.strftime('%H:%M:%S')}] Core Init."]
if 'terminal_out' not in st.session_state: st.session_state.terminal_out = ["DBA OS v2.0 Ready..."]
if 'training_sub' not in st.session_state: st.session_state.training_sub = "Home"

def add_log(msg):
    st.session_state.logs.append(f"[{time.strftime('%H:%M:%S')}] {msg}")
    if len(st.session_state.logs) > 10: st.session_state.logs.pop(0)

@st.cache_data
def get_db():
    nombres = ["Carlos Giron", "Juan Perez", "Maria Lopez", "Ana Garcia", "Luis Martinez", "Elena Rodriguez"]
    paises = ['Guatemala', 'Mexico', 'USA', 'España', 'El Salvador']
    roles = ['DBA', 'Lead Eng', 'Security Ops']
    return pd.DataFrame([{
        'ID': 1000 + i, 'Nombre': random.choice(nombres), 'Pais': random.choice(paises),
        'Rol': random.choice(roles), 'Estado': 'Activo', 'Storage': f"{random.randint(50, 500)}GB"
    } for i in range(1, 301)])

df_sql = get_db()

# =================================================================
# 3. SIDEBAR (PERFIL Y TELEMETRÍA)
# =================================================================
with st.sidebar:
    st.markdown("""
        <div style='text-align: center; margin-bottom: 20px;'>
            <img src='https://cdn-icons-png.flaticon.com/512/2312/2312676.png' width='80' style='filter: drop-shadow(0 0 10px #00FFAA);'>
            <h2 style='margin-top: 10px;'>DBA CORE</h2>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div class="user-card">
            <small style='color: #8B949E;'>IDENTIFIED OPERATOR</small><br>
            <b>Developer SY</b> <span class="online-led"></span><br>
            <small style='color: #00FFAA;'>LEVEL: SENIOR DBA</small>
        </div>
    """, unsafe_allow_html=True)

    # NAVEGACIÓN PRINCIPAL (SIDEBAR COMO CONTROL REMOTO)
    st.markdown("### 🧭 NAVIGATION")
    if st.button("🏠 DASHBOARD MAIN"): st.session_state.page = "dashboard"
    if st.button("📚 TRAINING MODULE"): st.session_state.page = "training"
    if st.button("🗄️ SQL STUDIO"): st.session_state.page = "sql"
    if st.button("📟 TERMINAL"): st.session_state.page = "terminal"
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 📡 TELEMETRY")
    log_content = "".join([f"<div>> {l}</div>" for l in st.session_state.logs])
    st.markdown(f'<div class="console-box">{log_content}</div>', unsafe_allow_html=True)

# =================================================================
# 4. VISTA: DASHBOARD PRINCIPAL (GRID DE TARJETAS)
# =================================================================
if st.session_state.page == "dashboard":
    st.markdown("<h1>⚡ MISSION CONTROL DASHBOARD</h1>", unsafe_allow_html=True)
    st.write("Bienvenido al núcleo del laboratorio. Selecciona un módulo para iniciar.")

    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="card"><h3>📚 Training</h3><p>Aprende inglés técnico y gramática aplicada a bases de datos.</p></div>', unsafe_allow_html=True)
        if st.button("LAUNCH TRAINING", key="go_train"): 
            st.session_state.page = "training"
            st.rerun()

    with col2:
        st.markdown('<div class="card"><h3>🗄️ SQL Studio</h3><p>Entorno de práctica para consultas SQL seguras y eficientes.</p></div>', unsafe_allow_html=True)
        if st.button("OPEN STUDIO", key="go_sql"): 
            st.session_state.page = "sql"
            st.rerun()

    with col3:
        st.markdown('<div class="card"><h3>📟 Terminal</h3><p>Consola de administración para auditoría de sistema.</p></div>', unsafe_allow_html=True)
        if st.button("BOOT TERMINAL", key="go_term"): 
            st.session_state.page = "terminal"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    col4, col5, col6 = st.columns(3)

    with col4:
        st.markdown('<div class="card"><h3>📊 Stats</h3><p>Monitoreo de progreso y puntos XP acumulados.</p></div>', unsafe_allow_html=True)
        if st.button("VIEW ANALYTICS"): add_log("Opening Stats...")

    with col5:
        st.markdown('<div class="card"><h3>🏆 Goals</h3><p>Desbloquea logros por tu desempeño en el código.</p></div>', unsafe_allow_html=True)
        if st.button("ACHIEVEMENTS"): add_log("Checking Medals...")

    with col6:
        st.markdown('<div class="card"><h3>⚙️ Config</h3><p>Ajustes de sistema y preferencias de usuario.</p></div>', unsafe_allow_html=True)
        if st.button("SYSTEM SETUP"): add_log("Access Denied.")

# =================================================================
# 5. VISTA: TRAINING MODE (SUB-MENÚ ORGANIZADO)
# =================================================================
elif st.session_state.page == "training":
    st.markdown("<h1>📚 TRAINING MODE SELECTION</h1>", unsafe_allow_html=True)
    
    # SUB-MENÚ DE OPCIONES (Nuevos bloques adentro)
    tabs = st.tabs(["📌 Categorías", "🎮 Quiz Active", "📖 Theory"])

    with tabs[0]:
        st.write("Selecciona una rama de estudio para cargar el dataset:")
        c_v1, c_v2 = st.columns(2)
        
        with c_v1:
            st.markdown("### 🏷️ Verbos & Vocabulario")
            if st.button("Irregular Verbs"): 
                st.session_state.training_sub = "Irregulars"
                add_log("Dataset: Irregulars loaded")
            if st.button("Regular Verbs"): 
                st.session_state.training_sub = "Regulars"
                add_log("Dataset: Regulars loaded")
            if st.button("SQL Vocabulary"): 
                st.session_state.training_sub = "SQL Vocab"
        
        with c_v2:
            st.markdown("### ⏳ Tiempos Verbales")
            if st.button("Present Continuous"): 
                st.session_state.training_sub = "Present Cont"
            if st.button("Past Simple"): 
                st.session_state.training_sub = "Past"
            if st.button("Future (Will/Going to)"): 
                st.session_state.training_sub = "Future"

        st.info(f"MODO ACTUAL CARGADO: **{st.session_state.training_sub}**")

    with tabs[1]:
        # Aquí va tu motor de Quiz original pero encapsulado
        st.markdown(f"## Testing: {st.session_state.training_sub}")
        
        m1, m2 = st.columns([1, 1])
        m1.metric("HEALTH", "❤️" * st.session_state.vidas)
        m2.metric("SCORE", f"{st.session_state.puntos} XP")

        # Simulación de carga de preguntas según sub-módulo
        st.markdown("---")
        st.write("Escribe el código para el siguiente reto:")
        st.info("Question placeholder: Translate 'The server is running' to Present Continuous.")
        
        ans = st.text_input("Your Response:")
        if st.button("VALIDATE ENTRY"):
            if ans: 
                st.success("Correct! +15 XP")
                st.session_state.puntos += 15
                add_log("Validation success.")
            else:
                st.error("Invalid input.")

    with tabs[2]:
        st.markdown("### 📘 Manual de Referencia")
        st.write("Aquí puedes consultar las reglas antes de tomar el quiz.")
        with st.expander("Ver reglas de Present Continuous"):
            st.write("Subject + am/is/are + verb-ing...")

# =================================================================
# 6. VISTA: SQL STUDIO PRO
# =================================================================
elif st.session_state.page == "sql":
    st.markdown("<h1>🗄️ SQL MANAGEMENT STUDIO PRO</h1>", unsafe_allow_html=True)
    
    col_l, col_r = st.columns([2, 1])
    
    with col_l:
        query = st.text_area("SQL Editor", height=250, placeholder="SELECT * FROM DB_TABLE WHERE...")
        if st.button("EXECUTE QUERY (F5)"):
            if "SELECT" in query.upper():
                st.success("Execution successful. 300 records found.")
                st.dataframe(df_sql, use_container_width=True)
                add_log("SQL Query executed.")
            else:
                st.warning("Only SELECT statements allowed in training.")

    with col_r:
        st.markdown("### 🤖 SQL Mentor AI")
        if query:
            st.info("Analysis: Your query looks optimal. Consider adding LIMIT for large datasets.")
        else:
            st.write("Waiting for code input...")

# =================================================================
# 7. VISTA: TERMINAL (CONSOLA DE COMANDOS)
# =================================================================
elif st.session_state.page == "terminal":
    st.markdown("<h1>📟 SYSTEM TERMINAL</h1>", unsafe_allow_html=True)
    
    # Caja de consola estilo Matrix
    terminal_box = ""
    for line in st.session_state.terminal_out[-10:]:
        terminal_box += f"> {line}\n"
    
    st.code(terminal_box, language="bash")
    
    cmd_in = st.text_input("root@dba_lab:~#")
    
    if st.button("RUN CMD"):
        if cmd_in:
            st.session_state.terminal_out.append(cmd_in)
            if "HELP" in cmd_in.upper():
                st.session_state.terminal_out.append("Commands: STATUS, CLEAR, FETCH_XP, WHOAMI")
            elif "STATUS" in cmd_in.upper():
                st.session_state.terminal_out.append("SYSTEM: OPTIMAL | LATENCY: 12ms")
            elif "CLEAR" in cmd_in.upper():
                st.session_state.terminal_out = ["Terminal cleared."]
            else:
                st.session_state.terminal_out.append(f"Error: command '{cmd_in}' not found.")
            add_log(f"Terminal use: {cmd_in}")
            st.rerun()

# =================================================================
# FIN DEL CÓDIGO - DBA CORE 2026
# =================================================================