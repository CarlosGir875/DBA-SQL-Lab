import streamlit as st
import pandas as pd
import random
import sqlite3
import requests

# --- 1. INTENTO DE CARGAR LIBRERÍAS EXTERNAS CON SEGURIDAD ---
try:
    from streamlit_lottie import st_lottie
    LOTTIE_AVAILABLE = True
except ImportError:
    LOTTIE_AVAILABLE = False
    # No detenemos la app, solo desactivamos animaciones

# --- 2. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="App Intecap (Modo Seguro)", page_icon="🛡️", layout="wide")

st.title("🛡️ Modo de Diagnóstico")

# --- 3. INTENTO DE CARGAR TU ARCHIVO DE PREGUNTAS ---
STATUS_PREGUNTAS = "Desconocido"
MSG_ERROR = ""
MIS_TEMAS = {}

try:
    import preguntas
    import importlib
    importlib.reload(preguntas) # Recargar por si hiciste cambios
    
    if hasattr(preguntas, 'temas'):
        MIS_TEMAS = preguntas.temas
        STATUS_PREGUNTAS = "OK"
    else:
        STATUS_PREGUNTAS = "Estructura Incorrecta"
        MSG_ERROR = "El archivo carga, pero no tiene la variable 'temas'."

except ImportError:
    STATUS_PREGUNTAS = "No Encontrado"
    MSG_ERROR = "No encuentro 'preguntas.py'. ¿Está en la misma carpeta que main.py?"
except SyntaxError as e:
    STATUS_PREGUNTAS = "Error de Escritura"
    MSG_ERROR = f"Hay un error de sintaxis en preguntas.py (línea {e.lineno}): {e.msg}"
except Exception as e:
    STATUS_PREGUNTAS = "Error Crítico"
    MSG_ERROR = f"Error desconocido: {e}"

# --- 4. MOSTRAR ESTADO DEL SISTEMA ---
if STATUS_PREGUNTAS == "OK":
    st.success("✅ Archivo 'preguntas.py' cargado correctamente.")
    if not LOTTIE_AVAILABLE:
        st.warning("⚠️ La librería de animaciones no está instalada, pero la app funcionará sin ellas.")
else:
    st.error(f"❌ PROBLEMA DETECTADO: {STATUS_PREGUNTAS}")
    st.error(f"Detalle: {MSG_ERROR}")
    st.info("💡 Mientras arreglas el archivo, la app usará datos de prueba para que puedas trabajar.")
    
    # DATOS DE RESPALDO (Para que la app no se quede vacía)
    MIS_TEMAS = {
        "Verbos de Prueba": [{
            "1. Básico": [{"pregunta": "Prueba", "opciones": ["A", "B"], "correcta": "A", "explicacion": "Test"}]
        }],
        "SQL (PREGUNTAS)": [{
            "1. Básico": ["Pregunta SQL de prueba"]
        }]
    }

st.divider()

# --- 5. APLICACIÓN PRINCIPAL (CÓDIGO ROBUSTO) ---

# Generador de Base de Datos
if 'db_trabajadores' not in st.session_state:
    data = []
    for i in range(300):
        data.append([i, f"Empleado{i}", "Apellido", "555-5555", "correo@test.com", "Admin", 5000])
    st.session_state.db_trabajadores = pd.DataFrame(data, columns=["ID", "NOMBRE", "APELLIDO", "NUMERO", "CORREO", "CARGO", "SUELDO"])

# Barra Lateral
with st.sidebar:
    st.header("Menú")
    # Detectamos si hay preguntas de SQL
    tiene_sql = any("SQL" in k.upper() for k in MIS_TEMAS.keys())
    opciones = ["Inglés"]
    if tiene_sql:
        opciones.append("SQL")
    
    navegacion = st.radio("Ir a:", opciones)

# Sección Inglés
if navegacion == "Inglés":
    temas_ingles = [k for k in MIS_TEMAS.keys() if "SQL" not in k.upper()]
    tema = st.selectbox("Selecciona Tema:", temas_ingles)
    
    if tema and len(MIS_TEMAS[tema]) > 0:
        datos = MIS_TEMAS[tema][0] # Accedemos al primer elemento de la lista
        if isinstance(datos, dict):
            nivel = st.selectbox("Nivel:", list(datos.keys()))
            preguntas_nivel = datos[nivel]
            
            for i, p in enumerate(preguntas_nivel):
                st.subheader(f"P{i+1}: {p.get('pregunta', 'Sin pregunta')}")
                opts = p.get('opciones', [])
                sel = st.radio("Respuesta:", opts, key=f"{tema}_{i}")
                if st.button("Revisar", key=f"btn_{tema}_{i}"):
                    if sel == p.get('correcta'):
                        st.success("Correcto")
                    else:
                        st.error("Incorrecto")

# Sección SQL
elif navegacion == "SQL":
    st.header("Laboratorio SQL")
    
    # Animación segura
    if LOTTIE_AVAILABLE:
        try:
            r = requests.get("https://assets2.lottiefiles.com/private_files/lf30_w1uxkbue.json")
            if r.status_code == 200:
                st_lottie(r.json(), height=150)
        except:
            pass

    tab1, tab2 = st.tabs(["Teoría", "Práctica"])
    
    with tab1:
        # Busca cualquier llave que diga SQL
        key_sql = next((k for k in MIS_TEMAS.keys() if "SQL" in k.upper()), None)
        if key_sql:
            datos_sql = MIS_TEMAS[key_sql][0]
            nivel = st.selectbox("Nivel SQL:", list(datos_sql.keys()))
            lista = datos_sql[nivel]
            for item in lista:
                # Maneja si es string o diccionario
                texto = item['pregunta'] if isinstance(item, dict) else item
                st.info(texto)
                
    with tab2:
        query = st.text_area("Query:", "SELECT * FROM TRABAJADORES LIMIT 5")
        if st.button("Ejecutar"):
            conn = sqlite3.connect(':memory:')
            st.session_state.db_trabajadores.to_sql('TRABAJADORES', conn, index=False, if_exists='replace')
            try:
                res = pd.read_sql_query(query, conn)
                st.dataframe(res)
            except Exception as e:
                st.error(f"Error SQL: {e}")