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
  2. UI ENGINE          : 'Aegis-Glass' v13. (NO NEON).
                          - Deep Space Particles Background.
                          - Frost-Glass Cards with 24px border-radius.
                          - Interactive Tooltips & Hover Effects.
  3. DATA ENGINE        : Omni-Parser v8. Handles external quiz data safely.
  4. EDUCATION ENGINE   : 'Codex-Titan'. Built-in encyclopedia for SQL & English theory.
  5. SQL ENGINE         : Hyper-Mock v6. 
                          - Generates 3 Tables (Employees, Products, Customers).
                          - 300+ Rows each with high entropy (low repetition).
                          - Complex schemas for JOIN practice.
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
    """Central Assets Repository"""
    ANIM_HOME = "https://lottie.host/embed/9863db83-4940-4ce0-8e18-60914fb499cb/pYM5sC8O3e.json"
    ANIM_VICTORY = "https://lottie.host/embed/a8c62c96-0365-4d76-805c-3e3518b26118/pQk5sH4O1e.json"
    
    # Icons
    ICON_DASH = "🏠"
    ICON_ACADEMY = "🎓"
    ICON_TRAIN = "🧠"
    ICON_SQL = "💾"
    ICON_USER = "👤"

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
            cursor: default;
        }
        
        .aegis-card:hover {
            border-color: var(--primary);
            transform: translateY(-4px);
        }
        
        /* CLICKABLE VARIANT */
        .aegis-click {
            cursor: pointer !important;
        }
        .aegis-click:active {
            transform: scale(0.98);
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
            cursor: pointer !important;
            width: 100%;
        }
        
        .stButton > button:hover {
            background-color: var(--primary);
            border-color: var(--primary);
            box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
        }

        /* --- TOOLTIPS --- */
        .tooltip {
            border-bottom: 2px dashed var(--primary);
            cursor: help !important;
            color: #60a5fa;
            position: relative;
            display: inline-block;
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
        h1, h2, h3 { font-weight: 800; letter-spacing: -0.5px; }
        .highlight { color: var(--primary); }
        
        /* --- INPUTS --- */
        .stTextArea textarea, .stTextInput input {
            background-color: #0f172a !important;
            border: 1px solid #334155 !important;
            color: white !important;
            border-radius: 12px !important;
        }
        </style>
        """, unsafe_allow_html=True)

    @staticmethod
    def render_lottie(url: str, height: int = 300):
        st.markdown(f'<iframe src="{url}" width="100%" height="{height}px" style="border:none; background:transparent;"></iframe>', unsafe_allow_html=True)

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
# SECTION 2: CODEX ENGINE (EDUCATIONAL CONTENT)
# ======================================================================================================================

class Codex:
    """
    Knowledge Base for the Academy Section.
    Hardcoded to ensure robustness and availability.
    """
    
    @staticmethod
    def get_sql_lessons():
        return {
            "Conceptos Básicos": {
                "SELECT": "El comando `SELECT` se utiliza para seleccionar datos de una base de datos. Los datos devueltos se almacenan en una tabla de resultados.",
                "WHERE": "La cláusula `WHERE` se utiliza para filtrar registros. Extrae solo aquellos registros que cumplen una condición específica.",
                "ORDER BY": "La palabra clave `ORDER BY` se utiliza para ordenar el conjunto de resultados en orden ascendente o descendente.",
                "INSERT INTO": "La instrucción `INSERT INTO` se utiliza para insertar nuevos registros en una tabla."
            },
            "Joins & Relaciones": {
                "INNER JOIN": "Selecciona registros que tienen valores coincidentes en ambas tablas.",
                "LEFT JOIN": "Selecciona todos los registros de la tabla izquierda, y los registros coincidentes de la tabla derecha.",
                "RIGHT JOIN": "Selecciona todos los registros de la tabla derecha, y los registros coincidentes de la tabla izquierda.",
                "FULL JOIN": "Selecciona todos los registros cuando hay una coincidencia en los registros de la tabla izquierda o derecha."
            },
            "Avanzado": {
                "STORED PROCEDURE": "Un procedimiento almacenado es un código SQL preparado que puedes guardar, para que el código pueda ser reutilizado una y otra vez.",
                "TRANSACTION (ACID)": "Una transacción es una unidad única de trabajo. Si una transacción tiene éxito, todos los cambios se confirman (COMMIT). Si falla, se deshacen (ROLLBACK).",
                "INDEX": "Los índices se utilizan para recuperar datos de la base de datos más rápidamente que de otra manera."
            }
        }

    @staticmethod
    def get_english_lessons():
        return [
            {"verb": "Be", "past": "Was/Were", "participle": "Been", "meaning": "Ser / Estar", "example": "I [was](estaba) here yesterday."},
            {"verb": "Become", "past": "Became", "participle": "Become", "meaning": "Convertirse / Llegar a ser", "example": "He [became](se convirtió) a doctor."},
            {"verb": "Begin", "past": "Began", "participle": "Begun", "meaning": "Empezar", "example": "The show [began](empezó) at 8 PM."},
            {"verb": "Break", "past": "Broke", "participle": "Broken", "meaning": "Romper", "example": "Who [broke](rompió) the window?"},
            {"verb": "Bring", "past": "Brought", "participle": "Brought", "meaning": "Traer", "example": "She [brought](trajo) cake."},
            {"verb": "Buy", "past": "Bought", "participle": "Bought", "meaning": "Comprar", "example": "I [bought](compré) a new car."},
            {"verb": "Catch", "past": "Caught", "participle": "Caught", "meaning": "Atrapar", "example": "He [caught](atrapó) the ball."},
            {"verb": "Choose", "past": "Chose", "participle": "Chosen", "meaning": "Elegir", "example": "I [chose](elegí) the red one."},
            {"verb": "Come", "past": "Came", "participle": "Come", "meaning": "Venir", "example": "They [came](vinieron) home late."},
            {"verb": "Do", "past": "Did", "participle": "Done", "meaning": "Hacer", "example": "I [did](hice) my homework."},
            {"verb": "Drink", "past": "Drank", "participle": "Drunk", "meaning": "Beber", "example": "He [drank](bebió) too much water."},
            {"verb": "Drive", "past": "Drove", "participle": "Driven", "meaning": "Conducir", "example": "We [drove](condujimos) all night."},
            {"verb": "Eat", "past": "Ate", "participle": "Eaten", "meaning": "Comer", "example": "Who [ate](se comió) my pizza?"},
            {"verb": "Fall", "past": "Fell", "participle": "Fallen", "meaning": "Caer", "example": "The leaves [fell](cayeron) down."},
            {"verb": "Feel", "past": "Felt", "participle": "Felt", "meaning": "Sentir", "example": "I [felt](sentí) sick yesterday."},
            {"verb": "Find", "past": "Found", "participle": "Found", "meaning": "Encontrar", "example": "I [found](encontré) my keys."},
            {"verb": "Fly", "past": "Flew", "participle": "Flown", "meaning": "Volar", "example": "The bird [flew](voló) away."},
            {"verb": "Forget", "past": "Forgot", "participle": "Forgotten", "meaning": "Olvidar", "example": "I [forgot](olvidé) your name."},
            {"verb": "Get", "past": "Got", "participle": "Got/Gotten", "meaning": "Obtener / Conseguir", "example": "I [got](conseguí) a new job."},
            {"verb": "Give", "past": "Gave", "participle": "Given", "meaning": "Dar", "example": "She [gave](dio) me a gift."},
            {"verb": "Go", "past": "Went", "participle": "Gone", "meaning": "Ir", "example": "We [went](fuimos) to the beach."},
            {"verb": "Have", "past": "Had", "participle": "Had", "meaning": "Tener", "example": "I [had](tuve) a dream."},
            {"verb": "Hear", "past": "Heard", "participle": "Heard", "meaning": "Oír", "example": "I [heard](oí) a noise."},
            {"verb": "Know", "past": "Knew", "participle": "Known", "meaning": "Saber / Conocer", "example": "I [knew](sabía) the answer."},
            {"verb": "Leave", "past": "Left", "participle": "Left", "meaning": "Irse / Dejar", "example": "He [left](se fue) early."},
            {"verb": "Lose", "past": "Lost", "participle": "Lost", "meaning": "Perder", "example": "We [lost](perdimos) the game."},
            {"verb": "Make", "past": "Made", "participle": "Made", "meaning": "Hacer (crear)", "example": "She [made](hizo) a cake."},
            {"verb": "Meet", "past": "Met", "participle": "Met", "meaning": "Conocer / Encontrarse", "example": "I [met](conocí) him there."},
            {"verb": "Pay", "past": "Paid", "participle": "Paid", "meaning": "Pagar", "example": "I [paid](pagué) the bill."},
            {"verb": "Put", "past": "Put", "participle": "Put", "meaning": "Poner", "example": "He [put](puso) it on the table."},
            {"verb": "Read", "past": "Read", "participle": "Read", "meaning": "Leer", "example": "I [read](leí) that book."},
            {"verb": "Run", "past": "Ran", "participle": "Run", "meaning": "Correr", "example": "He [ran](corrió) fast."},
            {"verb": "Say", "past": "Said", "participle": "Said", "meaning": "Decir", "example": "She [said](dijo) yes."},
            {"verb": "See", "past": "Saw", "participle": "Seen", "meaning": "Ver", "example": "I [saw](vi) a movie."},
            {"verb": "Sell", "past": "Sold", "participle": "Sold", "meaning": "Vender", "example": "He [sold](vendió) his car."},
            {"verb": "Send", "past": "Sent", "participle": "Sent", "meaning": "Enviar", "example": "I [sent](envié) an email."},
            {"verb": "Sit", "past": "Sat", "participle": "Sat", "meaning": "Sentarse", "example": "We [sat](nos sentamos) down."},
            {"verb": "Sleep", "past": "Slept", "participle": "Slept", "meaning": "Dormir", "example": "I [slept](dormí) well."},
            {"verb": "Speak", "past": "Spoke", "participle": "Spoken", "meaning": "Hablar", "example": "He [spoke](habló) clearly."},
            {"verb": "Spend", "past": "Spent", "participle": "Spent", "meaning": "Gastar / Pasar tiempo", "example": "I [spent](gasté) time there."},
            {"verb": "Stand", "past": "Stood", "participle": "Stood", "meaning": "Estar de pie", "example": "He [stood](se paró) up."},
            {"verb": "Take", "past": "Took", "participle": "Taken", "meaning": "Tomar / Llevar", "example": "I [took](tomé) the bus."},
            {"verb": "Teach", "past": "Taught", "participle": "Taught", "meaning": "Enseñar", "example": "She [taught](enseñó) me math."},
            {"verb": "Tell", "past": "Told", "participle": "Told", "meaning": "Decir / Contar", "example": "He [told](contó) a lie."},
            {"verb": "Think", "past": "Thought", "participle": "Thought", "meaning": "Pensar", "example": "I [thought](pensé) about it."},
            {"verb": "Understand", "past": "Understood", "participle": "Understood", "meaning": "Entender", "example": "I [understood](entendí) the lesson."},
            {"verb": "Wear", "past": "Wore", "participle": "Worn", "meaning": "Usar (ropa)", "example": "She [wore](usó) a red dress."},
            {"verb": "Win", "past": "Won", "participle": "Won", "meaning": "Ganar", "example": "We [won](ganamos)!"},
            {"verb": "Write", "past": "Wrote", "participle": "Written", "meaning": "Escribir", "example": "He [wrote](escribió) a letter."}
        ]

# ======================================================================================================================
# SECTION 3: DATA ENGINE (OMNI-PARSER v8)
# ======================================================================================================================

class DataRepository:
    FILENAME = "preguntas.py"
    
    @staticmethod
    def load_content() -> Dict:
        file_path = os.path.join(os.getcwd(), DataRepository.FILENAME)
        if not os.path.exists(file_path):
            st.warning("⚠️ Modo demostración: No se detectó archivo de preguntas externo.")
            return {} # Return empty to handle gracefully

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
# SECTION 4: SQL SIMULATOR (HYPER-MOCK v6)
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
        Generates 300+ unique rows for Employees, Products, and Customers.
        Ensures high entropy and diverse data for complex queries.
        """
        cursor = conn.cursor()
        
        # --- 1. EMPLOYEES TABLE ---
        first_names = ["Carlos", "Ana", "Luis", "Maria", "Jorge", "Sofia", "Miguel", "Lucia", "Diego", "Elena", "Javier", "Carmen", "Roberto", "Isabel", "Fernando", "Patricia", "Ricardo", "Teresa", "Daniel", "Beatriz"]
        last_names = ["Lopez", "Garcia", "Perez", "Martinez", "Sanchez", "Diaz", "Rodriguez", "Hernandez", "Gomez", "Fernandez", "Torres", "Ramirez", "Flores", "Rivera", "Guzman", "Reyes", "Morales", "Ortega", "Castillo", "Mendoza"]
        depts = ["IT", "Human Resources", "Sales", "Marketing", "Finance", "Operations", "Logistics", "Legal", "R&D", "Customer Support"]
        roles = ["Junior", "Senior", "Lead", "Manager", "Director", "Intern", "Specialist", "Analyst", "Consultant", "Coordinator"]
        locations = ["Guatemala City", "Quetzaltenango", "Escuintla", "Peten", "Izabal", "Sacatepequez", "Chiquimula", "Remote", "Zacapa", "Coban"]
        
        data_emp = []
        for i in range(1, 351): # 350 Employees
            fname = random.choice(first_names)
            lname = random.choice(last_names)
            dept = random.choice(depts)
            role = f"{random.choice(roles)} {dept} Officer"
            salary = random.randint(3500, 25000)
            loc = random.choice(locations)
            hire_date = (datetime.now() - timedelta(days=random.randint(0, 3000))).strftime("%Y-%m-%d")
            data_emp.append((i, fname, lname, dept, role, salary, loc, hire_date))
            
        df_emp = pd.DataFrame(data_emp, columns=["EmployeeID", "FirstName", "LastName", "Department", "JobTitle", "Salary", "Location", "HireDate"])
        df_emp.to_sql("Employees", conn, index=False)

        # --- 2. PRODUCTS TABLE ---
        adjectives = ["Ergonomic", "Wireless", "Gaming", "Mechanical", "Ultra-Slim", "4K", "HD", "Smart", "Portable", "Heavy-Duty", "Eco-Friendly", "Noise-Cancelling", "Bluetooth", "RGB", "Industrial"]
        nouns = ["Mouse", "Keyboard", "Monitor", "Laptop", "Headset", "Webcam", "Desk", "Chair", "Router", "Switch", "Server", "Tablet", "Phone", "Printer", "Scanner"]
        categories = ["Electronics", "Office Furniture", "Accessories", "Networking", "Hardware"]
        
        data_prod = []
        for i in range(1, 351):
            name = f"{random.choice(adjectives)} {random.choice(nouns)} {random.randint(100, 999)}"
            cat = random.choice(categories)
            price = round(random.uniform(10.0, 3000.0), 2)
            stock = random.randint(0, 500)
            data_prod.append((i, name, cat, price, stock))
            
        df_prod = pd.DataFrame(data_prod, columns=["ProductID", "ProductName", "Category", "Price", "Stock"])
        df_prod.to_sql("Products", conn, index=False)

        # --- 3. CUSTOMERS TABLE ---
        domains = ["gmail.com", "outlook.com", "yahoo.com", "hotmail.com", "corp.net", "live.com"]
        countries = ["Guatemala", "USA", "Mexico", "Spain", "Colombia", "Argentina", "Chile", "Brazil", "Canada", "Germany", "France", "Italy"]
        
        data_cust = []
        for i in range(1, 351):
            fname = random.choice(first_names)
            lname = random.choice(last_names)
            email = f"{fname.lower()}.{lname.lower()}{random.randint(1,99)}@{random.choice(domains)}"
            country = random.choice(countries)
            join_date = (datetime.now() - timedelta(days=random.randint(0, 1000))).strftime("%Y-%m-%d")
            active = random.choice([True, True, True, False]) # Mostly active
            data_cust.append((i, fname, lname, email, country, join_date, active))
            
        df_cust = pd.DataFrame(data_cust, columns=["CustomerID", "FirstName", "LastName", "Email", "Country", "JoinDate", "IsActive"])
        df_cust.to_sql("Customers", conn, index=False)
        
        logger.info("Database seeded with 1000+ total rows.")

    @classmethod
    def execute(cls, query: str) -> Tuple[Optional[pd.DataFrame], Optional[str]]:
        conn = cls.get_connection()
        forbidden = ['drop', 'delete', 'update', 'insert', 'alter', 'truncate', 'grant', 'create']
        if any(cmd in query.lower().split() for cmd in forbidden):
            return None, "🔒 ERROR DE SEGURIDAD: Solo se permiten consultas de lectura (SELECT)."
        
        try:
            df = pd.read_sql_query(query, conn)
            return df, None
        except Exception as e:
            return None, f"Error de Sintaxis SQL: {str(e)}"

# ======================================================================================================================
# SECTION 5: APP STATE & USER
# ======================================================================================================================

@dataclass
class UserProfile:
    username: str = "Administrator"
    role: str = "Senior Database Architect"
    xp: int = 15800
    streak: int = 12

class AppState:
    KEY = "TITAN_OMEGA_V13"
    
    @classmethod
    def get(cls):
        if cls.KEY not in st.session_state:
            st.session_state[cls.KEY] = {
                "view": "DASHBOARD",
                "user": UserProfile(),
                "quiz": {"active": False, "deck": [], "q_index": 0, "score": 0, "feedback": False},
                "nav_train": "TOPIC", # TOPIC -> LEVEL -> PLAY
                "nav_learn": "MENU"   # MENU -> SQL -> ENGLISH
            }
        return st.session_state[cls.KEY]

# ======================================================================================================================
# SECTION 6: VIEW CONTROLLERS (UI LOGIC)
# ======================================================================================================================

def render_dashboard():
    user = AppState.get()["user"]
    st.markdown(f"""
    <div style="margin-bottom: 30px;">
        <h1 style="font-size: 3.5rem; margin-bottom: 0;">IRONCLAD <span style="color:#3b82f6">TITAN</span></h1>
        <p style="color: #94a3b8; font-size: 1.2rem;">v13.0 Omega-Learner Edition | {user.role}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Grid Layout limpio
    col_main, col_anim = st.columns([2, 1])
    
    with col_main:
        # Métricas en tarjetas
        m1, m2, m3 = st.columns(3)
        m1.markdown("""
        <div class="aegis-card">
            <h3 style="margin:0; color:#3b82f6;">Nivel</h3>
            <h1 style="margin:0;">24</h1>
            <p style="margin:0; color:#94a3b8;">Arquitecto</p>
        </div>
        """, unsafe_allow_html=True)
        
        m2.markdown(f"""
        <div class="aegis-card">
            <h3 style="margin:0; color:#10b981;">XP Total</h3>
            <h1 style="margin:0;">{user.xp}</h1>
            <p style="margin:0; color:#94a3b8;">+450 hoy</p>
        </div>
        """, unsafe_allow_html=True)
        
        m3.markdown(f"""
        <div class="aegis-card">
            <h3 style="margin:0; color:#f59e0b;">Racha</h3>
            <h1 style="margin:0;">{user.streak}</h1>
            <p style="margin:0; color:#94a3b8;">Días seguidos</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 🚀 Accesos Directos")
        b1, b2 = st.columns(2)
        if b1.button("🎓 Ir a la Academia", use_container_width=True):
            AppState.get()["view"] = "ACADEMY"
            AppState.get()["nav_learn"] = "MENU"
            st.rerun()
        if b2.button("🧠 Práctica Rápida", use_container_width=True):
            AppState.get()["view"] = "TRAINING"
            AppState.get()["nav_train"] = "TOPIC"
            st.rerun()

    with col_anim:
        # Animación limpia sin texto alrededor
        VisualAssets.render_lottie(VisualAssets.ANIM_HOME)

def render_academy():
    """Nueva sección de enseñanza."""
    state = AppState.get()
    nav = state["nav_learn"]
    
    if nav == "MENU":
        st.markdown("## 🎓 Academia Titan")
        st.markdown("Selecciona una ruta de aprendizaje.")
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"""
            <div class="aegis-card" style="text-align:center; border-top: 4px solid #3b82f6;">
                <div style="font-size:3rem;">🇬🇧</div>
                <h3>English Mastery</h3>
                <p>Verbos irregulares, tiempos y gramática.</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Entrar a Inglés", key="btn_eng", use_container_width=True):
                state["nav_learn"] = "ENGLISH"
                st.rerun()
                
        with c2:
            st.markdown(f"""
            <div class="aegis-card" style="text-align:center; border-top: 4px solid #6366f1;">
                <div style="font-size:3rem;">💾</div>
                <h3>SQL Core</h3>
                <p>Teoría de bases de datos, Joins y ACID.</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Entrar a SQL", key="btn_sql", use_container_width=True):
                state["nav_learn"] = "SQL"
                st.rerun()
                
        if st.button("⬅️ Volver al Dashboard"):
            state["view"] = "DASHBOARD"
            st.rerun()

    elif nav == "ENGLISH":
        st.markdown("## 🇬🇧 Verbos Irregulares")
        if st.button("⬅️ Volver al Menú"):
            state["nav_learn"] = "MENU"
            st.rerun()
            
        verbs = Codex.get_english_lessons()
        
        # Search bar logic could go here, keeping it simple for now
        for v in verbs:
            # Renderizar cada verbo como una tarjeta
            parsed_example = AegisUI.parse_tooltips(v['example'])
            st.markdown(f"""
            <div class="aegis-card" style="padding: 15px; margin-bottom: 10px;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <h2 style="margin:0; color:#3b82f6;">{v['verb']}</h2>
                    <span style="background:rgba(59,130,246,0.2); padding:5px 10px; border-radius:10px; font-size:0.8rem;">{v['meaning']}</span>
                </div>
                <div style="display:flex; gap: 20px; margin-top:10px; color:#94a3b8;">
                    <div>Past: <b style="color:white;">{v['past']}</b></div>
                    <div>Participle: <b style="color:white;">{v['participle']}</b></div>
                </div>
                <div style="margin-top:10px; font-style:italic; border-top:1px solid rgba(255,255,255,0.05); padding-top:10px;">
                    📝 {parsed_example}
                </div>
            </div>
            """, unsafe_allow_html=True)

    elif nav == "SQL":
        st.markdown("## 💾 Teoría SQL")
        if st.button("⬅️ Volver al Menú"):
            state["nav_learn"] = "MENU"
            st.rerun()
            
        lessons = Codex.get_sql_lessons()
        tabs = st.tabs(list(lessons.keys()))
        
        for i, category in enumerate(lessons.keys()):
            with tabs[i]:
                concepts = lessons[category]
                for term, defn in concepts.items():
                    st.markdown(f"""
                    <div class="aegis-card">
                        <h3 style="color:#6366f1; margin-bottom: 5px;">{term}</h3>
                        <p style="color:#e2e8f0; line-height: 1.6;">{defn}</p>
                    </div>
                    """, unsafe_allow_html=True)

def render_training():
    state = AppState.get()
    repo = DataRepository.load_content()
    nav = state["nav_train"]
    
    if nav == "TOPIC":
        st.markdown("## 🧠 Selección de Módulo")
        cols = st.columns(3)
        for i, tema in enumerate(repo.keys()):
            with cols[i%3]:
                st.markdown(f"""
                <div class="aegis-card" style="text-align:center;">
                    <h3>{tema}</h3>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"Abrir {tema}", key=f"t_{i}", use_container_width=True):
                    state["quiz"]["topic"] = tema
                    state["nav_train"] = "LEVEL"
                    st.rerun()
        
        if st.button("⬅️ Salir"): state["view"] = "DASHBOARD"; st.rerun()

    elif nav == "LEVEL":
        tema = state["quiz"]["topic"]
        st.markdown(f"## 📂 {tema} - Niveles")
        niveles = list(repo[tema].keys())
        cols = st.columns(3)
        for i, niv in enumerate(niveles):
            with cols[i%3]:
                st.markdown(f"""
                <div class="aegis-card" style="text-align:center; border-top:3px solid #10b981;">
                    <h3>{niv}</h3>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"Iniciar {niv}", key=f"l_{i}", use_container_width=True):
                    raw = repo[tema][niv]
                    # List wrapper fix
                    if isinstance(raw, dict): raw = list(raw.values())[0] if raw else []
                    
                    state["quiz"]["deck"] = raw
                    random.shuffle(state["quiz"]["deck"])
                    state["quiz"]["q_index"] = 0
                    state["quiz"]["score"] = 0
                    state["quiz"]["feedback"] = False
                    state["nav_train"] = "PLAY"
                    st.rerun()
        
        if st.button("⬅️ Atrás"): state["nav_train"] = "TOPIC"; st.rerun()

    elif nav == "PLAY":
        deck = state["quiz"]["deck"]
        idx = state["quiz"]["q_index"]
        
        if idx >= len(deck):
            st.markdown("## 🎉 Entrenamiento Terminado")
            st.metric("Puntaje", f"{state['quiz']['score']} / {len(deck)}")
            VisualAssets.render_lottie(VisualAssets.ANIM_VICTORY)
            if st.button("Finalizar"): state["nav_train"] = "TOPIC"; st.rerun()
            return

        q = deck[idx]
        # Auto-Healer in action for string-only questions
        if isinstance(q, str):
            q_obj = {'pregunta': q, 'opciones': ['Ver Solución', 'Saltar'], 'correcta': 'Ver Solución', 'traduccion': 'Práctica'}
        else:
            q_obj = q

        progress = (idx + 1) / len(deck)
        st.progress(progress)
        
        # Tooltip parsing
        html_q = AegisUI.parse_tooltips(q_obj.get('pregunta', 'Error'))
        
        st.markdown(f"""
        <div class="aegis-card" style="border-left: 5px solid #3b82f6;">
            <h3 style="line-height:1.6;">{html_q}</h3>
        </div>
        """, unsafe_allow_html=True)
        
        opts = q_obj.get('opciones', ['Opción A', 'Opción B'])
        if isinstance(opts, str): opts = [opts]
        
        if not state["quiz"]["feedback"]:
            sel = st.radio("Respuesta:", opts, key=f"q_{idx}")
            if st.button("Confirmar", type="primary"):
                state["quiz"]["last"] = sel
                state["quiz"]["feedback"] = True
                if sel == q_obj.get('correcta'):
                    state["quiz"]["score"] += 1
                    st.balloons()
                st.rerun()
        else:
            corr = q_obj.get('correcta')
            sel = state["quiz"]["last"]
            if sel == corr:
                st.success(f"✅ Correcto! {corr}")
            else:
                st.error(f"❌ Incorrecto. Era: {corr}")
            
            with st.expander("📚 Explicación"):
                st.write(q_obj.get('explicacion', 'N/A'))
                st.caption(q_obj.get('traduccion', ''))
            
            if st.button("Siguiente ➡"):
                state["quiz"]["q_index"] += 1
                state["quiz"]["feedback"] = False
                st.rerun()

def render_sql():
    st.markdown("## 💾 SQL Lab - Entorno Seguro")
    st.caption("Base de datos en memoria regenerada en cada sesión.")
    
    col_code, col_schema = st.columns([3, 1])
    
    with col_code:
        q = st.text_area("Consulta SQL:", "SELECT * FROM Employees LIMIT 5;", height=250)
        c1, c2 = st.columns(2)
        exec_btn = c1.button("▶ Ejecutar Query", type="primary", use_container_width=True)
        if c2.button("🧹 Limpiar", use_container_width=True): pass
        
        if exec_btn:
            with st.spinner("Ejecutando..."):
                time.sleep(0.2)
                df, err = SQLSimulator.execute(q)
            
            if err:
                st.error(err)
            else:
                st.success(f"Resultados: {len(df)} filas.")
                st.dataframe(df, use_container_width=True)

    with col_schema:
        st.markdown("### 🗄️ Esquema")
        with st.expander("👤 Employees (350+)", expanded=True):
            st.markdown("""
            - **EmployeeID** (INT) PK
            - **FirstName** (TXT)
            - **LastName** (TXT)
            - **Department** (TXT)
            - **JobTitle** (TXT)
            - **Salary** (INT)
            - **Location** (TXT)
            - **HireDate** (TXT)
            """)
        with st.expander("📦 Products (350+)"):
            st.markdown("""
            - **ProductID** (INT) PK
            - **ProductName** (TXT)
            - **Category** (TXT)
            - **Price** (FLOAT)
            - **Stock** (INT)
            """)
        with st.expander("🌍 Customers (350+)"):
            st.markdown("""
            - **CustomerID** (INT) PK
            - **FirstName** (TXT)
            - **LastName** (TXT)
            - **Email** (TXT)
            - **Country** (TXT)
            - **JoinDate** (TXT)
            - **IsActive** (BOOL)
            """)

# ======================================================================================================================
# MAIN
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
            AppState.get()["view"] = "DASHBOARD"
            st.rerun()
        if st.button(f"{VisualAssets.ICON_ACADEMY} Academia", use_container_width=True):
            AppState.get()["view"] = "ACADEMY"
            AppState.get()["nav_learn"] = "MENU"
            st.rerun()
        if st.button(f"{VisualAssets.ICON_TRAIN} Training", use_container_width=True):
            AppState.get()["view"] = "TRAINING"
            AppState.get()["nav_train"] = "TOPIC"
            st.rerun()
        if st.button(f"{VisualAssets.ICON_SQL} SQL Lab", use_container_width=True):
            AppState.get()["view"] = "SQL"
            st.rerun()

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
        st.error("Error Crítico del Sistema")
        st.code(traceback.format_exc())
        if st.button("REINICIO DE EMERGENCIA"):
            st.session_state.clear()
            st.rerun()

if __name__ == "__main__":
    main()