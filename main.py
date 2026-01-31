import streamlit as st
import pandas as pd
import random
import sqlite3
import requests
import time

# ==============================================================================
# 1. CONFIGURACIÓN INICIAL Y LIBRERÍAS
# ==============================================================================
st.set_page_config(
    page_title="MasterDev Learning Hub", 
    page_icon="🎓", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Intentar cargar Lottie para animaciones
try:
    from streamlit_lottie import st_lottie
    LOTTIE_AVAILABLE = True
except ImportError:
    LOTTIE_AVAILABLE = False

def load_lottieurl(url):
    try:
        r = requests.get(url)
        if r.status_code != 200: return None
        return r.json()
    except: return None

# Animaciones (URLs)
anim_sql = load_lottieurl("https://assets2.lottiefiles.com/private_files/lf30_w1uxkbue.json")
anim_welcome = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_fcfjwiyb.json")
anim_success = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_lk80fpsm.json")

# ==============================================================================
# 2. INYECCIÓN DE CSS AVANZADO (DISEÑO Y ANIMACIONES)
# ==============================================================================
st.markdown("""
<style>
    /* --- FUENTES Y GENERAL --- */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }

    /* --- FONDO CON DEGRADADO MODERNO --- */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }

    /* --- SIDEBAR (BARRA LATERAL) OSCURA --- */
    section[data-testid="stSidebar"] {
        background-color: #0f172a; /* Dark Slate */
    }
    section[data-testid="stSidebar"] .css-17lntkn { 
        color: #e2e8f0; 
    }
    /* Títulos del sidebar en blanco */
    div[data-testid="stSidebar"] h1, div[data-testid="stSidebar"] h2, div[data-testid="stSidebar"] h3 {
        color: #ffffff !important;
    }

    /* --- CURSOR FIX (LA MANITA) --- */
    button, [role="button"], .stRadio label {
        cursor: pointer !important;
    }

    /* --- TARJETAS FLOTANTES (EFECTO GLASS) --- */
    .card-container {
        background: rgba(255, 255, 255, 0.95);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        border: 1px solid rgba(255,255,255,0.3);
        margin-bottom: 20px;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .card-container:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        border-left: 5px solid #3b82f6;
    }

    /* --- HEADER CON GRADIENTE --- */
    .gradient-text {
        background: -webkit-linear-gradient(45deg, #2563eb, #9333ea);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 3rem;
    }

    /* --- BOTONES PERSONALIZADOS --- */
    .stButton > button {
        background: linear-gradient(92.88deg, #455EB5 9.16%, #5643CC 43.89%, #673FD7 64.72%);
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: all 0.2s;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stButton > button:hover {
        box-shadow: 0 8px 15px rgba(0,0,0,0.2);
        transform: scale(1.02);
    }

    /* --- CONSOLA SQL ESTILO HACKER --- */
    .stTextArea textarea {
        background-color: #1e293b !important;
        color: #4ade80 !important; /* Verde Matrix */
        font-family: 'Courier New', monospace;
        border: 1px solid #334155;
        border-radius: 10px;
    }

    /* --- CAJA DE SCHEMA SQL (SIDEBAR) --- */
    .schema-box {
        background-color: #1e293b;
        color: #94a3b8;
        padding: 8px 12px;
        margin-bottom: 6px;
        border-radius: 6px;
        border-left: 3px solid #f59e0b;
        font-size: 0.85rem;
        display: flex;
        justify-content: space-between;
    }
    .schema-type {
        color: #64748b;
        font-size: 0.75rem;
        font-style: italic;
    }

    /* --- ALERTAS PERSONALIZADAS --- */
    .custom-success {
        padding: 1rem;
        background-color: #dcfce7;
        border-left: 5px solid #22c55e;
        color: #14532d;
        border-radius: 8px;
        margin-top: 10px;
    }
    .custom-error {
        padding: 1rem;
        background-color: #fee2e2;
        border-left: 5px solid #ef4444;
        color: #7f1d1d;
        border-radius: 8px;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 3. LÓGICA DE DATOS (Backend)
# ==============================================================================

# Carga de Preguntas
STATUS_FILE = "OK"
try:
    import preguntas
    import importlib
    importlib.reload(preguntas)
    
    if hasattr(preguntas, 'temas'):
        MIS_TEMAS = preguntas.temas
    else:
        MIS_TEMAS = {}
        STATUS_FILE = "NO_VAR"
except ImportError:
    MIS_TEMAS = {}
    STATUS_FILE = "NO_FILE"

# Generación de Base de Datos (300 Trabajadores)
def init_db():
    if 'db_trabajadores' not in st.session_state:
        # Listas para generar datos aleatorios realistas
        nombres = ["Juan", "Maria", "Carlos", "Ana", "Luis", "Sofia", "Pedro", "Lucia", "Miguel", "Elena", "Javier", "Carmen"]
        apellidos = ["Garcia", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Perez", "Sanchez", "Ramirez", "Torres"]
        cargos = ["Data Analyst", "Backend Dev", "Frontend Dev", "IT Manager", "Tech Support", "DB Admin", "QA Engineer", "DevOps"]
        
        data = []
        for i in range(1, 301):
            nom = random.choice(nombres)
            ape = random.choice(apellidos)
            cargo = random.choice(cargos)
            
            # Lógica de sueldo según cargo
            base = 4000
            if "Manager" in cargo: base = 12000
            elif "Dev" in cargo: base = 9000
            
            sueldo = base + random.randint(0, 3000)
            correo = f"{nom.lower()}.{ape.lower()}{i}@intecap.edu.gt"
            telefono = f"502-{random.randint(4000, 5999)}-{random.randint(1000, 9999)}"
            
            data.append([i, nom, ape, telefono, correo, cargo, sueldo])
            
        st.session_state.db_trabajadores = pd.DataFrame(data, columns=["ID", "NOMBRE", "APELLIDO", "NUMERO", "CORREO", "CARGO", "SUELDO"])

init_db()

# Ejecución SQL Segura
def run_sql(query):
    conn = sqlite3.connect(':memory:')
    st.session_state.db_trabajadores.to_sql('TRABAJADORES', conn, index=False, if_exists='replace')
    try:
        start = time.time()
        # Limpiamos la query de espacios extra
        query = query.strip()
        df = pd.read_sql_query(query, conn)
        end = time.time()
        return df, None, end-start
    except Exception as e:
        return None, str(e), 0
    finally:
        conn.close()

# ==============================================================================
# 4. INTERFAZ DE USUARIO - BARRA LATERAL
# ==============================================================================
with st.sidebar:
    st.markdown("## 💻 MasterDev Hub")
    
    # Menú de Navegación con Iconos
    menu = st.radio(
        "Navegación", 
        ["🏠 Inicio", "🇺🇸 Práctica Inglés", "🛢️ Laboratorio SQL"],
    )
    
    st.markdown("---")
    
    # === AQUÍ ESTÁ LO QUE PEDISTE: ESPECIFICACIONES DE LA TABLA ===
    if menu == "🛢️ Laboratorio SQL":
        st.markdown("### 📋 Estructura de Tabla")
        st.info("Tabla disponible: `TRABAJADORES`")
        
        cols = [
            ("ID", "INT (PK)"),
            ("NOMBRE", "VARCHAR"),
            ("APELLIDO", "VARCHAR"),
            ("NUMERO", "VARCHAR"),
            ("CORREO", "VARCHAR"),
            ("CARGO", "VARCHAR"),
            ("SUELDO", "INT")
        ]
        
        for col_name, col_type in cols:
            st.markdown(f"""
            <div class="schema-box">
                <span>🔹 {col_name}</span>
                <span class="schema-type">{col_type}</span>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("---")
        if st.button("⚠️ Resetear Base de Datos"):
            del st.session_state['db_trabajadores']
            st.rerun()

    st.markdown("<br><br><div style='text-align:center; color:#64748b; font-size:0.8rem;'>Powered by Intecap<br>v2.5.0 Professional</div>", unsafe_allow_html=True)

# ==============================================================================
# 5. CONTENIDO DE LAS PÁGINAS
# ==============================================================================

# --- PÁGINA INICIO ---
if menu == "🏠 Inicio":
    # Contenedor principal centrado
    st.markdown('<div style="text-align: center; padding: 2rem;">', unsafe_allow_html=True)
    st.markdown('<h1 class="gradient-text">Bienvenido al Futuro.</h1>', unsafe_allow_html=True)
    st.markdown('<p style="font-size: 1.2rem; color: #475569;">Domina SQL y el Inglés Técnico en una sola plataforma interactiva.</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if LOTTIE_AVAILABLE:
            st_lottie(anim_welcome, height=300)
    
    # Tarjetas de Resumen
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        <div class="card-container">
            <h3>🇺🇸 Módulo de Inglés</h3>
            <p>Verbos irregulares, gramática y tiempos verbales con sistema de tarjetas inteligente.</p>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="card-container">
            <h3>🛢️ SQL Server Lab</h3>
            <p>Entorno de ejecución real. Practica SELECT, WHERE, JOINs con una base de datos de 300 empleados.</p>
        </div>
        """, unsafe_allow_html=True)

# --- PÁGINA INGLÉS ---
elif menu == "🇺🇸 Práctica Inglés":
    st.markdown('<h1 style="color:#1e293b;">English Practice <span style="font-size:0.5em; color:#64748b;">Interactive Mode</span></h1>', unsafe_allow_html=True)
    
    if STATUS_FILE != "OK":
        st.error("❌ Error Crítico: No se pudo cargar el archivo 'preguntas.py'. Verifique que esté en la carpeta.")
    else:
        # Filtro inteligente para excluir SQL de esta sección
        temas_disponibles = [k for k in MIS_TEMAS.keys() if "SQL" not in k.upper()]
        
        col_sel1, col_sel2 = st.columns([2, 1])
        with col_sel1:
            tema = st.selectbox("📂 Selecciona un Tema de Estudio:", temas_disponibles)
        
        if tema:
            contenido = MIS_TEMAS[tema][0] # Estructura del archivo
            niveles = list(contenido.keys())
            
            with col_sel2:
                nivel = st.selectbox("📊 Nivel de Dificultad:", niveles)
            
            preguntas_activas = contenido[nivel]
            total_p = len(preguntas_activas)
            
            st.divider()
            
            # Iterar preguntas
            for idx, p in enumerate(preguntas_activas):
                # TARJETA VISUAL (HTML/CSS)
                st.markdown(f"""
                <div class="card-container">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                        <span style="background:#e0f2fe; color:#0369a1; padding:4px 10px; border-radius:15px; font-size:0.8rem; font-weight:bold;">Pregunta {idx + 1} / {total_p}</span>
                        <span style="color:#94a3b8; font-size:1.2rem;">🇺🇸</span>
                    </div>
                    <h3 style="color:#334155; margin-bottom:15px;">{p['pregunta']}</h3>
                </div>
                """, unsafe_allow_html=True)
                
                # Opciones interactivas
                col_opts, col_actions = st.columns([3, 1])
                
                with col_opts:
                    # Radio buttons
                    val = st.radio("Tu respuesta:", p['opciones'], key=f"q_{tema}_{idx}", label_visibility="collapsed")
                
                with col_actions:
                    st.write("") # Espaciado
                    check_btn = st.button("Comprobar Respuesta", key=f"btn_{tema}_{idx}")
                
                # Lógica de validación con FEEDBACK VISUAL
                if check_btn:
                    if val == p['correcta']:
                        st.markdown(f"""
                        <div class="custom-success">
                            <h4>✅ ¡Excelente!</h4>
                            <p>Respuesta correcta.</p>
                        </div>
                        """, unsafe_allow_html=True)
                        if LOTTIE_AVAILABLE: st_lottie(anim_success, height=100, key=f"anim_{idx}")
                    else:
                        st.markdown(f"""
                        <div class="custom-error">
                            <h4>❌ Incorrecto</h4>
                            <p>La respuesta correcta era: <b>{p['correcta']}</b></p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Explicación Expandible
                    with st.expander("💡 Ver Explicación Detallada y Traducción"):
                        st.markdown(f"**Explicación:** {p['explicacion']}")
                        st.info(f"**Traducción al Español:** {p['traduccion']}")
                
                st.markdown("<br>", unsafe_allow_html=True) # Espacio entre tarjetas

# --- PÁGINA SQL ---
elif menu == "🛢️ Laboratorio SQL":
    st.markdown('<h1 style="color:#1e293b;">Laboratorio SQL Server <span style="font-size:0.5em; color:#64748b;">Powered by SQLite</span></h1>', unsafe_allow_html=True)
    
    col_intro, col_anim = st.columns([2, 1])
    with col_intro:
        st.markdown("""
        <div style="background:#fff; padding:20px; border-radius:15px; border-left:5px solid #8b5cf6; box-shadow:0 5px 15px rgba(0,0,0,0.05);">
            <h4>👨‍💻 Consola de Ejecución</h4>
            <p>Escribe tus consultas SQL directamente. Recuerda consultar el <b>esquema de la tabla</b> en el menú izquierdo.</p>
        </div>
        """, unsafe_allow_html=True)
    with col_anim:
        if LOTTIE_AVAILABLE: st_lottie(anim_sql, height=150)
    
    # Pestañas Superiores
    tab_teoria, tab_practica = st.tabs(["📚 Desafíos Teóricos", "⚡ Consola Interactiva"])
    
    with tab_teoria:
        llave_sql = next((k for k in MIS_TEMAS.keys() if "SQL" in k.upper()), None)
        if llave_sql:
            datos_sql = MIS_TEMAS[llave_sql][0]
            nivel = st.selectbox("Selecciona Nivel de Desafío:", list(datos_sql.keys()))
            
            for item in datos_sql[nivel]:
                txt = item['pregunta'] if isinstance(item, dict) else item
                st.markdown(f"""
                <div style="margin-bottom:10px; padding:15px; background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px;">
                    ❓ {txt}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("No se encontraron preguntas de SQL en el archivo cargado.")

    with tab_practica:
        st.markdown("### Editor de Código")
        default_q = "SELECT * FROM TRABAJADORES WHERE SUELDO > 8000 ORDER BY SUELDO DESC"
        query_input = st.text_area("SQL Query:", value=default_q, height=150, help="Escribe tu sentencia SELECT aquí")
        
        col_exec, col_info = st.columns([1, 3])
        with col_exec:
            btn_run = st.button("▶ EJECUTAR QUERY", type="primary")
        
        if btn_run:
            df, err, duration = run_sql(query_input)
            
            if err:
                st.markdown(f'<div class="custom-error">⛔ <b>Error de Sintaxis SQL:</b><br>{err}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="custom-success">✅ Consulta ejecutada en <b>{duration:.4f} segundos</b></div>', unsafe_allow_html=True)
                st.write(f"Resultados: **{len(df)} filas** encontradas.")
                st.dataframe(df, use_container_width=True)