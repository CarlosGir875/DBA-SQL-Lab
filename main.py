"""
==============================================================================
  DEVMASTER PRO SUITE v5.0 - ULTIMATE EDITION
  Developed for: Intecap Student
  Target: Full Stack Mastery
  Year: 2026
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
import base64

# ==============================================================================
# 1. SISTEMA DE CONFIGURACIÓN Y CARGA DE ACTIVOS
# ==============================================================================

st.set_page_config(
    page_title="DevMaster v5 | Intecap",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CARGADOR DE ANIMACIONES (LOTTIE) ---
def load_lottie_url(url: str):
    """Descarga animaciones JSON de LottieFiles de forma segura."""
    try:
        r = requests.get(url, timeout=2)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

# Definición de URLs de Animaciones
ASSETS = {
    "sql": "https://assets2.lottiefiles.com/private_files/lf30_w1uxkbue.json",
    "coding": "https://assets5.lottiefiles.com/packages/lf20_fcfjwiyb.json",
    "success": "https://assets10.lottiefiles.com/packages/lf20_lk80fpsm.json",
    "error": "https://assets9.lottiefiles.com/packages/lf20_kcsr6fcp.json",
    "level_up": "https://assets6.lottiefiles.com/packages/lf20_p4s0msd0.json"
}

# Intentar importar librería Lottie
try:
    from streamlit_lottie import st_lottie
    LOTTIE_AVAILABLE = True
except ImportError:
    LOTTIE_AVAILABLE = False

# ==============================================================================
# 2. GESTOR DE ESTADO (STATE MANAGER)
# ==============================================================================

def init_session_state():
    """Inicializa todas las variables de sesión para evitar errores de Key."""
    DEFAULTS = {
        'view': 'dashboard',          # Vista actual
        'training_topic': None,       # Tema seleccionado
        'training_level': None,       # Nivel seleccionado
        'training_step': 0,           # Paso del drill-down
        'xp': 340,                    # Experiencia actual
        'level': 5,                   # Nivel de usuario
        'streak': 3,                  # Racha de días
        'history_sql': [],            # Historial de queries
        'correct_answers': 0,         # Contador de aciertos
        'wrong_answers': 0,           # Contador de errores
        'db_initialized': False       # Bandera de BD
    }

    for key, value in DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# ==============================================================================
# 3. MOTOR DE ESTILOS CSS (DISEÑO PROFESIONAL)
# ==============================================================================

def inject_custom_css():
    """Inyecta CSS avanzado para Glassmorphism y efectos Neon."""
    st.markdown("""
    <style>
        /* --- FUENTES E IMPORTACIONES --- */
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Fira+Code:wght@400;600&display=swap');

        :root {
            --primary: #6366f1;   /* Indigo Neon */
            --secondary: #ec4899; /* Pink Neon */
            --bg-dark: #0f172a;   /* Deep Blue */
            --panel: #1e293b;     /* Slate */
            --text-main: #f8fafc;
            --success: #10b981;
            --danger: #ef4444;
            --glass: rgba(30, 41, 59, 0.7);
        }

        /* --- RESET GENERAL --- */
        .stApp {
            background-color: var(--bg-dark);
            background-image: 
                radial-gradient(circle at 10% 20%, rgba(99, 102, 241, 0.15) 0%, transparent 40%),
                radial-gradient(circle at 90% 80%, rgba(236, 72, 153, 0.15) 0%, transparent 40%);
            font-family: 'Outfit', sans-serif;
        }

        h1, h2, h3, h4, h5, h6 { color: var(--text-main) !important; font-weight: 800; letter-spacing: -0.5px; }
        p, label, span, div { color: #cbd5e1; }
        
        /* --- SCROLLBAR PERSONALIZADO --- */
        ::-webkit-scrollbar { width: 8px; }
        ::-webkit-scrollbar-track { background: var(--bg-dark); }
        ::-webkit-scrollbar-thumb { background: #334155; border-radius: 4px; }
        ::-webkit-scrollbar-thumb:hover { background: var(--primary); }

        /* --- BOTONES CON EFECTO NEON --- */
        div.stButton > button {
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(236, 72, 153, 0.1));
            border: 1px solid rgba(255, 255, 255, 0.1);
            color: white;
            border-radius: 12px;
            padding: 15px 25px;
            font-weight: 600;
            transition: all 0.3s ease;
            backdrop-filter: blur(10px);
            width: 100%;
        }
        
        div.stButton > button:hover {
            border-color: var(--primary);
            box-shadow: 0 0 20px rgba(99, 102, 241, 0.4);
            transform: translateY(-2px);
            color: white;
        }

        /* --- TARJETAS DE MÓDULOS (GRID) --- */
        .module-card {
            background: var(--panel);
            border-radius: 20px;
            padding: 2rem;
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.05);
            transition: transform 0.3s, border-color 0.3s;
            cursor: pointer;
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }
        .module-card:hover {
            border-color: var(--secondary);
            transform: scale(1.03);
            background: linear-gradient(180deg, var(--panel) 0%, #283445 100%);
        }

        /* --- EDITOR SQL --- */
        .sql-container {
            position: relative;
            border-radius: 12px;
            overflow: hidden;
            border: 1px solid #475569;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }
        .sql-header {
            background: #0f172a;
            padding: 8px 15px;
            font-size: 0.8rem;
            color: #94a3b8;
            border-bottom: 1px solid #334155;
            display: flex; gap: 10px;
        }
        .stTextArea textarea {
            background-color: #1e1e1e !important;
            color: #a5b4fc !important;
            font-family: 'Fira Code', monospace !important;
            border: none;
        }

        /* --- SIDEBAR --- */
        section[data-testid="stSidebar"] {
            background-color: #020617;
            border-right: 1px solid #1e293b;
        }
        
        /* --- ESTADÍSTICAS --- */
        .stat-box {
            background: rgba(255,255,255,0.03);
            border-radius: 12px;
            padding: 15px;
            border: 1px solid rgba(255,255,255,0.05);
            text-align: center;
        }
        .stat-number {
            font-size: 2rem;
            font-weight: 800;
            background: linear-gradient(to right, var(--primary), var(--secondary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        /* --- ANIMACIONES --- */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .animate-enter { animation: fadeIn 0.5s ease-out forwards; }

    </style>
    """, unsafe_allow_html=True)

inject_custom_css()

# ==============================================================================
# 4. CAPA DE DATOS (DATA LAYER)
# ==============================================================================

# --- IMPORTACIÓN SEGURA DE PREGUNTAS (ANTI-CRASH) ---
# Si falla el archivo del usuario, usamos estos datos de respaldo
FALLBACK_DATA = {
    "Verbos Irregulares (Demo)": [{
        "1. Básico": [
            {"pregunta": "Past of 'Go'?", "opciones": ["Went", "Gone"], "correcta": "Went", "explicacion": "Irregular.", "traduccion": "Ir"},
            {"pregunta": "Past of 'See'?", "opciones": ["Saw", "Seen"], "correcta": "Saw", "explicacion": "Irregular.", "traduccion": "Ver"}
        ]
    }],
    "SQL Theory (Demo)": [{
        "1. Básico": ["¿Qué comando extrae datos?", "¿Cómo filtras filas?"]
    }]
}

TEMAS = {}
STATUS_MSG = ""

try:
    import preguntas
    import importlib
    importlib.reload(preguntas) # Recarga en caliente
    
    if hasattr(preguntas, 'temas'):
        TEMAS = preguntas.temas
        STATUS_MSG = "✅ Archivo cargado correctamente"
    else:
        TEMAS = FALLBACK_DATA
        STATUS_MSG = "⚠️ Estructura inválida en preguntas.py (Usando Demo)"
except ImportError:
    TEMAS = FALLBACK_DATA
    STATUS_MSG = "⚠️ No se encontró preguntas.py (Usando Demo)"
except Exception as e:
    TEMAS = FALLBACK_DATA
    STATUS_MSG = f"❌ Error de sintaxis: {str(e)}"

# --- GENERADOR DE BASE DE DATOS MASIVA ---
def get_db_connection():
    """Genera una BD SQLite en memoria con 400 registros realistas."""
    if st.session_state.db_trabajadores is None:
        names = ["James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph", "Thomas", "Charles", "Daniel", "Matthew"]
        surnames = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez", "Hernandez"]
        roles = ["Backend Dev", "Frontend Dev", "Fullstack", "Data Scientist", "DevOps", "QA Engineer", "Product Owner", "Tech Lead"]
        cities = ["New York", "San Francisco", "Austin", "Seattle", "Chicago", "Boston", "Remote"]
        
        data = []
        for i in range(1, 401):
            n = random.choice(names)
            s = random.choice(surnames)
            role = random.choice(roles)
            city = random.choice(cities)
            salary = random.randint(4500, 22000)
            email = f"{n.lower()}.{s.lower()}{i}@intecap.edu.gt"
            joined = (datetime.now() - timedelta(days=random.randint(0, 1500))).strftime("%Y-%m-%d")
            status = random.choice(["Active", "Active", "Active", "On Leave"])
            
            data.append([i, n, s, email, role, salary, city, joined, status])
            
        df = pd.DataFrame(data, columns=["ID", "NOMBRE", "APELLIDO", "EMAIL", "CARGO", "SUELDO", "CIUDAD", "FECHA_INGRESO", "ESTADO"])
        st.session_state.db_trabajadores = df
        
    conn = sqlite3.connect(':memory:')
    st.session_state.db_trabajadores.to_sql('TRABAJADORES', conn, index=False, if_exists='replace')
    return conn

# ==============================================================================
# 5. COMPONENTES UI REUTILIZABLES
# ==============================================================================

def render_sidebar():
    """Renderiza el menú lateral con perfil y navegación."""
    with st.sidebar:
        # Perfil
        st.markdown(f"""
        <div style="text-align:center; padding:20px; background:#111827; border-radius:15px; border:1px solid #374151; margin-bottom:20px;">
            <div style="width:80px; height:80px; background:linear-gradient(45deg, #6366f1, #ec4899); border-radius:50%; margin:0 auto 10px; display:flex; align-items:center; justify-content:center; font-size:2rem;">👨‍💻</div>
            <h3 style="margin:0; font-size:1.2rem;">Dev Student</h3>
            <p style="font-size:0.8rem; color:#9ca3af;">Full Stack Path</p>
            
            <div style="margin-top:15px; background:#374151; height:8px; border-radius:4px; overflow:hidden;">
                <div style="background:#10b981; width:{min(st.session_state.xp % 100, 100)}%; height:100%;"></div>
            </div>
            <div style="display:flex; justify-content:space-between; font-size:0.7rem; margin-top:5px; color:#cbd5e1;">
                <span>Nivel {st.session_state.level}</span>
                <span>{st.session_state.xp} XP</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 🧭 NAVEGACIÓN")
        
        if st.button("🏠 Dashboard Central", key="nav_dash"):
            st.session_state.view = 'dashboard'
            st.rerun()
            
        if st.button("🎓 Training Center", key="nav_train"):
            st.session_state.view = 'training'
            st.session_state.training_step = 0
            st.rerun()
            
        if st.button("🛢️ Laboratorio SQL", key="nav_sql"):
            st.session_state.view = 'sql'
            st.rerun()
            
        # Debug Info del archivo
        st.markdown("---")
        if "✅" in STATUS_MSG:
            st.caption(f"{STATUS_MSG}")
        else:
            st.error(STATUS_MSG)
            
        st.markdown("---")
        st.caption("DevMaster v5.0 Ultimate")

def gain_xp(amount):
    """Sistema de gamificación."""
    st.session_state.xp += amount
    if st.session_state.xp >= st.session_state.level * 100:
        st.session_state.level += 1
        st.balloons()
        st.toast(f"🎉 ¡NIVEL {st.session_state.level} ALCANZADO!", icon="🚀")

# ==============================================================================
# 6. VISTAS PRINCIPALES (CONTROLLERS)
# ==============================================================================

# --- VISTA 1: DASHBOARD ---
def view_dashboard():
    st.title(f"Bienvenido, Master Dev.")
    st.markdown("Tu centro de comando para dominar el desarrollo de software.")
    
    # 1. KPIs
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="stat-box"><div class="stat-number">{st.session_state.streak}🔥</div><div>Racha Días</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="stat-box"><div class="stat-number">{len(st.session_state.history_sql)}</div><div>Queries SQL</div></div>', unsafe_allow_html=True)
    with col3:
        total = st.session_state.correct_answers + st.session_state.wrong_answers
        acc = int((st.session_state.correct_answers / total * 100)) if total > 0 else 0
        st.markdown(f'<div class="stat-box"><div class="stat-number">{acc}%</div><div>Precisión</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="stat-box"><div class="stat-number">{len(TEMAS)}</div><div>Módulos</div></div>', unsafe_allow_html=True)

    st.markdown("---")
    
    # 2. Daily Challenge & Animation
    c_main, c_anim = st.columns([2, 1])
    
    with c_main:
        st.subheader("🎯 Reto Diario")
        st.info("Completa 5 preguntas de 'Verbos Irregulares' y ejecuta 1 JOIN en SQL para ganar +50 XP.")
        
        st.subheader("📊 Tu Progreso Semanal")
        # Gráfica simulada con Pandas
        chart_data = pd.DataFrame({
            'Día': ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom'],
            'XP Ganado': [20, 45, 30, 80, 10, 90, st.session_state.xp % 50]
        })
        st.bar_chart(chart_data.set_index('Día'))

    with c_anim:
        if LOTTIE_AVAILABLE:
            anim = load_lottie_url(ASSETS["coding"])
            if anim: st_lottie(anim, height=300)

# --- VISTA 2: TRAINING CENTER (DRILL-DOWN) ---
def view_training():
    step = st.session_state.training_step
    
    # --- PASO 0: SELECCIÓN DE TEMA ---
    if step == 0:
        st.title("🎓 Centro de Entrenamiento")
        st.markdown("Selecciona un módulo para especializarte.")
        
        temas = [k for k in TEMAS.keys()] # Obtener temas
        
        # Grid System for Cards
        cols = st.columns(3)
        for i, tema in enumerate(temas):
            with cols[i % 3]:
                # Hack para hacer toda la tarjeta clickeable visualmente
                st.markdown(f"""
                <div class="module-card">
                    <h2 style="margin:0; color:white;">📚</h2>
                    <h4 style="margin:10px 0 0 0;">{tema}</h4>
                </div>
                """, unsafe_allow_html=True)
                
                # Botón real invisible encima (o debajo) para la lógica
                if st.button(f"Iniciar {tema}", key=f"btn_tema_{i}"):
                    st.session_state.training_topic = tema
                    st.session_state.training_step = 1
                    st.rerun()
                st.markdown("<br>", unsafe_allow_html=True)

    # --- PASO 1: SELECCIÓN DE NIVEL ---
    elif step == 1:
        topic = st.session_state.training_topic
        st.button("⬅️ Volver", on_click=lambda: st.session_state.update(training_step=0))
        
        st.title(f"{topic}")
        st.markdown("### Selecciona Dificultad")
        
        try:
            levels = list(TEMAS[topic][0].keys())
            c_lvl = st.columns(len(levels))
            
            for i, lvl in enumerate(levels):
                with c_lvl[i]:
                    if st.button(f"📶 {lvl}", key=f"lvl_{i}", use_container_width=True):
                        st.session_state.training_level = lvl
                        st.session_state.training_step = 2
                        st.rerun()
        except Exception as e:
            st.error(f"Error en estructura de datos: {e}")

    # --- PASO 2: QUIZ ---
    elif step == 2:
        topic = st.session_state.training_topic
        lvl = st.session_state.training_level
        
        c1, c2 = st.columns([1, 6])
        with c1:
            st.button("⬅️ Niveles", on_click=lambda: st.session_state.update(training_step=1))
        with c2:
            st.progress(0.5, text=f"Estudiando: {topic} ({lvl})")

        try:
            preguntas = TEMAS[topic][0][lvl]
            
            for i, p in enumerate(preguntas):
                with st.container():
                    st.markdown(f'<div class="animate-enter" style="background:#1e293b; padding:20px; border-radius:15px; margin-bottom:20px; border-left:5px solid #6366f1;">'
                                f'<h4 style="margin:0;">Pregunta {i+1}</h4>'
                                f'<p style="font-size:1.2rem; color:white;">{p["pregunta"]}</p>'
                                f'</div>', unsafe_allow_html=True)
                    
                    c_opt, c_check = st.columns([3, 1])
                    
                    user_resp = c_opt.radio("Selecciona:", p['opciones'], key=f"q_{i}", horizontal=True)
                    
                    if c_check.button("Validar", key=f"chk_{i}"):
                        if user_resp == p['correcta']:
                            st.success("✅ ¡Correcto! +20 XP")
                            gain_xp(20)
                            st.session_state.correct_answers += 1
                        else:
                            st.error(f"❌ Incorrecto. Respuesta: {p['correcta']}")
                            st.session_state.wrong_answers += 1
                        
                        with st.expander("📚 Ver Explicación"):
                            st.info(p['explicacion'])
                            st.caption(p['traduccion'])
                            
                    st.divider()
                    
        except Exception as e:
            st.error(f"Error cargando preguntas: {e}")

# --- VISTA 3: SQL WORKBENCH ---
def view_sql():
    st.title("🛢️ Laboratorio SQL Profesional")
    
    col_help, col_work = st.columns([1, 3])
    
    with col_help:
        if LOTTIE_AVAILABLE:
            lottie = load_lottie_url(ASSETS["sql"])
            if lottie: st_lottie(lottie, height=150)
            
        st.markdown("### 📋 Esquema")
        st.caption("Tabla: TRABAJADORES")
        
        schema = [
            ("ID", "INT (PK)"), ("NOMBRE", "TEXT"), ("APELLIDO", "TEXT"),
            ("EMAIL", "TEXT"), ("CARGO", "TEXT"), ("SUELDO", "INT"),
            ("CIUDAD", "TEXT"), ("FECHA", "DATE"), ("ESTADO", "TEXT")
        ]
        
        for field, type_ in schema:
            st.markdown(f"""
            <div style="display:flex; justify-content:space-between; padding:5px; border-bottom:1px solid #334155; font-size:0.8rem;">
                <span style="color:#a5b4fc; font-weight:bold;">{field}</span>
                <span style="color:#64748b;">{type_}</span>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 Resetear DB"):
            st.session_state.db_trabajadores = None
            st.rerun()

    with col_work:
        # Pestañas
        tab_run, tab_hist = st.tabs(["⚡ Ejecutar", "📜 Historial"])
        
        with tab_run:
            st.markdown("Escribe tu consulta SQL:")
            
            # Editor Falso
            st.markdown('<div class="sql-container"><div class="sql-header"><span>SQL EDITOR</span><span>sqlite3 :: memory</span></div>', unsafe_allow_html=True)
            query = st.text_area("", value="SELECT * FROM TRABAJADORES WHERE SUELDO > 10000 LIMIT 5;", height=150, label_visibility="collapsed")
            st.markdown('</div>', unsafe_allow_html=True)
            
            c_exec, c_stat = st.columns([1, 4])
            if c_exec.button("▶ Ejecutar", type="primary"):
                conn = get_db_connection()
                try:
                    start_t = time.time()
                    # Ejecución segura
                    clean_q = query.strip()
                    st.session_state.history_sql.append(clean_q)
                    
                    if clean_q.lower().startswith("select"):
                        df = pd.read_sql_query(clean_q, conn)
                        dur = time.time() - start_t
                        
                        st.markdown(f"""
                        <div style="background:rgba(16, 185, 129, 0.2); padding:10px; border-radius:8px; margin-top:10px; border:1px solid #10b981;">
                            ✅ <b>Query Exitosa</b> ({len(df)} filas en {dur:.4f}s)
                        </div>
                        """, unsafe_allow_html=True)
                        st.dataframe(df, use_container_width=True)
                        gain_xp(10)
                    else:
                        cur = conn.cursor()
                        cur.execute(clean_q)
                        conn.commit()
                        st.success("✅ Comando ejecutado. (Nota: Cambios temporales en memoria)")
                        
                except Exception as e:
                    st.markdown(f"""
                    <div style="background:rgba(239, 68, 68, 0.2); padding:10px; border-radius:8px; margin-top:10px; border:1px solid #ef4444;">
                        ⛔ <b>Error SQL:</b> {e}
                    </div>
                    """, unsafe_allow_html=True)
                finally:
                    conn.close()

        with tab_hist:
            if st.session_state.history_sql:
                for q in reversed(st.session_state.history_sql):
                    st.code(q, language="sql")
            else:
                st.info("No hay historial aún.")

# ==============================================================================
# 7. ROUTER PRINCIPAL (MAIN LOOP)
# ==============================================================================

def main():
    render_sidebar()
    
    if st.session_state.view == 'dashboard':
        view_dashboard()
    elif st.session_state.view == 'training':
        view_training()
    elif st.session_state.view == 'sql':
        view_sql()

# Ejecución del programa
if __name__ == "__main__":
    main()

# ==============================================================================
# FIN DEL CÓDIGO - INTECAP 2026
# ==============================================================================