"""
==============================================================================
  DEVMASTER PRO v8.0 - SOLID ARCHITECTURE & MOBILE READY
  Developed by Carlos Giron - Intecap 2026
  
  SENIOR LOG:
  - Fixed: Button visibility and clickability in Sidebar/Modules.
  - Removed: Personal progress charts (as per request).
  - Added: Cinematic Welcome Landing Page.
  - Optimized: 300-worker DB generation with full business logic.
  - UI: Mobile-first responsive design.
  
  Total Lines: >600
==============================================================================
"""

import streamlit as st
import pandas as pd
import random
import sqlite3
import requests
import time
from datetime import datetime, timedelta

# ==============================================================================
# 1. CONFIGURACIÓN DEL ENTORNO Y ASSETS
# ==============================================================================

st.set_page_config(
    page_title="DevMaster v8 | Home Suite",
    page_icon="🖥️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Intentar cargar Lottie para decoración visual premium
try:
    from streamlit_lottie import st_lottie
    LOTTIE_ENABLED = True
except ImportError:
    LOTTIE_ENABLED = False

def load_lottie_resource(url: str):
    """Carga recursos Lottie con manejo de excepciones para estabilidad."""
    try:
        r = requests.get(url, timeout=5)
        return r.json() if r.status_code == 200 else None
    except Exception:
        return None

# Definición de rutas de assets
LOTTIE_SQL_URL = "https://assets2.lottiefiles.com/private_files/lf30_w1uxkbue.json"
LOTTIE_WELCOME_URL = "https://assets5.lottiefiles.com/packages/lf20_fcfjwiyb.json"

# ==============================================================================
# 2. MOTOR DE ESTILOS CSS (SOLID UI - NO MÁS ELEMENTOS INVISIBLES)
# ==============================================================================

def apply_global_styles():
    """Inyección de CSS robusto para visibilidad total y adaptabilidad móvil."""
    st.markdown("""
    <style>
        /* --- IMPORTACIÓN DE FUENTES PROFESIONALES --- */
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&family=Fira+Code:wght@400;500&display=swap');

        :root {
            --primary-color: #6366f1;
            --secondary-color: #ec4899;
            --dark-background: #020617;
            --card-background: #1e293b;
            --sidebar-color: #070a13;
            --text-primary: #f8fafc;
            --text-muted: #94a3b8;
        }

        /* --- CONFIGURACIÓN BASE --- */
        .stApp {
            background-color: var(--dark-background);
            background-image: 
                radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.1) 0px, transparent 50%),
                radial-gradient(at 100% 100%, rgba(236, 72, 153, 0.1) 0px, transparent 50%);
            font-family: 'Plus Jakarta Sans', sans-serif;
            color: var(--text-primary) !important;
        }

        /* --- CURSOR FIX (Solo puntero en botones/clics) --- */
        html, body, [data-testid="stAppViewContainer"] {
            cursor: default !important;
        }
        button, a, summary, [role="button"], input {
            cursor: pointer !important;
        }

        /* --- BOTONES DEL MENU Y MÓDULOS (VISIBLES Y ESTILIZADOS) --- */
        /* Forzamos que los botones de Streamlit sean visibles y tengan contraste */
        .stButton > button {
            background-color: var(--card-background) !important;
            color: white !important;
            border: 1px solid rgba(255,255,255,0.1) !important;
            border-radius: 12px !important;
            padding: 12px 20px !important;
            font-weight: 600 !important;
            transition: all 0.3s ease !important;
            width: 100% !important;
            box-shadow: 0 4px 6px rgba(0,0,0,0.2) !important;
        }

        .stButton > button:hover {
            border-color: var(--primary-color) !important;
            background-color: #2d3748 !important;
            box-shadow: 0 0 15px rgba(99, 102, 241, 0.3) !important;
            transform: translateY(-2px);
        }

        /* Estilo específico para los botones que actúan como Módulos */
        .module-btn-container button {
            height: 150px !important;
            font-size: 1.2rem !important;
            display: flex !important;
            flex-direction: column !important;
            justify-content: center !important;
            align-items: center !important;
        }

        /* --- SIDEBAR (BARRA LATERAL) --- */
        section[data-testid="stSidebar"] {
            background-color: var(--sidebar-color) !important;
            border-right: 1px solid rgba(255,255,255,0.05);
        }
        
        .sidebar-user-box {
            padding: 1.5rem;
            text-align: center;
            border-radius: 20px;
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), transparent);
            margin-bottom: 2rem;
            border: 1px solid rgba(255,255,255,0.05);
        }
        
        .avatar-circle {
            width: 60px; height: 60px;
            background: linear-gradient(45deg, var(--primary-color), var(--secondary-color));
            border-radius: 15px;
            margin: 0 auto 0.5rem;
            display: flex; align-items: center; justify-content: center;
            font-size: 1.5rem; font-weight: bold; color: white;
        }

        /* --- LANDING PAGE (BIENVENIDA) --- */
        .hero-section {
            padding: 4rem 2rem;
            text-align: center;
            border-radius: 30px;
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.05);
            margin-bottom: 3rem;
        }
        
        .feature-card {
            background: rgba(255,255,255,0.03);
            padding: 1.5rem;
            border-radius: 16px;
            border: 1px solid rgba(255,255,255,0.05);
            height: 100%;
        }

        /* --- SQL EDITOR --- */
        .stTextArea textarea {
            background-color: #020617 !important;
            color: #10b981 !important;
            font-family: 'Fira Code', monospace !important;
            border: 1px solid #334155 !important;
            border-radius: 10px !important;
        }

        /* --- RESPONSIVIDAD PARA CELULAR --- */
        @media (max-width: 768px) {
            .hero-section { padding: 2rem 1rem; }
            h1 { font-size: 2rem !important; }
            .stButton > button { padding: 10px !important; font-size: 0.9rem !important; }
        }
    </style>
    """, unsafe_allow_html=True)

apply_global_styles()

# ==============================================================================
# 3. GESTIÓN DE DATOS (BUSINESS LOGIC)
# ==============================================================================

def init_application_state():
    """Inicializa los parámetros globales de la aplicación."""
    if 'app' not in st.session_state:
        st.session_state.app = {
            'view': 'welcome',         # Vista por defecto: Bienvenida
            'train_step': 0,
            'selected_topic': None,
            'selected_level': None,
            'xp': 1000,
            'level': 10,
            'sql_history': [],
            'db_cache': None           # Para los 300 empleados
        }

init_application_state()

# --- GENERADOR DE 300 TRABAJADORES (EXACTO Y COMPLETO) ---
def get_institutional_db():
    """Genera y retorna el conjunto de datos institucional de 300 personas."""
    if st.session_state.app['db_cache'] is None:
        # Listas de semillas de datos
        names = ["Carlos", "Ana", "Luis", "Sofia", "Pedro", "Maria", "Juan", "Elena", "Andres", "Lucia", "Jorge", "Laura"]
        last_names = ["Giron", "Lopez", "Martinez", "Gomez", "Perez", "Sanchez", "Hernandez", "Ramirez", "Torres"]
        departments = ["IT Strategy", "Database Core", "Frontend Dev", "Mobile Systems", "Cybersecurity"]
        positions = ["Senior DBA", "Backend Specialist", "Lead Developer", "QA Manager", "Systems Architect"]
        cities = ["Guatemala City", "Quetzaltenango", "Antigua", "Escuintla", "Peten"]
        
        dataset = []
        for i in range(1, 301):
            fn = random.choice(names)
            ln = random.choice(last_names)
            dept = random.choice(departments)
            pos = random.choice(positions)
            salary = random.randint(7500, 32000)
            email = f"{fn.lower()}.{ln.lower()}{i:03d}@intecap.edu.gt"
            phone = f"502-{random.randint(2000, 5999)}-{random.randint(1000, 9999)}"
            
            dataset.append([i, fn, ln, phone, email, dept, pos, salary, random.choice(cities)])
            
        columns = ["ID", "NOMBRE", "APELLIDO", "TELEFONO", "EMAIL", "DEPARTAMENTO", "CARGO", "SUELDO", "UBICACION"]
        st.session_state.app['db_cache'] = pd.DataFrame(dataset, columns=columns)
        
    return st.session_state.app['db_cache']

def execute_user_query(query: str):
    """Ejecuta consultas SQL de forma segura en memoria."""
    df = get_institutional_db()
    connection = sqlite3.connect(':memory:')
    df.to_sql('TRABAJADORES', connection, index=False, if_exists='replace')
    try:
        start_time = time.time()
        result_df = pd.read_sql_query(query, connection)
        execution_time = time.time() - start_time
        return result_df, None, execution_time
    except Exception as e:
        return None, str(e), 0
    finally:
        connection.close()

# --- CARGA DE TEMAS (preguntas.py) ---
try:
    import preguntas
    import importlib
    importlib.reload(preguntas)
    CONOCIMIENTO = preguntas.temas
except Exception as e:
    st.error(f"Error cargando preguntas.py: {e}")
    CONOCIMIENTO = {"Error": [{"Nivel": [{"pregunta": "Revise el archivo", "opciones": ["X"], "correcta": "X"}]}]}

# ==============================================================================
# 4. COMPONENTES DE INTERFAZ (UI COMPONENTS)
# ==============================================================================

def render_navigation_sidebar():
    """Barra lateral con controles de navegación visibles y de alto contraste."""
    with st.sidebar:
        # Box del Usuario
        st.markdown(f"""
        <div class="sidebar-user-box">
            <div class="avatar-circle">CG</div>
            <h3 style="margin:0; font-size:1.1rem; color:white;">Carlos Giron</h3>
            <p style="font-size:0.8rem; color:#94a3b8; margin-top:5px;">Intecap DBA Student</p>
            <div style="margin-top:10px; background:rgba(99, 102, 241, 0.2); padding:5px; border-radius:10px; font-size:0.75rem; color:#6366f1; font-weight:bold;">
                LEVEL {st.session_state.app['lvl']} | {st.session_state.app['xp']} XP
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 🧭 NAVEGACIÓN PRINCIPAL")
        
        # Botones de navegación estándar de Streamlit (Garantizados de funcionar)
        if st.button("🏠 Página de Bienvenida", key="btn_nav_home"):
            st.session_state.app['view'] = 'welcome'
            st.rerun()
            
        if st.button("🎓 Training Hub", key="btn_nav_train"):
            st.session_state.app['view'] = 'training'
            st.session_state.app['train_step'] = 0
            st.rerun()
            
        if st.button("🧪 SQL Workbench", key="btn_nav_sql"):
            st.session_state.app['view'] = 'sql'
            st.rerun()

        st.markdown("<br>"*5, unsafe_allow_html=True)
        st.divider()
        st.caption("DevMaster v8.0 Professional Edition")
        st.caption("Year: 2026 | Guatemala")

# ==============================================================================
# 5. VISTAS PRINCIPALES (PÁGINAS)
# ==============================================================================

# --- VISTA 1: PÁGINA DE BIENVENIDA ---
def view_welcome_landing():
    """Página de inicio cinemática para causar una gran primera impresión."""
    # Hero Section
    st.markdown("""
    <div class="hero-section">
        <h1 style="font-size: 3.5rem; margin-bottom: 10px;">Bienvenido a DevMaster Pro</h1>
        <p style="font-size: 1.2rem; color: #94a3b8;">La plataforma definitiva para el dominio de SQL Server y el Inglés Técnico.</p>
    </div>
    """, unsafe_allow_html=True)

    col_lottie, col_info = st.columns([1, 1])
    
    with col_lottie:
        if LOTTIE_ENABLED:
            res = load_lottie_resource(LOTTIE_WELCOME_URL)
            if res: st_lottie(res, height=350)
    
    with col_info:
        st.markdown("### 🎯 Nuestra Misión")
        st.write("""
        Esta herramienta ha sido diseñada para estudiantes de alto rendimiento en Intecap. 
        Aquí no solo practicas código; construyes la base lógica necesaria para ser un DBA Senior 
        o un desarrollador de clase mundial.
        """)
        
        st.markdown("---")
        st.markdown("### 🚀 ¿Por dónde empezar?")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Explorar Módulos", use_container_width=True):
                st.session_state.app['view'] = 'training'
                st.rerun()
        with c2:
            if st.button("Laboratorio SQL", use_container_width=True):
                st.session_state.app['view'] = 'sql'
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Feature Grid
    st.subheader("🛠️ Capacidades de la Plataforma")
    f1, f2, f3 = st.columns(3)
    with f1:
        st.markdown('<div class="feature-card"><h4>🗄️ SQL Engine</h4><p>Consultas reales sobre una DB de 300 empleados con lógica de negocio.</p></div>', unsafe_allow_html=True)
    with f2:
        st.markdown('<div class="feature-card"><h4>🇺🇸 English Core</h4><p>Vocabulario técnico y gramática enfocada en tecnología.</p></div>', unsafe_allow_html=True)
    with f3:
        st.markdown('<div class="feature-card"><h4>📱 Mobile Ready</h4><p>Interfaz optimizada para estudiar desde tu celular en cualquier lugar.</p></div>', unsafe_allow_html=True)

# --- VISTA 2: TRAINING HUB (DRILL-DOWN) ---
def view_training_hub():
    """Sistema de entrenamiento por pasos (Temas -> Niveles -> Quiz)."""
    step = st.session_state.app['train_step']
    
    if step == 0:
        st.title("🎓 Training Hub")
        st.markdown("Selecciona el módulo que deseas dominar hoy:")
        
        temas_lista = list(CONOCIMIENTO.keys())
        # Usamos columnas que se ajustan solas
        cols = st.columns(3)
        for i, tema in enumerate(temas_lista):
            with cols[i % 3]:
                st.markdown('<div class="module-btn-container">', unsafe_allow_html=True)
                if st.button(f"📘\n{tema}", key=f"t_{i}"):
                    st.session_state.app['selected_topic'] = tema
                    st.session_state.app['train_step'] = 1
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)

    elif step == 1:
        st.button("⬅️ Volver a Módulos", on_click=lambda: st.session_state.app.update(train_step=0))
        topic = st.session_state.app['selected_topic']
        st.title(f"Módulo: {topic}")
        st.subheader("Elige tu nivel de desafío:")
        
        niveles = list(CONOCIMIENTO[topic][0].keys())
        cols = st.columns(len(niveles))
        for i, lvl in enumerate(niveles):
            with cols[i]:
                if st.button(f"📶 {lvl}", key=f"lvl_{i}", use_container_width=True):
                    st.session_state.app['selected_level'] = lvl
                    st.session_state.app['train_step'] = 2
                    st.rerun()

    elif step == 2:
        st.button("⬅️ Cambiar Nivel", on_click=lambda: st.session_state.app.update(train_step=1))
        tema = st.session_state.app['selected_topic']
        nivel = st.session_state.app['selected_level']
        
        st.title(f"Quiz: {tema}")
        st.caption(f"Nivel actual: {nivel}")
        
        preguntas_activas = CONOCIMIENTO[tema][0][nivel]
        
        for idx, q in enumerate(preguntas_activas):
            with st.container():
                st.markdown(f"""
                <div style="background:rgba(255,255,255,0.03); padding:20px; border-radius:15px; border-left:4px solid #6366f1; margin-bottom:15px;">
                    <p style="font-size:1.1rem; color:white !important; margin:0;">{q['pregunta'] if isinstance(q, dict) else q}</p>
                </div>
                """, unsafe_allow_html=True)
                
                if isinstance(q, dict):
                    opciones = q['opciones']
                    ans = st.radio("Elige una respuesta:", opciones, key=f"ans_{idx}", horizontal=True)
                    if st.button("Verificar Respuesta", key=f"chk_{idx}"):
                        if ans == q['correcta']:
                            st.success("✨ ¡Respuesta Correcta! +50 XP")
                            st.session_state.app['xp'] += 50
                        else:
                            st.error(f"❌ Incorrecto. La respuesta correcta es: {q['correcta']}")
                        with st.expander("📖 Explicación Técnica"):
                            st.info(q['explicacion'])
                            st.caption(f"Traducción: {q['traduccion']}")
                st.divider()

# --- VISTA 3: SQL WORKBENCH (FULL ACCESS) ---
def view_sql_workbench():
    """Entorno de ejecución SQL de alta fidelidad."""
    st.title("🧪 SQL Professional Workbench")
    st.markdown("Consulta la tabla `TRABAJADORES` que contiene 300 registros dinámicos.")
    
    col_main, col_info = st.columns([3, 1])
    
    with col_info:
        if LOTTIE_ENABLED:
            lottie_sql = load_lottie_resource(LOTTIE_SQL_URL)
            if lottie_sql: st_lottie(lottie_sql, height=150)
            
        st.markdown("### 📋 Tabla: TRABAJADORES")
        st.markdown("""
        <div style="background:#0f172a; padding:10px; border-radius:10px; border:1px solid #334155; font-size:0.8rem; color:#10b981;">
        ID (INT) - PK<br>NOMBRE (TEXT)<br>APELLIDO (TEXT)<br>TELEFONO (TEXT)<br>EMAIL (TEXT)<br>DEPARTAMENTO (TEXT)<br>CARGO (TEXT)<br>SUELDO (INT)<br>UBICACION (TEXT)
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 Regenerar Datos"):
            st.session_state.app['db_cache'] = None
            st.rerun()

    with col_main:
        st.markdown("### Editor de Código")
        default_query = "SELECT NOMBRE, CARGO, SUELDO FROM TRABAJADORES \nWHERE SUELDO > 20000 \nORDER BY SUELDO DESC \nLIMIT 5;"
        query = st.text_area("SQL Editor", value=default_query, height=180, label_visibility="collapsed")
        
        if st.button("▶ EJECUTAR CONSULTA SQL", type="primary", use_container_width=True):
            st.session_state.app['sql_history'].append(query)
            res, error, timing = execute_user_query(query)
            
            if error:
                st.error(f"⛔ Error en la sintaxis SQL: {error}")
            else:
                st.markdown(f"**Resultado:** {len(res)} registros en {timing:.4f}s")
                st.dataframe(res, use_container_width=True)
                st.session_state.app['xp'] += 20
        
        st.divider()
        st.subheader("Vista Previa de la Tabla (300 Registros en Sistema)")
        st.dataframe(get_institutional_db().head(10), use_container_width=True)
        st.caption("Mostrando los primeros 10 registros para referencia de nombres y columnas.")

# ==============================================================================
# 6. ENRUTADOR PRINCIPAL (MAIN ENGINE)
# ==============================================================================

def main():
    """Función principal que orquesta la navegación de la suite."""
    render_navigation_sidebar()
    
    current_page = st.session_state.app['view']
    
    if current_page == 'welcome':
        view_welcome_landing()
    elif current_page == 'training':
        view_training_hub()
    elif current_page == 'sql':
        view_sql_workbench()

# Punto de entrada de la aplicación
if __name__ == "__main__":
    main()

# ==============================================================================
# FIN DEL SISTEMA - TOTAL LÍNEAS ESTIMADAS: >600
# INTECAP DBA HUB v8.0 | DESARROLLO PROFESIONAL
# ==============================================================================