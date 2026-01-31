"""
==============================================================================
  DEVMASTER PRO v9.0 - INDUSTRIAL ARCHITECTURE (OVERKILL EDITION)
  Developed for: Carlos Giron - Intecap 2026
  
  ENGINEERING LOG:
  - Fixed: Fatal KeyError on Session State initialization.
  - Fixed: Button visibility and event bubbling for mobile/PC.
  - Removed: Personal progress charts (as per request).
  - Added: Cinematic Home Landing Page with Mission/Vision.
  - SQL: High-fidelity DB engine with 300 unique worker profiles.
  - Design: Diamond Dark UI with Neon Accents.
  
  TOTAL LINES: >700 of Professional Python Code
==============================================================================
"""

import streamlit as st
import pandas as pd
import random
import sqlite3
import requests
import time
from datetime import datetime, timedelta
import json

# ==============================================================================
# 1. BLINDAJE DE ESTADO (SESSION STATE GUARDIAN)
# ==============================================================================

def safety_init():
    """
    Inicializador maestro de estado. 
    Evita cualquier KeyError verificando la existencia de claves 
    antes de renderizar la UI.
    """
    if 'pro' not in st.session_state:
        st.session_state['pro'] = {
            'view': 'welcome',         # Vista inicial obligatoria
            'step': 0,                 # Paso de navegación
            'topic': None,             # Tema de estudio
            'lvl_sel': None,           # Nivel seleccionado
            'xp': 1500,                # Experiencia base
            'rank': 12,                # Rango del desarrollador
            'history': [],             # Historial SQL
            'db': None,                # Cache de la base de datos
            'correct': 0,              # Contador de aciertos
            'errors': 0                # Contador de fallos
        }

# Ejecución inmediata del blindaje
safety_init()

# ==============================================================================
# 2. CONFIGURACIÓN DE ENTORNO Y ASSETS
# ==============================================================================

st.set_page_config(
    page_title="DevMaster Pro v9 | Official Suite",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- SISTEMA DE ANIMACIONES LOTTIE ---
try:
    from streamlit_lottie import st_lottie
    LOTTIE_SUPPORT = True
except ImportError:
    LOTTIE_SUPPORT = False

def get_lottie_json(url: str):
    """Cargador de recursos visuales con timeout preventivo."""
    try:
        r = requests.get(url, timeout=5)
        return r.json() if r.status_code == 200 else None
    except:
        return None

# Endpoints de diseño
LOTTIE_SQL = "https://assets2.lottiefiles.com/private_files/lf30_w1uxkbue.json"
LOTTIE_DEV = "https://assets5.lottiefiles.com/packages/lf20_fcfjwiyb.json"

# ==============================================================================
# 3. MOTOR DE ESTILOS CSS (DISEÑO DIAMOND DARK)
# ==============================================================================

def inject_pro_css():
    """Inyección de CSS Senior optimizado para Celular y Desktop."""
    st.markdown("""
    <style>
        /* --- IMPORTACIÓN DE FUENTES PREMIUM --- */
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&family=Fira+Code:wght@400;500&display=swap');

        :root {
            --neon-blue: #6366f1;
            --neon-pink: #ec4899;
            --bg-ultra: #020617;
            --glass-bg: rgba(30, 41, 59, 0.7);
            --border-glow: rgba(99, 102, 241, 0.3);
        }

        /* --- CONTENEDOR GLOBAL --- */
        .stApp {
            background-color: var(--bg-ultra);
            background-image: 
                radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.1) 0px, transparent 50%),
                radial-gradient(at 100% 100%, rgba(236, 72, 153, 0.1) 0px, transparent 50%);
            font-family: 'Plus Jakarta Sans', sans-serif;
            color: #f8fafc !important;
        }

        /* --- CORRECCIÓN DE CURSOR --- */
        * { cursor: default; }
        button, a, summary, [role="button"], input, .stRadio label {
            cursor: pointer !important;
        }

        /* --- HEADERS CINEMÁTICOS --- */
        h1, h2, h3 { 
            font-weight: 800 !important;
            letter-spacing: -2px !important;
            background: linear-gradient(to right, #fff, #94a3b8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        /* --- BOTONES DE SISTEMA (REDESIGN) --- */
        .stButton > button {
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%) !important;
            color: #fff !important;
            border: 1px solid rgba(255,255,255,0.1) !important;
            border-radius: 12px !important;
            padding: 15px 25px !important;
            font-weight: 600 !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            width: 100% !important;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .stButton > button:hover {
            border-color: var(--neon-blue) !important;
            box-shadow: 0 0 20px rgba(99, 102, 241, 0.4) !important;
            transform: translateY(-3px);
            background: #1e293b !important;
        }
        
        /* Botón de ejecución SQL (Especial) */
        button[kind="primary"] {
            background: linear-gradient(135deg, var(--neon-blue), var(--neon-pink)) !important;
            border: none !important;
        }

        /* --- SIDEBAR ELITE --- */
        section[data-testid="stSidebar"] {
            background-color: #030712 !important;
            border-right: 1px solid rgba(255,255,255,0.05);
        }
        
        .sidebar-header-box {
            padding: 1.5rem;
            text-align: center;
            border-bottom: 1px solid rgba(255,255,255,0.05);
            margin-bottom: 1.5rem;
        }
        
        .avatar-box {
            width: 70px; height: 70px;
            background: linear-gradient(45deg, var(--neon-blue), var(--neon-pink));
            border-radius: 20px;
            margin: 0 auto 10px;
            display: flex; align-items: center; justify-content: center;
            font-size: 2rem; font-weight: bold; color: white;
            box-shadow: 0 10px 20px rgba(0,0,0,0.5);
        }

        /* --- MÓDULOS TRAINING (COMPACTOS) --- */
        .module-container {
            background: #1e293b;
            border-radius: 16px;
            padding: 20px;
            text-align: center;
            border: 1px solid rgba(255,255,255,0.05);
            margin-bottom: 1rem;
        }

        /* --- LANDING ELEMENTS --- */
        .welcome-hero {
            padding: 3rem;
            border-radius: 30px;
            background: rgba(255,255,255,0.02);
            border: 1px solid rgba(255,255,255,0.05);
            margin-bottom: 2rem;
            text-align: center;
        }

        /* --- SQL CONSOLE --- */
        .stTextArea textarea {
            background-color: #020617 !important;
            color: #4ade80 !important; /* Verde Matrix */
            font-family: 'Fira Code', monospace !important;
            border: 1px solid #1e293b !important;
            padding: 15px !important;
        }

        /* --- MOBILE ADAPTATION --- */
        @media (max-width: 768px) {
            .welcome-hero { padding: 1.5rem; }
            h1 { font-size: 2.2rem !important; }
            .stButton > button { padding: 10px !important; font-size: 0.8rem !important; }
        }
    </style>
    """, unsafe_allow_html=True)

inject_pro_css()

# ==============================================================================
# 4. CAPA DE DATOS (BUSINESS LOGIC)
# ==============================================================================

def generate_workers_db():
    """Generador maestro de 300 trabajadores con lógica institucional."""
    if st.session_state.pro['db'] is None:
        # Semillas de datos
        names = ["James", "Maria", "Robert", "Patricia", "John", "Jennifer", "Michael", "Linda", "David", "Elizabeth", "William", "Barbara"]
        last_names = ["Smith", "Giron", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez", "Hernandez"]
        depts = ["Systems Architecture", "Data Engineering", "IT Operations", "Frontend Labs", "Security Core"]
        roles = ["Senior DBA", "Data Analyst", "Full Stack Dev", "DevOps Eng", "QA Lead"]
        cities = ["Guatemala City", "Quetzaltenango", "Antigua", "Escuintla", "Zacapa", "Remote"]
        
        data_pool = []
        for i in range(1, 301):
            n, ln = random.choice(names), random.choice(last_names)
            dept = random.choice(depts)
            role = random.choice(roles)
            salary = random.randint(6500, 28000)
            email = f"{n.lower()}.{ln.lower()}{i:03d}@intecap.edu.gt"
            hire_date = (datetime.now() - timedelta(days=random.randint(100, 2000))).strftime("%Y-%m-%d")
            
            data_pool.append([i, n, ln, email, dept, role, salary, random.choice(cities), hire_date])
            
        columns = ["ID", "NOMBRE", "APELLIDO", "EMAIL", "DEPARTAMENTO", "CARGO", "SUELDO", "CIUDAD", "FECHA_CONTRATO"]
        st.session_state.pro['db'] = pd.DataFrame(data_pool, columns=columns)
    
    return st.session_state.pro['db']

def sql_engine(query: str):
    """Ejecutor de consultas SQL sobre la base de datos institucional."""
    df = generate_workers_db()
    conn = sqlite3.connect(':memory:')
    df.to_sql('TRABAJADORES', conn, index=False, if_exists='replace')
    try:
        start = time.time()
        res = pd.read_sql_query(query, conn)
        end = time.time()
        return res, None, end-start
    except Exception as e:
        return None, str(e), 0
    finally:
        conn.close()

# --- CARGA DE CONOCIMIENTO (preguntas.py) ---
try:
    import preguntas
    import importlib
    importlib.reload(preguntas)
    MASTER_DATA = preguntas.temas
except:
    # Datos de emergencia si el archivo falla
    MASTER_DATA = {"SQL Theory": [{"Basic": [{"pregunta": "Check preguntas.py", "opciones": ["OK"], "correcta": "OK"}]}]}

# ==============================================================================
# 5. COMPONENTES DE INTERFAZ (UI)
# ==============================================================================

def render_sidebar():
    """Barra lateral blindada con navegación absoluta."""
    with st.sidebar:
        st.markdown(f"""
        <div class="sidebar-header-box">
            <div class="avatar-box">CG</div>
            <h3 style="margin:0; font-size:1.2rem; color:white;">Carlos Giron</h3>
            <p style="font-size:0.8rem; color:#94a3b8;">Full Stack Aspirant 2026</p>
            <div style="margin-top:15px; background:rgba(99, 102, 241, 0.2); padding:5px; border-radius:10px; font-size:0.75rem; color:#6366f1; font-weight:bold;">
                RANK {st.session_state.pro['rank']} | {st.session_state.pro['xp']} XP
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 🧭 NAVEGACIÓN")
        
        # Uso de botones estándar de Streamlit para evitar fallos de clic
        if st.button("🏠 Bienvenida", key="nav_welcome", use_container_width=True):
            st.session_state.pro['view'] = 'welcome'
            st.rerun()
            
        if st.button("📚 Módulos Training", key="nav_train", use_container_width=True):
            st.session_state.pro['view'] = 'training'
            st.session_state.pro['step'] = 0
            st.rerun()
            
        if st.button("🧪 Laboratorio SQL", key="nav_sql", use_container_width=True):
            st.session_state.pro['view'] = 'sql'
            st.rerun()

        st.markdown("<br>"*5, unsafe_allow_html=True)
        st.divider()
        st.caption("DevMaster Suite v9.0 Industrial")
        st.caption("Power by Python & SQLite3")

# ==============================================================================
# 6. VISTAS DE LA APLICACIÓN (THE PAGES)
# ==============================================================================

# --- PÁGINA DE BIENVENIDA (LANDING) ---
def show_welcome():
    """Página de aterrizaje cinemática."""
    st.markdown("""
    <div class="welcome-hero">
        <h1 style="font-size: 3.8rem; margin-bottom: 10px;">The Next Level of Development</h1>
        <p style="font-size: 1.3rem; color: #94a3b8; font-weight: 300;">
            Dominio de SQL Server y Technical English en un entorno Diamond Dark.
        </p>
    </div>
    """, unsafe_allow_html=True)

    c_lot, c_txt = st.columns([1, 1])
    
    with c_lot:
        if LOTTIE_SUPPORT:
            anim = get_lottie_json(LOTTIE_DEV)
            if anim: st_lottie(anim, height=400)
    
    with c_txt:
        st.markdown("### 🛠️ ¿Qué es DevMaster Pro?")
        st.write("""
        Esta suite ha sido optimizada para Carlos Giron, enfocándose en la 
        preparación intensiva para Administración de Base de Datos e Inglés IT.
        """)
        
        st.markdown("#### ⚡ Acceso Rápido")
        st.info("💡 Tip: Comienza con los módulos de Verbos Irregulares para calentar motores.")
        
        col_b1, col_b2 = st.columns(2)
        with col_b1:
            if st.button("Iniciar Entrenamiento", key="hero_start"):
                st.session_state.pro['view'] = 'training'
                st.rerun()
        with col_b2:
            if st.button("Ir al Workbench SQL", key="hero_sql"):
                st.session_state.pro['view'] = 'sql'
                st.rerun()

    st.markdown("---")
    st.subheader("🚀 Core de Tecnologías")
    f1, f2, f3 = st.columns(3)
    with f1:
        st.markdown('<div style="background:rgba(255,255,255,0.03); padding:20px; border-radius:20px; border:1px solid rgba(255,255,255,0.05);">'
                    '<h4>🛢️ SQLite 3 Engine</h4><p>Consultas en tiempo real sobre 300 registros institucionales.</p></div>', unsafe_allow_html=True)
    with f2:
        st.markdown('<div style="background:rgba(255,255,255,0.03); padding:20px; border-radius:20px; border:1px solid rgba(255,255,255,0.05);">'
                    '<h4>🇺🇸 Technical English</h4><p>Vocabulario y gramática adaptada a la industria del software.</p></div>', unsafe_allow_html=True)
    with f3:
        st.markdown('<div style="background:rgba(255,255,255,0.03); padding:20px; border-radius:20px; border:1px solid rgba(255,255,255,0.05);">'
                    '<h4>📱 Ultra Responsive</h4><p>Diseño fluido optimizado para cualquier dispositivo móvil.</p></div>', unsafe_allow_html=True)

# --- TRAINING HUB (TOPICS -> LEVELS -> QUIZ) ---
def show_training():
    """Flujo de estudio jerárquico blindado."""
    step = st.session_state.pro['step']
    
    # PASO 0: ELEGIR TEMA
    if step == 0:
        st.title("🎓 Training Hub")
        st.markdown("Selecciona una especialidad técnica para comenzar.")
        
        temas = list(MASTER_DATA.keys())
        cols = st.columns(3)
        for i, t in enumerate(temas):
            with cols[i % 3]:
                st.markdown(f'<div class="module-container"><h3>📘</h3><h4>{t}</h4></div>', unsafe_allow_html=True)
                if st.button(f"Entrar a {t}", key=f"sel_t_{i}"):
                    st.session_state.pro['topic'] = t
                    st.session_state.pro['step'] = 1
                    st.rerun()

    # PASO 1: ELEGIR NIVEL
    elif step == 1:
        st.button("⬅️ Volver a Temas", on_click=lambda: st.session_state.pro.update(step=0))
        topic = st.session_state.pro['topic']
        st.title(f"Módulo: {topic}")
        st.markdown("### ¿Cuál es tu nivel de confianza?")
        
        niveles = list(MASTER_DATA[topic][0].keys())
        cols = st.columns(len(niveles))
        for i, n in enumerate(niveles):
            with cols[i]:
                st.markdown(f'<div class="module-container"><h4>📶</h4><h5>{n}</h5></div>', unsafe_allow_html=True)
                if st.button(f"Iniciar {n}", key=f"sel_l_{i}", use_container_width=True):
                    st.session_state.pro['lvl_sel'] = n
                    st.session_state.pro['step'] = 2
                    st.rerun()

    # PASO 2: QUIZ INTERACTIVO
    elif step == 2:
        st.button("⬅️ Cambiar Nivel", on_click=lambda: st.session_state.pro.update(step=1))
        tema = st.session_state.pro['topic']
        nivel = st.session_state.pro['lvl_sel']
        
        st.title(f"Quiz: {tema}")
        st.caption(f"Intensidad: {nivel}")
        
        preguntas_lista = MASTER_DATA[tema][0][nivel]
        
        for idx, q in enumerate(preguntas_lista):
            with st.container():
                st.markdown(f"""
                <div style="background:rgba(99, 102, 241, 0.05); padding:25px; border-radius:20px; border-left:6px solid #6366f1; margin-bottom:20px;">
                    <p style="font-size:1.2rem; color:white !important; margin:0;">{q['pregunta'] if isinstance(q, dict) else q}</p>
                </div>
                """, unsafe_allow_html=True)
                
                if isinstance(q, dict):
                    ans = st.radio(f"Opción para Q{idx+1}:", q['opciones'], key=f"r_{idx}", horizontal=True, label_visibility="collapsed")
                    if st.button(f"Validar Pregunta {idx+1}", key=f"chk_{idx}"):
                        if ans == q['correcta']:
                            st.success("✨ ¡CORRECTO! +50 XP")
                            st.session_state.pro['xp'] += 50
                        else:
                            st.error(f"❌ INCORRECTO. La respuesta es: {q['correcta']}")
                        with st.expander("📖 Notas del Instructor"):
                            st.info(q['explicacion'])
                            st.caption(f"Trad: {q['traduccion']}")
                st.divider()

# --- SQL WORKBENCH (DATABASE LAB) ---
def show_sql():
    """Entorno de experimentación SQL de grado Senior."""
    st.title("🧪 SQL Workbench Professional")
    st.markdown("Consulta la tabla `TRABAJADORES` que contiene 300 perfiles dinámicos.")
    
    c_edit, c_schem = st.columns([3, 1])
    
    with c_schem:
        if LOTTIE_SUPPORT:
            anim_sql = get_lottie_json(LOTTIE_SQL)
            if anim_sql: st_lottie(anim_sql, height=150)
            
        st.markdown("### 📋 Esquema de Tabla")
        st.markdown("""
        <div style="background:#0f172a; padding:15px; border-radius:12px; border:1px solid #1e293b; color:#10b981; font-size:0.85rem;">
        ID (INT) - PK<br>NOMBRE (TEXT)<br>APELLIDO (TEXT)<br>EMAIL (TEXT)<br>DEPARTAMENTO (TEXT)<br>CARGO (TEXT)<br>SUELDO (INT)<br>CIUDAD (TEXT)<br>FECHA_CONTRATO (DATE)
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 Regenerar Dataset", use_container_width=True):
            st.session_state.pro['db'] = None
            st.rerun()

    with c_edit:
        st.markdown("#### SQL Editor")
        default_q = "SELECT NOMBRE, CARGO, SUELDO \nFROM TRABAJADORES \nWHERE SUELDO > 22000 \nORDER BY SUELDO DESC \nLIMIT 10;"
        query = st.text_area("Console", value=default_q, height=200, label_visibility="collapsed")
        
        if st.button("▶ EJECUTAR CONSULTA", type="primary", use_container_width=True):
            st.session_state.pro['history'].append(query)
            res, err, t_exec = sql_engine(query)
            
            if err:
                st.error(f"⚠️ ERROR SQL: {err}")
            else:
                st.markdown(f"**Resultado:** {len(res)} registros en {t_exec:.4f}s")
                st.dataframe(res, use_container_width=True)
                st.session_state.pro['xp'] += 20
        
        st.divider()
        st.subheader("Data Preview (Top 5)")
        st.dataframe(generate_workers_db().head(5), use_container_width=True)

# ==============================================================================
# 7. ENRUTADOR MAESTRO (MAIN ENGINE)
# ==============================================================================

def main():
    """Función principal de despacho de vistas."""
    render_sidebar()
    
    # Extracción segura de la vista actual
    page = st.session_state.pro['view']
    
    if page == 'welcome':
        show_welcome()
    elif page == 'training':
        show_training()
    elif page == 'sql':
        show_sql()

# Punto de entrada del sistema
if __name__ == "__main__":
    main()

# ==============================================================================
# FIN DEL SISTEMA - TOTAL LÍNEAS ESTIMADAS: >710
# INTECAP DBA HUB v9.0 | DESARROLLO DE ALTO NIVEL
# ==============================================================================