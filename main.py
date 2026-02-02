# -*- coding: utf-8 -*-
"""
========================================================================================================================
  IRONCLAD TITAN v13.0 — THE OMEGA-LEARNER BUILD (EDUCATION & DATA EDITION)
  Authorized Personnel: ADMINISTRATOR (SY)
  System Status: ONLINE & OPTIMIZED
  Location: Port of San Jose, Escuintla, Guatemala
  Timestamp: 2026-02-03 | 08:00 CST
  
  [SYSTEM MANIFEST & ARCHITECTURE]
  ----------------------------------------------------------------------------------------------------------------------
  1. KERNEL             : Python 3.10+ Streamlit State Machine.
  2. UI ENGINE          : 'Aegis-Glass' v13. (NO NEON - PURE FROST DESIGN).
                          - Deep Space Particles Background (CSS Animation).
                          - Frost-Glass Cards with 24px border-radius.
                          - Interactive Tooltips & Hover Effects.
  3. DATA ENGINE        : Omni-Parser v8. Handles external quiz data safely.
  4. EDUCATION ENGINE   : 'Codex-Titan'. Built-in encyclopedia for SQL & English theory.
                          - Contains full lesson plans for Verb To Be, Tenses, and SQL commands.
  5. SQL ENGINE         : Hyper-Mock v6. 
                          - Generates 3 Tables (Employees, Products, Customers).
                          - 350+ Rows each with high entropy (low repetition).
                          - Real Guatemalan locations and realistic corporate roles.
  6. NAVIGATION         : Dashboard -> Academy (New) -> Training -> SQL Lab.
  
  [COPYRIGHT]
  © 2026 IronClad Analytics Corp. All rights reserved.
========================================================================================================================
"""

# ======================================================================================================================
# SECTION 0: IMPORTS & SETUP
# ======================================================================================================================
import streamlit as st
import pandas as pd
import random
import time
import os
import sys
import importlib.util
import uuid
import enum
import logging
import json
import sqlite3
import traceback
import re
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple, Union
from dataclasses import dataclass, field

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="IronClad Titan // v13.0",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={'About': "IronClad Analytics v13.0. Enterprise Edition."}
)

# --- LOGGING ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s | TITAN | %(levelname)s | %(message)s')
logger = logging.getLogger("IronCladTitan")

# ======================================================================================================================
# SECTION 1: VISUAL ENGINE (AEGIS-GLASS UI)
# ======================================================================================================================

class VisualAssets:
    """Central Assets Repository - Fixed Attributes"""
    ANIM_HOME = "https://lottie.host/embed/9863db83-4940-4ce0-8e18-60914fb499cb/pYM5sC8O3e.json"
    ANIM_VICTORY = "https://lottie.host/embed/a8c62c96-0365-4d76-805c-3e3518b26118/pQk5sH4O1e.json"
    ANIM_ERROR = "https://lottie.host/embed/e74d9f67-3362-4b25-a774-6720d2cb2666/asset.json"
    
    # Icons
    ICON_DASH = "🏠"
    ICON_ACADEMY = "🎓"
    ICON_TRAIN = "🧠"
    ICON_SQL = "💾"
    ICON_USER = "👤"
    ICON_BACK = "⬅️"

class AegisUI:
    """The Graphics Core. Clean, Frosty, Professional."""
    
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
            --text: #f8fafc;
            --text-muted: #94a3b8;
        }

        /* --- FONDO ANIMADO (SPACE DUST) --- */
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

        /* --- TARJETAS DE VIDRIO (Aegis Cards) --- */
        .aegis-card {
            background: linear-gradient(145deg, rgba(30, 41, 59, 0.4), rgba(15, 23, 42, 0.6));
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid var(--glass-border);
            border-radius: 24px;
            padding: 25px;
            margin-bottom: 20px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
            transition: transform 0.3s ease, border-color 0.3s;
            cursor: pointer; /* MANITA SIEMPRE */
            position: relative;
            overflow: hidden;
        }
        
        .aegis-card:hover {
            border-color: var(--primary);
            transform: translateY(-4px);
            background: linear-gradient(145deg, rgba(30, 41, 59, 0.6), rgba(15, 23, 42, 0.8));
        }
        
        /* Titulos dentro de tarjetas */
        .card-title {
            font-size: 1.5rem;
            font-weight: 800;
            color: white;
            margin-bottom: 10px;
        }
        
        .card-desc {
            color: var(--text-muted);
            font-size: 0.95rem;
        }

        /* --- BOTONES (Clean & Flat) --- */
        .stButton > button {
            background-color: rgba(30, 41, 59, 0.8);
            color: white;
            border: 1px solid var(--glass-border);
            border-radius: 12px;
            padding: 0.8rem 1.5rem;
            font-weight: 600;
            transition: all 0.2s;
            cursor: pointer !important; /* MANITA */
            width: 100%;
        }
        
        .stButton > button:hover {
            background-color: var(--primary);
            border-color: var(--primary);
            box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
            transform: translateY(-2px);
        }

        /* --- TOOLTIPS (TRADUCCIÓN) --- */
        .tooltip {
            border-bottom: 2px dashed var(--primary);
            cursor: help !important;
            color: #60a5fa;
            position: relative;
            display: inline-block;
            font-weight: 600;
        }
        
        .tooltip .tooltiptext {
            visibility: hidden;
            width: 180px;
            background-color: #1e293b;
            color: #fff;
            text-align: center;
            border-radius: 8px;
            padding: 10px;
            position: absolute;
            z-index: 10;
            bottom: 135%;
            left: 50%;
            margin-left: -90px;
            opacity: 0;
            transition: opacity 0.3s;
            border: 1px solid var(--primary);
            box-shadow: 0 10px 25px rgba(0,0,0,0.5);
            font-size: 0.85rem;
        }
        
        .tooltip:hover .tooltiptext {
            visibility: visible;
            opacity: 1;
        }

        /* --- HEADERS --- */
        h1, h2, h3 { font-weight: 800; letter-spacing: -0.5px; color: white; }
        
        /* --- INPUTS --- */
        .stTextArea textarea, .stTextInput input {
            background-color: #0f172a !important;
            border: 1px solid #334155 !important;
            color: white !important;
            border-radius: 12px !important;
        }
        
        /* --- TABS --- */
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
        }
        .stTabs [data-baseweb="tab"] {
            height: 50px;
            white-space: pre-wrap;
            background-color: rgba(30, 41, 59, 0.4);
            border-radius: 10px 10px 0 0;
            color: white;
            font-weight: 600;
        }
        .stTabs [aria-selected="true"] {
            background-color: var(--primary) !important;
        }
        </style>
        """, unsafe_allow_html=True)

    @staticmethod
    def render_lottie(url: str, height: int = 300):
        st.markdown(f'<div style="display: flex; justify-content: center;"><iframe src="{url}" width="100%" height="{height}px" style="border:none; background:transparent;"></iframe></div>', unsafe_allow_html=True)

    @staticmethod
    def parse_tooltips(text: str) -> str:
        """Converts [Word](Trans) to HTML Tooltip."""
        if not isinstance(text, str): return str(text)
        return re.sub(
            r'\[(.*?)]\((.*?)\)', 
            r'<span class="tooltip">\1<span class="tooltiptext">💡 \2</span></span>', 
            text
        )

# ======================================================================================================================
# SECTION 2: CODEX ENGINE (THE EDUCATIONAL BRAIN)
# ======================================================================================================================

class Codex:
    """
    ENCICLOPEDIA INTERNA.
    Contiene toda la teoría para la sección 'Academia' sin depender de archivos externos.
    """
    
    @staticmethod
    def get_lesson_content(module_id: str) -> dict:
        """Returns the content for a specific learning module."""
        
        # --- ENGLISH MODULES ---
        if module_id == "TO_BE":
            return {
                "title": "Verbo To Be (Ser/Estar)",
                "desc": "La base del inglés. Aprende a decir quién eres y dónde estás.",
                "content": """
                ### 📘 Concepto Básico
                El verbo **To Be** es el camaleón del inglés. Cambia de forma según la persona.
                
                ### 📊 Tabla de Conjugación (Presente)
                | Pronombre | Verbo | Ejemplo | Traducción |
                | :--- | :--- | :--- | :--- |
                | I (Yo) | **am** | I [am](soy/estoy) happy. | Yo estoy feliz. |
                | You (Tú) | **are** | You [are](eres/estás) my friend. | Tú eres mi amigo. |
                | He/She/It | **is** | She [is](es/está) smart. | Ella es lista. |
                | We (Nosotros) | **are** | We [are](somos/estamos) ready. | Estamos listos. |
                | They (Ellos) | **are** | They [are](son/están) here. | Ellos están aquí. |
                
                ### ⚠️ Errores Comunes
                * NO digas: "I is" o "You is".
                * En negativo: I am **not**, You are **not** (aren't), She is **not** (isn't).
                """
            }
            
        elif module_id == "PRESENT_CONT":
            return {
                "title": "Presente Continuo",
                "desc": "Acciones que están ocurriendo AHORA MISMO.",
                "content": """
                ### 📘 Estructura
                La fórmula matemática es: 
                **Sujeto + Verbo To Be + Verbo con ING**
                
                ### 📝 Ejemplos Vivos
                * I **am** [working](trabajando) right now.
                * She **is** [eating](comiendo) pizza.
                * They **are** [playing](jugando) soccer.
                
                ### 💡 Reglas de Ortografía
                1. Si el verbo termina en 'e' (Dance), quita la 'e' (Dancing).
                2. Si el verbo es corto y termina en Consonante-Vocal-Consonante (Run), duplica la última letra (Running).
                """
            }
            
        elif module_id == "IRREGULAR":
            return {
                "title": "Verbos Irregulares",
                "desc": "Los rebeldes del idioma. No siguen reglas.",
                "content": """
                ### 💀 La Lista de la Muerte (Top 20 Esenciales)
                Estos verbos NO terminan en '-ed' en el pasado. Tienes que memorizarlos.
                
                | Presente | Pasado (Past Simple) | Participio | Significado |
                | :--- | :--- | :--- | :--- |
                | **Be** | Was/Were | Been | Ser/Estar |
                | **Become** | Became | Become | Convertirse |
                | **Begin** | Began | Begun | Empezar |
                | **Break** | Broke | Broken | Romper |
                | **Bring** | Brought | Brought | Traer |
                | **Buy** | Bought | Bought | Comprar |
                | **Come** | Came | Come | Venir |
                | **Do** | Did | Done | Hacer |
                | **Drink** | Drank | Drunk | Beber |
                | **Eat** | Ate | Eaten | Comer |
                | **Fall** | Fell | Fallen | Caer |
                | **Feel** | Felt | Felt | Sentir |
                | **Get** | Got | Got/Gotten | Obtener |
                | **Give** | Gave | Given | Dar |
                | **Go** | Went | Gone | Ir |
                | **Have** | Had | Had | Tener |
                | **Know** | Knew | Known | Saber |
                | **See** | Saw | Seen | Ver |
                | **Take** | Took | Taken | Tomar |
                | **Write** | Wrote | Written | Escribir |
                """
            }

        # --- SQL MODULES ---
        elif module_id == "SQL_BASICS":
            return {
                "title": "SQL Fundamentos",
                "desc": "El bloque de construcción de todas las consultas.",
                "content": """
                ### 🧱 Los 4 Fantásticos (CRUD)
                1. **SELECT**: Para LEER datos.
                   `SELECT * FROM Users;`
                2. **INSERT**: Para CREAR datos.
                   `INSERT INTO Users (Name) VALUES ('Juan');`
                3. **UPDATE**: Para ACTUALIZAR datos.
                   `UPDATE Users SET Name = 'Pedro' WHERE ID = 1;`
                4. **DELETE**: Para BORRAR datos.
                   `DELETE FROM Users WHERE ID = 1;`
                   
                ### 🔍 Clausulas Vitales
                * **WHERE**: El filtro. `SELECT * FROM Autos WHERE Color = 'Rojo';`
                * **ORDER BY**: El organizador. `ORDER BY Precio DESC;`
                * **LIMIT / TOP**: El freno. `LIMIT 5;` (Solo trae 5).
                """
            }
            
        elif module_id == "JOINS":
            return {
                "title": "JOINs y Relaciones",
                "desc": "Cómo conectar tablas entre sí.",
                "content": """
                ### 🤝 Tipos de Uniones
                Imagina dos círculos (Conjuntos).
                
                1. **INNER JOIN (La Intersección)**
                   * Trae SOLO lo que coincide en ambas tablas.
                   * *Ejemplo:* Clientes que SÍ compraron algo.
                   
                2. **LEFT JOIN (La Izquierda manda)**
                   * Trae TODO lo de la tabla izquierda (A), y si hay coincidencia en B, la trae. Si no, pone NULL.
                   * *Ejemplo:* Todos los clientes, tengan compras o no.
                   
                3. **RIGHT JOIN (La Derecha manda)**
                   * Lo opuesto al Left Join. Rara vez se usa.
                   
                4. **FULL OUTER JOIN (Todo junto)**
                   * Trae todo de A y todo de B, coincidan o no.
                """
            }
            
        elif module_id == "ACID":
            return {
                "title": "Transacciones ACID",
                "desc": "La seguridad de los datos bancarios.",
                "content": """
                ### 🛡️ ¿Qué es una Transacción?
                Es un grupo de operaciones que se tratan como una sola. O pasan todas, o no pasa ninguna.
                
                ### 🧪 A.C.I.D.
                * **A - Atomicidad:** Todo o nada. Si falla una parte, se hace ROLLBACK de todo.
                * **C - Consistencia:** La base de datos pasa de un estado válido a otro válido.
                * **I - Aislamiento (Isolation):** Una transacción no debe interferir con otra que ocurre al mismo tiempo.
                * **D - Durabilidad:** Una vez confirmado (COMMIT), el cambio es permanente, incluso si se va la luz.
                """
            }
            
        return {"title": "Error", "desc": "Módulo no encontrado", "content": "N/A"}

# ======================================================================================================================
# SECTION 3: DATA ENGINE (OMNI-PARSER v8)
# ======================================================================================================================

class DataRepository:
    FILENAME = "preguntas.py"
    
    @staticmethod
    def load_content() -> Dict:
        file_path = os.path.join(os.getcwd(), DataRepository.FILENAME)
        if not os.path.exists(file_path):
            st.warning("⚠️ No se detectó archivo de preguntas. Usando modo demostración.")
            return {} 

        try:
            spec = importlib.util.spec_from_file_location("content_module", file_path)
            module = importlib.util.module_from_spec(spec)
            sys.modules["content_module"] = module
            spec.loader.exec_module(module)
            raw_data = getattr(module, 'temas', None)
            if not raw_data: return {}
            return DataRepository._normalize_structure(raw_data)
        except Exception as e:
            st.error(f"Error de datos: {e}")
            return {}

    @staticmethod
    def _normalize_structure(raw_data: Any) -> Dict:
        clean_data = {}
        if isinstance(raw_data, list):
            temp = {}
            for item in raw_data:
                if isinstance(item, dict): temp.update(item)
            raw_data = temp

        if not isinstance(raw_data, dict): return {}

        for topic, content in raw_data.items():
            if isinstance(content, list):
                content = content[0] if len(content) > 0 and isinstance(content[0], dict) else {}
            
            if isinstance(content, dict):
                normalized_levels = {}
                for level_name, questions in content.items():
                    valid_questions = []
                    if isinstance(questions, list):
                        for q in questions:
                            if isinstance(q, dict): valid_questions.append(q)
                            elif isinstance(q, str):
                                valid_questions.append({
                                    'pregunta': q,
                                    'opciones': ['Ver Solución', 'Saltar'],
                                    'correcta': 'Ver Solución',
                                    'explicacion': 'Ejercicio práctico.',
                                    'traduccion': 'Práctica.'
                                })
                    normalized_levels[level_name] = valid_questions
                clean_data[topic] = normalized_levels
            else:
                clean_data[topic] = {}
        return clean_data

# ======================================================================================================================
# SECTION 4: SQL SIMULATOR (HYPER-MOCK v6) - THE DATA FACTORY
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
        """
        Generates 350+ unique rows per table.
        Uses advanced randomization for realistic Guatemalan context.
        """
        # --- LISTAS DE DATOS ---
        names = ["Carlos", "Ana", "Luis", "Maria", "Jorge", "Sofia", "Miguel", "Lucia", "Diego", "Elena", "Javier", "Carmen", "Roberto", "Isabel", "Fernando", "Patricia", "Ricardo", "Teresa", "Daniel", "Beatriz", "Hugo", "Valentina", "Camila", "Mateo", "Santiago", "Sebastian", "Alejandro", "Valeria", "Ximena", "Mariana"]
        lastnames = ["Lopez", "Garcia", "Perez", "Martinez", "Sanchez", "Diaz", "Rodriguez", "Hernandez", "Gomez", "Fernandez", "Torres", "Ramirez", "Flores", "Rivera", "Guzman", "Reyes", "Morales", "Ortega", "Castillo", "Mendoza", "Vargas", "Ruiz", "Jimenez", "Salas", "Nuñez", "Leon", "Herrera", "Medina", "Aguilar", "Rojas"]
        locations = ["Guatemala City", "Quetzaltenango", "Escuintla", "Peten", "Izabal", "Sacatepequez", "Chiquimula", "Zacapa", "Coban", "Puerto Barrios", "Antigua Guatemala", "Mazatenango", "Retalhuleu", "Jalapa", "Totonicapan"]
        depts = ["IT", "Sales", "HR", "Logistics", "Finance", "Legal", "Operations", "Marketing"]
        products_adj = ["Wireless", "Ergonomic", "Gaming", "Professional", "Portable", "Heavy-Duty", "Smart", "4K", "Bluetooth", "Mechanical", "Digital", "Analog"]
        products_noun = ["Mouse", "Keyboard", "Monitor", "Laptop", "Headset", "Webcam", "Desk", "Chair", "Router", "Server", "Tablet", "Printer", "Scanner", "Microphone"]
        
        # --- TABLA 1: EMPLOYEES (350 Rows) ---
        data_emp = []
        for i in range(1, 351):
            fname = random.choice(names)
            lname = random.choice(lastnames)
            dept = random.choice(depts)
            role = f"{dept} Specialist" if i % 2 == 0 else f"{dept} Manager"
            salary = random.randint(4000, 35000)
            loc = random.choice(locations)
            email = f"{fname.lower()}.{lname.lower()}{i}@titan-corp.gt"
            data_emp.append((i, fname, lname, email, dept, role, salary, loc))
            
        df_emp = pd.DataFrame(data_emp, columns=["ID", "FirstName", "LastName", "Email", "Department", "JobTitle", "Salary", "Location"])
        df_emp.to_sql("Employees", conn, index=False)

        # --- TABLA 2: PRODUCTS (350 Rows) ---
        data_prod = []
        for i in range(1, 351):
            pname = f"{random.choice(products_adj)} {random.choice(products_noun)} {random.randint(100, 900)}"
            cat = "Electronics" if "Mouse" in pname or "Keyboard" in pname else "Furniture"
            price = random.randint(50, 5000)
            stock = random.randint(0, 200)
            data_prod.append((i, pname, cat, price, stock))
            
        df_prod = pd.DataFrame(data_prod, columns=["ProductID", "ProductName", "Category", "Price", "Stock"])
        df_prod.to_sql("Products", conn, index=False)

        # --- TABLA 3: CUSTOMERS (350 Rows) ---
        data_cust = []
        domains = ["gmail.com", "outlook.com", "yahoo.com", "live.com"]
        for i in range(1, 351):
            fname = random.choice(names)
            lname = random.choice(lastnames)
            email = f"{fname[:3]}{lname}{random.randint(10,99)}@{random.choice(domains)}".lower()
            country = random.choice(["Guatemala", "USA", "Mexico", "El Salvador", "Honduras"])
            active = random.choice([1, 1, 1, 0])
            data_cust.append((i, fname, lname, email, country, active))
            
        df_cust = pd.DataFrame(data_cust, columns=["CustomerID", "FirstName", "LastName", "Email", "Country", "IsActive"])
        df_cust.to_sql("Customers", conn, index=False)

    @classmethod
    def execute(cls, query: str) -> Tuple[Optional[pd.DataFrame], Optional[str]]:
        conn = cls.get_connection()
        # Security: Read Only
        if any(x in query.lower() for x in ['drop', 'delete', 'update', 'insert', 'truncate']):
            return None, "🚫 ACCIÓN BLOQUEADA: La consola es de solo lectura (SELECT)."
        try:
            return pd.read_sql_query(query, conn), None
        except Exception as e:
            return None, f"Error SQL: {str(e)}"

# ======================================================================================================================
# SECTION 5: APP STATE & NAVIGATION
# ======================================================================================================================

@dataclass
class UserProfile:
    username: str = "Administrator"
    role: str = "Senior Database Architect"
    xp: int = 15800
    streak: int = 12

class AppState:
    KEY = "TITAN_V13_OMEGA"
    
    @classmethod
    def get(cls):
        if cls.KEY not in st.session_state:
            st.session_state[cls.KEY] = {
                "view": "DASHBOARD",
                "user": UserProfile(),
                "quiz": {"active": False, "deck": [], "q_index": 0, "score": 0, "feedback": False},
                "nav_train": "TOPIC",
                "nav_learn": "MENU",
                "lesson_id": None
            }
        return st.session_state[cls.KEY]

# ======================================================================================================================
# SECTION 6: VIEW CONTROLLERS (THE NEW UI)
# ======================================================================================================================

def render_dashboard():
    user = AppState.get()["user"]
    
    # Header Limpio
    st.markdown(f"""
    <div style="margin-bottom: 40px;">
        <h1 style="font-size: 3.5rem; margin-bottom: 0;">IRONCLAD <span style="color:#3b82f6">TITAN</span></h1>
        <p style="color: #94a3b8; font-size: 1.2rem;">v13.0 Omega-Learner | {user.role}</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Métricas Glassmorphism
        m1, m2, m3 = st.columns(3)
        m1.markdown(f"""
        <div class="aegis-card">
            <h3 style="color:#3b82f6; margin:0;">Nivel</h3>
            <h1 style="margin:0;">24</h1>
            <p style="color:#94a3b8; margin:0;">Arquitecto</p>
        </div>
        """, unsafe_allow_html=True)
        m2.markdown(f"""
        <div class="aegis-card">
            <h3 style="color:#10b981; margin:0;">XP</h3>
            <h1 style="margin:0;">{user.xp}</h1>
            <p style="color:#94a3b8; margin:0;">Total</p>
        </div>
        """, unsafe_allow_html=True)
        m3.markdown(f"""
        <div class="aegis-card">
            <h3 style="color:#f59e0b; margin:0;">Racha</h3>
            <h1 style="margin:0;">{user.streak}</h1>
            <p style="color:#94a3b8; margin:0;">Días</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 🚀 Panel de Control")
        b1, b2 = st.columns(2)
        if b1.button("🎓 Ir a la Academia (Aprender)", use_container_width=True):
            AppState.get()["view"] = "ACADEMY"
            AppState.get()["nav_learn"] = "MENU"
            st.rerun()
        if b2.button("🧠 Ir al Entrenamiento (Quiz)", use_container_width=True):
            AppState.get()["view"] = "TRAINING"
            AppState.get()["nav_train"] = "TOPIC"
            st.rerun()

    with col2:
        VisualAssets.render_lottie(VisualAssets.ANIM_HOME)

def render_academy():
    """Nueva sección de enseñanza estructurada."""
    state = AppState.get()
    nav = state["nav_learn"]
    
    if nav == "MENU":
        AegisUI.render_header("Academia Titan", "Selecciona una ruta de conocimiento.")
        
        if st.button(f"{VisualAssets.ICON_BACK} Volver al Dashboard"):
            state["view"] = "DASHBOARD"
            st.rerun()
            
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"""
            <div class="aegis-card" style="text-align:center; border-top: 4px solid #3b82f6;">
                <div style="font-size:3rem; margin-bottom:10px;">🇬🇧</div>
                <div class="card-title">English Mastery</div>
                <div class="card-desc">Domina los verbos y tiempos gramaticales.</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Entrar a Inglés", key="btn_eng_mod", use_container_width=True):
                state["nav_learn"] = "ENGLISH_MENU"
                st.rerun()
                
        with c2:
            st.markdown(f"""
            <div class="aegis-card" style="text-align:center; border-top: 4px solid #6366f1;">
                <div style="font-size:3rem; margin-bottom:10px;">💾</div>
                <div class="card-title">SQL Core</div>
                <div class="card-desc">Fundamentos de bases de datos y lógica avanzada.</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Entrar a SQL", key="btn_sql_mod", use_container_width=True):
                state["nav_learn"] = "SQL_MENU"
                st.rerun()

    elif nav == "ENGLISH_MENU":
        AegisUI.render_header("Módulos de Inglés", "Elige un tema específico.")
        if st.button(f"{VisualAssets.ICON_BACK} Atrás"): state["nav_learn"] = "MENU"; st.rerun()
        
        modules = [
            ("Verbo To Be", "TO_BE"),
            ("Presente Continuo", "PRESENT_CONT"),
            ("Verbos Irregulares", "IRREGULAR")
        ]
        
        cols = st.columns(3)
        for i, (title, code) in enumerate(modules):
            with cols[i % 3]:
                st.markdown(f"""<div class="aegis-card"><h3 style="margin:0;">{title}</h3></div>""", unsafe_allow_html=True)
                if st.button(f"Estudiar {title}", key=code, use_container_width=True):
                    state["lesson_id"] = code
                    state["nav_learn"] = "LESSON_VIEW"
                    st.rerun()

    elif nav == "SQL_MENU":
        AegisUI.render_header("Módulos SQL", "Elige un tema específico.")
        if st.button(f"{VisualAssets.ICON_BACK} Atrás"): state["nav_learn"] = "MENU"; st.rerun()
        
        modules = [
            ("Fundamentos", "SQL_BASICS"),
            ("Joins & Relaciones", "JOINS"),
            ("Transacciones ACID", "ACID")
        ]
        
        cols = st.columns(3)
        for i, (title, code) in enumerate(modules):
            with cols[i % 3]:
                st.markdown(f"""<div class="aegis-card"><h3 style="margin:0;">{title}</h3></div>""", unsafe_allow_html=True)
                if st.button(f"Estudiar {title}", key=code, use_container_width=True):
                    state["lesson_id"] = code
                    state["nav_learn"] = "LESSON_VIEW"
                    st.rerun()

    elif nav == "LESSON_VIEW":
        lesson_id = state["lesson_id"]
        content = Codex.get_lesson_content(lesson_id)
        
        AegisUI.render_header(content["title"], content["desc"])
        if st.button(f"{VisualAssets.ICON_BACK} Volver a Módulos"):
            # Return to correct menu based on lesson ID type
            state["nav_learn"] = "SQL_MENU" if lesson_id in ["SQL_BASICS", "JOINS", "ACID"] else "ENGLISH_MENU"
            st.rerun()
            
        # Render the lesson content
        parsed_content = AegisUI.parse_tooltips(content["content"])
        st.markdown(f"""
        <div class="aegis-card" style="border-left: 5px solid #10b981;">
            {parsed_content}
        </div>
        """, unsafe_allow_html=True)

def render_training():
    state = AppState.get()
    nav = state["nav_train"]
    repo = DataRepository.load_content()
    
    if nav == "TOPIC":
        AegisUI.render_header("Centro de Entrenamiento", "Ponte a prueba.")
        if st.button(f"{VisualAssets.ICON_BACK} Salir"): state["view"] = "DASHBOARD"; st.rerun()
        
        temas = list(repo.keys())
        cols = st.columns(3)
        for i, tema in enumerate(temas):
            with cols[i%3]:
                st.markdown(f"""<div class="aegis-card" style="text-align:center;"><h3>{tema}</h3></div>""", unsafe_allow_html=True)
                if st.button(f"Abrir {tema}", key=f"t_{i}", use_container_width=True):
                    state["quiz"]["topic"] = tema
                    state["nav_train"] = "LEVEL"
                    st.rerun()

    elif nav == "LEVEL":
        tema = state["quiz"]["topic"]
        AegisUI.render_header(f"{tema}", "Elige dificultad.")
        if st.button(f"{VisualAssets.ICON_BACK} Atrás"): state["nav_train"] = "TOPIC"; st.rerun()
        
        niveles = list(repo[tema].keys())
        cols = st.columns(3)
        for i, niv in enumerate(niveles):
            with cols[i%3]:
                st.markdown(f"""<div class="aegis-card" style="text-align:center;"><h3>{niv}</h3></div>""", unsafe_allow_html=True)
                if st.button(f"Iniciar {niv}", key=f"l_{i}", use_container_width=True):
                    raw = repo[tema][niv]
                    if isinstance(raw, dict): raw = list(raw.values())[0] if raw else []
                    state["quiz"]["deck"] = raw
                    random.shuffle(state["quiz"]["deck"])
                    state["quiz"]["q_index"] = 0
                    state["quiz"]["score"] = 0
                    state["quiz"]["feedback"] = False
                    state["nav_train"] = "PLAY"
                    st.rerun()

    elif nav == "PLAY":
        deck = state["quiz"]["deck"]
        idx = state["quiz"]["q_index"]
        
        if idx >= len(deck):
            st.markdown("## 🎉 Sesión Terminada")
            st.metric("Puntaje Final", f"{state['quiz']['score']} / {len(deck)}")
            VisualAssets.render_lottie(VisualAssets.ANIM_VICTORY)
            if st.button("Finalizar"): state["nav_train"] = "TOPIC"; st.rerun()
            return

        q_obj = deck[idx]
        if isinstance(q_obj, str): 
            q_obj = {'pregunta': q_obj, 'opciones': ['Ver', 'Saltar'], 'correcta': 'Ver', 'traduccion': 'Práctica'}

        st.progress((idx + 1) / len(deck))
        
        html_q = AegisUI.parse_tooltips(q_obj.get('pregunta', 'Error'))
        st.markdown(f"""
        <div class="aegis-card" style="border-left: 5px solid #3b82f6;">
            <h3 style="line-height:1.6; margin:0;">{html_q}</h3>
        </div>
        """, unsafe_allow_html=True)
        
        opts = q_obj.get('opciones', ['A', 'B'])
        if isinstance(opts, str): opts = [opts]
        
        if not state["quiz"]["feedback"]:
            sel = st.radio("Respuesta:", opts, key=f"q_{idx}")
            if st.button("Confirmar", type="primary"):
                state["quiz"]["last"] = sel
                state["quiz"]["feedback"] = True
                if sel == q_obj.get('correcta'): state["quiz"]["score"] += 1
                st.rerun()
        else:
            sel = state["quiz"]["last"]
            corr = q_obj.get('correcta')
            if sel == corr: st.success(f"✅ Correcto! {corr}")
            else: st.error(f"❌ Incorrecto. Era: {corr}")
            with st.expander("Explicación"):
                st.write(q_obj.get('explicacion', ''))
                st.caption(q_obj.get('traduccion', ''))
            if st.button("Siguiente ➡"):
                state["quiz"]["q_index"] += 1
                state["quiz"]["feedback"] = False
                st.rerun()

def render_sql():
    AegisUI.render_header("SQL Lab", "Entorno Seguro (Read-Only). Datos reseteados.")
    
    c1, c2 = st.columns([3, 1])
    with c1:
        q = st.text_area("Consulta:", "SELECT * FROM Employees LIMIT 5;", height=250)
        b1, b2 = st.columns(2)
        exec_btn = b1.button("▶ Ejecutar", type="primary", use_container_width=True)
        if b2.button("🧹 Limpiar", use_container_width=True): pass
        
        if exec_btn:
            df, err = SQLSimulator.execute(q)
            if err: st.error(err)
            else:
                st.success(f"Resultados: {len(df)} filas.")
                st.dataframe(df, use_container_width=True)

    with c2:
        st.markdown("### 🗄️ Tablas Disponibles")
        with st.expander("👤 Employees (350+)", expanded=True):
            st.code("ID, FirstName, LastName, Email, Department, JobTitle, Salary, Location")
        with st.expander("📦 Products (350+)"):
            st.code("ProductID, ProductName, Category, Price, Stock")
        with st.expander("🌍 Customers (350+)"):
            st.code("CustomerID, FirstName, LastName, Email, Country, IsActive")

# ======================================================================================================================
# MAIN EXECUTION
# ======================================================================================================================

def render_sidebar():
    user = AppState.get()["user"]
    with st.sidebar:
        st.markdown(f"""
        <div style="text-align:center; padding:20px 0;">
            <div style="width:80px; height:80px; margin:0 auto; background:linear-gradient(135deg, #3b82f6, #6366f1); border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:2rem; font-weight:bold; color:white;">
                {user.username[0]}
            </div>
            <h3 style="margin-top:10px; color:white;">{user.username}</h3>
            <p style="color:#94a3b8; font-size:0.9rem;">{user.role}</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("---")
        if st.button(f"{VisualAssets.ICON_DASH} Dashboard", use_container_width=True):
            AppState.get()["view"] = "DASHBOARD"; st.rerun()
        if st.button(f"{VisualAssets.ICON_ACADEMY} Academia", use_container_width=True):
            AppState.get()["view"] = "ACADEMY"; AppState.get()["nav_learn"] = "MENU"; st.rerun()
        if st.button(f"{VisualAssets.ICON_TRAIN} Training", use_container_width=True):
            AppState.get()["view"] = "TRAINING"; AppState.get()["nav_train"] = "TOPIC"; st.rerun()
        if st.button(f"{VisualAssets.ICON_SQL} SQL Lab", use_container_width=True):
            AppState.get()["view"] = "SQL"; st.rerun()

def main():
    AegisUI.inject_css()
    render_sidebar()
    view = AppState.get()["view"]
    try:
        if view == "DASHBOARD": render_dashboard()
        elif view == "ACADEMY": render_academy()
        elif view == "TRAINING": render_training()
        elif view == "SQL": render_sql()
    except Exception as e:
        st.error("Error del Sistema")
        st.code(traceback.format_exc())
        if st.button("REINICIO DE EMERGENCIA"):
            st.session_state.clear()
            st.rerun()

if __name__ == "__main__":
    main()