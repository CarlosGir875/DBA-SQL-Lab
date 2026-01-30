import streamlit as st
import random
import pandas as pd
import time
from preguntas import temas 

# =================================================================
# 1. CONFIGURACIÓN DE PÁGINA Y UI (DARK PREMIUM & REFLECTORS)
# =================================================================
st.set_page_config(page_title="DBA English & SQL Lab", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    /* Fondo General Dark Mate */
    .stApp { background-color: #0F1116; color: #E0E0E0; }
    
    /* Bloqueo de selección para evitar copiar respuestas */
    * { user-select: none !important; -webkit-user-select: none; caret-color: transparent !important; }
    
    /* Sidebar Estilo Consola con degradado sutil */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #161920 0%, #0E1117 100%);
        border-right: 1px solid #2D333B;
    }
    
    /* Inputs y Textareas con cursor activo */
    [data-testid="stSidebar"] input[type="text"], textarea { 
        user-select: text !important; caret-color: #00FFAA !important; cursor: text !important; 
    }

    /* Alertas Estilo Glassmorphism con borde "Reflector" */
    .stAlert { 
        border-radius: 12px; 
        border: 1px solid #30363D; 
        background-color: rgba(22, 25, 32, 0.8);
        transition: 0.5s;
    }
    .stAlert:hover { border-color: #00FFAA; box-shadow: 0 0 20px rgba(0, 255, 170, 0.2); }

    /* Títulos con brillo estratégico */
    h1, h2 { 
        color: #FFFFFF; 
        text-shadow: 0 0 5px rgba(255,255,255,0.1);
        font-family: 'Inter', sans-serif;
    }
    
    /* Progress Bar Neón */
    .stProgress > div > div > div > div { 
        background-image: linear-gradient(to right, #00FFAA, #00D4FF); 
        box-shadow: 0 0 10px rgba(0, 255, 170, 0.5);
    }

    /* Botones con efecto Reflector al Hover */
    .stButton>button {
        border-radius: 6px;
        transition: all 0.3s ease;
        border: 1px solid #30363D;
        background-color: #161920;
        color: #C9D1D9;
        font-weight: 600;
        width: 100%;
    }
    .stButton>button:hover {
        border-color: #00FFAA;
        color: #00FFAA;
        box-shadow: 0 0 15px rgba(0, 255, 170, 0.3);
        transform: translateY(-2px);
    }

    /* Consola de logs (Nueva decoración) */
    .log-container {
        background-color: #010409;
        border: 1px solid #30363D;
        padding: 10px;
        border-radius: 5px;
        font-family: 'Courier New', monospace;
        color: #8B949E;
        font-size: 0.8rem;
    }
    </style>
    """, unsafe_allow_html=True)

# =================================================================
# 2. BASE DE DATOS SIMULADA (CARGA_DB)
# =================================================================
@st.cache_data
def cargar_base_datos():
    return pd.DataFrame({
        'ID': range(1, 301),
        'Nombre': ["Carlos Giron", "Juan Perez", "Maria Lopez", "Ana Garcia", "Luis Martinez", "Elena Rodriguez", "Diego Sosa", "Carmen Ruiz", "Pablo Duarte", "Lucia Mendez"] * 30,
        'Pais': ['Guatemala', 'Mexico', 'USA', 'España', 'El Salvador', 'Honduras'] * 50,
        'Estado': ['Activo', 'Inactivo', 'Pendiente'] * 100,
        'Rol': ['DBA', 'Dev', 'Analista', 'Soporte', 'Manager'] * 60
    })

df_sql = cargar_base_datos()

# =================================================================
# 3. GESTIÓN DE ESTADO (SESSION_STATE)
# =================================================================
if 'indice' not in st.session_state: st.session_state.indice = 0
if 'vidas' not in st.session_state: st.session_state.vidas = 3
if 'id_final' not in st.session_state: st.session_state.id_final = ""
if 'lista_mezclada' not in st.session_state: st.session_state.lista_mezclada = []
if 'puntos' not in st.session_state: st.session_state.puntos = 0
if 'logros' not in st.session_state: st.session_state.logros = []
if 'logs' not in st.session_state: st.session_state.logs = [f"[{time.strftime('%H:%M:%S')}] System Initialized..."]

def add_log(msg):
    st.session_state.logs.append(f"[{time.strftime('%H:%M:%S')}] {msg}")
    if len(st.session_state.logs) > 5: st.session_state.logs.pop(0)

# =================================================================
# 4. BARRA LATERAL (MENU_LATERAL)
# =================================================================
st.sidebar.title("⚡ DBA CONTROL PANEL")

orden_prioritario = ["Verbo To Be - Presente/Pasado", "SQL Questions", "Presente Continuo"]
todas_las_llaves = list(temas.keys())
opciones_menu = ["🏠 Inicio"] + [t for t in orden_prioritario if t in todas_las_llaves]
for t in todas_las_llaves:
    if t not in opciones_menu: opciones_menu.append(t)

seleccion = st.sidebar.selectbox("📂 Módulo de aprendizaje:", opciones_menu)

def obtener_rango(xp):
    if xp < 50: return "Novato (Trainee)"
    if xp < 150: return "Junior DBA"
    if xp < 300: return "Senior DBA"
    return "SQL Master Elite"

# =================================================================
# 5. MOTOR DE CARGA (LOADER_LOGIC) - ¡BUSCADOR ANTIFALLOS!
# =================================================================
if seleccion != "🏠 Inicio":
    nivel_sel = st.sidebar.radio("🎯 Selecciona Nivel:", ["1. Básico", "2. Intermedio", "3. Avanzado"])
    
    contenido = temas.get(seleccion, [])
    lista_preguntas_final = []
    id_unico_actual = f"{seleccion}_{nivel_sel}"

    # Escaneo robusto
    if isinstance(contenido, list):
        for bloque in contenido:
            if isinstance(bloque, dict):
                for llave in bloque.keys():
                    if nivel_sel.split(". ")[-1] in llave or llave in nivel_sel:
                        lista_preguntas_final = bloque[llave]
                        break
    
    # Reset si cambia el módulo/nivel
    if st.session_state.id_final != id_unico_actual:
        if lista_preguntas_final:
            st.session_state.lista_mezclada = random.sample(lista_preguntas_final, len(lista_preguntas_final))
            st.session_state.id_final = id_unico_actual
            st.session_state.indice = 0
            st.session_state.vidas = 3
            add_log(f"Module {seleccion} loaded successfully.")
        else:
            st.session_state.lista_mezclada = []
            st.session_state.id_final = id_unico_actual
            add_log(f"Warning: Level {nivel_sel} is empty.")

st.sidebar.divider()
seccion_ir = st.sidebar.radio("🧭 Navegación:", ["📚 Modo Examen", "🗄️ SQL Studio Pro", "📊 Mi Progreso"])

# Nueva decoración: Consola de Logs en el Sidebar
st.sidebar.markdown("### 🖥️ System Logs")
log_html = "".join([f"<div>{l}</div>" for l in st.session_state.logs])
st.sidebar.markdown(f'<div class="log-container">{log_html}</div>', unsafe_allow_html=True)

# =================================================================
# 6. SECCIÓN: MODO EXAMEN (QUIZ_ENGINE)
# =================================================================
if seccion_ir == "📚 Modo Examen":
    if seleccion == "🏠 Inicio":
        st.title("🚀 DBA English & SQL Lab")
        st.markdown("---")
        st.info("Selecciona un módulo en el menú lateral para desplegar los datos.")
        st.image("https://streamlit.io/images/brand/streamlit-logo-secondary-colormark-darktext.png", width=200)
    else:
        st.title(f"📖 {seleccion}")
        
        # Dashboard HUD
        col_vidas, col_puntos, col_reset = st.columns([1,1,1])
        col_vidas.markdown(f"### Vidas: {'❤️' * st.session_state.vidas}")
        col_puntos.markdown(f"### XP: {st.session_state.puntos} ⭐")
        with col_reset:
            if st.button("🔄 Reiniciar Módulo"):
                st.session_state.indice = 0
                st.session_state.vidas = 3
                add_log("Module manual reset.")
                st.rerun()

        if not st.session_state.lista_mezclada:
            st.warning("⚠️ No se encontraron registros para esta configuración.")
        
        elif st.session_state.indice < len(st.session_state.lista_mezclada):
            pregunta_obj = st.session_state.lista_mezclada[st.session_state.indice]
            st.progress((st.session_state.indice + 1) / len(st.session_state.lista_mezclada))
            st.caption(f"Registro {st.session_state.indice + 1} de {len(st.session_state.lista_mezclada)}")

            # Caso A: Preguntas con Opciones (Básico / Intermedio)
            if isinstance(pregunta_obj, dict) and 'pregunta' in pregunta_obj:
                st.info(f"#### {pregunta_obj['pregunta']}")
                
                with st.form(key=f"form_{st.session_state.indice}_{seleccion}"):
                    opc = st.radio("Sintaxis recomendada:", pregunta_obj['opciones'])
                    btn_validar = st.form_submit_button("EJECUTAR VALIDACIÓN ⚡")
                    
                    if btn_validar:
                        if opc == pregunta_obj['correcta']:
                            st.success(f"✅ SUCCESS: {pregunta_obj['explicacion']}")
                            st.session_state.puntos += 10
                            add_log("Query Success +10XP")
                        else:
                            st.error(f"❌ SYNTAX ERROR: La respuesta era {pregunta_obj['correcta']}")
                            st.session_state.vidas -= 1
                            add_log("Query Failed -1 Life")
                        st.markdown(f"**Traducción:** {pregunta_obj['traduccion']}")

                if st.button("Siguiente Registro ➡️"):
                    if st.session_state.vidas > 0:
                        st.session_state.indice += 1
                        st.rerun()
                    else:
                        st.error("🚨 CRITICAL ERROR: Database connection lost (0 Vidas).")
                        time.sleep(2)
                        st.session_state.indice = 0
                        st.session_state.vidas = 3
                        st.rerun()

            # Caso B: Retos de Escritura (Avanzado SQL)
            else:
                st.warning("📝 SQL SCRIPTING CHALLENGE (AVANZADO)")
                st.code(pregunta_obj, language="sql")
                st.text_area("Input Console:", placeholder="Escribe tu código aquí...", key=f"sql_{st.session_state.indice}")
                
                c_btn1, c_btn2 = st.columns(2)
                with c_btn1:
                    if st.button("Commit Changes ➡️"):
                        st.session_state.indice += 1
                        st.session_state.puntos += 15
                        add_log("Commit successful.")
                        st.rerun()
                with c_btn2:
                    if st.button("🆘 Get Hint"):
                        st.toast("Verifica el uso de WHERE o GROUP BY.", icon="💡")

        else:
            st.balloons()
            st.success("🎊 MÓDULO COMPLETADO: Integridad de datos al 100%.")
            if st.button("Volver al Inicio"):
                st.session_state.indice = 0
                st.rerun()

# =================================================================
# 7. SECCIÓN: SQL STUDIO PRO
# =================================================================
elif seccion_ir == "🗄️ SQL Studio Pro":
    st.title("🖥️ SQL Management Studio")
    st.markdown("Ejecuta consultas sobre la tabla `Usuarios`.")
    
    q_input = st.text_area("SQL Editor:", height=150, placeholder="SELECT * FROM Usuarios...")
    
    if st.button("RUN QUERY ▶️", type="primary"):
        st.toast("Query executed successfully.")
        st.dataframe(df_sql, use_container_width=True)
        add_log("Custom query executed.")
    
    st.divider()
    st.markdown("### 📋 Esquema de Tabla: `Usuarios`")
    st.table(pd.DataFrame({
        "Columna": ["ID", "Nombre", "Pais", "Estado", "Rol"],
        "Tipo": ["INT", "VARCHAR", "VARCHAR", "VARCHAR", "VARCHAR"]
    }))

# =================================================================
# 8. SECCIÓN: MI PROGRESO
# =================================================================
elif seccion_ir == "📊 Mi Progreso":
    st.title("📈 Database Performance")
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Puntos Acumulados", f"{st.session_state.puntos} XP")
    m2.metric("Rango DBA", obtener_rango(st.session_state.puntos))
    m3.metric("Uptime (Vidas)", f"{st.session_state.vidas}/3")

    st.write("### Historial de Crecimiento")
    dummy_data = pd.DataFrame({"Módulos": [1, 2, 3, 4, 5], "Progreso": [10, 30, 45, 80, st.session_state.puntos]})
    st.area_chart(dummy_data, x="Módulos", y="Progreso")

    if st.session_state.puntos >= 100 and "First 100" not in st.session_state.logros:
        st.session_state.logros.append("First 100")
        st.success("🏆 LOGRO DESBLOQUEADO: Centurión de Datos (100 XP)")

# =================================================================
# FIN DEL CÓDIGO (Líneas totales: 300+)
# =================================================================