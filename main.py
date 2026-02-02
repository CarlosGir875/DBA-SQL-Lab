# -*- coding: utf-8 -*-
"""
========================================================================================================================
  IRONCLAD TITAN v18.0 — THE COLOSSUS BUILD (ULTIMATE STABILITY)
  Authorized Personnel: ADMINISTRATOR (SY)
  System Status: ONLINE
  Location: Port of San Jose, Escuintla, Guatemala
  Timestamp: 2026-02-04 | 20:00 CST
  
  [SYSTEM ARCHITECTURE & MANIFEST]
  ----------------------------------------------------------------------------------------------------------------------
  1. CORE KERNEL        : Python 3.10+ Streamlit State Machine.
  2. UI ENGINE          : 'Aegis-Glass' v18. 
                          - Deep Space Particles Background (CSS Animation).
                          - Interactive Tooltips with [Word](Translation) logic.
                          - Dynamic 'Slide' Learning Mode (Step-by-step).
  3. DATA ENGINE        : Omni-Parser v9. 
                          - Robust Import System: Detects errors in external files and switches to Internal Backup 
                            without crashing the UI.
  4. SQL ENGINE         : Hyper-Mock v8 (The Data Factory).
                          - 4 MASSIVE TABLES: Employees, Customers, Products, Sales.
                          - 300+ Rows each with high entropy (Names, Emails, Dates, Categories).
                          - Relational Integrity for COMPLEX JOINs.
  5. NAVIGATION         : Dashboard -> Academy (Slides) -> Training (Quiz) -> SQL Lab.
  
  [CHANGELOG v18.0]
  - NEW: 'Slide Learning' Mode in Academy. No more text walls. Click 'Next' to learn.
  - NEW: 4th SQL Table 'Sales' added for advanced queries.
  - FIX: Dashboard completely cleaned. No red tracebacks.
  - VISUAL: Enhanced glassmorphism and animations.
  
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
from dataclasses import dataclass
from typing import Dict, Any, List

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="IronClad Titan // v18.0",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={'About': "IronClad Analytics v18.0. Enterprise Edition."}
)

# --- SISTEMA DE IMPORTACIÓN ROBUSTA (FAIL-SAFE) ---
# Intentamos cargar los archivos externos. Si fallan, usamos contenido de respaldo.
EXTERNAL_CONTENT_LOADED = False
EXTERNAL_QUIZ_LOADED = False

try:
    from academia_content import Codex as ExternalCodex
    EXTERNAL_CONTENT_LOADED = True
except ImportError:
    pass
except SyntaxError:
    pass

try:
    from preguntas import temas as ExternalQuiz
    EXTERNAL_QUIZ_LOADED = True
except ImportError:
    pass
except SyntaxError:
    pass

# ======================================================================================================================
# SECTION 1: VISUAL ENGINE (AEGIS-GLASS UI v18)
# ======================================================================================================================

class VisualAssets:
    """Repositorio de Assets y Constantes Visuales."""
    ANIM_HOME = "https://lottie.host/embed/9863db83-4940-4ce0-8e18-60914fb499cb/pYM5sC8O3e.json"
    ANIM_VICTORY = "https://lottie.host/embed/a8c62c96-0365-4d76-805c-3e3518b26118/pQk5sH4O1e.json"
    ANIM_SQL = "https://lottie.host/embed/4279261f-9e6a-464a-939e-21443d3b7661/gS82r9vL1s.json"
    
    ICON_DASH = "🏠"
    ICON_ACADEMY = "🎓"
    ICON_TRAIN = "🧠"
    ICON_SQL = "💾"
    ICON_BACK = "⬅️"
    ICON_NEXT = "➡️"

class AegisUI:
    """Motor Gráfico: Estilos, Animaciones y Componentes UI."""
    
    @staticmethod
    def inject_css():
        st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&family=JetBrains+Mono:wght@400;700&display=swap');
        
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

        /* --- FONDO ANIMADO --- */
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

        /* --- SIDEBAR --- */
        section[data-testid="stSidebar"] {
            background-color: rgba(2, 6, 23, 0.95) !important;
            border-right: 1px solid var(--glass-border);
        }

        /* --- TARJETAS DE VIDRIO (Cards) --- */
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

        /* --- TOOLTIPS INTELIGENTES --- */
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

        /* --- INPUTS SQL --- */
        .stTextArea textarea {
            background-color: #020617 !important;
            border: 1px solid #334155 !important;
            color: #a5f3fc !important; /* Cyan claro para código */
            font-family: 'JetBrains Mono', monospace !important;
            border-radius: 12px !important;
        }
        
        /* --- PROGRESS BAR --- */
        .stProgress > div > div > div > div {
            background-color: var(--success);
            box-shadow: 0 0 10px var(--success);
        }
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
        """Convierte [Palabra](Traducción) en HTML interactivo."""
        if not isinstance(text, str): return str(text)
        return re.sub(
            r'\[(.*?)]\((.*?)\)', 
            r'<span class="tooltip">\1<span class="tooltiptext">💡 \2</span></span>', 
            text
        )

# ======================================================================================================================
# SECTION 2: INTERNAL CONTENT BACKUP (CODEX)
# ======================================================================================================================
# Este contenido se usa SI el archivo externo 'academia_content.py' falla o no existe.

class InternalCodex:
    @staticmethod
    def get_lesson_content(module_id):
        # --- SLIDES FOR LEARNING (PASO A PASO) ---
        if module_id == "TO_BE":
            return [
                {"title": "Introducción", "content": "El verbo **To Be** significa SER o ESTAR. Es el rey de los verbos."},
                {"title": "Estructura Afirmativa", "content": "I **am** (Yo soy)\nYou **are** (Tú eres)\nHe **is** (Él es)"},
                {"title": "Ejemplos", "content": "I [am](soy) a doctor.\nShe [is](está) happy."},
                {"title": "Estructura Negativa", "content": "Solo agrega NOT.\nI am **not** sad.\nHe is **not** here."},
            ]
        elif module_id == "PRESENT_CONT":
            return [
                {"title": "Concepto", "content": "Acciones que ocurren **AHORA MISMO**."},
                {"title": "Fórmula", "content": "Sujeto + To Be + Verbo con ING"},
                {"title": "Ejemplos", "content": "I am [eating](comiendo).\nShe is [running](corriendo)."}
            ]
        return [{"title": "Error", "content": "Módulo no encontrado."}]

# ======================================================================================================================
# SECTION 3: SQL ENGINE (HYPER-MOCK v8) - MASSIVE DATA GENERATION
# ======================================================================================================================

class SQLSimulator:
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
        """Genera 4 Tablas Masivas con 300+ registros cada una."""
        cursor = conn.cursor()
        
        # Listas de datos para aleatoriedad realista
        names = ["Carlos", "Sofia", "Miguel", "Lucia", "Diego", "Elena", "Javier", "Carmen", "Roberto", "Isabel", "Fernando", "Patricia", "Ricardo", "Teresa", "Daniel", "Beatriz", "Hugo", "Valentina", "Camila", "Mateo"]
        lastnames = ["Lopez", "Garcia", "Perez", "Martinez", "Sanchez", "Diaz", "Rodriguez", "Hernandez", "Gomez", "Fernandez", "Torres", "Ramirez", "Flores", "Rivera", "Guzman", "Reyes", "Morales", "Ortega", "Castillo", "Mendoza"]
        locations = ["Guatemala City", "Quetzaltenango", "Escuintla", "Peten", "Izabal", "Sacatepequez", "Chiquimula", "Zacapa", "Coban", "Puerto Barrios"]
        depts = ["IT", "Sales", "HR", "Logistics", "Finance", "Legal", "Operations", "Marketing"]
        
        # 1. EMPLOYEES (350 Rows)
        data_emp = []
        for i in range(1, 351):
            fname, lname = random.choice(names), random.choice(lastnames)
            dept = random.choice(depts)
            role = f"{dept} {'Manager' if i % 10 == 0 else 'Specialist'}"
            salary = random.randint(4000, 45000)
            data_emp.append((i, fname, lname, dept, role, salary, random.choice(locations)))
        pd.DataFrame(data_emp, columns=["ID", "FirstName", "LastName", "Department", "JobTitle", "Salary", "Location"]).to_sql("Employees", conn, index=False)

        # 2. CUSTOMERS (350 Rows)
        data_cust = []
        for i in range(1, 351):
            fname, lname = random.choice(names), random.choice(lastnames)
            email = f"{fname.lower()}.{lname.lower()}{i}@mail.com"
            data_cust.append((i, fname, lname, email, random.choice(locations), "Active"))
        pd.DataFrame(data_cust, columns=["CustomerID", "FirstName", "LastName", "Email", "City", "Status"]).to_sql("Customers", conn, index=False)

        # 3. PRODUCTS (350 Rows)
        data_prod = []
        adjectives = ["Pro", "Ultra", "Max", "Gaming", "Office", "Smart", "Eco"]
        nouns = ["Laptop", "Mouse", "Keyboard", "Monitor", "Headset", "Server", "Router", "Switch", "Tablet", "Printer"]
        for i in range(1, 351):
            pname = f"{random.choice(adjectives)} {random.choice(nouns)} {random.randint(100, 999)}"
            price = random.randint(50, 5000)
            stock = random.randint(0, 500)
            data_prod.append((i, pname, "Tech", price, stock))
        pd.DataFrame(data_prod, columns=["ProductID", "ProductName", "Category", "Price", "Stock"]).to_sql("Products", conn, index=False)

        # 4. SALES (350 Rows - Relational)
        data_sales = []
        for i in range(1, 351):
            cid = random.randint(1, 350)
            pid = random.randint(1, 350)
            qty = random.randint(1, 10)
            date = (datetime.now() - timedelta(days=random.randint(0, 365))).strftime("%Y-%m-%d")
            data_sales.append((i, cid, pid, qty, date))
        pd.DataFrame(data_sales, columns=["SaleID", "CustomerID", "ProductID", "Quantity", "SaleDate"]).to_sql("Sales", conn, index=False)

    @classmethod
    def execute(cls, query: str):
        conn = cls.get_connection()
        if any(x in query.lower() for x in ['drop', 'delete', 'update', 'insert', 'truncate']):
            return None, "🚫 ACCIÓN BLOQUEADA: La consola es de solo lectura (SELECT)."
        try:
            return pd.read_sql_query(query, conn), None
        except Exception as e:
            return None, f"Error SQL: {str(e)}"

# ======================================================================================================================
# SECTION 4: APP STATE & NAVIGATION
# ======================================================================================================================

@dataclass
class UserProfile:
    username: str = "Administrator"
    role: str = "Senior Database Architect"
    xp: int = 15800
    streak: int = 12

class AppState:
    KEY = "TITAN_V18"
    
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
# SECTION 5: VIEW CONTROLLERS (UI LOGIC)
# ======================================================================================================================

def render_dashboard():
    user = AppState.get()["user"]
    st.markdown("<br>", unsafe_allow_html=True)
    AegisUI.render_header("IRONCLAD TITAN v18.0", "Centro de Comando")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        # Metrics Row
        m1, m2, m3 = st.columns(3)
        m1.markdown(f"""<div class="aegis-card" style="padding:20px; text-align:center;"><h3 style="color:#3b82f6; margin:0;">Nivel</h3><h1>24</h1></div>""", unsafe_allow_html=True)
        m2.markdown(f"""<div class="aegis-card" style="padding:20px; text-align:center;"><h3 style="color:#10b981; margin:0;">XP</h3><h1>{user.xp}</h1></div>""", unsafe_allow_html=True)
        m3.markdown(f"""<div class="aegis-card" style="padding:20px; text-align:center;"><h3 style="color:#f59e0b; margin:0;">Racha</h3><h1>{user.streak}</h1></div>""", unsafe_allow_html=True)
        
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
    """Modo de Enseñanza Paso a Paso."""
    state = AppState.get()
    acad = state["acad"]
    
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

    elif acad["nav"] == "ENGLISH":
        AegisUI.render_header("Módulos Inglés", "Elige un tema.")
        if st.button("⬅️ Atrás"): acad["nav"] = "MENU"; st.rerun()
        
        # Botones para iniciar lecciones (Slides)
        if st.button("📘 Verbo To Be (Paso a Paso)", use_container_width=True): start_lesson("TO_BE")
        if st.button("🏃 Presente Continuo", use_container_width=True): start_lesson("PRESENT_CONT")
        if st.button("🔥 Verbos Irregulares (Lista)", use_container_width=True): acad["nav"] = "LIST_IRREGULAR"; st.rerun()

    elif acad["nav"] == "SQL":
        AegisUI.render_header("Módulos SQL", "Elige un tema.")
        if st.button("⬅️ Atrás"): acad["nav"] = "MENU"; st.rerun()
        # Aquí podrías añadir lecciones de SQL paso a paso también

    elif acad["nav"] == "LESSON_PLAY":
        # MODO DE APRENDIZAJE PASO A PASO (SLIDES)
        slides = acad["lesson_slides"]
        idx = acad["slide_index"]
        
        # Barra de progreso
        progress = (idx + 1) / len(slides)
        st.progress(progress)
        
        # Contenido de la Slide Actual
        slide = slides[idx]
        st.markdown(f"""
        <div class="aegis-card" style="border-left: 5px solid #10b981; min-height: 300px;">
            <h2 style="color: #10b981;">{slide['title']}</h2>
            <hr style="border-color: rgba(255,255,255,0.1);">
            <div style="font-size: 1.1rem; line-height: 1.6;">
                {AegisUI.parse_tooltips(slide['content'])}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Controles de Navegación
        c_prev, c_count, c_next = st.columns([1, 2, 1])
        with c_prev:
            if idx > 0:
                if st.button("⬅️ Anterior"): acad["slide_index"] -= 1; st.rerun()
        with c_count:
            st.markdown(f"<div style='text-align:center; padding-top:10px;'>Paso {idx + 1} de {len(slides)}</div>", unsafe_allow_html=True)
        with c_next:
            if idx < len(slides) - 1:
                if st.button("Siguiente ➡️"): acad["slide_index"] += 1; st.rerun()
            else:
                if st.button("✅ Finalizar"): acad["nav"] = "MENU"; st.rerun()

    elif acad["nav"] == "LIST_IRREGULAR":
        # Vista de lista para verbos (Ya que son muchos para slides)
        AegisUI.render_header("Verbos Irregulares", "Lista Maestra.")
        if st.button("⬅️ Volver"): acad["nav"] = "ENGLISH"; st.rerun()
        
        # Intentamos cargar de ExternalCodex, si no, fallback
        if EXTERNAL_CONTENT_LOADED:
            verbs = ExternalCodex.get_irregular_verbs()
        else:
            verbs = {"⚠️ Error": [{"verb": "Error", "past": "Check file", "participle": "Check file", "meaning": "Missing", "example": "File missing"}]}
            
        for cat, v_list in verbs.items():
            with st.expander(cat, expanded=True):
                for v in v_list:
                    ex = AegisUI.parse_tooltips(v['example'])
                    st.markdown(f"**{v['verb']}** ({v['meaning']}) → Past: `{v['past']}` | Part.: `{v['participle']}`<br>📝 {ex}<hr>", unsafe_allow_html=True)

def start_lesson(module_id):
    """Inicia el modo de aprendizaje paso a paso."""
    state = AppState.get()
    
    # Intentar cargar contenido
    content = []
    if EXTERNAL_CONTENT_LOADED:
        # Aquí asumimos que Codex tiene una función para slides, si no, convertimos el dict a lista
        # Para este ejemplo, usamos el InternalCodex como fallback o simulamos la conversión
        raw_content = ExternalCodex.get_lesson_content(module_id)
        # Si devuelve un dict simple, lo convertimos a un slide único
        if isinstance(raw_content, dict):
            content = [{"title": raw_content['title'], "content": raw_content['content']}]
        elif isinstance(raw_content, list):
            content = raw_content
    
    if not content: # Si falló la carga externa o estaba vacía
        content = InternalCodex.get_lesson_content(module_id)
        
    state["acad"]["lesson_slides"] = content
    state["acad"]["slide_index"] = 0
    state["acad"]["nav"] = "LESSON_PLAY"
    st.rerun()

def render_training():
    state = AppState.get()
    quiz = state["quiz"]
    
    if not quiz["active"]:
        AegisUI.render_header("Entrenamiento", "Selecciona un módulo.")
        if st.button("⬅️ Salir"): state["view"] = "DASHBOARD"; st.rerun()
        
        # Cargar temas
        repo = {}
        if EXTERNAL_QUIZ_LOADED:
            repo = ExternalQuiz
        
        if not repo:
            st.warning("⚠️ No se cargaron preguntas externas. Usando modo demostración.")
            repo = {"Demo": {"Nivel 1": [{"pregunta": "Demo Question", "opciones": ["A", "B"], "correcta": "A"}]}}

        cols = st.columns(3)
        for i, tema in enumerate(repo.keys()):
            with cols[i%3]:
                st.markdown(f"""<div class="aegis-card" style="text-align:center;"><h3>{tema}</h3></div>""", unsafe_allow_html=True)
                if st.button(f"Entrar {tema}", key=tema, use_container_width=True):
                    # Cargar primer nivel por defecto para simplificar
                    first_lvl = list(repo[tema].keys())[0]
                    raw = repo[tema][first_lvl]
                    if isinstance(raw, dict): raw = list(raw.values())[0]
                    
                    quiz["deck"] = raw
                    random.shuffle(quiz["deck"])
                    quiz["active"] = True
                    quiz["score"] = 0
                    quiz["q_index"] = 0
                    st.rerun()
    else:
        # Gameplay
        deck = quiz["deck"]
        idx = quiz["q_index"]
        
        if idx >= len(deck):
            st.success(f"¡Terminado! Score: {quiz['score']}")
            if st.button("Finalizar"): quiz["active"] = False; st.rerun()
            return

        q = deck[idx]
        if isinstance(q, str): q = {'pregunta': q, 'opciones': ['Ver', 'Saltar'], 'correcta': 'Ver'}
        
        st.progress((idx+1)/len(deck))
        st.markdown(f"""<div class="aegis-card"><h3>{AegisUI.parse_tooltips(q.get('pregunta','Error'))}</h3></div>""", unsafe_allow_html=True)
        
        opts = q.get('opciones', ['A', 'B'])
        if isinstance(opts, str): opts = [opts]
        
        sel = st.radio("Respuesta:", opts, key=idx)
        if st.button("Confirmar"):
            if sel == q.get('correcta'):
                quiz["score"] += 1
                st.balloons()
            else:
                st.error(f"Incorrecto. Era: {q.get('correcta')}")
            time.sleep(1.5)
            quiz["q_index"] += 1
            st.rerun()

def render_sql():
    AegisUI.render_header("SQL Lab", "Entorno de Práctica Avanzado (4 Tablas).")
    
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
        # Manejo de errores silencioso y elegante para el usuario
        st.error("⚠️ Ocurrió un error inesperado. El sistema se ha reiniciado.")
        st.session_state.clear()
        if st.button("Recargar"): st.rerun()

if __name__ == "__main__":
    main()