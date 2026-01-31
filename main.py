import streamlit as st
import pandas as pd
import random
import sqlite3
import requests
import time

# ==========================================
# 1. CONFIGURACIÓN Y ESTILOS (EL "MAQUILLAJE")
# ==========================================
st.set_page_config(page_title="Intecap Learning Hub", page_icon="🎓", layout="wide")

# --- ANIMACIONES LOTTIE ---
def load_lottieurl(url):
    try:
        r = requests.get(url)
        if r.status_code != 200: return None
        return r.json()
    except: return None

# Cargamos animaciones (si fallan, no pasa nada)
try:
    from streamlit_lottie import st_lottie
    lottie_coding = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_fcfjwiyb.json")
    lottie_sql = load_lottieurl("https://assets2.lottiefiles.com/private_files/lf30_w1uxkbue.json")
    LOTTIE_AVAILABLE = True
except:
    LOTTIE_AVAILABLE = False

# --- INYECCIÓN DE CSS "PROFESIONAL" (Más de 100 líneas de puro estilo) ---
st.markdown("""
<style>
    /* IMPORTAR FUENTE GOOGLE */
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Roboto', sans-serif;
    }

    /* FONDO Y COLORES PRINCIPALES */
    .stApp {
        background-color: #f0f2f6;
    }

    /* BARRA LATERAL (SIDEBAR) */
    section[data-testid="stSidebar"] {
        background-color: #1e293b; /* Dark Navy */
        color: white;
    }
    section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] label {
        color: #e2e8f0 !important;
    }

    /* TARJETAS DE PREGUNTAS (CARD STYLE) */
    .question-card {
        background-color: white;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 25px;
        border-left: 6px solid #3b82f6; /* Azul Intecap */
        transition: transform 0.2s;
    }
    .question-card:hover {
        transform: translateY(-2px);
    }

    /* ENCABEZADOS PERSONALIZADOS */
    .header-style {
        font-size: 40px;
        font-weight: 700;
        background: -webkit-linear-gradient(45deg, #3b82f6, #8b5cf6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 20px;
    }

    /* BOTONES PERSONALIZADOS */
    .stButton>button {
        background: linear-gradient(90deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        border: none;
        padding: 10px 25px;
        border-radius: 8px;
        font-weight: bold;
        box-shadow: 0 4px 6px rgba(59, 130, 246, 0.3);
        transition: 0.3s;
        width: 100%;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #2563eb 0%, #1d4ed8 100%);
        box-shadow: 0 6px 10px rgba(59, 130, 246, 0.5);
    }

    /* TABLAS DE DATOS */
    div[data-testid="stDataFrame"] {
        border-radius: 10px;
        overflow: hidden;
        border: 1px solid #e2e8f0;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }

    /* CAJA DE CÓDIGO SQL */
    .stTextArea textarea {
        background-color: #0f172a;
        color: #00ff9d; /* Letra verde hacker */
        font-family: 'Courier New', monospace;
        border-radius: 8px;
    }

    /* MENSAJES DE ESTADO */
    .success-msg {
        padding: 15px; background-color: #dcfce7; color: #166534; 
        border-radius: 8px; border: 1px solid #86efac; margin-top:10px;
    }
    .error-msg {
        padding: 15px; background-color: #fee2e2; color: #991b1b; 
        border-radius: 8px; border: 1px solid #fca5a5; margin-top:10px;
    }

    /* DECORACIÓN SIDEBAR SQL */
    .sql-info-box {
        background-color: #334155;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 5px;
        font-size: 0.9em;
        border-left: 3px solid #f59e0b; /* Naranja */
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. LOGICA DE DATOS Y CARGA
# ==========================================

# Carga segura de preguntas
try:
    import preguntas
    import importlib
    importlib.reload(preguntas)
    MIS_TEMAS = preguntas.temas if hasattr(preguntas, 'temas') else {}
    DATA_LOADED = True
except:
    MIS_TEMAS = {}
    DATA_LOADED = False

# Generador de Base de Datos (300 Trabajadores)
def inicializar_db():
    if 'db_trabajadores' not in st.session_state:
        nombres = ["Juan", "Maria", "Carlos", "Ana", "Luis", "Sofia", "Pedro", "Lucia", "Miguel", "Elena"]
        apellidos = ["Garcia", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Perez", "Sanchez"]
        cargos = ["Analista Datos", "Dev Backend", "Gerente TI", "Soporte", "Admin BD", "Dev Frontend", "QA"]
        
        data = []
        for i in range(1, 301):
            nom = random.choice(nombres)
            ape = random.choice(apellidos)
            cargo = random.choice(cargos)
            sueldo = random.randint(3500, 15000)
            correo = f"{nom.lower()}.{ape.lower()}{i}@intecap.edu.gt"
            data.append([i, nom, ape, f"555-{random.randint(1000,9999)}", correo, cargo, sueldo])
            
        st.session_state.db_trabajadores = pd.DataFrame(data, columns=["ID", "NOMBRE", "APELLIDO", "NUMERO", "CORREO", "CARGO", "SUELDO"])

inicializar_db()

# Función para ejecutar SQL
def run_query(query):
    conn = sqlite3.connect(':memory:')
    st.session_state.db_trabajadores.to_sql('TRABAJADORES', conn, index=False, if_exists='replace')
    try:
        start_time = time.time()
        res = pd.read_sql_query(query, conn)
        end_time = time.time()
        return res, None, end_time - start_time
    except Exception as e:
        return None, str(e), 0

# ==========================================
# 3. INTERFAZ DE USUARIO (UI)
# ==========================================

# --- BARRA LATERAL INTELIGENTE ---
with st.sidebar:
    st.markdown("### 🚀 Navegación")
    
    # Menú Principal
    modo = st.radio("", ["Inicio", "Práctica de Inglés", "Laboratorio SQL"], label_visibility="collapsed")
    
    st.markdown("---")
    
    # MENÚ ESPECIAL: Solo aparece si estás en SQL
    if modo == "Laboratorio SQL":
        st.markdown("#### 🗄️ Database Schema")
        st.info("Usa estos nombres exactos en tus consultas:")
        
        st.markdown("""
        <div class="sql-info-box"><b>TRABAJADORES</b> (Tabla)</div>
        <div class="sql-info-box">🔑 <b>ID</b> (INT)</div>
        <div class="sql-info-box">👤 <b>NOMBRE</b> (VARCHAR)</div>
        <div class="sql-info-box">👤 <b>APELLIDO</b> (VARCHAR)</div>
        <div class="sql-info-box">📱 <b>NUMERO</b> (VARCHAR)</div>
        <div class="sql-info-box">📧 <b>CORREO</b> (VARCHAR)</div>
        <div class="sql-info-box">💼 <b>CARGO</b> (VARCHAR)</div>
        <div class="sql-info-box">💵 <b>SUELDO</b> (INT)</div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 Resetear BD"):
            del st.session_state['db_trabajadores']
            inicializar_db()
            st.experimental_rerun()

    st.markdown("---")
    st.caption("Developed for Intecap © 2026")

# --- PÁGINA: INICIO ---
if modo == "Inicio":
    col1, col2 = st.columns([1.5, 1])
    with col1:
        st.markdown('<p class="header-style">Bienvenido, Developer</p>', unsafe_allow_html=True)
        st.markdown("""
        ### Tu plataforma de entrenamiento intensivo.
        
        Esta aplicación ha sido diseñada para perfeccionar tus habilidades técnicas y lingüísticas.
        
        * **🧠 English Module:** Mejora tu gramática con verbos irregulares y tiempos verbales.
        * **💾 SQL Lab:** Entorno real de ejecución de consultas sobre una base de datos de 300 empleados.
        """)
        
        st.info("👈 Selecciona un módulo en la barra lateral para comenzar.")
        
        if not DATA_LOADED:
            st.error("⚠️ ALERTA: No se encontró 'preguntas.py'. Sube el archivo para ver el contenido real.")

    with col2:
        if LOTTIE_AVAILABLE:
            st_lottie(lottie_coding, height=350)

# --- PÁGINA: INGLÉS (MODO TARJETAS) ---
elif modo == "Práctica de Inglés":
    st.markdown('<p class="header-style">English Practice 🇺🇸</p>', unsafe_allow_html=True)
    
    if not DATA_LOADED:
        st.warning("Necesitas subir 'preguntas.py' para ver este módulo.")
    else:
        # Filtrar solo temas de inglés
        temas_ingles = [k for k in MIS_TEMAS.keys() if "SQL" not in k.upper()]
        tema_sel = st.selectbox("Selecciona un tema:", temas_ingles)
        
        if tema_sel:
            # Lógica para extraer niveles
            contenido = MIS_TEMAS[tema_sel][0]
            nivel_sel = st.select_slider("Nivel de Dificultad:", options=list(contenido.keys()))
            
            preguntas_lista = contenido[nivel_sel]
            
            # BARRA DE PROGRESO
            progreso = st.progress(0)
            
            for i, item in enumerate(preguntas_lista):
                # TARJETA PERSONALIZADA (CSS)
                st.markdown(f"""
                <div class="question-card">
                    <h4>Pregunta {i+1}</h4>
                    <p style="font-size:18px;">{item['pregunta']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                col_opts, col_btn = st.columns([3, 1])
                
                with col_opts:
                    # Usamos radio buttons nativos de Streamlit
                    respuesta = st.radio(f"Select option:", item['opciones'], key=f"q_{i}", horizontal=True)
                
                with col_btn:
                    st.write("") # Espacio
                    st.write("") # Espacio
                    check = st.button(f"Comprobar", key=f"btn_{i}")
                
                if check:
                    if respuesta == item['correcta']:
                        st.markdown(f'<div class="success-msg">✅ <b>Correct!</b> Muy bien hecho.</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="error-msg">❌ <b>Incorrect.</b> La respuesta era: <b>{item["correcta"]}</b></div>', unsafe_allow_html=True)
                    
                    with st.expander("📚 Ver Explicación y Traducción"):
                        st.write(f"**Explicación:** {item['explicacion']}")
                        st.markdown(f"**Traducción:** *{item['traduccion']}*")
                
                st.markdown("---")

# --- PÁGINA: LABORATORIO SQL (EL FUERTE) ---
elif modo == "Laboratorio SQL":
    st.markdown('<p class="header-style">Laboratorio SQL Server 🛢️</p>', unsafe_allow_html=True)

    col_a, col_b = st.columns([2, 1])
    with col_a:
        st.markdown("""
        Bienvenido a la consola interactiva. Tienes acceso total a la tabla `TRABAJADORES`.
        
        * Usa el menú de la izquierda para ver los nombres de las columnas.
        * Puedes usar `SELECT`, `WHERE`, `GROUP BY`, `ORDER BY`, etc.
        """)
    with col_b:
        if LOTTIE_AVAILABLE:
            st_lottie(lottie_sql, height=120, key="sql")

    # TABS
    tab_teoria, tab_consola = st.tabs(["📘 Desafíos SQL", "💻 Consola de Ejecución"])

    with tab_teoria:
        # Buscar la llave de SQL
        key_sql = next((k for k in MIS_TEMAS.keys() if "SQL" in k.upper()), None)
        if key_sql and DATA_LOADED:
            datos_sql = MIS_TEMAS[key_sql][0]
            nivel_sql = st.selectbox("Selecciona dificultad:", list(datos_sql.keys()))
            
            for desafio in datos_sql[nivel_sql]:
                texto = desafio['pregunta'] if isinstance(desafio, dict) else desafio
                st.info(f"🔹 {texto}")
        else:
            st.warning("No se encontraron preguntas de SQL en el archivo.")

    with tab_consola:
        query_default = "SELECT * FROM TRABAJADORES WHERE CARGO = 'Desarrollador Backend'"
        query = st.text_area("Escribe tu Query SQL aquí:", value=query_default, height=150)
        
        col_exec, col_clear = st.columns([1, 4])
        with col_exec:
            run_btn = st.button("⚡ EJECUTAR QUERY")
        
        if run_btn:
            df_res, error, duracion = run_query(query)
            
            if error:
                st.markdown(f'<div class="error-msg">⛔ <b>Error SQL:</b><br>{error}</div>', unsafe_allow_html=True)
            else:
                st.success(f"✅ Query ejecutada exitosamente en {duracion:.4f} segundos.")
                st.write(f"Filas obtenidas: {len(df_res)}")
                st.dataframe(df_res, use_container_width=True)