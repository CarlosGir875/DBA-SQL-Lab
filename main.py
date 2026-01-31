import streamlit as st
import pandas as pd
import random
import sqlite3
import requests
from streamlit_lottie import st_lottie

# --- INTENTO DE IMPORTAR TUS PREGUNTAS CON SEGURIDAD ---
try:
    import preguntas
    # Verificamos que exista la variable 'temas'
    if not hasattr(preguntas, 'temas'):
        st.error("Error: El archivo 'preguntas.py' no tiene una variable llamada 'temas'.")
        st.stop()
except ImportError:
    st.error("⚠️ No encontré el archivo 'preguntas.py'. Asegúrate de que esté en la misma carpeta que este archivo.")
    st.stop()
except Exception as e:
    st.error(f"⚠️ Hay un error de sintaxis en tu archivo 'preguntas.py': {e}")
    st.stop()

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="App Intecap", page_icon="🚀", layout="wide")

# --- LÓGICA DE DATOS (ANTIGUO UTILS.PY) ---
def generar_datos_trabajadores(n=300):
    nombres = ["Juan", "Maria", "Carlos", "Ana", "Luis", "Sofia", "Pedro", "Lucia"]
    apellidos = ["Garcia", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Perez"]
    cargos = ["Analista", "Dev Backend", "Gerente", "Soporte", "Admin BD", "Dev Frontend"]
    data = []
    for i in range(1, n + 1):
        nombre = random.choice(nombres)
        apellido = random.choice(apellidos)
        correo = f"{nombre.lower()}.{apellido.lower()}{i}@intecap.edu.gt"
        numero = f"{random.randint(4000, 5999)}-{random.randint(1000, 9999)}"
        cargo = random.choice(cargos)
        sueldo = random.randint(3500, 12000)
        data.append([i, nombre, apellido, numero, correo, cargo, sueldo])
    return pd.DataFrame(data, columns=["ID", "NOMBRE", "APELLIDO", "NUMERO", "CORREO", "CARGO", "SUELDO"])

def ejecutar_sql(df, query):
    conn = sqlite3.connect(':memory:')
    df.to_sql('TRABAJADORES', conn, index=False, if_exists='replace')
    try:
        resultado = pd.read_sql_query(query, conn)
        return resultado, None
    except Exception as e:
        return None, str(e)
    finally:
        conn.close()

# --- ANIMACIONES ---
def load_lottieurl(url):
    try:
        r = requests.get(url)
        if r.status_code != 200: return None
        return r.json()
    except: return None

lottie_sql = load_lottieurl("https://assets2.lottiefiles.com/private_files/lf30_w1uxkbue.json")

# --- ESTADO DE LA APP ---
if 'db_trabajadores' not in st.session_state:
    st.session_state.db_trabajadores = generar_datos_trabajadores(300)

# --- BARRA LATERAL ---
with st.sidebar:
    st.title("Navegación Intecap")
    opcion = st.radio("Ir a:", ["Inicio", "Inglés", "SQL"])

# --- LÓGICA PRINCIPAL ---
if opcion == "Inicio":
    st.title("Bienvenido a tu App de Práctica 🚀")
    st.write("Selecciona una opción en el menú de la izquierda para comenzar.")

elif opcion == "Inglés":
    st.header("Práctica de Inglés")
    
    # Filtramos las llaves para que no salga la de SQL aquí
    # Buscamos cualquier llave que NO tenga "SQL" en el nombre
    temas_ingles = [k for k in preguntas.temas.keys() if "SQL" not in k.upper()]
    
    tema = st.selectbox("Elige tema:", temas_ingles)
    
    if tema:
        # Accedemos a la lista y luego al primer diccionario (estructura de tu archivo)
        datos_tema = preguntas.temas[tema][0] 
        nivel = st.selectbox("Nivel:", list(datos_tema.keys()))
        
        lista_preguntas = datos_tema[nivel]
        
        for i, p in enumerate(lista_preguntas):
            st.markdown(f"**{i+1}. {p['pregunta']}**")
            opciones = p['opciones']
            # Radio button con clave única
            resp = st.radio("Opción:", opciones, key=f"p_{tema}_{i}")
            
            if st.button(f"Revisar {i+1}", key=f"btn_{tema}_{i}"):
                if resp == p['correcta']:
                    st.success("Correcto! ✅")
                else:
                    st.error(f"Incorrecto. Era: {p['correcta']}")
                st.info(f"Explicación: {p['explicacion']}")
            st.divider()

elif opcion == "SQL":
    st.header("Laboratorio SQL Server")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.info("Tabla disponible: **TRABAJADORES** (ID, NOMBRE, APELLIDO, NUMERO, CORREO, CARGO, SUELDO)")
    with col2:
        if lottie_sql: st_lottie(lottie_sql, height=100)

    # Buscar automáticamente la llave de SQL en tu archivo
    llave_sql = next((k for k in preguntas.temas.keys() if "SQL" in k.upper()), None)

    tab1, tab2 = st.tabs(["Preguntas Teóricas", "Consola SQL"])

    with tab1:
        if llave_sql:
            datos_sql = preguntas.temas[llave_sql][0]
            nivel_sql = st.selectbox("Nivel SQL:", list(datos_sql.keys()))
            for item in datos_sql[nivel_sql]:
                # Dependiendo de si es diccionario o string en tu archivo
                if isinstance(item, dict):
                    st.write(f"❓ {item['pregunta']}")
                else:
                    st.write(f"❓ {item}")
        else:
            st.warning("No encontré una sección con 'SQL' en el nombre dentro de preguntas.py")

    with tab2:
        query = st.text_area("Escribe tu Query:", "SELECT * FROM TRABAJADORES WHERE SUELDO > 8000")
        if st.button("Ejecutar"):
            res, err = ejecutar_sql(st.session_state.db_trabajadores, query)
            if err:
                st.error(f"Error SQL: {err}")
            else:
                st.dataframe(res)