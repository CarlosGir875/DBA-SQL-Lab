import streamlit as st
import pandas as pd
import random
import sqlite3
import requests
import time
from datetime import datetime

# ==============================================================================
# 1. CONFIGURACIÓN DEL SISTEMA Y ESTADO
# ==============================================================================
st.set_page_config(
    page_title="DevMaster Pro Suite", 
    page_icon="⚡", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- GESTIÓN DE ESTADO (GAMIFICACIÓN) ---
if 'user_xp' not in st.session_state: st.session_state.user_xp = 120
if 'user_level' not in st.session_state: st.session_state.user_level = 3
if 'queries_run' not in st.session_state: st.session_state.queries_run = 0

def add_xp(amount):
    st.session_state.user_xp += amount
    if st.session_state.user_xp > (st.session_state.user_level * 100):
        st.session_state.user_level += 1
        st.session_state.user_xp = 0
        st.toast(f"🎉 LEVEL UP! Eres Nivel {st.session_state.user_level}!", icon="🔥")

# --- CARGA DE LIBRERÍAS EXTERNAS ---
try:
    from streamlit_lottie import st_lottie
    LOTTIE_ON = True
except:
    LOTTIE_ON = False

def load_lottie(url):
    try:
        r = requests.get(url)
        return r.json() if r.status_code == 200 else None
    except: return None

# Assets
lottie_db = load_lottie("https://assets2.lottiefiles.com/private_files/lf30_w1uxkbue.json")
lottie_code = load_lottie("https://assets5.lottiefiles.com/packages/lf20_fcfjwiyb.json")

# ==============================================================================
# 2. CSS MASTER CLASS (ESTILOS Y ANIMACIONES)
# ==============================================================================
st.markdown("""
<style>
    /* --- FUENTES & RESET GLOBAL --- */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
    
    * { font-family: 'Inter', sans-serif; }
    
    /* CURSOR FIX: Texto normal, botones con mano */
    div, p, span, h1, h2, h3 { cursor: default; }
    button, a, .stRadio label { cursor: pointer !important; }

    /* --- PALETA DE COLORES FORZADA (Evita el problema blanco sobre blanco) --- */
    :root {
        --bg-color: #0f172a;       /* Fondo Principal Oscuro */
        --card-bg: #1e293b;        /* Fondo Tarjetas */
        --text-primary: #f1f5f9;   /* Texto Blanco Puro */
        --text-secondary: #94a3b8; /* Texto Gris */
        --accent: #3b82f6;         /* Azul Brillante */
        --success: #10b981;        /* Verde Matrix */
        --danger: #ef4444;         /* Rojo Error */
    }

    /* Fondo de la App */
    .stApp {
        background-color: var(--bg-color);
        background-image: radial-gradient(at 0% 0%, rgba(59, 130, 246, 0.15) 0px, transparent 50%),
                          radial-gradient(at 100% 100%, rgba(16, 185, 129, 0.1) 0px, transparent 50%);
    }

    /* --- SIDEBAR PERSONALIZADO --- */
    section[data-testid="stSidebar"] {
        background-color: #020617;
        border-right: 1px solid #1e293b;
    }
    
    /* Perfil en Sidebar */
    .profile-card {
        text-align: center;
        padding: 20px 10px;
        background: rgba(255,255,255,0.03);
        border-radius: 15px;
        margin-bottom: 20px;
        border: 1px solid rgba(255,255,255,0.05);
    }
    .profile-img {
        width: 80px; height: 80px;
        border-radius: 50%;
        border: 3px solid var(--accent);
        margin: 0 auto 10px auto;
        background-image: url('https://cdn-icons-png.flaticon.com/512/4140/4140048.png');
        background-size: cover;
    }
    .xp-bar {
        height: 6px;
        width: 100%;
        background: #334155;
        border-radius: 3px;
        margin-top: 5px;
        overflow: hidden;
    }
    .xp-fill {
        height: 100%;
        background: linear-gradient(90deg, #3b82f6, #a855f7);
        width: 0%; /* Se llenará dinámicamente */
        transition: width 0.5s ease;
    }

    /* --- TARJETAS (CARDS) --- */
    .glass-card {
        background: var(--card-bg);
        border: 1px solid #334155;
        border-radius: 16px;
        padding: 25px;
        margin-bottom: 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        animation: fadeIn 0.6s ease-out;
    }
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(59, 130, 246, 0.15);
        border-color: var(--accent);
    }

    /* Texto Forzado (Para arreglar tu problema de visibilidad) */
    h1, h2, h3, h4, h5, h6 { color: var(--text-primary) !important; }
    p, label, span, div { color: var(--text-secondary); }
    .glass-card h3 { color: #fff !important; }
    .glass-card p { color: #cbd5e1 !important; }

    /* --- BOTONES ESTILO CYBERPUNK --- */
    .stButton > button {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        color: white !important;
        border: none;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        border-radius: 8px;
        transition: all 0.3s;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        width: 100%;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        box-shadow: 0 0 15px rgba(59, 130, 246, 0.5);
        transform: scale(1.02); 
    }

    /* --- CONSOLA SQL --- */
    .sql-editor textarea {
        background-color: #020617 !important;
        color: #10b981 !important; /* Verde Hacker */
        font-family: 'Fira Code', monospace;
        border: 1px solid #334155;
    }

    /* --- SCHEMA VISUALIZER --- */
    .schema-row {
        display: flex; justify-content: space-between;
        padding: 8px 12px;
        border-bottom: 1px solid #334155;
        font-size: 0.85rem;
    }
    .schema-row:last-child { border-bottom: none; }
    .col-name { color: #e2e8f0; font-weight: 600; }
    .col-type { color: #64748b; font-style: italic; }

    /* --- ANIMACIONES --- */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* MENSAJES DE ERROR/EXITO */
    .msg-box {
        padding: 15px; border-radius: 10px; margin-top: 10px; animation: fadeIn 0.4s;
    }
    .msg-success { background: rgba(16, 185, 129, 0.2); border: 1px solid #10b981; color: #fff; }
    .msg-error { background: rgba(239, 68, 68, 0.2); border: 1px solid #ef4444; color: #fff; }

</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 3. BACKEND ROBUSTO (Manejo de Datos)
# ==============================================================================

# Carga de Preguntas (Con manejo de errores silencioso)
PREGUNTAS_DATA = {}
try:
    import preguntas
    import importlib
    importlib.reload(preguntas)
    if hasattr(preguntas, 'temas'):
        PREGUNTAS_DATA = preguntas.temas
except:
    PREGUNTAS_DATA = {} # Se maneja vacío si falla

# Generador de Base de Datos (Más datos, más realismo)
def get_db():
    if 'db_trabajadores' not in st.session_state:
        # Datos ampliados
        nombres = ["James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph", "Sofia", "Maria", "Lucia"]
        apellidos = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]
        cargos = ["Senior Dev", "Junior Dev", "Data Scientist", "Project Manager", "HR Specialist", "CTO", "Intern", "DevOps"]
        ciudades = ["Guatemala City", "Quetzaltenango", "Escuintla", "Antigua", "Peten"]
        
        rows = []
        for i in range(1, 351): # 350 Empleados
            nom = random.choice(nombres)
            ape = random.choice(apellidos)
            cargo = random.choice(cargos)
            sueldo = random.randint(4000, 25000)
            fecha_ingreso = f"{random.randint(2018, 2025)}-{random.randint(1,12):02d}-{random.randint(1,28):02d}"
            
            rows.append([
                i, nom, ape, 
                f"{nom[0].lower()}{ape.lower()}{i}@intecap.edu.gt", 
                cargo, sueldo, fecha_ingreso, random.choice(ciudades)
            ])
            
        df = pd.DataFrame(rows, columns=["ID", "NOMBRE", "APELLIDO", "CORREO", "CARGO", "SUELDO", "FECHA_INGRESO", "CIUDAD"])
        st.session_state.db_trabajadores = df
    return st.session_state.db_trabajadores

# ==============================================================================
# 4. SIDEBAR "SENIOR" (Perfil + Navegación)
# ==============================================================================
with st.sidebar:
    # SECCIÓN PERFIL
    st.markdown(f"""
    <div class="profile-card">
        <div class="profile-img"></div>
        <h3 style="margin:0; font-size:1.2rem; color:white;">Senior Student</h3>
        <p style="margin:0; font-size:0.8rem; color:#94a3b8;">Full Stack Aspirant</p>
        <div style="margin-top:15px; text-align:left;">
            <div style="display:flex; justify-content:space-between; font-size:0.8rem; color:#cbd5e1;">
                <span>Lvl {st.session_state.user_level}</span>
                <span>{st.session_state.user_xp} XP</span>
            </div>
            <div class="xp-bar">
                <div class="xp-fill" style="width: {(st.session_state.user_xp / (st.session_state.user_level*100))*100}%"></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🧭 MENU PRINCIPAL")
    
    # Navegación personalizada (Radio Buttons disfrazados)
    selected = st.radio(
        "Ir a:", 
        ["Dashboard", "English Training", "SQL Workbench"], 
        label_visibility="collapsed"
    )

    # WIDGET DE AYUDA SQL (Solo visible en SQL)
    if selected == "SQL Workbench":
        st.markdown("---")
        st.markdown("### 🗄️ DATABASE SCHEMA")
        st.caption("Tabla: `TRABAJADORES` (350 filas)")
        
        schema_html = ""
        cols_info = [
            ("ID", "INT (PK)"), ("NOMBRE", "VARCHAR"), ("APELLIDO", "VARCHAR"),
            ("CORREO", "VARCHAR"), ("CARGO", "VARCHAR"), ("SUELDO", "INT"),
            ("FECHA_INGRESO", "DATE"), ("CIUDAD", "VARCHAR")
        ]
        for c, t in cols_info:
            schema_html += f'<div class="schema-row"><span class="col-name">{c}</span><span class="col-type">{t}</span></div>'
        
        st.markdown(f'<div style="background:#0f172a; border-radius:8px; border:1px solid #334155;">{schema_html}</div>', unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("⚠️ Reiniciar DB"):
            del st.session_state['db_trabajadores']
            st.rerun()

# ==============================================================================
# 5. CONTENIDO PRINCIPAL (EL CORE)
# ==============================================================================

# --- DASHBOARD (HOME) ---
if selected == "Dashboard":
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("# 👋 Welcome back, Dev.")
        st.markdown("""
        <p style="font-size:1.1rem;">
            Estás en el <b>Intecap Learning Hub v3.0</b>. Esta plataforma está optimizada para 
            el aprendizaje acelerado de bases de datos y lenguajes técnicos.
        </p>
        """, unsafe_allow_html=True)
        
        # Stats Cards
        c1, c2, c3 = st.columns(3)
        c1.markdown(f"""<div class="glass-card" style="text-align:center;"><h3>{st.session_state.queries_run}</h3><p>Queries SQL</p></div>""", unsafe_allow_html=True)
        c2.markdown(f"""<div class="glass-card" style="text-align:center;"><h3>{st.session_state.user_level}</h3><p>Nivel Actual</p></div>""", unsafe_allow_html=True)
        c3.markdown(f"""<div class="glass-card" style="text-align:center;"><h3>A+</h3><p>Rendimiento</p></div>""", unsafe_allow_html=True)

    with col2:
        if LOTTIE_ON and lottie_code: st_lottie(lottie_code, height=250)

# --- ENGLISH TRAINING ---
elif selected == "English Training":
    st.markdown("# 🇺🇸 Technical English Module")
    st.markdown("Perfecciona tu vocabulario técnico y verbos irregulares.")
    
    if not PREGUNTAS_DATA:
        st.error("⚠️ Archivo 'preguntas.py' no detectado o corrupto.")
    else:
        # Filtramos SQL para que no salga aquí
        temas = [k for k in PREGUNTAS_DATA.keys() if "SQL" not in k.upper()]
        
        c_filter, c_level = st.columns(2)
        tema = c_filter.selectbox("Selecciona Tema", temas)
        
        if tema:
            levels = list(PREGUNTAS_DATA[tema][0].keys())
            lvl = c_level.select_slider("Nivel de Dificultad", options=levels)
            
            preguntas = PREGUNTAS_DATA[tema][0][lvl]
            
            st.markdown("---")
            
            # Loop de Tarjetas
            for i, p in enumerate(preguntas):
                # CONTENEDOR VISUAL DE LA PREGUNTA
                st.markdown(f"""
                <div class="glass-card">
                    <div style="display:flex; justify-content:space-between;">
                        <span style="color:#3b82f6; font-weight:bold;">QUESTION {i+1}</span>
                        <span style="background:#334155; padding:2px 8px; border-radius:4px; font-size:0.8rem;">{lvl}</span>
                    </div>
                    <h3 style="margin-top:10px; font-size:1.4rem;">{p['pregunta']}</h3>
                </div>
                """, unsafe_allow_html=True)
                
                c_opt, c_btn = st.columns([3, 1])
                user_ans = c_opt.radio("Selecciona:", p['opciones'], key=f"en_{i}", horizontal=True)
                
                if c_btn.button("Verificar", key=f"btn_en_{i}"):
                    if user_ans == p['correcta']:
                        st.markdown(f'<div class="msg-box msg-success">✅ <b>Correcto!</b> +20 XP</div>', unsafe_allow_html=True)
                        add_xp(20)
                    else:
                        st.markdown(f'<div class="msg-box msg-error">❌ <b>Incorrecto.</b> La respuesta es: {p["correcta"]}</div>', unsafe_allow_html=True)
                    
                    with st.expander("📘 Explicación Técnica"):
                        st.write(p['explicacion'])
                        st.caption(f"Traducción: {p['traduccion']}")

# --- SQL WORKBENCH ---
elif selected == "SQL Workbench":
    st.markdown("# 🛢️ SQL Server Workbench")
    
    # Layout Superior
    c_intro, c_anim = st.columns([3, 1])
    with c_intro:
        st.markdown("""
        Entorno de ejecución aislado. Tienes permisos de `LECTURA/ESCRITURA` sobre la instancia en memoria.
        Usa el panel lateral para ver las columnas disponibles.
        """)
    with c_anim:
        if LOTTIE_ON and lottie_db: st_lottie(lottie_db, height=120)

    # Tabs Profesionales
    tab1, tab2 = st.tabs(["📝 Retos & Teoría", "⚡ Consola Interactiva"])
    
    with tab1:
        st.markdown("### 🛡️ Desafíos de Código")
        sql_key = next((k for k in PREGUNTAS_DATA.keys() if "SQL" in k.upper()), None)
        
        if sql_key:
            datos = PREGUNTAS_DATA[sql_key][0]
            nivel = st.selectbox("Dificultad:", list(datos.keys()))
            
            for item in datos[nivel]:
                txt = item['pregunta'] if isinstance(item, dict) else item
                st.markdown(f"""
                <div style="background:#1e293b; border-left:4px solid #a855f7; padding:15px; margin-bottom:10px; border-radius:0 8px 8px 0;">
                    <span style="color:#e2e8f0;">{txt}</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No hay retos cargados.")

    with tab2:
        st.markdown("### 💻 Editor SQL")
        
        default_query = "-- Selecciona los programadores con sueldo alto\nSELECT * FROM TRABAJADORES \nWHERE CARGO LIKE '%Dev%' \nAND SUELDO > 8000 \nORDER BY SUELDO DESC;"
        
        # Clase especial para el text area
        st.markdown('<div class="sql-editor">', unsafe_allow_html=True)
        query = st.text_area("Script:", value=default_query, height=200, label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)
        
        col_exec, col_stat = st.columns([1, 4])
        
        if col_exec.button("▶ EJECUTAR SCRIPT"):
            conn = sqlite3.connect(':memory:')
            db = get_db()
            db.to_sql('TRABAJADORES', conn, index=False, if_exists='replace')
            
            st.session_state.queries_run += 1
            add_xp(15) # XP por practicar
            
            try:
                start_t = time.time()
                res = pd.read_sql_query(query, conn)
                duration = time.time() - start_t
                
                st.markdown(f"""
                <div class="msg-box msg-success">
                    <b>✅ Query Exitosa</b> | {len(res)} filas retornadas en {duration:.4f}s
                </div>
                """, unsafe_allow_html=True)
                
                st.dataframe(res, use_container_width=True)
                
            except Exception as e:
                st.markdown(f"""
                <div class="msg-box msg-error">
                    <b>⛔ Error de Ejecución:</b><br>{str(e)}
                </div>
                """, unsafe_allow_html=True)
            finally:
                conn.close()

# Footer sutil
st.markdown("---")
st.markdown("<div style='text-align:center; color:#475569; font-size:0.8rem;'>Intecap Learning Systems © 2026 | Developed by Master Student</div>", unsafe_allow_html=True)