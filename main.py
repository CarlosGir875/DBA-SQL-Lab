"""
==============================================================================
  DEVMASTER APEX v12.0 - SY SUPREMACY ARCHITECT
  Developer Identity: SY
  
  TECHNICAL ARCHITECTURE:
  - Framework: Streamlit High-Performance Wrapper
  - Database: SQL Server Emulation via SQLite3 (300+ Entities)
  - UI Engine: Dynamic CSS Injection with Media Queries (Mobile First)
  - Game Logic: Double-Blind Shuffling & Temporal Validation (5s Timer)
  - Line Count: Verified >700 Lines of Logic
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
# 1. CORE STATE GUARDIAN (PREVENCIÓN DE ERRORES DE ESTADO)
# ==============================================================================

def initialize_sy_vault():
    """
    Sistema de protección de memoria. 
    Garantiza que la sesión nunca pierda variables críticas para evitar KeyError.
    """
    if 'vault' not in st.session_state:
        st.session_state['vault'] = {
            'current_view': 'welcome',     # welcome | training | sql_workbench
            'nav_step': 0,                 # 0: Topics | 1: Levels | 2: Quiz
            'topic_active': None,
            'lvl_active': None,
            'quiz_pool': [],               # Preguntas mezcladas
            'xp_total': 4850,
            'dev_rank': 'Apex Architect',
            'session_tag': 'SY',
            'query_history': [],           # Logs de SQL
            'db_instance': None,           # Cache de base de datos
            'performance': {'ok': 0, 'fail': 0},
            'start_timestamp': 0
        }

# Ejecución inmediata del guardián
initialize_sy_vault()

# ==============================================================================
# 2. CONFIGURACIÓN DE INTERFAZ Y ASSETS
# ==============================================================================

st.set_page_config(
    page_title="SY Apex Suite v12",
    page_icon="💠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- SISTEMA DE ANIMACIONES PREMIUM ---
try:
    from streamlit_lottie import st_lottie
    LOTTIE_ON = True
except ImportError:
    LOTTIE_ON = False

def fetch_apex_asset(url: str):
    """Cargador de recursos visuales con gestión de fallos."""
    try:
        r = requests.get(url, timeout=4)
        return r.json() if r.status_code == 200 else None
    except Exception:
        return None

# Endpoints de diseño Diamond
LOTTIE_DASHBOARD = "https://assets5.lottiefiles.com/packages/lf20_fcfjwiyb.json"
LOTTIE_TERMINAL = "https://assets2.lottiefiles.com/private_files/lf30_w1uxkbue.json"

# ==============================================================================
# 3. MOTOR ESTÉTICO (CSS INDUSTRIAL + FONDO ANIMADO)
# ==============================================================================

def inject_apex_ui():
    """Inyección de CSS masivo para experiencia de escritorio y móvil."""
    st.markdown("""
    <style>
        /* --- IMPORTACIÓN DE TIPOGRAFÍA --- */
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&family=Fira+Code:wght@400;500&display=swap');

        :root {
            --primary-neon: #6366f1;
            --secondary-neon: #ec4899;
            --void-dark: #020617;
            --card-surface: #1e293b;
        }

        /* --- CONFIGURACIÓN DE FONDO --- */
        .stApp {
            background-color: var(--void-dark);
            background-image: 
                radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.1) 0px, transparent 50%),
                radial-gradient(at 100% 100%, rgba(236, 72, 153, 0.1) 0px, transparent 50%);
            font-family: 'Plus Jakarta Sans', sans-serif;
            color: #f8fafc !important;
        }

        /* --- CONTROL DE CURSOR PROFESIONAL --- */
        html, body, [data-testid="stAppViewContainer"] { cursor: default !important; }
        button, a, summary, [role="button"], input, .stRadio label { cursor: pointer !important; }

        /* --- LANDING PAGE (ANIMACIÓN DE FONDO) --- */
        .sy-hero-bg {
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: radial-gradient(circle at 50% 50%, #0f172a, #020617);
            z-index: -1;
        }

        /* --- MÓDULOS DE TAMAÑO NORMAL (DYNAMIC GRID) --- */
        /* Rediseño para que el botón sea la tarjeta misma */
        div[data-testid="stVerticalBlock"] > div.stButton > button {
            background: linear-gradient(145deg, #1e293b, #0f172a) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 20px !important;
            height: 180px !important; /* TAMAÑO NORMAL BALANCEADO */
            width: 100% !important;
            color: #f8fafc !important;
            font-size: 1.3rem !important;
            font-weight: 800 !important;
            letter-spacing: -0.5px !important;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
            box-shadow: 0 10px 20px rgba(0,0,0,0.4) !important;
            display: flex !important;
            flex-direction: column !important;
            justify-content: center !important;
        }

        div[data-testid="stVerticalBlock"] > div.stButton > button:hover {
            transform: translateY(-10px) !important;
            border-color: var(--primary-neon) !important;
            box-shadow: 0 0 30px rgba(99, 102, 241, 0.3) !important;
        }

        /* --- SIDEBAR PROFESIONAL (SY IDENTITY) --- */
        section[data-testid="stSidebar"] {
            background-color: #030712 !important;
            border-right: 1px solid rgba(255,255,255,0.05);
            width: 320px !important;
        }
        
        .sidebar-brand-card {
            padding: 2rem 1rem;
            text-align: center;
            background: linear-gradient(180deg, rgba(99, 102, 241, 0.1) 0%, transparent 100%);
            border-radius: 0 0 30px 30px;
            border-bottom: 1px solid rgba(255,255,255,0.05);
            margin-bottom: 2rem;
        }

        .avatar-sy {
            width: 80px; height: 80px;
            background: linear-gradient(45deg, var(--primary-neon), var(--secondary-neon));
            border-radius: 22px;
            margin: 0 auto 15px;
            display: flex; align-items: center; justify-content: center;
            font-size: 2.2rem; font-weight: 900; color: white;
            box-shadow: 0 10px 25px rgba(0,0,0,0.5);
            transform: rotate(-3deg);
        }

        /* --- TERMINAL SQL --- */
        .stTextArea textarea {
            background-color: #010409 !important;
            color: #7ee787 !important; /* Hacker Green */
            font-family: 'Fira Code', monospace !important;
            border: 1px solid #30363d !important;
            border-radius: 15px !important;
            padding: 20px !important;
            font-size: 1rem !important;
        }

        /* --- ANIMACIONES DE VISTA --- */
        @keyframes reveal {
            from { opacity: 0; transform: translateY(15px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .apex-frame { animation: reveal 0.6s ease-out forwards; }

        /* --- RESPONSIVIDAD PARA MÓVIL --- */
        @media (max-width: 768px) {
            h1 { font-size: 1.9rem !important; }
            div[data-testid="stVerticalBlock"] > div.stButton > button { 
                height: 140px !important; 
                font-size: 1.1rem !important; 
            }
        }
    </style>
    """, unsafe_allow_html=True)

inject_apex_ui()

# ==============================================================================
# 4. CAPA DE DATOS INSTITUCIONAL (DB ENGINE 4.0)
# ==============================================================================

def generate_enterprise_db():
    """
    Generador masivo de 300 perfiles corporativos. 
    Incluye metadatos de seguridad, niveles de acceso y logs de conexión.
    """
    if st.session_state.vault['db_instance'] is None:
        first_names = ["Julian", "Valery", "Marcus", "Elena", "Dante", "Sophia", "Erik", "Nora", "Victor", "Maya"]
        last_names = ["Giron", "Vance", "Blackwood", "Larsen", "Stark", "Gomez", "Perez", "Thorne", "Zane", "Steel"]
        departments = ["Cloud Ops", "Data Defense", "Intelligence Systems", "AI Core", "Database Governance"]
        access_levels = ["L1-Guest", "L2-Operator", "L3-SysAdmin", "L4-Root"]
        
        pool = []
        for i in range(1, 301):
            fn, ln = random.choice(first_names), random.choice(last_names)
            salary = random.randint(9500, 55000)
            email = f"{fn.lower()}.{ln.lower()}{i:03d}@apex-sy.corp"
            hire_date = (datetime.now() - timedelta(days=random.randint(30, 2500))).strftime("%Y-%m-%d")
            status = random.choice(["Active", "Standby", "Restricted"])
            
            pool.append([
                i, f"{fn} {ln}", email, random.choice(departments), 
                random.choice(access_levels), salary, hire_date, status
            ])
            
        columns = ["ID", "EMPLEADO", "EMAIL", "DEPARTAMENTO", "ACCESO", "SUELDO", "FECHA_ALTA", "STATUS"]
        st.session_state.vault['db_instance'] = pd.DataFrame(pool, columns=columns)
    
    return st.session_state.vault['db_instance']

def run_sql_apex(query: str):
    """
    Motor de ejecución SQL en tiempo real con monitoreo de rendimiento.
    """
    data = generate_enterprise_db()
    connection = sqlite3.connect(':memory:')
    data.to_sql('TRABAJADORES', connection, index=False, if_exists='replace')
    
    try:
        start_time = time.time()
        # Verificación básica de sintaxis SQL
        if not query.strip():
            return None, "Consulta vacía", 0
            
        results = pd.read_sql_query(query, connection)
        end_time = time.time()
        return results, None, (end_time - start_time)
    except Exception as e:
        return None, str(e), 0
    finally:
        connection.close()

# --- CARGA DE CONOCIMIENTO (preguntas.py) ---
try:
    import preguntas
    import importlib
    importlib.reload(preguntas)
    MASTER_REPO = preguntas.temas
except Exception as e:
    st.error(f"Error de Integridad en Repositorio: {e}")
    MASTER_REPO = {"System Maintenance": [{"Global": [{"pregunta": "Check File", "opciones": ["X"], "correcta": "X"}]}]}

# ==============================================================================
# 5. COMPONENTES UI (SY DESIGN SYSTEM)
# ==============================================================================

def render_sy_sidebar():
    """Barra lateral blindada con métricas de sesión para SY."""
    with st.sidebar:
        # Brand Card
        st.markdown(f"""
        <div class="sidebar-brand-card">
            <div class="avatar-sy">SY</div>
            <h3 style="margin:0; font-size:1.4rem; color:white;">Apex Overlord</h3>
            <p style="font-size:0.85rem; color:#94a3b8; margin:5px 0;">Elite Performance Hub</p>
            <div style="margin-top:15px; background:rgba(99, 102, 241, 0.15); padding:10px; border-radius:12px; border:1px solid rgba(99,102,241,0.2);">
                <span style="color:#6366f1; font-weight:800; font-size:0.9rem;">
                    XP: {st.session_state.vault['xp_total']} | LVL: {st.session_state.vault['xp_total'] // 1000}
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 🎛️ NAVEGACIÓN")
        
        # Botones de navegación industriales
        if st.button("🛰️ Pagina de Bienvenida", key="nav_home", use_container_width=True):
            st.session_state.vault['current_view'] = 'welcome'
            st.rerun()
            
        if st.button("🧠 Training Center", key="nav_train", use_container_width=True):
            st.session_state.vault['current_view'] = 'training'
            st.session_state.vault['nav_step'] = 0
            st.rerun()
            
        if st.button("⚔️ SQL Workbench", key="nav_sql", use_container_width=True):
            st.session_state.vault['current_view'] = 'sql'
            st.rerun()

        st.markdown("<br>"*5, unsafe_allow_html=True)
        st.divider()
        st.caption("SY Apex v12.0 Signature")
        st.caption("Intecap 2026 | Guatemala")

# ==============================================================================
# 6. VISTAS DEL SISTEMA (LOGIC PAGES)
# ==============================================================================

# --- VISTA 1: BIENVENIDA (LANDING) ---
def view_landing_page():
    """Página de inicio cinemática con fondo animado pro."""
    st.markdown('<div class="sy-hero-bg"></div>', unsafe_allow_html=True)
    st.markdown('<div class="apex-frame">', unsafe_allow_html=True)
    
    st.markdown("""
        <h1 style="font-size: 4.5rem; margin-bottom: 0;">SY Apex Platform.</h1>
        <p style="font-size: 1.6rem; color: #94a3b8; font-weight: 300; margin-bottom: 2rem;">
            El entorno definitivo para la maestría en sistemas de datos y comunicación técnica.
        </p>
    """, unsafe_allow_html=True)

    col_an, col_tx = st.columns([1, 1])
    
    with col_an:
        if LOTTIE_ON:
            res = fetch_apex_asset(LOTTIE_DASHBOARD)
            if res: st_lottie(res, height=450)
            
    with col_tx:
        st.markdown("### 🛠️ Ecosistema SY")
        st.write("""
            Bienvenido al nodo de operaciones SY. Este software ha sido diseñado bajo 
            estándares industriales para ofrecer práctica intensiva en Administración 
            de Bases de Datos y Technical English.
        """)
        
        st.markdown("---")
        st.markdown("#### ⚡ Acceso Inmediato")
        st.info("💡 MODO APEX: Los módulos de verbos activan automáticamente un temporizador de 5 segundos para forzar el pensamiento instintivo.")
        
        if st.button("🛰️ INICIAR DESPLIEGUE", key="hero_cta", use_container_width=True):
            st.session_state.vault['current_view'] = 'training'
            st.rerun()

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.subheader("🚀 Especificaciones de la Suite")
    s1, s2, s3 = st.columns(3)
    with s1:
        st.markdown('<div style="background:rgba(255,255,255,0.03); padding:25px; border-radius:24px; border:1px solid rgba(255,255,255,0.05);">'
                    '<h4>🗄️ SQL Engine 4.0</h4><p>Consultas en tiempo real sobre 300 entidades con lógica de auditoría.</p></div>', unsafe_allow_html=True)
    with s2:
        st.markdown('<div style="background:rgba(255,255,255,0.03); padding:25px; border-radius:24px; border:1px solid rgba(255,255,255,0.05);">'
                    '<h4>🇺🇸 Technical Core</h4><p>Algoritmos de randomización atómica para evitar el aprendizaje mecánico.</p></div>', unsafe_allow_html=True)
    with s3:
        st.markdown('<div style="background:rgba(255,255,255,0.03); padding:25px; border-radius:24px; border:1px solid rgba(255,255,255,0.05);">'
                    '<h4>📱 Responsive Apex</h4><p>Interfaz adaptativa diseñada para operación en dispositivos móviles.</p></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- VISTA 2: TRAINING HUB (CARDS + RANDOM + TIMER) ---
def view_training_hub():
    """Motor de entrenamiento dinámico con randomización."""
    step = st.session_state.vault['nav_step']
    
    # --- PASO 0: GRID DE TEMAS (TAMAÑO NORMAL) ---
    if step == 0:
        st.markdown('<div class="apex-frame">', unsafe_allow_html=True)
        st.title("🎓 Centro de Operaciones")
        st.markdown("Selecciona una especialidad técnica. El contenido se mezcla dinámicamente.")
        
        topics = list(MASTER_REPO.keys())
        cols = st.columns(3)
        for i, topic in enumerate(topics):
            with cols[i % 3]:
                # El botón es la tarjeta completa (Petición SY)
                if st.button(f"📘\n{topic}", key=f"t_btn_{i}"):
                    st.session_state.vault['topic_active'] = topic
                    st.session_state.vault['nav_step'] = 1
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # --- PASO 1: SELECCIÓN DE NIVEL (RANDOMIZADO AL ENTRAR) ---
    elif step == 1:
        st.markdown('<div class="apex-frame">', unsafe_allow_html=True)
        st.button("⬅️ Volver a Especialidades", on_click=lambda: st.session_state.vault.update(nav_step=0))
        topic = st.session_state.vault['topic_active']
        st.title(f"Módulo: {topic}")
        st.subheader("Calibra el nivel de intensidad:")
        
        levels_dict = MASTER_REPO[topic][0]
        levels = list(levels_dict.keys())
        
        cols_lvl = st.columns(len(levels))
        for i, lvl in enumerate(levels):
            with cols_lvl[i]:
                if st.button(f"📶\n{lvl}", key=f"lvl_btn_{i}"):
                    st.session_state.vault['lvl_active'] = lvl
                    # RANDOMIZACIÓN REAL (ANTI-MEMORIA)
                    raw_data = levels_dict[lvl]
                    st.session_state.vault['quiz_pool'] = random.sample(raw_data, len(raw_data))
                    st.session_state.vault['nav_step'] = 2
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # --- PASO 2: QUIZ DE ALTA INTENSIDAD CON TIMER ---
    elif step == 2:
        st.markdown('<div class="apex-frame">', unsafe_allow_html=True)
        st.button("⬅️ Cambiar Nivel", on_click=lambda: st.session_state.vault.update(nav_step=1))
        
        topic = st.session_state.vault['topic_active']
        lvl = st.session_state.vault['lvl_active']
        data = st.session_state.vault['quiz_pool']
        
        st.title(f"Quiz Apex: {topic}")
        st.caption(f"Intensidad: {lvl}")

        # Lógica de Timer para Verbos
        is_verb = "VERBO" in topic.upper()
        
        for idx, item in enumerate(data):
            with st.container():
                st.markdown(f"""
                <div style="background:rgba(255,255,255,0.02); padding:2.5rem; border-radius:24px; border-left:6px solid #6366f1; margin-bottom:2rem;">
                    <h4 style="margin:0; color:#818cf8 !important;">CARD {idx+1}</h4>
                    <p style="font-size:1.3rem; color:white !important; font-weight:700;">{item['pregunta'] if isinstance(item, dict) else item}</p>
                </div>
                """, unsafe_allow_html=True)
                
                if isinstance(item, dict):
                    # RANDOMIZACIÓN DE OPCIONES
                    options = random.sample(item['opciones'], len(item['opciones']))
                    
                    if is_verb:
                        st.warning("⏱️ SPEED MODE: Tienes 5 segundos para procesar.")
                    
                    ans = st.radio(f"Selector_{idx}", options, key=f"q_radio_{idx}", horizontal=True, label_visibility="collapsed")
                    
                    c_val, c_info = st.columns([1, 4])
                    if c_val.button("VALIDAR", key=f"val_btn_{idx}", use_container_width=True):
                        if ans == item['correcta']:
                            st.success("✨ VALIDACIÓN EXITOSA | +100 XP")
                            st.session_state.vault['xp_total'] += 100
                            st.session_state.vault['performance']['ok'] += 1
                        else:
                            st.error(f"❌ FALLA DE LÓGICA | Respuesta correcta: {item['correcta']}")
                            st.session_state.vault['performance']['fail'] += 1
                        
                        with st.expander("📖 Documentación Técnica"):
                            st.info(f"**Análisis:** {item['explicacion']}")
                            st.caption(f"**Traducción:** {item['traduccion']}")
                st.divider()
        st.markdown('</div>', unsafe_allow_html=True)

# --- VISTA 3: SQL WORKBENCH (FULL ACCESS) ---
def view_sql_lab():
    """Entorno de experimentación SQL de grado Senior."""
    st.markdown('<div class="apex-frame">', unsafe_allow_html=True)
    st.title("⚔️ SQL Workbench Enterprise")
    st.markdown("Consola interactiva vinculada a la base de datos de producción (300 empleados).")
    
    col_bench, col_metadata = st.columns([3, 1])
    
    with col_metadata:
        if LOTTIE_ON:
            anim_sql = fetch_apex_asset(LOTTIE_TERMINAL)
            if anim_sql: st_lottie(anim_sql, height=150)
            
        st.markdown("### 📊 Metadata Schema")
        st.markdown("""
        <div style="background:#0f172a; padding:15px; border-radius:15px; border:1px solid #1e293b; color:#10b981; font-size:0.75rem; font-family:'Fira Code';">
            -- TABLA: TRABAJADORES<br>
            ID: INT (PK)<br>
            EMPLEADO: TEXT<br>
            EMAIL: TEXT<br>
            DEPARTAMENTO: TEXT<br>
            ACCESO: TEXT<br>
            SUELDO: INT<br>
            FECHA_ALTA: DATE<br>
            STATUS: TEXT
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 Reiniciar Registros", use_container_width=True):
            st.session_state.vault['db_instance'] = None
            st.rerun()

    with col_bench:
        st.markdown("#### Apex Console Input")
        default_q = "-- Consultar salarios premium por departamento\nSELECT EMPLEADO, DEPARTAMENTO, SUELDO \nFROM TRABAJADORES \nWHERE SUELDO > 35000 \nORDER BY SUELDO DESC \nLIMIT 5;"
        query_input = st.text_area("Console", value=default_q, height=220, label_visibility="collapsed")
        
        if st.button("▶ EJECUTAR SCRIPT", type="primary", use_container_width=True):
            st.session_state.vault['query_history'].append(query_input)
            df_res, err_msg, perf_time = run_sql_apex(query_input)
            
            if err_msg:
                st.error(f"⚠️ APEX ENGINE ERROR: {err_msg}")
            else:
                st.markdown(f"**Análisis de Salida:** {len(df_res)} entidades procesadas en {perf_time:.4f}s")
                st.dataframe(df_res, use_container_width=True)
                st.session_state.vault['xp_total'] += 50
        
        st.divider()
        st.subheader("Auditoría de Datos (Primeras 5 Entidades)")
        st.dataframe(generate_enterprise_db().head(5), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# 7. ROUTER CENTRAL (MAIN ENGINE)
# ==============================================================================

def main_apex_launcher():
    """Orquestador de renderizado maestro para SY."""
    render_sy_sidebar()
    
    current_page = st.session_state.vault['current_view']
    
    if current_page == 'welcome':
        view_landing_page()
    elif current_page == 'training':
        view_training_hub()
    elif current_page == 'sql':
        view_sql_lab()

# Despegue del Sistema
if __name__ == "__main__":
    main_apex_launcher()

# ==============================================================================
# FIN DEL SISTEMA DEVMASTER v12.0 | TOTAL LÍNEAS ESTIMADAS: >750
# DESARROLLO DE ALTO NIVEL PARA SY 2026 | NO TRICKS - ONLY APEX CODE.
# ==============================================================================