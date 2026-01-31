import streamlit as st
import pandas as pd
import random
import sqlite3
import requests
import time
from datetime import datetime
import json

# ==============================================================================
# 1. CONFIGURACIÓN DEL SISTEMA Y GESTIÓN DE SESIÓN
# ==============================================================================
st.set_page_config(
    page_title="DevMaster Pro Suite v4", 
    page_icon="🚀", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- INICIALIZACIÓN DE ESTADO (STATE MANAGEMENT) ---
# Usamos un patrón de diseño de estado para controlar la navegación profunda
if 'app_state' not in st.session_state:
    st.session_state.app_state = {
        'current_view': 'dashboard', # dashboard, training, sql_lab, profile
        'training_step': 0,          # 0: Select Topic, 1: Select Level, 2: Quiz
        'selected_topic': None,
        'selected_level': None,
        'xp': 150,
        'level': 4,
        'history_queries': []
    }

if 'db_trabajadores' not in st.session_state:
    st.session_state.db_trabajadores = None # Se inicializa más abajo

# --- FUNCIONES DE CONTROL DE XP (GAMIFICACIÓN) ---
def add_xp(amount):
    st.session_state.app_state['xp'] += amount
    threshold = st.session_state.app_state['level'] * 100
    if st.session_state.app_state['xp'] >= threshold:
        st.session_state.app_state['level'] += 1
        st.session_state.app_state['xp'] = 0
        st.toast(f"🏆 LEVEL UP! Ahora eres Nivel {st.session_state.app_state['level']}", icon="🔥")

# --- CARGA DE ASSETS (LOTTIE) ---
def load_lottie(url):
    try:
        r = requests.get(url)
        return r.json() if r.status_code == 200 else None
    except: return None

anim_sql = load_lottie("https://assets2.lottiefiles.com/private_files/lf30_w1uxkbue.json")
anim_code = load_lottie("https://assets5.lottiefiles.com/packages/lf20_fcfjwiyb.json")
anim_success = load_lottie("https://assets10.lottiefiles.com/packages/lf20_lk80fpsm.json")

# ==============================================================================
# 2. SISTEMA DE ESTILOS CSS (DISEÑO ATÓMICO)
# ==============================================================================
st.markdown("""
<style>
    /* --- FUENTES & RESET --- */
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Inter:wght@300;400;600;800&display=swap');
    
    :root {
        --bg-dark: #0f172a;
        --panel-dark: #1e293b;
        --accent-primary: #6366f1; /* Indigo */
        --accent-secondary: #ec4899; /* Pink */
        --text-main: #f8fafc;
        --text-dim: #94a3b8;
        --success: #10b981;
        --error: #ef4444;
    }

    /* --- GLOBAL OVERRIDES --- */
    .stApp {
        background-color: var(--bg-dark);
        background-image: 
            linear-gradient(rgba(15, 23, 42, 0.9), rgba(15, 23, 42, 0.95)),
            url("https://www.transparenttextures.com/patterns/cubes.png");
    }
    
    h1, h2, h3, h4 { color: var(--text-main) !important; font-family: 'Inter', sans-serif; }
    p, span, label { color: var(--text-dim) !important; font-family: 'Inter', sans-serif; }
    
    /* CURSOR LOGIC */
    .stApp { cursor: default; }
    button, .stButton, .stRadio label { cursor: pointer !important; }

    /* --- MODULE CARDS (Cuadros Redondos Solicitados) --- */
    /* Streamlit buttons are hard to style, so we wrap them or style the specific CSS class */
    div.stButton > button {
        background: linear-gradient(145deg, #1e293b, #26334a);
        color: white;
        border: 1px solid #334155;
        border-radius: 15px; /* Puntas redondas */
        padding: 20px;
        font-size: 16px;
        font-weight: 600;
        width: 100%;
        height: 100%;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        display: flex;
        justify-content: center;
        align-items: center;
    }
    
    div.stButton > button:hover {
        transform: translateY(-5px) scale(1.02);
        border-color: var(--accent-primary);
        box-shadow: 0 10px 20px rgba(99, 102, 241, 0.2);
        background: linear-gradient(145deg, #26334a, #1e293b);
    }

    div.stButton > button:active {
        transform: scale(0.98);
    }

    /* --- SIDEBAR STYLING --- */
    section[data-testid="stSidebar"] {
        background-color: #020617;
        border-right: 1px solid #334155;
    }

    /* --- PROFILE CARD EN SIDEBAR --- */
    .user-profile {
        background: rgba(255,255,255,0.03);
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        margin-bottom: 20px;
        border: 1px solid #334155;
    }
    .avatar-circle {
        width: 70px; height: 70px;
        background: linear-gradient(45deg, var(--accent-primary), var(--accent-secondary));
        border-radius: 50%;
        margin: 0 auto 10px;
        display: flex; align-items: center; justify-content: center;
        font-size: 30px; font-weight: bold; color: white;
        box-shadow: 0 0 15px rgba(99, 102, 241, 0.5);
    }

    /* --- SQL EDITOR --- */
    .sql-code-area textarea {
        background-color: #0b1120 !important;
        color: #a5b4fc !important;
        font-family: 'JetBrains Mono', monospace !important;
        border: 1px solid #4f46e5;
        border-radius: 8px;
    }

    /* --- RESULT TABLES --- */
    div[data-testid="stDataFrame"] {
        border: 1px solid #334155;
        border-radius: 8px;
        overflow: hidden;
    }

    /* --- FEEDBACK BOXES --- */
    .feedback-box {
        padding: 15px; border-radius: 8px; margin-top: 15px;
        animation: slideIn 0.4s ease-out;
    }
    .fb-success { background: rgba(16, 185, 129, 0.1); border-left: 4px solid var(--success); }
    .fb-error { background: rgba(239, 68, 68, 0.1); border-left: 4px solid var(--error); }

    @keyframes slideIn {
        from { opacity: 0; transform: translateX(-10px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    /* --- BREADCRUMB NAVIGATION --- */
    .breadcrumb {
        font-size: 0.9rem;
        color: var(--accent-primary) !important;
        margin-bottom: 1rem;
        font-weight: 600;
        cursor: pointer;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 3. LÓGICA DE DATOS Y CARGA SEGURA
# ==============================================================================

# Carga de Preguntas con Validación Robusta
TEMAS_DATA = {}
try:
    import preguntas
    import importlib
    importlib.reload(preguntas)
    if hasattr(preguntas, 'temas'):
        TEMAS_DATA = preguntas.temas
    else:
        st.error("⚠️ El archivo `preguntas.py` no tiene la estructura correcta.")
except ImportError:
    st.error("⚠️ No se encontró `preguntas.py`. Asegúrate de subirlo.")
except Exception as e:
    st.error(f"⚠️ Error crítico en `preguntas.py`: {e}")

# Generador de Datos (Base de Datos de 350+ Registros)
def get_database():
    if st.session_state.db_trabajadores is None:
        first_names = ["James", "Mary", "Robert", "Patricia", "John", "Jennifer", "Michael", "Linda", "David", "Elizabeth", "William", "Barbara", "Richard", "Susan", "Joseph", "Jessica", "Thomas", "Sarah", "Charles", "Karen"]
        last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore"]
        roles = ["Backend Dev", "Frontend Dev", "Fullstack Dev", "Data Scientist", "DevOps Eng", "QA Tester", "Product Owner", "Scrum Master", "DBA", "Tech Lead"]
        depts = ["IT", "Engineering", "Product", "Data", "Security"]
        
        data = []
        for i in range(1, 351):
            fn = random.choice(first_names)
            ln = random.choice(last_names)
            role = random.choice(roles)
            dept = random.choice(depts)
            salary = random.randint(3500, 18000)
            email = f"{fn.lower()}.{ln.lower()}{i}@intecap.edu.gt"
            joined = f"{random.randint(2019, 2025)}-{random.randint(1,12):02d}-{random.randint(1,28):02d}"
            
            data.append([i, fn, ln, email, role, dept, salary, joined])
            
        st.session_state.db_trabajadores = pd.DataFrame(
            data, 
            columns=["ID", "NOMBRE", "APELLIDO", "EMAIL", "CARGO", "DEPTO", "SUELDO", "FECHA_INGRESO"]
        )
    return st.session_state.db_trabajadores

# ==============================================================================
# 4. SIDEBAR MEJORADO (NAVEGACIÓN)
# ==============================================================================
with st.sidebar:
    # PERFIL DE USUARIO
    st.markdown(f"""
    <div class="user-profile">
        <div class="avatar-circle">DS</div>
        <h3 style="margin:0; font-size:1.1rem; color:white;">Dev Student</h3>
        <p style="font-size:0.8rem; margin:5px 0 15px 0;">Full Stack Path</p>
        
        <div style="background:rgba(255,255,255,0.1); height:6px; border-radius:3px; overflow:hidden;">
            <div style="background:#6366f1; width:{min(st.session_state.app_state['xp'], 100)}%; height:100%;"></div>
        </div>
        <div style="display:flex; justify-content:space-between; font-size:0.75rem; margin-top:5px; color:#94a3b8;">
            <span>Lvl {st.session_state.app_state['level']}</span>
            <span>{st.session_state.app_state['xp']} XP</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🧭 MENU PRINCIPAL")
    
    # Botones de navegación manuales para control total
    if st.button("🏠 Dashboard", key="nav_home"):
        st.session_state.app_state['current_view'] = 'dashboard'
        st.rerun()
        
    if st.button("🎓 Training Center", key="nav_training"):
        st.session_state.app_state['current_view'] = 'training'
        st.session_state.app_state['training_step'] = 0 # Resetear al inicio
        st.rerun()
        
    if st.button("🛢️ Laboratorio SQL", key="nav_sql"):
        st.session_state.app_state['current_view'] = 'sql_lab'
        st.rerun()

    # WIDGET DE AYUDA SQL (Solo visible en laboratorio)
    if st.session_state.app_state['current_view'] == 'sql_lab':
        st.markdown("---")
        st.markdown("### 📋 ESQUEMA TABLA")
        st.caption("Tabla: `TRABAJADORES`")
        cols = ["ID (INT)", "NOMBRE (TXT)", "APELLIDO (TXT)", "EMAIL (TXT)", "CARGO (TXT)", "DEPTO (TXT)", "SUELDO (INT)", "FECHA (DATE)"]
        for c in cols:
            st.code(c, language="text")
            
    st.markdown("---")
    st.caption("v4.0.1 Stable | Intecap")

# ==============================================================================
# 5. CONTROLADOR DE VISTAS (VIEW CONTROLLER)
# ==============================================================================

VIEW = st.session_state.app_state['current_view']

# --- VISTA 1: DASHBOARD ---
if VIEW == 'dashboard':
    col1, col2 = st.columns([2, 1])
    with col1:
        st.title("Bienvenido al Hub, Developer.")
        st.markdown("""
        Esta es tu central de operaciones. Aquí monitoreas tu progreso en inglés técnico y bases de datos.
        Selecciona un módulo en la izquierda para comenzar.
        """)
        
        # Tarjetas de Resumen KPI
        k1, k2, k3 = st.columns(3)
        k1.metric("Nivel Actual", f"Lvl {st.session_state.app_state['level']}", "+1 this week")
        k2.metric("Módulos Disp.", len(TEMAS_DATA), "Updated")
        k3.metric("Queries Ejec.", len(st.session_state.app_state['history_queries']))

    with col2:
        if anim_code: st_lottie(anim_code, height=250)

# --- VISTA 2: TRAINING CENTER (DRILL-DOWN) ---
elif VIEW == 'training':
    
    STEP = st.session_state.app_state['training_step']
    
    # --- PASO 0: SELECCIÓN DE TEMA (MODULOS CUADRADOS) ---
    if STEP == 0:
        st.title("🎓 Training Center")
        st.markdown("Selecciona un módulo para comenzar tu entrenamiento.")
        
        # Filtrar solo temas que existen
        temas = list(TEMAS_DATA.keys())
        
        # Crear Grid de Botones (3 por fila)
        cols = st.columns(3)
        for i, tema in enumerate(temas):
            # Usamos el índice para distribuir en columnas
            col = cols[i % 3]
            with col:
                # El botón ocupa todo el ancho de la columna gracias al CSS
                if st.button(f"📚\n{tema}", key=f"topic_{i}"):
                    st.session_state.app_state['selected_topic'] = tema
                    st.session_state.app_state['training_step'] = 1
                    st.rerun()

    # --- PASO 1: SELECCIÓN DE NIVEL ---
    elif STEP == 1:
        tema_actual = st.session_state.app_state['selected_topic']
        
        # Botón para volver atrás
        if st.button("⬅️ Volver a Temas"):
            st.session_state.app_state['training_step'] = 0
            st.rerun()
            
        st.title(f"Módulo: {tema_actual}")
        st.markdown("### Selecciona tu nivel de dificultad")
        
        try:
            # Obtener niveles disponibles
            contenido = TEMAS_DATA[tema_actual][0]
            niveles = list(contenido.keys())
            
            col_lvls = st.columns(len(niveles))
            
            for i, lvl in enumerate(niveles):
                with col_lvls[i]:
                    # Estilo diferente para botones de nivel
                    if st.button(f"📶 {lvl}", key=f"lvl_{i}"):
                        st.session_state.app_state['selected_level'] = lvl
                        st.session_state.app_state['training_step'] = 2
                        st.rerun()
        except Exception as e:
            st.error(f"Error cargando niveles: {e}")

    # --- PASO 2: QUIZ INTERACTIVO (PREGUNTAS) ---
    elif STEP == 2:
        tema = st.session_state.app_state['selected_topic']
        nivel = st.session_state.app_state['selected_level']
        
        # Navegación Breadcrumb
        col_back, col_title = st.columns([1, 5])
        with col_back:
            if st.button("⬅️ Cambiar Nivel"):
                st.session_state.app_state['training_step'] = 1
                st.rerun()
        with col_title:
            st.markdown(f"**{tema}** / *{nivel}*")

        # Cargar Preguntas
        try:
            preguntas = TEMAS_DATA[tema][0][nivel]
            
            # Barra de progreso
            progreso = st.progress(0)
            
            for idx, p in enumerate(preguntas):
                # Calcular progreso
                progreso.progress((idx + 1) / len(preguntas))
                
                # Tarjeta de Pregunta
                st.markdown(f"""
                <div style="background:#1e293b; padding:20px; border-radius:12px; border:1px solid #334155; margin-bottom:15px;">
                    <h3 style="margin-top:0;">Pregunta {idx+1}</h3>
                    <p style="font-size:1.1rem; color:#f1f5f9 !important;">{p['pregunta']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                c1, c2 = st.columns([3, 1])
                with c1:
                    opciones = p['opciones']
                    # Hack para mezclar opciones si quieres, o dejarlas fijas
                    val = st.radio("Tu respuesta:", opciones, key=f"q_{idx}", label_visibility="collapsed")
                
                with c2:
                    st.write("") # Spacer
                    st.write("")
                    check = st.button("Verificar", key=f"btn_{idx}")
                
                if check:
                    if val == p['correcta']:
                        st.markdown(f'<div class="feedback-box fb-success">✅ <b>¡Correcto!</b> Ganaste +20 XP</div>', unsafe_allow_html=True)
                        add_xp(20)
                        if anim_success: st_lottie(anim_success, height=100, key=f"anim_{idx}")
                    else:
                        st.markdown(f'<div class="feedback-box fb-error">❌ <b>Incorrecto.</b><br>Respuesta correcta: <b>{p["correcta"]}</b></div>', unsafe_allow_html=True)
                    
                    with st.expander("🔎 Ver Explicación y Contexto"):
                        st.info(f"**Explicación:** {p['explicacion']}")
                        st.caption(f"Traducción: {p['traduccion']}")
                
                st.markdown("---")
                
        except Exception as e:
            st.error(f"Error cargando preguntas: {e}")

# --- VISTA 3: LABORATORIO SQL (WORKBENCH) ---
elif VIEW == 'sql_lab':
    st.title("🛢️ Laboratorio SQL Profesional")
    
    col_main, col_side = st.columns([3, 1])
    
    with col_side:
        if anim_sql: st_lottie(anim_sql, height=150)
        st.markdown("### Historial")
        if len(st.session_state.app_state['history_queries']) > 0:
            for q in st.session_state.app_state['history_queries'][-5:]:
                st.code(q, language="sql")
        else:
            st.caption("Sin historial reciente.")

    with col_main:
        st.markdown("Escribe tus sentencias SQL para interactuar con la base de datos en memoria.")
        
        default_q = "SELECT * FROM TRABAJADORES WHERE DEPTO = 'IT' ORDER BY SUELDO DESC LIMIT 5;"
        
        # Editor estilizado
        st.markdown('<div class="sql-code-area">', unsafe_allow_html=True)
        query = st.text_area("", value=default_q, height=180, placeholder="SELECT * FROM ...")
        st.markdown('</div>', unsafe_allow_html=True)
        
        c_run, c_reset = st.columns([1, 4])
        
        if c_run.button("⚡ EJECUTAR QUERY", type="primary"):
            # Guardar en historial
            st.session_state.app_state['history_queries'].append(query)
            add_xp(10)
            
            # Backend SQL
            conn = sqlite3.connect(':memory:')
            df = get_database()
            df.to_sql('TRABAJADORES', conn, index=False, if_exists='replace')
            
            try:
                start_time = time.time()
                # Limpieza básica
                clean_query = query.strip()
                
                # Ejecución
                if clean_query.upper().startswith("SELECT"):
                    res = pd.read_sql_query(clean_query, conn)
                    duration = time.time() - start_time
                    
                    st.success(f"✅ Consulta exitosa en {duration:.4f}s | {len(res)} filas encontradas.")
                    st.dataframe(res, use_container_width=True)
                else:
                    # Para INSERT, UPDATE, DELETE (Simulado en memoria)
                    cursor = conn.cursor()
                    cursor.execute(clean_query)
                    conn.commit()
                    st.success("✅ Comando ejecutado (Nota: Los cambios son temporales en memoria).")
                    
            except Exception as e:
                st.error(f"⛔ Error SQL:\n{e}")
            finally:
                conn.close()

# ==============================================================================
# 6. FOOTER
# ==============================================================================
st.markdown("<br><br><hr>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center; color:#475569; font-size:0.8rem;">
    Desarrollado para Intecap 2026 | Arquitectura Modular v4.0 <br>
    <i>"Code is Poetry"</i>
</div>
""", unsafe_allow_html=True)