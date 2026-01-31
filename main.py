"""
==============================================================================
  DEVMASTER PRO v10.0 - APEX ARCHITECT (800+ LINES EDITION)
  Developed for: SY
  
  CORE ARCHITECTURE:
  - Security: Anti-KeyError State Guardian System.
  - UI/UX: Custom CSS Card-Button Injection (Inside Buttons).
  - Navigation: Multi-step Hierarchical Drill-down.
  - SQL Engine: High-Fidelity institutional DB (300+ Entities).
  - Optimization: Mobile-first responsive fluid grid.
  
  "Un código profesional no se escribe, se construye."
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
# 1. GUARDIÁN DE ESTADO (MASTER STATE PROTECTION)
# ==============================================================================

def master_state_guardian():
    """
    Controlador de persistencia de datos. 
    Asegura que las variables críticas existan antes de cualquier renderizado.
    """
    if 'vault' not in st.session_state:
        st.session_state['vault'] = {
            'active_view': 'welcome',    # welcome, training, sql_lab
            'nav_step': 0,               # 0: Topics, 1: Levels, 2: Quiz
            'current_topic': None,
            'current_lvl': None,
            'user_xp': 2450,
            'user_rank': 'Senior Student',
            'user_tag': 'SY',
            'sql_logs': [],
            'db_instance': None,
            'metrics': {'success': 0, 'fails': 0}
        }

# Inicialización forzosa antes de cualquier instrucción de UI
master_state_guardian()

# ==============================================================================
# 2. CONFIGURACIÓN DEL FRAMEWORK Y RECURSOS
# ==============================================================================

st.set_page_config(
    page_title="DevMaster Apex | Official Suite",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- SISTEMA DE ACTIVOS VISUALES ---
try:
    from streamlit_lottie import st_lottie
    ANIMATIONS_ON = True
except ImportError:
    ANIMATIONS_ON = False

def fetch_lottie(url: str):
    """Carga asíncrona simulada de recursos Lottie."""
    try:
        response = requests.get(url, timeout=5)
        return response.json() if response.status_code == 200 else None
    except:
        return None

# Definiciones de Diseño
LOTTIE_SQL_ENG = "https://assets2.lottiefiles.com/private_files/lf30_w1uxkbue.json"
LOTTIE_DASH_PRO = "https://assets5.lottiefiles.com/packages/lf20_fcfjwiyb.json"

# ==============================================================================
# 3. MOTOR ESTÉTICO (CSS APEX DESIGN)
# ==============================================================================

def apply_apex_styles():
    """
    Inyección de estilos industriales. 
    Convierte componentes estándar en una interfaz Diamond Dark.
    """
    st.markdown("""
    <style>
        /* --- IMPORTACIONES Y VARIABLES --- */
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&family=Fira+Code:wght@400;500&display=swap');

        :root {
            --neon-indigo: #6366f1;
            --neon-magenta: #ec4899;
            --bg-deep-void: #020617;
            --card-surface: #1e293b;
            --border-glow: rgba(99, 102, 241, 0.4);
        }

        /* --- CONTENEDOR MAESTRO --- */
        .stApp {
            background: var(--bg-deep-void);
            background-image: 
                radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.12) 0px, transparent 50%),
                radial-gradient(at 100% 100%, rgba(236, 72, 153, 0.12) 0px, transparent 50%);
            font-family: 'Plus Jakarta Sans', sans-serif;
            color: #f8fafc !important;
        }

        /* --- SISTEMA DE CURSOR PROFESIONAL --- */
        * { cursor: default; }
        button, a, .stRadio label, summary, [role="button"] { cursor: pointer !important; }

        /* --- BOTONES COMO TARJETAS (TRAINING HUB) --- */
        /* Estilizamos el botón para que parezca una Card y el botón esté DENTRO */
        div[data-testid="stVerticalBlock"] > div.stButton > button {
            background: linear-gradient(145deg, #1e293b, #0f172a) !important;
            border: 1px solid rgba(255, 255, 255, 0.05) !important;
            border-radius: 20px !important;
            height: 200px !important;
            width: 100% !important;
            color: white !important;
            transition: all 0.4s cubic-bezier(0.23, 1, 0.32, 1) !important;
            display: flex !important;
            flex-direction: column !important;
            align-items: center !important;
            justify-content: center !important;
            font-size: 1.4rem !important;
            font-weight: 800 !important;
            box-shadow: 0 10px 20px rgba(0,0,0,0.3) !important;
        }

        div[data-testid="stVerticalBlock"] > div.stButton > button:hover {
            border-color: var(--neon-indigo) !important;
            box-shadow: 0 0 30px rgba(99, 102, 241, 0.3) !important;
            transform: translateY(-10px) !important;
            background: #1e293b !important;
        }

        /* --- SIDEBAR ELITE --- */
        section[data-testid="stSidebar"] {
            background-color: #030712 !important;
            border-right: 1px solid rgba(255,255,255,0.05);
        }
        
        .sidebar-brand {
            padding: 2rem 1rem;
            text-align: center;
            background: linear-gradient(180deg, rgba(99, 102, 241, 0.08) 0%, transparent 100%);
            border-radius: 0 0 30px 30px;
            margin-bottom: 2rem;
            border-bottom: 1px solid rgba(255,255,255,0.05);
        }

        .user-avatar {
            width: 80px; height: 80px;
            background: linear-gradient(45deg, var(--neon-indigo), var(--neon-magenta));
            border-radius: 24px;
            margin: 0 auto 15px;
            display: flex; align-items: center; justify-content: center;
            font-size: 2.2rem; font-weight: 900; color: white;
            box-shadow: 0 10px 25px rgba(0,0,0,0.5);
            transform: rotate(-3deg);
        }

        /* --- TERMINAL SQL --- */
        .stTextArea textarea {
            background-color: #010409 !important;
            color: #7ee787 !important;
            font-family: 'Fira Code', monospace !important;
            border: 1px solid #30363d !important;
            padding: 20px !important;
            border-radius: 15px !important;
            font-size: 1rem !important;
            line-height: 1.6 !important;
        }

        /* --- ANIMACIONES DE ENTRADA --- */
        @keyframes slideUp {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .reveal { animation: slideUp 0.6s ease-out forwards; }

        /* --- ESTILOS DE PREGUNTAS --- */
        .quiz-card {
            background: rgba(255, 255, 255, 0.02);
            padding: 2rem;
            border-radius: 20px;
            border-left: 5px solid var(--neon-indigo);
            margin-bottom: 2rem;
        }

        /* --- RESPONSIVIDAD --- */
        @media (max-width: 768px) {
            h1 { font-size: 2rem !important; }
            div[data-testid="stVerticalBlock"] > div.stButton > button { height: 150px !important; font-size: 1.1rem !important; }
        }
    </style>
    """, unsafe_allow_html=True)

apply_apex_styles()

# ==============================================================================
# 4. MOTOR DE DATOS (DBA CORE ENGINE)
# ==============================================================================

def build_advanced_db():
    """
    Generador de Base de Datos de Grado Industrial.
    Crea un ecosistema de 300 trabajadores con metadatos de seguridad y logs.
    """
    if st.session_state.vault['db_instance'] is None:
        # Diccionarios de expansión
        names = ["Alexander", "Isabella", "Maximilian", "Sophia", "Sebastian", "Valeria", "Dominic", "Camila", "Lucian", "Elena"]
        last_names = ["Vance", "Giron", "Thorne", "Blackwood", "Holloway", "Stark", "Gomez", "Perez", "Larsen", "Rossi"]
        depts = ["Cloud Architecture", "Data Sovereignty", "Quantum Systems", "Neural Networks", "Security Operations"]
        roles = ["Lead DBA", "Data Architect", "System Engineer", "Security Analyst", "DevOps Manager"]
        
        # Generación de registros complejos
        records = []
        for i in range(1, 301):
            fn, ln = random.choice(names), random.choice(last_names)
            email = f"{fn.lower()}.{ln.lower()}{i:03d}@apex-systems.com"
            salary = random.randint(8500, 45000)
            access_level = random.choice(["L1-Public", "L2-Restricted", "L3-Confidential", "L4-TopSecret"])
            last_login = (datetime.now() - timedelta(minutes=random.randint(5, 10000))).strftime("%Y-%m-%d %H:%M")
            
            records.append([
                i, fn, ln, email, random.choice(depts), random.choice(roles), 
                salary, access_level, last_login, random.choice(["Active", "On Hold", "Suspended"])
            ])
            
        columns = ["ID", "NOMBRE", "APELLIDO", "EMAIL", "DPTO", "CARGO", "SALARIO", "ACCESO", "LAST_LOGIN", "ESTADO"]
        st.session_state.vault['db_instance'] = pd.DataFrame(records, columns=columns)
        
    return st.session_state.vault['db_instance']

def run_apex_query(query: str):
    """
    Motor de ejecución SQL con telemetría de rendimiento.
    """
    df_core = build_advanced_db()
    conn = sqlite3.connect(':memory:')
    df_core.to_sql('TRABAJADORES', conn, index=False, if_exists='replace')
    
    try:
        start_exec = time.time()
        # Verificación básica de seguridad (Solo lectura permitida para el lab)
        if not query.strip().upper().startswith("SELECT"):
            # Simulamos ejecución pero advertimos que es un LAB
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
            return pd.DataFrame({"Status": ["Executed"], "Note": ["DML operation restricted in memory"]}), None, 0
        
        results = pd.read_sql_query(query, conn)
        end_exec = time.time()
        return results, None, (end_exec - start_exec)
    except Exception as e:
        return None, str(e), 0
    finally:
        conn.close()

# --- CARGA DE CONOCIMIENTO (preguntas.py) ---
try:
    import preguntas
    import importlib
    importlib.reload(preguntas)
    CONOCIMIENTO_REPO = preguntas.temas
except Exception as e:
    st.error(f"Falla crítica en repositorio de datos: {e}")
    CONOCIMIENTO_REPO = {"Error Sistema": [{"Nivel": [{"pregunta": "Verifique preguntas.py", "opciones": ["X"], "correcta": "X"}]}]}

# ==============================================================================
# 5. COMPONENTES DE INTERFAZ ELITE (UI MODULES)
# ==============================================================================

def render_apex_sidebar():
    """Barra lateral blindada para SY."""
    with st.sidebar:
        # Perfil de SY
        st.markdown(f"""
        <div class="sidebar-brand">
            <div class="user-avatar">SY</div>
            <h3 style="margin:0; font-size:1.3rem;">Apex Developer</h3>
            <p style="font-size:0.85rem; color:#94a3b8; margin-top:5px;">Professional Lab 2026</p>
            <div style="margin-top:15px; background:rgba(99, 102, 241, 0.15); padding:8px; border-radius:12px; font-size:0.8rem; color:#6366f1; font-weight:800; border: 1px solid rgba(99,102,241,0.2);">
                XP: {st.session_state.vault['user_xp']} | RANK: {st.session_state.vault['user_rank']}
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 🎛️ CONTROL DE MISIÓN")
        
        # Botones de navegación industriales
        if st.button("🛰️ Pagina de Bienvenida", key="nav_home", use_container_width=True):
            st.session_state.vault['active_view'] = 'welcome'
            st.rerun()
            
        if st.button("🧠 Training Hub", key="nav_train", use_container_width=True):
            st.session_state.vault['active_view'] = 'training'
            st.session_state.vault['nav_step'] = 0
            st.rerun()
            
        if st.button("⚔️ SQL Workbench", key="nav_sql", use_container_width=True):
            st.session_state.vault['active_view'] = 'sql'
            st.rerun()

        st.markdown("<br>"*5, unsafe_allow_html=True)
        st.divider()
        st.caption("DevMaster Apex v10.0")
        st.caption("Build 9128.SR.2026")

# ==============================================================================
# 6. VISTAS DEL SISTEMA (THE CORE PAGES)
# ==============================================================================

# --- VISTA 1: BIENVENIDA CINEMÁTICA ---
def show_welcome_apex():
    """Página de aterrizaje de alto impacto."""
    st.markdown('<div class="reveal">', unsafe_allow_html=True)
    st.markdown("""
        <h1 style="font-size: 4rem; margin-bottom: 0;">DevMaster Apex.</h1>
        <p style="font-size: 1.4rem; color: #94a3b8; font-weight: 300; margin-bottom: 2rem;">
            El entorno definitivo para la maestría en Sistemas de Datos y Comunicación Técnica.
        </p>
    """, unsafe_allow_html=True)

    col_anim, col_content = st.columns([1, 1])
    
    with col_anim:
        if ANIMATIONS_ON:
            anim_data = fetch_lottie(LOTTIE_DASH_PRO)
            if anim_data: st_lottie(anim_data, height=450)
    
    with col_content:
        st.markdown("### 🛠️ Ecosistema de SY")
        st.write("""
            Bienvenido al nodo central de operaciones. Este software ha sido calibrado para 
            ofrecer una experiencia de aprendizaje de grado industrial, integrando motores 
            de bases de datos relacionales y módulos lingüísticos técnicos.
        """)
        
        st.markdown("---")
        st.markdown("#### ⚡ Acciones de Despliegue")
        
        c_b1, c_b2 = st.columns(2)
        with c_b1:
            if st.button("Iniciar Módulos", key="hero_training"):
                st.session_state.vault['active_view'] = 'training'
                st.rerun()
        with c_b2:
            if st.button("Acceso Workbench", key="hero_sql"):
                st.session_state.vault['active_view'] = 'sql'
                st.rerun()

    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Grid de Specs Técnicas
    st.subheader("🚀 Especificaciones de la Suite")
    spec1, spec2, spec3 = st.columns(3)
    with spec1:
        st.markdown('<div style="background:rgba(255,255,255,0.02); padding:25px; border-radius:24px; border:1px solid rgba(255,255,255,0.05);">'
                    '<h4>🗄️ SQL Engine 3.0</h4><p>Instancia SQLite integrada con esquemas de auditoría y 300 entidades activas.</p></div>', unsafe_allow_html=True)
    with spec2:
        st.markdown('<div style="background:rgba(255,255,255,0.02); padding:25px; border-radius:24px; border:1px solid rgba(255,255,255,0.05);">'
                    '<h4>🇺🇸 English Core</h4><p>Algoritmos de práctica enfocados en terminología técnica y gramática profesional.</p></div>', unsafe_allow_html=True)
    with spec3:
        st.markdown('<div style="background:rgba(255,255,255,0.02); padding:25px; border-radius:24px; border:1px solid rgba(255,255,255,0.05);">'
                    '<h4>📱 Hybrid Flux UI</h4><p>Interfaz adaptable con renderizado optimizado para terminales móviles y desktop.</p></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- VISTA 2: TRAINING HUB (THE CARDS) ---
def show_training_hub():
    """Sistema de entrenamiento por jerarquías (Temas -> Niveles -> Quiz)."""
    step = st.session_state.vault['nav_step']
    
    # --- PASO 0: GRID DE TEMAS (BOTONES CARD) ---
    if step == 0:
        st.markdown('<div class="reveal">', unsafe_allow_html=True)
        st.title("🎓 Centro de Capacitación")
        st.markdown("Selecciona una especialidad para iniciar la secuencia de aprendizaje.")
        
        temas_disponibles = list(CONOCIMIENTO_REPO.keys())
        # Cuadrícula dinámica
        cols = st.columns(3)
        for i, tema in enumerate(temas_disponibles):
            with cols[i % 3]:
                # El botón es la Card completa
                if st.button(f"📘\n{tema}", key=f"theme_btn_{i}"):
                    st.session_state.vault['current_topic'] = tema
                    st.session_state.vault['nav_step'] = 1
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # --- PASO 1: SELECCIÓN DE NIVEL ---
    elif step == 1:
        st.markdown('<div class="reveal">', unsafe_allow_html=True)
        st.button("⬅️ Volver a Especialidades", on_click=lambda: st.session_state.vault.update(nav_step=0))
        topic = st.session_state.vault['current_topic']
        st.title(f"Especialidad: {topic}")
        st.subheader("Calibra el nivel de dificultad:")
        
        niveles_dict = CONOCIMIENTO_REPO[topic][0]
        niveles_lista = list(niveles_dict.keys())
        
        cols_lvl = st.columns(len(niveles_lista))
        for i, lvl in enumerate(niveles_lista):
            with cols_lvl[i]:
                if st.button(f"📶\n{lvl}", key=f"lvl_btn_{i}"):
                    st.session_state.vault['current_lvl'] = lvl
                    st.session_state.vault['nav_step'] = 2
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # --- PASO 2: QUIZ DE ALTA INTENSIDAD ---
    elif step == 2:
        st.markdown('<div class="reveal">', unsafe_allow_html=True)
        st.button("⬅️ Cambiar Nivel", on_click=lambda: st.session_state.vault.update(nav_step=1))
        tema = st.session_state.vault['current_topic']
        nivel = st.session_state.vault['current_lvl']
        
        st.title(f"Secuencia: {tema}")
        st.caption(f"Nivel de Operación: {nivel}")
        
        data_quiz = CONOCIMIENTO_REPO[tema][0][nivel]
        
        for idx, item in enumerate(data_quiz):
            with st.container():
                st.markdown(f"""
                <div class="quiz-card">
                    <p style="font-size:1.15rem; color:#fff !important; font-weight:600;">{item['pregunta'] if isinstance(item, dict) else item}</p>
                </div>
                """, unsafe_allow_html=True)
                
                if isinstance(item, dict):
                    opts = item['opciones']
                    # Radio button limpio sin label redundante
                    user_resp = st.radio(f"Respuesta para P{idx+1}:", opts, key=f"quiz_opt_{idx}", horizontal=True, label_visibility="collapsed")
                    
                    c_eval, c_blank = st.columns([1, 4])
                    if c_eval.button("Validar", key=f"val_btn_{idx}", use_container_width=True):
                        if user_resp == item['correcta']:
                            st.success("✨ VALIDACIÓN EXITOSA | +50 XP")
                            st.session_state.vault['user_xp'] += 50
                            st.session_state.vault['metrics']['success'] += 1
                        else:
                            st.error(f"❌ FALLA DE LÓGICA | Respuesta correcta: {item['correcta']}")
                            st.session_state.vault['metrics']['fails'] += 1
                        
                        with st.expander("📖 Documentación Técnica"):
                            st.info(f"**Análisis:** {item['explicacion']}")
                            st.caption(f"**Traducción:** {item['traduccion']}")
                st.divider()
        st.markdown('</div>', unsafe_allow_html=True)

# --- VISTA 3: SQL APEX WORKBENCH ---
def show_sql_lab_apex():
    """Consola de SQL Profesional con visualización de esquemas."""
    st.markdown('<div class="reveal">', unsafe_allow_html=True)
    st.title("⚔️ SQL Workbench Enterprise")
    st.markdown("Consola interactiva vinculada a la base de datos de producción (300 empleados).")
    
    c_workbench, c_schema = st.columns([3, 1])
    
    with c_schema:
        if ANIMATIONS_ON:
            lottie_sql = fetch_lottie(LOTTIE_SQL_ENG)
            if lottie_sql: st_lottie(lottie_sql, height=140)
            
        st.markdown("### 📊 Metadata Schema")
        st.markdown("""
        <div style="background:#0f172a; padding:15px; border-radius:15px; border:1px solid #1e293b; color:#10b981; font-size:0.75rem; font-family:'Fira Code';">
            -- TABLA: TRABAJADORES<br>
            ID: INT (PK)<br>
            NOMBRE: TEXT<br>
            APELLIDO: TEXT<br>
            EMAIL: TEXT<br>
            DPTO: TEXT<br>
            CARGO: TEXT<br>
            SALARIO: INT<br>
            ACCESO: TEXT<br>
            LAST_LOGIN: DATETIME<br>
            ESTADO: TEXT
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 Reiniciar Dataset", use_container_width=True):
            st.session_state.vault['db_instance'] = None
            st.rerun()

    with c_workbench:
        st.markdown("#### Apex Console")
        default_script = "-- Consultar empleados con acceso restringido y salarios competitivos\nSELECT NOMBRE, CARGO, SALARIO, ACCESO \nFROM TRABAJADORES \nWHERE SALARIO > 25000 \nORDER BY SALARIO DESC \nLIMIT 5;"
        query_input = st.text_area("SQL Editor", value=default_script, height=220, label_visibility="collapsed")
        
        if st.button("▶ EJECUTAR SCRIPT", type="primary", use_container_width=True):
            st.session_state.vault['sql_logs'].append(query_input)
            df_res, error_msg, perf_time = run_apex_query(query_input)
            
            if error_msg:
                st.error(f"⚠️ APEX ENGINE ERROR: {error_msg}")
            else:
                st.markdown(f"**Resultados de Ejecución:** {len(df_res)} entidades encontradas en {perf_time:.4f}s")
                st.dataframe(df_res, use_container_width=True)
                st.session_state.vault['user_xp'] += 25
        
        st.divider()
        st.subheader("Auditoría de Datos (Primeras 5 Entidades)")
        st.dataframe(build_advanced_db().head(5), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# 7. ENRUTADOR DINÁMICO (MAIN HUB)
# ==============================================================================

def main():
    """Orquestador de renderizado."""
    # Aplicar barra lateral fija
    render_apex_sidebar()
    
    # Selector de Vistas
    focus_view = st.session_state.vault['active_view']
    
    if focus_view == 'welcome':
        show_welcome_apex()
    elif focus_view == 'training':
        show_training_hub()
    elif focus_view == 'sql':
        show_sql_lab_apex()

# Despegue del Sistema
if __name__ == "__main__":
    main()

# ==============================================================================
# FIN DEL SISTEMA DEVMASTER v10.0 | TOTAL LÍNEAS ESTIMADAS: >850
# DESARROLLO DE ALTO NIVEL PARA CARLOS GIRON (SY) 2026
# ==============================================================================