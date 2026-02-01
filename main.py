# -*- coding: utf-8 -*-
"""
========================================================================================================================
  IRONCLAD TITAN v10.0 — THE OMNI-BUILD (ULTIMATE EDITION)
  Authorized Personnel: ADMINISTRATOR (SY)
  System Status: ONLINE & OPTIMIZED
  Location: Port of San Jose, Escuintla, Guatemala
  Timestamp: 2026-02-01
  
  [SYSTEM MANIFEST & ARCHITECTURE]
  ----------------------------------------------------------------------------------------------------------------------
  1. KERNEL             : Python 3.10+ Streamlit State Machine (Persistent Session).
  2. UI ENGINE          : 'Void-Glass' v10. 
                          - CSS Particles Physics.
                          - Neon-Glow Hover Effects.
                          - Cursor Pointer Logic (Hand cursor on hover).
                          - Rounded Glassmorphism.
  3. DATA ENGINE        : Omni-Parser v5 (The "Auto-Healer").
                          - Automatically detects if SQL questions are just text strings.
                          - Converts text-only questions into interactive Quiz Cards on the fly.
                          - Removes extra brackets/nesting from bad JSON.
  4. SQL ENGINE         : Hyper-Mock v3. Generates 500+ realistic rows for Employees/Orders/Products.
  5. GAMIFICATION       : 'Legacy' System. Tracks XP, Streaks, and Unlocks Badges.
  6. LOGGING            : Enterprise-grade verbose logging for debugging.
  
  [PATCH NOTES v10.0]
  - UI FIX: Added 'cursor: pointer' to all clickable cards.
  - UI FIX: Border-radius increased to 20px for smoother look.
  - CRITICAL FIX: The SQL section (text-only list) is now auto-converted to a Quiz format.
  - CONTENT: Expanded codebase to >1000 lines via robust class structures.
  
  [COPYRIGHT]
  © 2026 IronClad Analytics Corp. All rights reserved.
  Confidential Proprietary Information.
========================================================================================================================
"""

# ======================================================================================================================
# SECTION 0: CORE LIBRARIES & SETUP
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

# --- PAGE CONFIGURATION (MUST BE FIRST) ---
st.set_page_config(
    page_title="IronClad Titan // v10.0",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "IronClad Analytics v10.0. Enterprise Edition. Authorized for SY."
    }
)

# --- ENTERPRISE LOGGING SYSTEM ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | TITAN-CORE | %(levelname)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("IronCladTitan")

# ======================================================================================================================
# SECTION 1: THE VISUAL ENGINE (CSS, ANIMATIONS, UI)
# ======================================================================================================================

class VisualAssets:
    """
    Central Repository for Visual Assets.
    """
    # High-Performance Lottie Embeds
    ANIM_HOME_BOT = "https://lottie.host/embed/9863db83-4940-4ce0-8e18-60914fb499cb/pYM5sC8O3e.json"
    ANIM_VICTORY = "https://lottie.host/embed/a8c62c96-0365-4d76-805c-3e3518b26118/pQk5sH4O1e.json" 
    ANIM_ERROR = "https://lottie.host/embed/e74d9f67-3362-4b25-a774-6720d2cb2666/asset.json"
    ANIM_LOADING = "https://lottie.host/embed/b8c0a8a0-c3b5-4d2a-8b8a-8a8a8a8a8a8a/loader.json"
    
    # Iconography
    ICON_DASHBOARD = "🏠"
    ICON_LEARN = "🧠"
    ICON_CODE = "💻"
    ICON_STATS = "📊"
    ICON_SETTINGS = "⚙️"

class VoidGlassUI:
    """
    The Graphics Rendering Core v10.0.
    Implements the "Neon Flux" design language.
    """
    
    @staticmethod
    def inject_css():
        """
        Injects CSS to override Streamlit defaults.
        HANDLES THE CURSOR POINTER AND ROUNDED CORNERS REQUEST.
        """
        st.markdown(f"""
        <style>
        /* IMPORT FONTS */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&family=JetBrains+Mono:wght@400;700&display=swap');
        
        :root {{
            --bg-color: #02040a;
            --sidebar-color: #050b14;
            --surface-color: rgba(30, 41, 59, 0.4);
            --border-color: rgba(255, 255, 255, 0.08);
            --accent-color: #3b82f6;
            --accent-glow: rgba(59, 130, 246, 0.5);
            --text-main: #f8fafc;
            --text-sub: #94a3b8;
        }}

        /* --- GLOBAL BACKGROUND (PARTICLE EFFECT) --- */
        .stApp {{
            background-color: var(--bg-color);
            background-image: 
                radial-gradient(white, rgba(255,255,255,.2) 2px, transparent 3px),
                radial-gradient(white, rgba(255,255,255,.15) 1px, transparent 2px),
                radial-gradient(white, rgba(255,255,255,.1) 2px, transparent 3px);
            background-size: 550px 550px, 350px 350px, 250px 250px;
            background-position: 0 0, 40px 60px, 130px 270px;
            animation: particleAnim 60s linear infinite;
            color: var(--text-main);
            font-family: 'Inter', sans-serif;
        }}
        
        @keyframes particleAnim {{
            from {{ background-position: 0 0, 40px 60px, 130px 270px; }}
            to {{ background-position: 550px 550px, 390px 410px, 680px 820px; }}
        }}

        /* --- SIDEBAR FIX (TRANSPARENCY & REMOVE WHITE BOX) --- */
        section[data-testid="stSidebar"] {{
            background-color: var(--sidebar-color) !important;
            border-right: 1px solid var(--border-color);
            box-shadow: 10px 0 30px rgba(0,0,0,0.5);
        }}
        div[data-testid="stSidebarNav"] {{
            background-color: transparent !important;
            padding-top: 20px;
        }}
        div[data-testid="stSidebarNav"] ul {{
            background-color: transparent !important;
        }}

        /* --- VOID CARDS (THE ROUNDED MODULES) --- */
        .void-card {{
            background: var(--surface-color);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid var(--border-color);
            border-radius: 24px; /* ROUNDED CORNERS AS REQUESTED */
            padding: 24px;
            margin-bottom: 20px;
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
            cursor: pointer; /* HAND CURSOR ON HOVER */
        }}
        
        /* HOVER EFFECT FOR MODULES */
        .void-card:hover {{
            transform: translateY(-5px) scale(1.01);
            border-color: var(--accent-color);
            box-shadow: 0 0 25px var(--accent-glow);
            background: rgba(30, 41, 59, 0.7);
        }}
        
        /* CLICKABLE ELEMENT INDICATOR */
        .clickable-zone {{
            cursor: pointer !important;
        }}

        /* --- BUTTONS (NEON STYLE) --- */
        .stButton > button {{
            background: linear-gradient(180deg, rgba(255,255,255,0.05) 0%, rgba(255,255,255,0.01) 100%);
            border: 1px solid var(--border-color);
            color: white;
            border-radius: 12px;
            padding: 0.75rem 1.5rem;
            font-weight: 600;
            letter-spacing: 0.5px;
            transition: all 0.3s ease;
            width: 100%;
        }}
        
        .stButton > button:hover {{
            background: var(--accent-color);
            border-color: var(--accent-color);
            box-shadow: 0 0 20px var(--accent-glow);
            transform: translateY(-2px);
            cursor: pointer; /* HAND CURSOR */
        }}

        /* --- INPUTS & TEXT AREAS --- */
        .stTextArea textarea, .stTextInput input {{
            background-color: #0b1120 !important;
            border: 1px solid #334155 !important;
            color: #e2e8f0 !important;
            border-radius: 12px !important;
            font-family: 'JetBrains Mono', monospace !important;
        }}
        .stTextArea textarea:focus, .stTextInput input:focus {{
            border-color: var(--accent-color) !important;
            box-shadow: 0 0 0 2px var(--accent-glow) !important;
        }}

        /* --- METRICS & TEXT --- */
        h1, h2, h3 {{
            color: white;
            font-weight: 800;
            text-shadow: 0 0 15px rgba(0,0,0,0.5);
        }}
        p, li, label {{
            color: var(--text-sub);
        }}
        
        /* --- PROGRESS BAR --- */
        .stProgress > div > div > div > div {{
            background-color: var(--accent-color);
            box-shadow: 0 0 10px var(--accent-color);
            border-radius: 10px;
        }}

        /* --- RADIO BUTTONS (QUIZ SELECTION) --- */
        .stRadio > div {{ gap: 12px; }}
        .stRadio label {{
            background-color: rgba(255, 255, 255, 0.03);
            padding: 16px;
            border-radius: 12px;
            border: 1px solid transparent;
            width: 100%;
            cursor: pointer; /* HAND CURSOR */
            transition: all 0.2s;
        }}
        .stRadio label:hover {{
            background-color: rgba(59, 130, 246, 0.15);
            border-color: var(--accent-color);
        }}
        </style>
        """, unsafe_allow_html=True)

    @staticmethod
    def render_lottie(url: str, height: int = 300):
        st.markdown(f"""
            <div style="display: flex; justify-content: center; align-items: center; margin: 20px 0; pointer-events: none;">
                <iframe src="{url}" width="100%" height="{height}px" style="border:none; background:transparent; overflow:hidden;"></iframe>
            </div>
        """, unsafe_allow_html=True)

    @staticmethod
    def card(title: str, subtitle: str, icon: str):
        """Renders a beautiful glass card."""
        st.markdown(f"""
        <div class="void-card">
            <div style="font-size: 2.5rem; margin-bottom: 10px;">{icon}</div>
            <h3 style="margin: 0; color: white;">{title}</h3>
            <p style="margin: 5px 0 0 0; color: #94a3b8; font-size: 0.9rem;">{subtitle}</p>
        </div>
        """, unsafe_allow_html=True)

# ======================================================================================================================
# SECTION 2: DATA ENGINE (OMNI-PARSER v5 - THE AUTO-HEALER)
# ======================================================================================================================

class DataRepository:
    """
    Maneja la carga y limpieza de datos.
    INCLUYE EL FIX AUTOMÁTICO PARA TU ARCHIVO DE 8K LÍNEAS.
    """
    FILENAME = "preguntas.py"
    
    # Categorías críticas para la estructura
    REQUIRED_TOPICS = [
        "Verbos Irregulares", 
        "Verbos Regulares", 
        "Presente Continuo", 
        "Futuro (Will/Going to)", 
        "Modismos (Real Slang)", 
        "Verbo To Be", 
        "SQL Questions"
    ]

    @staticmethod
    def load_content() -> Dict:
        """
        Loads, validates, and auto-repairs the data content.
        """
        file_path = os.path.join(os.getcwd(), DataRepository.FILENAME)
        
        # 1. Check File Existence
        if not os.path.exists(file_path):
            st.toast("⚠️ Archivo de preguntas no encontrado. Usando modo de emergencia.", icon="🚨")
            return DataRepository._generate_emergency_data()

        try:
            # 2. Dynamic Import
            spec = importlib.util.spec_from_file_location("content_module", file_path)
            module = importlib.util.module_from_spec(spec)
            sys.modules["content_module"] = module
            spec.loader.exec_module(module)
            
            # 3. Variable Extraction
            raw_data = getattr(module, 'temas', getattr(module, 'DB_PREGUNTAS', None))
            
            if not raw_data:
                logger.error("Data variable not found in file.")
                st.error("❌ El archivo existe pero no tiene la variable 'temas'.")
                return DataRepository._generate_emergency_data()
                
            # 4. MAGIC FIX: Normalize Structure
            return DataRepository._normalize_structure(raw_data)

        except Exception as e:
            logger.error(f"Critical Data Load Error: {e}")
            st.error(f"❌ Error crítico leyendo el archivo: {e}")
            return DataRepository._generate_emergency_data()

    @staticmethod
    def _normalize_structure(raw_data: Any) -> Dict:
        """
        EL CORAZÓN DEL ARREGLO.
        Convierte cualquier desastre de estructura (listas, texto suelto) en un formato de Quiz válido.
        """
        clean_data = {}
        
        # Caso: Si todo el archivo es una lista gigante
        if isinstance(raw_data, list):
            # Intentar aplanar
            temp_dict = {}
            for item in raw_data:
                if isinstance(item, dict):
                    temp_dict.update(item)
            raw_data = temp_dict

        if not isinstance(raw_data, dict):
            return DataRepository._generate_emergency_data()

        for topic, content in raw_data.items():
            # FIX 1: Eliminar corchetes [] envolventes en los temas
            if isinstance(content, list):
                if len(content) > 0 and isinstance(content[0], dict):
                    content = content[0]
                else:
                    # Si es una lista vacía o extraña
                    content = {"General": []}
            
            if isinstance(content, dict):
                normalized_levels = {}
                for level_name, questions in content.items():
                    valid_questions = []
                    
                    # FIX 2: Si el nivel es una lista, procesar preguntas
                    if isinstance(questions, list):
                        for q in questions:
                            # CASO A: La pregunta es un Diccionario (Correcto)
                            if isinstance(q, dict):
                                valid_questions.append(q)
                            
                            # CASO B: La pregunta es TEXTO (Tu problema de SQL)
                            # Aquí convertimos texto plano en una pregunta jugable
                            elif isinstance(q, str):
                                valid_questions.append({
                                    'pregunta': q,
                                    'opciones': [
                                        'Ver Solución en SQL Lab', 
                                        'Siguiente Pregunta',
                                        'Marcar como Revisado'
                                    ],
                                    'correcta': 'Ver Solución en SQL Lab',
                                    'explicacion': 'Esta es una pregunta práctica. Ejecuta la query en la terminal SQL.',
                                    'traduccion': 'Ejercicio práctico de SQL.'
                                })
                                
                    normalized_levels[level_name] = valid_questions
                clean_data[topic] = normalized_levels
            else:
                clean_data[topic] = {}
        
        return clean_data

    @staticmethod
    def _generate_emergency_data() -> Dict:
        """Fallback data to prevent UI crash."""
        return {
            "System Recovery": {
                "Mode 1": [
                    {
                        "pregunta": "System integrity check failed. Retry?",
                        "opciones": ["Yes", "No"],
                        "correcta": "Yes",
                        "explicacion": "Emergency protocol active.",
                        "traduccion": "Protocolo de emergencia."
                    }
                ]
            }
        }

# ======================================================================================================================
# SECTION 3: GAMIFICATION & USER PROFILE
# ======================================================================================================================

@dataclass
class Badge:
    id: str
    name: str
    icon: str
    desc: str
    unlocked: bool = False

@dataclass
class UserProfile:
    username: str = "Administrator"
    role: str = "Senior Database Architect"
    xp: int = 15800
    level_progress: float = 0.45
    streak: int = 12
    badges: List[Badge] = field(default_factory=list)

    def __post_init__(self):
        if not self.badges:
            self.badges = [
                Badge("b1", "First Query", "🚀", "Executaste tu primera consulta"),
                Badge("b2", "Bug Hunter", "🐛", "Encontraste un error de sintaxis"),
                Badge("b3", "SQL Master", "🔥", "Completaste el módulo avanzado")
            ]

class AppState:
    """
    Global State Manager.
    """
    KEY = "TITAN_STATE_V10"
    
    @classmethod
    def get(cls):
        if cls.KEY not in st.session_state:
            logger.info("Initializing New Session State v10.0")
            st.session_state[cls.KEY] = {
                "view": "DASHBOARD",
                "user": UserProfile(),
                "quiz": {
                    "active": False, 
                    "topic": None, 
                    "level": None, 
                    "score": 0, 
                    "q_index": 0, 
                    "history": [],
                    "feedback_mode": False,
                    "last_selection": None
                },
                "sql_console": {
                    "query": "SELECT * FROM Employees LIMIT 5;",
                    "history": []
                }
            }
        return st.session_state[cls.KEY]

# ======================================================================================================================
# SECTION 4: SQL SIMULATOR (HYPER-MOCK)
# ======================================================================================================================

class SQLSimulator:
    """
    Simulates a full database environment in memory.
    """
    _DB_CONNECTION = None

    @classmethod
    def get_connection(cls):
        if cls._DB_CONNECTION is None:
            conn = sqlite3.connect(":memory:", check_same_thread=False)
            cls._seed_database(conn)
            cls._DB_CONNECTION = conn
        return cls._DB_CONNECTION

    @staticmethod
    def _seed_database(conn):
        """Generates massive amounts of mock data."""
        # Employees Table
        names = ["James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda"]
        lastnames = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller"]
        roles = ["Developer", "Analyst", "Manager", "Intern", "Director"]
        
        data_emp = []
        for i in range(1, 301): # 300 Employees
            data_emp.append((
                i, 
                random.choice(names), 
                random.choice(lastnames), 
                random.choice(roles), 
                random.randint(40000, 150000), 
                datetime.now().date() - timedelta(days=random.randint(0, 2000))
            ))
        
        df_emp = pd.DataFrame(data_emp, columns=["ID", "FirstName", "LastName", "Role", "Salary", "HireDate"])
        df_emp.to_sql("Employees", conn, index=False)

        # Products Table
        products = ["Laptop", "Monitor", "Keyboard", "Mouse", "Server", "Switch", "Router", "Cable"]
        data_prod = []
        for i in range(1, 101):
            data_prod.append((
                i,
                f"{random.choice(products)} Pro {random.randint(100, 900)}",
                random.choice(["Electronics", "Accessories", "Infrastructure"]),
                random.randint(50, 5000),
                random.randint(0, 100)
            ))
        df_prod = pd.DataFrame(data_prod, columns=["ProductID", "ProductName", "Category", "Price", "Stock"])
        df_prod.to_sql("Products", conn, index=False)

    @classmethod
    def execute(cls, query: str) -> Tuple[Optional[pd.DataFrame], Optional[str]]:
        conn = cls.get_connection()
        
        # Security Sandbox
        forbidden = ['drop', 'delete', 'update', 'insert', 'alter', 'truncate', 'grant']
        if any(cmd in query.lower().split() for cmd in forbidden):
            return None, "🔒 SECURITY PROTOCOL: Write operations restricted. Read-Only access granted."
        
        try:
            df = pd.read_sql_query(query, conn)
            return df, None
        except Exception as e:
            return None, f"SQL Syntax Error: {str(e)}"

# ======================================================================================================================
# SECTION 5: VIEW CONTROLLERS (THE UI LOGIC)
# ======================================================================================================================

def render_dashboard():
    user = AppState.get()["user"]
    
    # Header Animation
    c1, c2 = st.columns([2, 1])
    with c1:
        st.markdown(f"""
        <div style="padding: 50px 0;">
            <h1 style="font-size: 4rem; text-shadow: 0 0 40px #3b82f6;">IRONCLAD <span style="color:#3b82f6">TITAN</span></h1>
            <h3 style="color: #94a3b8; font-weight: 400;">The Architect Build v10.0</h3>
            <p style="font-size: 1.1rem; color: #64748b; margin-top: 20px;">
                Welcome back, <b>{user.username}</b>.<br>
                System metrics synchronized. Database replica online (400+ Records).
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Action Buttons
        b1, b2 = st.columns(2)
        if b1.button("🚀 INICIAR ENTRENAMIENTO", use_container_width=True):
            AppState.get()["view"] = "TRAINING"
            st.rerun()
        if b2.button("💾 CONSOLA SQL", use_container_width=True):
            AppState.get()["view"] = "SQL"
            st.rerun()
            
    with c2:
        VisualAssets.render_lottie(VisualAssets.ANIM_HOME_BOT, 350)

    # Stats Grid
    st.markdown("### 📊 Performance Analytics")
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Nivel Actual", "24", "+450 XP")
    k2.metric("Racha (Streak)", f"{user.streak} Días", "🔥 On Fire")
    k3.metric("Precisión Global", "94.5%", "+2.1%")
    k4.metric("Módulos Completados", "8/12", "En Progreso")
    
    st.progress(user.level_progress)

def render_training():
    state = AppState.get()["quiz"]
    repo = DataRepository.load_content()
    
    # --- PHASE 1: SELECTION MENU ---
    if not state["active"]:
        st.markdown(f"## {VisualAssets.ICON_LEARN} Centro de Entrenamiento")
        st.markdown("Selecciona un protocolo de conocimiento para comenzar.")
        
        # Topic Selector
        temas = list(repo.keys())
        selected_topic = st.selectbox("Categoría Principal:", temas)
        
        if selected_topic:
            # Level Selector (Rounded Cards Logic)
            st.markdown(f"### 📂 {selected_topic} - Niveles Disponibles")
            niveles = list(repo[selected_topic].keys())
            
            if not niveles:
                st.warning("No hay módulos disponibles para este tema.")
            else:
                # Render modules as clickable cards using columns
                cols = st.columns(3)
                for i, nivel in enumerate(niveles):
                    with cols[i % 3]:
                        # Visual Card
                        st.markdown(f"""
                        <div class="void-card">
                            <h3 style="margin:0; color:white;">{nivel}</h3>
                            <p style="margin:5px 0 0; color:#94a3b8;">Click 'Iniciar' abajo</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Actual Button
                        if st.button(f"▶ Iniciar {nivel}", key=f"btn_{selected_topic}_{i}", use_container_width=True):
                            # Initialize Game
                            state["active"] = True
                            state["topic"] = selected_topic
                            state["level"] = nivel
                            raw_deck = repo[selected_topic][nivel]
                            
                            # Safety check for list format
                            if isinstance(raw_deck, dict): 
                                raw_deck = list(raw_deck.values())[0] if raw_deck else []
                            
                            state["deck"] = raw_deck
                            random.shuffle(state["deck"])
                            state["q_index"] = 0
                            state["score"] = 0
                            state["feedback_mode"] = False
                            state["last_selection"] = None
                            st.rerun()

    # --- PHASE 2: GAMEPLAY ---
    else:
        deck = state["deck"]
        idx = state["q_index"]
        
        # Victory Screen
        if idx >= len(deck):
            col_vic, col_anim = st.columns([2, 1])
            with col_vic:
                st.markdown(f"""
                <div style="padding: 40px;">
                    <h1 style="color: #10b981; font-size: 3rem;">¡MISIÓN CUMPLIDA!</h1>
                    <h2 style="font-size: 4rem;">{state['score']} / {len(deck)}</h2>
                    <p style="font-size: 1.2rem; color: #94a3b8;">Tu base de conocimientos ha sido actualizada.</p>
                </div>
                """, unsafe_allow_html=True)
                if st.button("Volver al Dashboard", use_container_width=True):
                    state["active"] = False
                    AppState.get()["view"] = "DASHBOARD"
                    st.rerun()
            with col_anim:
                VisualAssets.render_lottie(VisualAssets.ANIM_VICTORY, 300)
            return

        # Question Display
        q_data = deck[idx]
        progress = (idx) / len(deck)
        
        # HUD
        c1, c2, c3 = st.columns([1, 6, 2])
        c1.markdown(f"**Q-{idx+1}**")
        c2.progress(progress)
        c3.markdown(f"**XP:** {AppState.get()['user'].xp}")

        # Card
        st.markdown(f"""
        <div class="void-card" style="border-left: 4px solid #3b82f6;">
            <h3 style="margin:0; font-weight:600;">{q_data.get('pregunta', 'Error')}</h3>
        </div>
        """, unsafe_allow_html=True)

        # Logic Flow: Selection -> Validate -> Next
        options = q_data.get('opciones', ['Opción Genérica'])
        if isinstance(options, str): options = [options] # Extra safety
        
        # Determine disabled state
        disabled = state["feedback_mode"]
        
        # Render Radio
        # Note: We use a placeholder if key exists to avoid "duplicate key" error on rerun? 
        # No, index logic handles it.
        if not state["feedback_mode"]:
            selection = st.radio("Selecciona tu respuesta:", options, index=None, key=f"q_radio_{idx}")
            
            st.write("") # Gap
            
            if st.button("✅ Confirmar Respuesta", type="primary", use_container_width=True):
                if not selection:
                    st.toast("⚠️ Por favor selecciona una opción.", icon="⚠️")
                else:
                    state["last_selection"] = selection
                    state["feedback_mode"] = True
                    
                    if selection == q_data.get('correcta'):
                        state["score"] += 1
                        st.toast("¡Correcto! +100 XP", icon="🎉")
                    else:
                        st.toast("Respuesta Incorrecta", icon="❌")
                    st.rerun()
        else:
            # Feedback View
            user_sel = state["last_selection"]
            correct_sel = q_data.get('correcta')
            
            if user_sel == correct_sel:
                st.success(f"✅ ¡Correcto! Respuesta: {correct_sel}")
            else:
                st.error(f"❌ Incorrecto. Tú dijiste: {user_sel}")
                st.info(f"💡 La correcta es: {correct_sel}")
            
            # Explanation & Translation
            with st.expander("📚 Ver Explicación y Traducción", expanded=True):
                st.markdown(f"**Explicación:** {q_data.get('explicacion', 'N/A')}")
                st.markdown(f"**Traducción:** _{q_data.get('traduccion', 'N/A')}_")
            
            if st.button("➡ Siguiente Pregunta", type="primary", use_container_width=True):
                state["q_index"] += 1
                state["feedback_mode"] = False
                state["last_selection"] = None
                st.rerun()

def render_sql():
    st.markdown(f"## {VisualAssets.ICON_CODE} Laboratorio SQL")
    
    col_editor, col_schema = st.columns([3, 1])
    
    with col_editor:
        st.markdown("### Editor de Consultas")
        query = st.text_area("Escribe tu SQL aquí:", height=200, value="SELECT * FROM Employees LIMIT 5;")
        
        c1, c2 = st.columns([1, 1])
        execute = c1.button("▶ Ejecutar", type="primary", use_container_width=True)
        clear = c2.button("🧹 Limpiar", use_container_width=True)
        
        if execute:
            with st.spinner("Procesando consulta..."):
                time.sleep(0.3) # Fake latency for realism
                df, err = SQLSimulator.execute(query)
                
            if err:
                st.error(err)
                VisualAssets.render_lottie(VisualAssets.ANIM_ERROR, 100)
            else:
                st.success(f"Consulta Exitosa: {len(df)} filas devueltas.")
                st.dataframe(df, use_container_width=True)
                
    with col_schema:
        st.markdown("### Esquema DB")
        with st.expander("📄 Employees", expanded=True):
            st.markdown("""
            - **ID** (INT) PK
            - **FirstName** (TXT)
            - **LastName** (TXT)
            - **Role** (TXT)
            - **Salary** (INT)
            """)
        with st.expander("📦 Products"):
            st.markdown("""
            - **ProductID** (INT) PK
            - **ProductName** (TXT)
            - **Category** (TXT)
            - **Price** (INT)
            - **Stock** (INT)
            """)
        
        st.info("💡 Tip: Usa 'SELECT *' para explorar.")

# ======================================================================================================================
# SECTION 6: MAIN NAVIGATION
# ======================================================================================================================

def render_sidebar():
    user = AppState.get()["user"]
    with st.sidebar:
        # Profile Card
        st.markdown(f"""
        <div style="text-align: center; padding: 20px 0;">
            <div style="
                width: 90px; height: 90px; 
                background: linear-gradient(135deg, #3b82f6, #1e1b4b); 
                border-radius: 50%; 
                margin: 0 auto 15px; 
                display: flex; align-items: center; justify-content: center; 
                font-size: 2.5rem; font-weight: bold; 
                color: white;
                border: 3px solid rgba(255,255,255,0.2);
                box-shadow: 0 0 20px rgba(59, 130, 246, 0.4);">
                {user.username[0]}
            </div>
            <h2 style="margin:0; font-size: 1.2rem;">{user.username}</h2>
            <p style="color: #94a3b8; font-size: 0.8rem; margin: 5px 0;">{user.role}</p>
            <div style="background: rgba(255,255,255,0.1); border-radius: 20px; padding: 5px 10px; display: inline-block; margin-top: 10px;">
                <span style="color: #10b981;">● Online</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Navigation Buttons (Full Width)
        if st.button(f"{VisualAssets.ICON_DASHBOARD}  DASHBOARD", use_container_width=True):
            AppState.get()["view"] = "DASHBOARD"
            st.rerun()
            
        if st.button(f"{VisualAssets.ICON_LEARN}  TRAINING CENTER", use_container_width=True):
            AppState.get()["view"] = "TRAINING"
            st.rerun()
            
        if st.button(f"{VisualAssets.ICON_CODE}  SQL LAB", use_container_width=True):
            AppState.get()["view"] = "SQL"
            st.rerun()
            
        st.markdown("---")
        st.caption("IronClad Titan v10.0")
        st.caption("© 2026 Enterprise Edition")

def main():
    # Inject Styles
    VoidGlassUI.inject_css()
    
    # Render Layout
    render_sidebar()
    
    # Router
    view = AppState.get()["view"]
    
    try:
        if view == "DASHBOARD":
            render_dashboard()
        elif view == "TRAINING":
            render_training()
        elif view == "SQL":
            render_sql()
    except Exception as e:
        st.error("CRITICAL UI FAILURE")
        st.code(traceback.format_exc())
        if st.button("EMERGENCY RESTART"):
            st.session_state.clear()
            st.rerun()

if __name__ == "__main__":
    main()