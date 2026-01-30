import streamlit as st
import random
import pandas as pd
import time
from preguntas import temas 

# =================================================================
# 1. CONFIGURACIÓN DE PÁGINA Y UI (REFLECTORES & CURSOR SYSTEM)
# =================================================================
st.set_page_config(page_title="DBA English & SQL Lab 2026", page_icon="⚡", layout="wide")

# CSS PERSONALIZADO - DECORACIÓN EXTREMA DEL MENÚ (Líneas 14 - 105)
st.markdown("""
<style>
    .stApp { background-color: #0F1116; color: #E0E0E0; font-family: 'Segoe UI', sans-serif; }
    
    /* CURSOR POINTER (MANITA) PARA TODO */
    * { 
        user-select: none !important; 
        caret-color: transparent !important; 
        cursor: pointer !important; 
    }
    
    /* EXCEPCIÓN: CAJAS DE TEXTO */
    input[type="text"], textarea, [data-testid="stSidebar"] input[type="text"], .stTextArea textarea { 
        user-select: text !important; 
        caret-color: #00FFAA !important; 
        cursor: text !important; 
    }

    /* SIDEBAR DECORADO (CYBERPUNK STYLE) */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0A0C10 0%, #161920 100%) !important;
        border-right: 2px solid #00FFAA22;
    }

    /* CARD DE USUARIO EN EL MENÚ */
    .user-profile {
        padding: 15px;
        background: rgba(0, 255, 170, 0.05);
        border: 1px solid #00FFAA33;
        border-radius: 10px;
        margin-bottom: 20px;
        text-align: center;
    }

    /* INDICADOR DE STATUS PARPADEANTE */
    .status-blink {
        width: 10px;
        height: 10px;
        background-color: #00FFAA;
        border-radius: 50%;
        display: inline-block;
        margin-right: 5px;
        animation: blink 1.5s infinite;
        box-shadow: 0 0 10px #00FFAA;
    }
    @keyframes blink {
        0% { opacity: 0.2; }
        50% { opacity: 1; }
        100% { opacity: 0.2; }
    }

    /* ETIQUETAS DE SECCIÓN EN MENÚ */
    .menu-label {
        color: #00FFAA;
        font-size: 0.7rem;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-top: 20px;
        margin-bottom: 10px;
        opacity: 0.8;
    }

    /* BOTONES CON REFLECTOR Y ANIMACIÓN */
    .stButton>button {
        border-radius: 8px;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        border: 1px solid #30363D;
        background-color: #161920;
        color: #C9D1D9;
        font-weight: 700;
        height: 3em;
        width: 100%;
    }
    .stButton>button:hover {
        border-color: #00FFAA;
        color: #00FFAA;
        box-shadow: 0 0 25px rgba(0, 255, 170, 0.4);
        transform: scale(1.02);
    }

    /* CONSOLA DE LOGS */
    .log-container {
        background-color: #010409;
        border: 1px solid #00FFAA22;
        padding: 15px;
        border-radius: 10px;
        font-family: 'Consolas', monospace;
        color: #00FFAA;
        font-size: 0.8rem;
        box-shadow: inset 0 0 15px #000;
        overflow-y: auto;
        height: 150px;
        border-left: 4px solid #00FFAA;
    }

    /* REMOVER DECORACIÓN POR DEFECTO */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# =================================================================
# 2. DATA ENGINE (BASE DE DATOS DE ALTO RENDIMIENTO)
# =================================================================
@st.cache_data
def cargar_base_datos():
    nombres = ["Carlos Giron", "Juan Perez", "Maria Lopez", "Ana Garcia", "Luis Martinez", "Elena Rodriguez", "Diego Sosa", "Carmen Ruiz", "Pablo Duarte", "Lucia Mendez"]
    paises = ['Guatemala', 'Mexico', 'USA', 'España', 'El Salvador', 'Honduras', 'Colombia', 'Argentina']
    roles = ['DBA', 'DevOps', 'Data Scientist', 'Security Analyst', 'Manager', 'QA Engineer']
    estados = ['Activo', 'Inactivo', 'En Auditoría', 'Bloqueado']
    
    data = []
    for i in range(1, 301):
        data.append({
            'ID': 1000 + i,
            'Nombre': random.choice(nombres),
            'Pais': random.choice(paises),
            'Estado': random.choice(estados),
            'Rol': random.choice(roles),
            'Last_Login': f"2026-01-{random.randint(1,29):02d}",
            'Storage_Used': f"{random.randint(10, 500)}GB"
        })
    return pd.DataFrame(data)

df_sql = cargar_base_datos()

# =================================================================
# 3. GESTIÓN DE ESTADO AVANZADA
# =================================================================
if 'indice' not in st.session_state: st.session_state.indice = 0
if 'vidas' not in st.session_state: st.session_state.vidas = 3
if 'puntos' not in st.session_state: st.session_state.puntos = 0
if 'logs' not in st.session_state: st.session_state.logs = [f"[{time.strftime('%H:%M:%S')}] Kernel Loaded."]
if 'id_final' not in st.session_state: st.session_state.id_final = ""
if 'lista_mezclada' not in st.session_state: st.session_state.lista_mezclada = []
if 'terminal_output' not in st.session_state: st.session_state.terminal_output = ["Welcome to DBA Terminal v1.0. Type 'HELP' to start."]

def add_log(msg):
    st.session_state.logs.append(f"[{time.strftime('%H:%M:%S')}] {msg}")
    if len(st.session_state.logs) > 8: st.session_state.logs.pop(0)

# =================================================================
# 4. SIDEBAR - CONTROL DE NAVEGACIÓN Y DECORACIÓN (Líneas 165 - 235)
# =================================================================
with st.sidebar:
    # NUEVO LOGO INNOVADOR
    st.markdown("""
        <div style='text-align: center; padding: 10px;'>
            <img src='https://cdn-icons-png.flaticon.com/512/2312/2312676.png' width='100' style='filter: drop-shadow(0 0 10px #00FFAA);'>
            <h1 style='color: white; font-size: 1.2rem; margin-top: 10px;'>DBA CORE 2026</h1>
        </div>
    """, unsafe_allow_html=True)

    # USER PROFILE CARD
    st.markdown(f"""
        <div class="user-profile">
            <div style="font-size: 0.8rem; color: #8B949E;">OPERATOR IDENTIFIED</div>
            <div style="font-weight: bold; color: #00FFAA; letter-spacing: 1px;">Developer SY</div>
            <div style="font-size: 0.7rem; margin-top:5px;">
                <span class="status-blink"></span> <span style="color: #00FFAA;">SYSTEM ONLINE</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="menu-label">Explorador de Datos</div>', unsafe_allow_html=True)
    opciones_menu = ["🏠 Inicio"] + list(temas.keys())
    seleccion = st.selectbox("📂 Módulo Actual:", opciones_menu, label_visibility="collapsed")

    # MOTOR DE CARGA REFORZADO
    if seleccion != "🏠 Inicio":
        st.markdown('<div class="menu-label">Nivel de Seguridad</div>', unsafe_allow_html=True)
        nivel_sel = st.radio("🎯 Nivel de Acceso:", ["1. Básico", "2. Intermedio", "3. Avanzado"], label_visibility="collapsed")
        
        contenido = temas.get(seleccion, [])
        lista_final = []
        id_actual = f"{seleccion}_{nivel_sel}"

        if isinstance(contenido, list):
            for bloque in contenido:
                if isinstance(bloque, dict):
                    for llave in bloque.keys():
                        if nivel_sel.split(". ")[-1] in llave or llave in nivel_sel:
                            lista_final = bloque[llave]
                            break

        if st.session_state.id_final != id_actual:
            if lista_final:
                st.session_state.lista_mezclada = random.sample(lista_final, len(lista_final))
                st.session_state.id_final = id_actual
                st.session_state.indice = 0
                st.session_state.vidas = 3
                add_log(f"Load: {seleccion} {nivel_sel}")
            else:
                st.session_state.lista_mezclada = []
                st.session_state.id_final = id_actual

    st.markdown('<div class="menu-label">Módulos de Sistema</div>', unsafe_allow_html=True)
    nav_path = st.radio("🧭 Navegación:", 
                         ["📚 Training Mode", "🗄️ SQL Studio Pro", "📟 Terminal Auditor", "📊 Performance"], label_visibility="collapsed")

    # Dashboard de Logs en Sidebar
    st.markdown('<div class="menu-label">System Telemetry</div>', unsafe_allow_html=True)
    log_text = "".join([f"<div style='margin-bottom:2px;'>{l}</div>" for l in st.session_state.logs])
    st.markdown(f'<div class="log-container">{log_text}</div>', unsafe_allow_html=True)

# =================================================================
# 5. TRAINING MODE (QUIZ ENGINE)
# =================================================================
if nav_path == "📚 Training Mode":
    if seleccion == "🏠 Inicio":
        st.title("🛡️ DBA English & SQL Lab")
        st.write("Welcome to my app learning, this is my new project I mean my first project, I hope you can learn with my project!.")
        st.image("https://cdn-icons-png.flaticon.com/512/2721/2721614.png", width=120)
    else:
        st.title(f"📖 Unidad: {seleccion}")
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Vidas", f"{'❤️' * st.session_state.vidas}")
        c2.metric("Puntos Ganados", f"{st.session_state.puntos} XP")
        with c3:
            if st.button("RESET SYSTEM"):
                st.session_state.indice = 0
                st.session_state.vidas = 3
                st.rerun()

        if not st.session_state.lista_mezclada:
            st.warning("⚠️ Sin datos para esta configuración de nivel.")
        elif st.session_state.indice < len(st.session_state.lista_mezclada):
            pregunta = st.session_state.lista_mezclada[st.session_state.indice]
            st.progress((st.session_state.indice + 1) / len(st.session_state.lista_mezclada))

            with st.container():
                st.markdown(f"### 📋 Pregunta {st.session_state.indice + 1}")
                st.info(pregunta['pregunta'])
                
                with st.form(key=f"form_{st.session_state.indice}"):
                    ans = st.radio("Sintaxis correcta:", pregunta['opciones'])
                    if st.form_submit_button("EJECUTAR VALIDACIÓN"):
                        if ans == pregunta['correcta']:
                            st.success(f"✅ EXPLICACIÓN: {pregunta['explicacion']}")
                            st.session_state.puntos += 15
                            add_log("SQL Syntax Validated.")
                        else:
                            st.error(f"❌ FALLO: La respuesta era {pregunta['correcta']}")
                            st.session_state.vidas -= 1
                            add_log("Integrity Violation.")
                        st.markdown(f"**Traducción:** {pregunta['traduccion']}")

                if st.button("Continuar al Siguiente Registro ➡️"):
                    if st.session_state.vidas > 0:
                        st.session_state.indice += 1
                        st.rerun()
                    else:
                        st.error("DATABASE LOCKED. Superaste los fallos permitidos.")
                        time.sleep(2)
                        st.session_state.indice = 0
                        st.session_state.vidas = 3
                        st.rerun()
        else:
            st.balloons()
            st.success("✅ MÓDULO COMPLETADO CON ÉXITO")

# =================================================================
# 6. SQL STUDIO PRO (MODO APRENDIZAJE)
# =================================================================
elif nav_path == "🗄️ SQL Studio Pro":
    st.title("🗄️ SQL Management Studio Pro")
    
    col_a, col_b = st.columns([2, 1])
    
    with col_a:
        sql_input = st.text_area("SQL Script Editor:", height=250, placeholder="SELECT * FROM Usuarios WHERE Pais = 'Guatemala'...")
        if st.button("RUN QUERY (F5)"):
            if "SELECT" in sql_input.upper():
                st.success("Query ejecutada exitosamente.")
                st.dataframe(df_sql, use_container_width=True)
                add_log("Select query executed.")
            else:
                st.warning("El simulador está en modo de lectura. Prueba un comando SELECT.")

    with col_b:
        st.markdown("### 🤖 SQL Mentor AI")
        if sql_input:
            if "WHERE" not in sql_input.upper():
                st.error("🚨 REGLA DE ORO: Siempre usa WHERE en UPDATE/DELETE (y SELECT para ahorrar recursos).")
            if "*" in sql_input:
                st.warning("⚠️ Nota: SELECT * es cómodo pero lento en tablas de millones de registros.")
            if "FROM USUARIOS" in sql_input.upper():
                st.success("✅ Tabla 'Usuarios' detectada correctamente.")
        else:
            st.info("Escribe tu código SQL para recibir feedback en tiempo real.")

    with st.expander("📚 Ver Diccionario de Datos"):
        st.table(pd.DataFrame({
            "Columna": df_sql.columns,
            "Tipo": ["INT", "VARCHAR", "VARCHAR", "VARCHAR", "VARCHAR", "DATE", "SIZE"],
            "Descripción": ["ID Único", "Nombre Completo", "País de Origen", "Estatus Cuenta", "Puesto", "Última Conexión", "Espacio en Disco"]
        }))

# =================================================================
# 7. TERMINAL AUDITOR (MODO CONSOLA)
# =================================================================
elif nav_path == "📟 Terminal Auditor":
    st.title("📟 Terminal de Auditoría de Servidor")
    st.markdown('<div style="background-color:black; color:#00FF00; padding:20px; font-family:monospace; border-radius:5px; border: 1px solid #333;">', unsafe_allow_html=True)
    for line in st.session_state.terminal_output[-8:]:
        st.write(f"> {line}")
    st.markdown('</div>', unsafe_allow_html=True)
    
    cmd = st.text_input("Admin Command:", key="terminal_cmd")
    
    if st.button("Send Command"):
        cmd_up = cmd.upper()
        if cmd_up == "HELP":
            res = "Available commands: WHOAMI, SHOW TABLES, STATUS, CLEAR, GET XP"
        elif cmd_up == "WHOAMI":
            res = f"USER: Carlos_Giron_DBA | ACCESS_LEVEL: Admin"
        elif cmd_up == "SHOW TABLES":
            res = "Tables: [Usuarios], [Logs], [Config], [Achievments]"
        elif cmd_up == "STATUS":
            res = f"Server Uptime: 99.9% | Active Records: {len(df_sql)} | Health: Good"
        elif cmd_up == "CLEAR":
            st.session_state.terminal_output = ["Console cleared."]
            st.rerun()
        else:
            res = f"Command '{cmd}' not recognized."
        
        st.session_state.terminal_output.append(f"{cmd}")
        st.session_state.terminal_output.append(res)
        add_log(f"Terminal Command: {cmd}")
        st.rerun()

# =================================================================
# 8. PERFORMANCE & PROGRESS
# =================================================================
elif nav_path == "📊 Performance":
    st.title("📊 DBA Performance Analytics")
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Puntos Totales", f"{st.session_state.puntos} XP")
    m2.metric("Estado de Conexión", "Estable", delta="100%")
    m3.metric("Tablas Auditadas", "1/1")

    st.write("### Crecimiento de Conocimiento")
    chart_data = pd.DataFrame({
        'Día': ['Lun', 'Mar', 'Mie', 'Jue', 'Vie', 'Hoy'],
        'Nivel': [10, 25, 45, 70, 90, st.session_state.puntos]
    })
    st.area_chart(chart_data, x='Día', y='Nivel')
    
    if st.session_state.puntos > 200:
        st.success("🏆 NIVEL ELITE ALCANZADO")

# =================================================================
# FIN DEL CÓDIGO (Línea 415 aproximadamente)
# =================================================================