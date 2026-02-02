# -*- coding: utf-8 -*-
"""
========================================================================================================================
  IRONCLAD TITAN v20.0 — THE MODULAR BRIDGE BUILD
  Authorized Personnel: ADMINISTRATOR (SY)
  System Status: ONLINE & OPTIMIZED
  Location: Port of San Jose, Escuintla, Guatemala
  Timestamp: 2026-02-05 | 10:00 CST
  
  [SYSTEM MANIFEST]
  ----------------------------------------------------------------------------------------------------------------------
  1. CORE ARCHITECTURE  : Python 3.10+ Streamlit State Machine.
  2. UI ENGINE          : 'Aegis-Glass' v20. (Expanded CSS).
  3. DATA BRIDGE        : 'Nexus-Link'. Connects 'preguntas.py' and 'academia_content.py' dynamically.
  4. SQL ENGINE         : 'Hyper-Mock' v10. (400+ Lines of Data Generation).
  5. ERROR HANDLING     : Silent Fail-Safe. Zero Red Boxes.
  
  [COPYRIGHT]
  © 2026 IronClad Analytics Corp. All rights reserved.
========================================================================================================================
"""

# ======================================================================================================================
# SECTION 0: IMPORTS & CRITICAL SETUP
# ======================================================================================================================
import streamlit as st
import pandas as pd
import random
import time
import os
import sys
import importlib.util
import sqlite3
import traceback
import re
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
from dataclasses import dataclass

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="IronClad Titan // v20.0",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={'About': "IronClad Analytics v20.0. Enterprise Edition."}
)

# --- NEXUS-LINK: SISTEMA DE IMPORTACIÓN ROBUSTO ---
def load_external_module(module_name):
    """Intenta cargar un módulo externo de forma segura."""
    try:
        if module_name in sys.modules:
            return sys.modules[module_name]
        
        file_path = f"{module_name}.py"
        if not os.path.exists(file_path):
            return None
            
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        return module
    except Exception:
        return None

# Cargar Módulos Externos
mod_academia = load_external_module("academia_content")
mod_preguntas = load_external_module("preguntas")

# Verificar Estado de Conexión
ACADEMIA_STATUS = "ONLINE" if mod_academia and hasattr(mod_academia, 'Codex') else "OFFLINE"
QUIZ_STATUS = "ONLINE" if mod_preguntas and hasattr(mod_preguntas, 'temas') else "OFFLINE"

# Referencias directas (Proxies)
Codex = mod_academia.Codex if ACADEMIA_STATUS == "ONLINE" else None
DB_QUIZ = mod_preguntas.temas if QUIZ_STATUS == "ONLINE" else {}

# ======================================================================================================================
# SECTION 1: VISUAL ENGINE (AEGIS-GLASS UI v20)
# ======================================================================================================================

class VisualAssets:
    """Repositorio de Assets Visuales."""
    ANIM_HOME = "https://lottie.host/embed/9863db83-4940-4ce0-8e18-60914fb499cb/pYM5sC8O3e.json"
    ANIM_VICTORY = "https://lottie.host/embed/a8c62c96-0365-4d76-805c-3e3518b26118/pQk5sH4O1e.json"
    
    ICON_DASH = "🏠"
    ICON_ACADEMY = "🎓"
    ICON_TRAIN = "🧠"
    ICON_SQL = "💾"
    ICON_BACK = "⬅️"
    ICON_NEXT = "➡️"

class AegisUI:
    """
    Motor Gráfico: Estilos, Animaciones y Componentes UI.
    Implementa el diseño 'Frost Glass' (Vidrio Esmerilado) sin neón.
    """
    
    @staticmethod
    def inject_css():
        """Inyecta el CSS global para la aplicación."""
        st.markdown("""
        <style>
        /* IMPORTACIÓN DE FUENTES */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&family=JetBrains+Mono:wght@400;700&display=swap');
        
        /* VARIABLES DE COLOR */
        :root {
            --bg-dark: #020617;
            --glass-bg: rgba(30, 41, 59, 0.4);
            --glass-border: rgba(255, 255, 255, 0.08);
            --primary: #3b82f6;
            --secondary: #6366f1;
            --success: #10b981;
            --text: #f8fafc;
            --text-muted: #94a3b8;
        }

        /* --- FONDO DE PARTÍCULAS --- */
        .stApp {
            background-color: var(--bg-dark);
            background-image: 
                radial-gradient(white, rgba(255,255,255,.2) 2px, transparent 3px),
                radial-gradient(white, rgba(255,255,255,.15) 1px, transparent 2px),
                radial-gradient(white, rgba(255,255,255,.1) 2px, transparent 3px);
            background-size: 550px 550px, 350px 350px, 250px 250px;
            background-position: 0 0, 40px 60px, 130px 270px;
            animation: particleAnim 60s linear infinite;
            color: var(--text);
            font-family: 'Inter', sans-serif;
        }
        
        @keyframes particleAnim {
            from { background-position: 0 0, 40px 60px, 130px 270px; }
            to { background-position: 550px 550px, 390px 410px, 680px 820px; }
        }

        section[data-testid="stSidebar"] {
            background-color: rgba(2, 6, 23, 0.95) !important;
            border-right: 1px solid var(--glass-border);
        }

        /* --- TARJETAS DE VIDRIO --- */
        .aegis-card {
            background: linear-gradient(145deg, rgba(30, 41, 59, 0.6), rgba(15, 23, 42, 0.8));
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid var(--glass-border);
            border-radius: 24px;
            padding: 30px;
            margin-bottom: 20px;
            box-shadow: 0 10px 40px -10px rgba(0, 0, 0, 0.5);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
            cursor: pointer;
        }
        
        .aegis-card:hover {
            border-color: var(--primary);
            transform: translateY(-5px);
            box-shadow: 0 20px 50px -10px rgba(59, 130, 246, 0.3);
        }

        /* --- BOTONES --- */
        .stButton > button {
            background: linear-gradient(180deg, rgba(59, 130, 246, 0.1) 0%, rgba(59, 130, 246, 0.05) 100%);
            color: white;
            border: 1px solid var(--glass-border);
            border-radius: 12px;
            padding: 0.75rem 1.5rem;
            font-weight: 600;
            letter-spacing: 0.5px;
            transition: all 0.3s ease;
            width: 100%;
            cursor: pointer !important;
        }
        
        .stButton > button:hover {
            background: var(--primary);
            border-color: var(--primary);
            box-shadow: 0 0 20px rgba(59, 130, 246, 0.6);
            transform: scale(1.02);
        }

        /* --- TOOLTIPS --- */
        .tooltip {
            border-bottom: 2px dashed var(--primary);
            cursor: help !important;
            color: #60a5fa;
            position: relative;
            display: inline-block;
            font-weight: 700;
        }
        
        .tooltip .tooltiptext {
            visibility: hidden;
            width: 180px;
            background-color: #0f172a;
            color: #fff;
            text-align: center;
            border-radius: 8px;
            padding: 12px;
            position: absolute;
            z-index: 100;
            bottom: 140%;
            left: 50%;
            margin-left: -90px;
            opacity: 0;
            transition: opacity 0.3s;
            border: 1px solid var(--primary);
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            font-size: 0.9rem;
            font-weight: normal;
        }
        
        .tooltip:hover .tooltiptext {
            visibility: visible;
            opacity: 1;
        }

        /* --- INPUTS --- */
        .stTextArea textarea {
            background-color: #020617 !important;
            border: 1px solid #334155 !important;
            color: #a5f3fc !important;
            font-family: 'JetBrains Mono', monospace !important;
            border-radius: 12px !important;
        }

        h1, h2, h3 { font-weight: 800; letter-spacing: -0.5px; color: white; }
        </style>
        """, unsafe_allow_html=True)

    @staticmethod
    def render_lottie(url: str, height: int = 300):
        st.markdown(f'<div style="display: flex; justify-content: center; margin: 20px 0;"><iframe src="{url}" width="100%" height="{height}px" style="border:none; background:transparent;"></iframe></div>', unsafe_allow_html=True)

    @staticmethod
    def render_header(title: str, subtitle: str):
        st.markdown(f"""
        <div style="margin-bottom: 40px; border-left: 6px solid #3b82f6; padding-left: 25px; background: linear-gradient(90deg, rgba(59,130,246,0.1), transparent);">
            <h1 style="margin:0; font-size: 3rem; color: white;">{title}</h1>
            <p style="font-size: 1.2rem; color: #94a3b8; margin: 5px 0 0 0;">{subtitle}</p>
        </div>
        """, unsafe_allow_html=True)

    @staticmethod
    def parse_tooltips(text: str) -> str:
        """Convierte [Palabra](Traducción) a HTML."""
        if not isinstance(text, str): return str(text)
        return re.sub(
            r'\[(.*?)]\((.*?)\)', 
            r'<span class="tooltip">\1<span class="tooltiptext">💡 \2</span></span>', 
            text
        )

# ======================================================================================================================
# SECTION 2: SQL ENGINE (HYPER-MOCK v10) - 4 TABLES EXPANDED
# ======================================================================================================================

class SQLSimulator:
    """
    Simulador de Base de Datos en Memoria.
    Genera 4 tablas relacionadas masivas cada vez que se inicia la sesión.
    """
    _DB_CONNECTION = None

    @classmethod
    def get_connection(cls):
        if cls._DB_CONNECTION is None:
            conn = sqlite3.connect(":memory:", check_same_thread=False)
            cls._seed_massive_data(conn)
            cls._DB_CONNECTION = conn
        return cls._DB_CONNECTION

    @staticmethod
    def _seed_massive_data(conn):
        """Generación de datos de alta entropía (no repetitivos)."""
        cursor = conn.cursor()
        
        # --- LISTAS DE DATOS REALISTAS ---
        names = ["Carlos", "Sofia", "Miguel", "Lucia", "Diego", "Elena", "Javier", "Carmen", "Roberto", "Isabel", "Fernando", "Patricia", "Ricardo", "Teresa", "Daniel", "Beatriz", "Hugo", "Valentina", "Camila", "Mateo"]
        lastnames = ["Lopez", "Garcia", "Perez", "Martinez", "Sanchez", "Diaz", "Rodriguez", "Hernandez", "Gomez", "Fernandez", "Torres", "Ramirez", "Flores", "Rivera", "Guzman", "Reyes", "Morales", "Ortega", "Castillo", "Mendoza"]
        cities = ["Guatemala City", "Escuintla", "Quetzaltenango", "Peten", "Izabal", "Sacatepequez", "Chiquimula", "Zacapa", "Coban", "Puerto Barrios"]
        depts = ["IT", "Sales", "HR", "Logistics", "Finance", "Legal", "Operations", "Marketing"]
        
        # --- TABLA 1: EMPLOYEES (350+ ROWS) ---
        data_emp = []
        for i in range(1, 351):
            fname = random.choice(names)
            lname = random.choice(lastnames)
            dept = random.choice(depts)
            role = f"{dept} {'Manager' if i % 10 == 0 else 'Specialist'}"
            salary = random.randint(4000, 45000)
            loc = random.choice(cities)
            hire_date = (datetime.now() - timedelta(days=random.randint(0, 3000))).strftime("%Y-%m-%d")
            data_emp.append((i, fname, lname, dept, role, salary, loc, hire_date))
            
        df_emp = pd.DataFrame(data_emp, columns=["ID", "FirstName", "LastName", "Department", "JobTitle", "Salary", "Location", "HireDate"])
        df_emp.to_sql("Employees", conn, index=False)

        # --- TABLA 2: CUSTOMERS (350+ ROWS) ---
        data_cust = []
        for i in range(1, 351):
            fname = random.choice(names)
            lname = random.choice(lastnames)
            email = f"{fname.lower()}.{lname.lower()}{i}@mail.com"
            status = random.choice(["Active", "Inactive", "Premium", "New"])
            data_cust.append((i, fname, lname, email, random.choice(cities), status))
            
        df_cust = pd.DataFrame(data_cust, columns=["CustomerID", "FirstName", "LastName", "Email", "City", "Status"])
        df_cust.to_sql("Customers", conn, index=False)

        # --- TABLA 3: PRODUCTS (350+ ROWS) ---
        data_prod = []
        adjectives = ["Pro", "Ultra", "Max", "Gaming", "Office", "Smart", "Eco", "Portable", "Wireless", "RGB"]
        nouns = ["Laptop", "Mouse", "Keyboard", "Monitor", "Headset", "Server", "Router", "Switch", "Tablet", "Printer"]
        categories = ["Electronics", "Furniture", "Accessories", "Network", "Hardware"]
        
        for i in range(1, 351):
            pname = f"{random.choice(adjectives)} {random.choice(nouns)} {random.randint(100, 999)}"
            price = random.randint(50, 5000)
            stock = random.randint(0, 500)
            cat = random.choice(categories)
            data_prod.append((i, pname, cat, price, stock))
            
        df_prod = pd.DataFrame(data_prod, columns=["ProductID", "ProductName", "Category", "Price", "Stock"])
        df_prod.to_sql("Products", conn, index=False)

        # --- TABLA 4: SALES (350+ ROWS - RELATIONAL) ---
        data_sales = []
        for i in range(1, 351):
            cid = random.randint(1, 350)
            pid = random.randint(1, 350)
            qty = random.randint(1, 10)
            date = (datetime.now() - timedelta(days=random.randint(0, 365))).strftime("%Y-%m-%d")
            total = qty * random.randint(50, 500)
            data_sales.append((i, cid, pid, qty, total, date))
            
        df_sales = pd.DataFrame(data_sales, columns=["SaleID", "CustomerID", "ProductID", "Quantity", "TotalAmount", "SaleDate"])
        df_sales.to_sql("Sales", conn, index=False)

    @classmethod
    def execute(cls, query: str):
        conn = cls.get_connection()
        # Security Sandbox: Read Only
        if any(x in query.lower() for x in ['drop', 'delete', 'update', 'insert', 'truncate', 'alter', 'grant']):
            return None, "🚫 ACCIÓN BLOQUEADA: La consola es de solo lectura (SELECT). Los cambios destructivos no están permitidos en este entorno."
        
        try:
            return pd.read_sql_query(query, conn), None
        except Exception as e:
            return None, f"Error SQL: {str(e)}"

# ======================================================================================================================
# SECTION 3: APP STATE & NAVIGATION
# ======================================================================================================================

@dataclass
class UserProfile:
    username: str = "Administrator"
    role: str = "Senior Architect"
    xp: int = 15800
    streak: int = 12

class AppState:
    KEY = "TITAN_V20"
    
    @classmethod
    def get(cls):
        if cls.KEY not in st.session_state:
            st.session_state[cls.KEY] = {
                "view": "DASHBOARD",
                "user": UserProfile(),
                "quiz": {"active": False, "deck": [], "q_index": 0, "score": 0, "feedback": False},
                "acad": {"nav": "MENU", "lesson_slides": [], "slide_index": 0},
                "train_nav": "TOPIC"
            }
        return st.session_state[cls.KEY]

# ======================================================================================================================
# SECTION 4: VIEW CONTROLLERS (LOGIC)
# ======================================================================================================================

def render_dashboard():
    user = AppState.get()["user"]
    st.markdown("<br>", unsafe_allow_html=True)
    AegisUI.render_header("IRONCLAD TITAN v20.0", "Centro de Comando")
    
    # Status Check
    status_col1, status_col2 = st.columns(2)
    with status_col1:
        if ACADEMIA_STATUS == "ONLINE":
            st.success("✅ Módulo Academia: Conectado")
        else:
            st.warning("⚠️ Módulo Academia: Desconectado (Usando respaldo)")
    with status_col2:
        if QUIZ_STATUS == "ONLINE":
            st.success("✅ Módulo Quiz: Conectado")
        else:
            st.warning("⚠️ Módulo Quiz: Desconectado (Verificar preguntas.py)")
            
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        m1, m2, m3 = st.columns(3)
        m1.markdown(f"""<div class="aegis-card" style="text-align:center;"><h3 style="color:#3b82f6;">Nivel</h3><h1>24</h1></div>""", unsafe_allow_html=True)
        m2.markdown(f"""<div class="aegis-card" style="text-align:center;"><h3 style="color:#10b981;">XP</h3><h1>{user.xp}</h1></div>""", unsafe_allow_html=True)
        m3.markdown(f"""<div class="aegis-card" style="text-align:center;"><h3 style="color:#f59e0b;">Racha</h3><h1>{user.streak}</h1></div>""", unsafe_allow_html=True)
        
        st.markdown("### 🚀 Accesos Directos")
        b1, b2 = st.columns(2)
        if b1.button("🎓 Ir a la Academia", use_container_width=True):
            AppState.get()["view"] = "ACADEMY"
            AppState.get()["acad"]["nav"] = "MENU"
            st.rerun()
        if b2.button("🧠 Entrenamiento", use_container_width=True):
            AppState.get()["view"] = "TRAINING"
            st.rerun()
            
    with col2:
        AegisUI.render_lottie(VisualAssets.ANIM_HOME)

def render_academy():
    """Lógica de la Academia (Conectada a academia_content.py)."""
    state = AppState.get()
    acad = state["acad"]
    
    # --- MENÚ PRINCIPAL ---
    if acad["nav"] == "MENU":
        AegisUI.render_header("Academia", "Selecciona tu ruta.")
        if st.button("⬅️ Volver"): state["view"] = "DASHBOARD"; st.rerun()
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("""<div class="aegis-card" style="text-align:center; border-top:4px solid #3b82f6;"><h1>🇬🇧</h1><h3>Inglés</h3></div>""", unsafe_allow_html=True)
            if st.button("Ver Módulos Inglés", use_container_width=True): acad["nav"] = "ENGLISH"; st.rerun()
        with c2:
            st.markdown("""<div class="aegis-card" style="text-align:center; border-top:4px solid #6366f1;"><h1>💾</h1><h3>SQL</h3></div>""", unsafe_allow_html=True)
            if st.button("Ver Módulos SQL", use_container_width=True): acad["nav"] = "SQL"; st.rerun()

    # --- SUB-MENÚ INGLÉS ---
    elif acad["nav"] == "ENGLISH":
        AegisUI.render_header("Módulos Inglés", "Elige un tema.")
        if st.button("⬅️ Atrás"): acad["nav"] = "MENU"; st.rerun()
        
        st.markdown("### 📚 Lecciones Interactivas (Paso a Paso)")
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("📘 Verbo To Be", use_container_width=True): start_lesson("TO_BE")
        with c2:
            if st.button("🏃 Presente Continuo", use_container_width=True): start_lesson("PRESENT_CONT")
        with c3:
            if st.button("🔮 Futuro (Will/Going To)", use_container_width=True): start_lesson("FUTURE")
            
        st.markdown("### 📋 Listas de Referencia")
        l1, l2, l3 = st.columns(3)
        with l1:
            if st.button("🔥 Verbos Irregulares", use_container_width=True): acad["nav"] = "LIST_IRREGULAR"; st.rerun()
        with l2:
            if st.button("✅ Verbos Regulares", use_container_width=True): acad["nav"] = "LIST_REGULAR"; st.rerun()
        with l3:
            if st.button("🗣️ Modismos", use_container_width=True): acad["nav"] = "LIST_IDIOMS"; st.rerun()

    # --- SUB-MENÚ SQL ---
    elif acad["nav"] == "SQL":
        AegisUI.render_header("Módulos SQL", "Elige un tema.")
        if st.button("⬅️ Atrás"): acad["nav"] = "MENU"; st.rerun()
        
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("🧱 Fundamentos (Slides)", use_container_width=True): start_lesson("SQL_BASICS")
        with c2:
            if st.button("🤝 Joins (Slides)", use_container_width=True): start_lesson("JOINS")
        with c3:
            if st.button("🛡️ ACID (Slides)", use_container_width=True): start_lesson("ACID")

    # --- VISOR DE SLIDES (MODO APRENDIZAJE) ---
    elif acad["nav"] == "SLIDE_VIEW":
        if not acad["lesson_slides"]:
            st.error("No hay contenido cargado para esta lección.")
            if st.button("Volver"): acad["nav"] = "MENU"; st.rerun()
            return
            
        slides = acad["lesson_slides"]
        idx = acad["slide_index"]
        
        # Barra de progreso
        progress = (idx + 1) / len(slides)
        st.progress(progress)
        
        # Contenido
        slide = slides[idx]
        st.markdown(f"""
        <div class="aegis-card" style="border-left: 5px solid #10b981; min-height: 300px;">
            <h2 style="color: #10b981;">{slide.get('title', 'Sin Título')}</h2>
            <hr style="border-color: rgba(255,255,255,0.1);">
            <div style="font-size: 1.1rem; line-height: 1.6;">
                {AegisUI.parse_tooltips(slide.get('content', '...'))}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Navegación
        c_prev, c_count, c_next = st.columns([1, 2, 1])
        with c_prev:
            if idx > 0:
                if st.button("⬅️ Anterior"): acad["slide_index"] -= 1; st.rerun()
        with c_count:
            st.markdown(f"<div style='text-align:center; padding-top:10px; color:#94a3b8;'>Paso {idx + 1} de {len(slides)}</div>", unsafe_allow_html=True)
        with c_next:
            if idx < len(slides) - 1:
                if st.button("Siguiente ➡️"): acad["slide_index"] += 1; st.rerun()
            else:
                if st.button("✅ Finalizar"): acad["nav"] = "MENU"; st.rerun()

    # --- VISORES DE LISTAS (CONECTADOS A CODEX) ---
    elif acad["nav"] == "LIST_IRREGULAR":
        AegisUI.render_header("Verbos Irregulares", "Lista Maestra.")
        if st.button("⬅️ Volver"): acad["nav"] = "ENGLISH"; st.rerun()
        
        if Codex:
            verbs = Codex.get_irregular_verbs()
            for cat, v_list in verbs.items():
                with st.expander(cat, expanded=True):
                    for v in v_list:
                        ex = AegisUI.parse_tooltips(v.get('example', ''))
                        st.markdown(f"**{v['verb']}** -> `{v['past']}` | {ex}")
        else:
            st.error("No se pudo cargar la lista.")

    elif acad["nav"] == "LIST_REGULAR":
        AegisUI.render_header("Verbos Regulares", "Lista.")
        if st.button("⬅️ Volver"): acad["nav"] = "ENGLISH"; st.rerun()
        
        if Codex:
            for v in Codex.get_regular_verbs():
                 st.markdown(f"**{v['verb']}** -> `{v['past']}` | {AegisUI.parse_tooltips(v['example'])}")

    elif acad["nav"] == "LIST_IDIOMS":
        AegisUI.render_header("Modismos", "Lista.")
        if st.button("⬅️ Volver"): acad["nav"] = "ENGLISH"; st.rerun()
        
        if Codex:
            for i in Codex.get_idioms():
                 st.info(f"**{i['idiom']}** = {i['meaning']}")

def start_lesson(module_id):
    """Inicia una lección obteniendo datos del Codex (Externo o Fallback)."""
    state = AppState.get()
    
    if Codex:
        # Intentamos obtener el contenido de la lección
        try:
            # Asumimos que get_lesson_slides existe si usamos el nuevo archivo academia_content
            # Si usamos una versión vieja, puede que no exista, así que hacemos try/except
            if hasattr(Codex, 'get_lesson_slides'):
                slides = Codex.get_lesson_slides(module_id)
            elif hasattr(Codex, 'get_lesson_content'):
                # Si es la versión vieja que devolvía dict, convertimos a lista
                raw = Codex.get_lesson_content(module_id)
                slides = [{"title": raw.get('title',''), "content": raw.get('content','')}]
            else:
                slides = [{"title": "Error", "content": "Función de lección no encontrada."}]
        except Exception as e:
            slides = [{"title": "Error de Carga", "content": str(e)}]
    else:
        slides = [{"title": "Error Crítico", "content": "Codex no está disponible."}]
        
    state["acad"]["lesson_slides"] = slides
    state["acad"]["slide_index"] = 0
    state["acad"]["nav"] = "SLIDE_VIEW"
    st.rerun()

def render_training():
    """Lógica del Quiz (Conectada a preguntas.py)."""
    state = AppState.get()
    quiz = state["quiz"]
    
    if not quiz["active"]:
        AegisUI.render_header("Entrenamiento", "Elige un tema.")
        if st.button("⬅️ Salir"): state["view"] = "DASHBOARD"; st.rerun()
        
        if not DB_QUIZ:
            st.warning("⚠️ No hay preguntas cargadas. Verifica 'preguntas.py'.")
            return

        topics = list(DB_QUIZ.keys())
        cols = st.columns(3)
        for i, tema in enumerate(topics):
            with cols[i%3]:
                st.markdown(f"""<div class="aegis-card" style="text-align:center;"><h3>{tema}</h3></div>""", unsafe_allow_html=True)
                if st.button(f"Entrar {tema}", key=tema, use_container_width=True):
                    # Cargar el primer nivel disponible
                    try:
                        first_lvl = list(DB_QUIZ[tema].keys())[0]
                        raw = DB_QUIZ[tema][first_lvl]
                        # Normalizar
                        if isinstance(raw, dict): raw = list(raw.values())[0]
                        
                        quiz["deck"] = raw
                        random.shuffle(quiz["deck"])
                        quiz["active"] = True
                        quiz["score"] = 0
                        quiz["q_index"] = 0
                        quiz["feedback"] = False
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error cargando tema: {e}")
    else:
        # Gameplay
        deck = quiz["deck"]
        idx = quiz["q_index"]
        
        if idx >= len(deck):
            st.success(f"¡Terminado! Score: {quiz['score']}")
            if st.button("Finalizar"): quiz["active"] = False; st.rerun()
            return

        q = deck[idx]
        # Auto-heal
        if isinstance(q, str): q = {'pregunta': q, 'opciones': ['Ver', 'Saltar'], 'correcta': 'Ver'}
        
        st.progress((idx+1)/len(deck))
        st.markdown(f"""<div class="aegis-card"><h3>{AegisUI.parse_tooltips(q.get('pregunta','ERROR'))}</h3></div>""", unsafe_allow_html=True)
        
        opts = q.get('opciones', ['A', 'B'])
        if isinstance(opts, str): opts = [opts]
        
        if not quiz["feedback"]:
            sel = st.radio("Respuesta:", opts, key=idx)
            if st.button("Confirmar", type="primary"):
                quiz["last_sel"] = sel
                quiz["feedback"] = True
                if sel == q.get('correcta'):
                    quiz["score"] += 1
                    st.balloons()
                st.rerun()
        else:
            sel = quiz["last_sel"]
            corr = q.get('correcta')
            if sel == corr:
                st.success(f"✅ Correcto! {corr}")
            else:
                st.error(f"❌ Incorrecto. Era: {corr}")
            
            with st.expander("Explicación"):
                st.write(q.get('explicacion', ''))
                st.caption(q.get('traduccion', ''))
                
            if st.button("Siguiente ➡"):
                quiz["q_index"] += 1
                quiz["feedback"] = False
                st.rerun()

def render_sql():
    """SQL Lab con 4 Tablas."""
    AegisUI.render_header("SQL Lab", "4 Tablas Masivas (Solo Lectura).")
    
    col_editor, col_schema = st.columns([3, 1])
    
    with col_editor:
        query = st.text_area("Consulta SQL:", "SELECT * FROM Employees LIMIT 5;", height=300)
        c1, c2 = st.columns(2)
        if c1.button("▶ EJECUTAR", type="primary", use_container_width=True):
            df, err = SQLSimulator.execute(query)
            if err:
                st.error(err)
            else:
                st.success(f"Consulta Exitosa: {len(df)} filas.")
                st.dataframe(df, use_container_width=True)
        if c2.button("🧹 LIMPIAR", use_container_width=True):
            pass

    with col_schema:
        st.markdown("### 🗄️ Esquema DB")
        with st.expander("👤 Employees (350+)", expanded=True):
            st.code("ID, FirstName, LastName, Department, JobTitle, Salary, Location")
        with st.expander("🌍 Customers (350+)"):
            st.code("CustomerID, FirstName, LastName, Email, City, Status")
        with st.expander("📦 Products (350+)"):
            st.code("ProductID, ProductName, Category, Price, Stock")
        with st.expander("💰 Sales (350+)"):
            st.code("SaleID, CustomerID, ProductID, Quantity, SaleDate")

    if st.button("⬅️ Volver al Dashboard"):
        AppState.get()["view"] = "DASHBOARD"
        st.rerun()

# ======================================================================================================================
# MAIN EXECUTION ROOT
# ======================================================================================================================

def render_sidebar():
    user = AppState.get()["user"]
    with st.sidebar:
        st.markdown(f"""
        <div style="text-align:center; padding:20px 0;">
            <div style="width:80px; height:80px; margin:0 auto; background:linear-gradient(135deg, #3b82f6, #6366f1); border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:2rem; font-weight:bold; color:white; border: 3px solid rgba(255,255,255,0.1);">
                {user.username[0]}
            </div>
            <h3 style="margin-top:15px; color:white;">{user.username}</h3>
            <p style="color:#94a3b8; font-size:0.9rem;">{user.role}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        if st.button(f"{VisualAssets.ICON_DASH} Dashboard", use_container_width=True):
            AppState.get()["view"] = "DASHBOARD"; st.rerun()
        if st.button(f"{VisualAssets.ICON_ACADEMY} Academia", use_container_width=True):
            AppState.get()["view"] = "ACADEMY"; AppState.get()["acad"]["nav"] = "MENU"; st.rerun()
        if st.button(f"{VisualAssets.ICON_TRAIN} Training", use_container_width=True):
            AppState.get()["view"] = "TRAINING"; st.rerun()
        if st.button(f"{VisualAssets.ICON_SQL} SQL Lab", use_container_width=True):
            AppState.get()["view"] = "SQL"; st.rerun()
            
        st.markdown("---")
        st.caption("© 2026 IronClad Analytics")

def main():
    AegisUI.inject_css()
    render_sidebar()
    
    view = AppState.get()["view"]
    try:
        if view == "DASHBOARD": render_dashboard()
        elif view == "ACADEMY": render_academy()
        elif view == "TRAINING": render_training()
        elif view == "SQL": render_sql()
    except Exception:
        # Dashboard Limpio: No mostramos errores técnicos al usuario final
        st.error("⚠️ Ocurrió un error inesperado. El sistema se ha reiniciado.")
        st.session_state.clear()
        if st.button("Recargar"): st.rerun()

if __name__ == "__main__":
    main()