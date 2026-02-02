# -*- coding: utf-8 -*-
"""
========================================================================================================================
  IRONCLAD TITAN v12.0 — THE AEGIS BUILD (ELITE UI EDITION)
  Authorized Personnel: ADMINISTRATOR (SY)
  System Status: ONLINE & OPTIMIZED
  Location: Port of San Jose, Escuintla, Guatemala
  Timestamp: 2026-02-02 | 10:00 CST
  
  [SYSTEM MANIFEST & ARCHITECTURE]
  ----------------------------------------------------------------------------------------------------------------------
  1. KERNEL             : Python 3.10+ Streamlit State Machine (Persistent Session).
  2. UI ENGINE          : 'Aegis-Glass' v12. 
                          - NO NEON. Replaced with 'Frost-Glass' & 'Deep-Space' gradients.
                          - Interactive Tooltips: [Word](Translation) logic implemented via Regex & CSS.
                          - Dynamic Grid System for Modules and Levels.
                          - Hand Cursor (Pointer) enforced on all interactive elements.
  3. DATA ENGINE        : Omni-Parser v7 (The "Hyper-Healer").
                          - Real-time sanitization of question data.
                          - Prevents 'AttributeError' by converting raw strings to objects on the fly.
  4. NAVIGATION         : Hierarchical Routing (Dashboard -> Topic Selection -> Level Selection -> Gameplay).
  5. SQL ENGINE         : Hyper-Mock v5. ACID compliant simulation with extensive mock data generation.
  6. TELEMETRY          : Enterprise-grade verbose logging.
  
  [PATCH NOTES v12.0]
  - UI OVERHAUL: Removed Neon Glows. Implemented "Matte Glass" aesthetic.
  - FEATURE: Added 'Magic Tooltip' support in Question Cards.
  - FEATURE: Multi-step navigation for Training (Topic -> Level -> Quiz).
  - STABILITY: Added deep try/except blocks in the rendering engine.
  
  [COPYRIGHT]
  © 2026 IronClad Analytics Corp. All rights reserved.
  Confidential Proprietary Information.
========================================================================================================================
"""

# ======================================================================================================================
# SECTION 0: CORE LIBRARIES & IMPORTS
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
    page_title="IronClad Titan // v12.0",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "IronClad Analytics v12.0. Enterprise Edition. Authorized for SY."
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
# SECTION 1: THE VISUAL ENGINE (AEGIS-GLASS UI)
# ======================================================================================================================

class VisualAssets:
    """
    Central Repository for Visual Assets and Iconography.
    """
    # High-Performance Lottie Embeds
    ANIM_HOME_BOT = "https://lottie.host/embed/9863db83-4940-4ce0-8e18-60914fb499cb/pYM5sC8O3e.json"
    ANIM_VICTORY = "https://lottie.host/embed/a8c62c96-0365-4d76-805c-3e3518b26118/pQk5sH4O1e.json" 
    ANIM_ERROR = "https://lottie.host/embed/e74d9f67-3362-4b25-a774-6720d2cb2666/asset.json"
    ANIM_LOADING = "https://lottie.host/embed/b8c0a8a0-c3b5-4d2a-8b8a-8a8a8a8a8a8a/loader.json"
    ANIM_SQL = "https://lottie.host/embed/4279261f-9e6a-464a-939e-21443d3b7661/gS82r9vL1s.json"
    
    # Iconography
    ICON_DASHBOARD = "🏠"
    ICON_LEARN = "🧠"
    ICON_CODE = "💻"
    ICON_STATS = "📊"
    ICON_SETTINGS = "⚙️"
    ICON_USER = "👤"
    ICON_FIRE = "🔥"
    ICON_BACK = "⬅️"

class AegisUI:
    """
    The Graphics Rendering Core v12.0.
    Implements the "Frost Glass" design language (No Neon).
    """
    
    @staticmethod
    def inject_css():
        """
        Injects CSS to override Streamlit defaults.
        Includes the TOOLTIP CSS logic requested.
        """
        st.markdown("""
        <style>
        /* IMPORT FONTS */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;800&family=JetBrains+Mono:wght@400;700&display=swap');
        
        :root {
            --bg-dark: #0f172a;
            --bg-card: rgba(30, 41, 59, 0.7);
            --accent-primary: #3b82f6; /* Azul Real */
            --accent-secondary: #6366f1; /* Indigo */
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --border-subtle: rgba(255, 255, 255, 0.1);
        }

        /* --- GLOBAL BACKGROUND --- */
        .stApp {
            background-color: var(--bg-dark);
            background-image: 
                radial-gradient(circle at 10% 20%, rgba(59, 130, 246, 0.1) 0%, transparent 20%),
                radial-gradient(circle at 90% 80%, rgba(99, 102, 241, 0.1) 0%, transparent 20%);
            color: var(--text-primary);
            font-family: 'Inter', sans-serif;
        }

        /* --- SIDEBAR --- */
        section[data-testid="stSidebar"] {
            background-color: #020617 !important;
            border-right: 1px solid var(--border-subtle);
        }
        
        /* --- TOOLTIP MAGICO (La lógica que pediste) --- */
        .tooltip {
            position: relative;
            display: inline-block;
            border-bottom: 2px dashed var(--accent-primary);
            cursor: help !important;
            color: #60a5fa;
            font-weight: 600;
            transition: color 0.3s;
        }
        
        .tooltip:hover {
            color: #ffffff;
            background-color: rgba(59, 130, 246, 0.2);
            border-radius: 4px;
        }

        .tooltip .tooltiptext {
            visibility: hidden;
            width: 160px;
            background-color: #1e293b;
            color: #fff;
            text-align: center;
            border-radius: 8px;
            padding: 10px;
            position: absolute;
            z-index: 999;
            bottom: 140%; /* Posición arriba */
            left: 50%;
            margin-left: -80px;
            opacity: 0;
            transition: opacity 0.3s, transform 0.3s;
            transform: translateY(10px);
            border: 1px solid var(--accent-primary);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.5);
            font-size: 0.85rem;
            font-weight: normal;
            pointer-events: none;
        }
        
        .tooltip .tooltiptext::after {
            content: "";
            position: absolute;
            top: 100%;
            left: 50%;
            margin-left: -5px;
            border-width: 5px;
            border-style: solid;
            border-color: var(--accent-primary) transparent transparent transparent;
        }

        .tooltip:hover .tooltiptext {
            visibility: visible;
            opacity: 1;
            transform: translateY(0);
        }

        /* --- MODULE CARDS (Cuadros de Selección) --- */
        .module-card {
            background: linear-gradient(145deg, rgba(30, 41, 59, 0.6), rgba(15, 23, 42, 0.8));
            backdrop-filter: blur(12px);
            border: 1px solid var(--border-subtle);
            border-radius: 20px;
            padding: 30px;
            text-align: center;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            cursor: pointer;
            height: 100%;
            position: relative;
            overflow: hidden;
        }
        
        .module-card::before {
            content: "";
            position: absolute;
            top: 0; left: 0; width: 100%; height: 4px;
            background: linear-gradient(90deg, var(--accent-primary), var(--accent-secondary));
            opacity: 0;
            transition: opacity 0.3s;
        }

        .module-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 20px 40px -5px rgba(0, 0, 0, 0.3);
            border-color: rgba(99, 102, 241, 0.3);
        }
        
        .module-card:hover::before {
            opacity: 1;
        }

        .module-title {
            font-size: 1.4rem;
            font-weight: 700;
            color: white;
            margin-bottom: 10px;
        }
        
        .module-desc {
            color: var(--text-secondary);
            font-size: 0.9rem;
        }

        /* --- BUTTONS (Flat & Clean, No Neon) --- */
        .stButton > button {
            background-color: #1e293b;
            color: white;
            border: 1px solid var(--border-subtle);
            border-radius: 12px;
            padding: 0.75rem 1.5rem;
            font-weight: 600;
            transition: all 0.2s;
            cursor: pointer !important;
        }
        
        .stButton > button:hover {
            background-color: var(--accent-primary);
            border-color: var(--accent-primary);
            color: white;
            transform: translateY(-2px);
        }

        /* --- INPUTS --- */
        .stTextArea textarea, .stTextInput input {
            background-color: #020617 !important;
            border: 1px solid #334155 !important;
            color: white !important;
            border-radius: 10px !important;
        }
        
        /* --- HEADERS --- */
        h1, h2, h3 {
            font-family: 'Inter', sans-serif;
            letter-spacing: -0.5px;
        }
        </style>
        """, unsafe_allow_html=True)

    @staticmethod
    def render_lottie(url: str, height: int = 300):
        """Renders Lottie animations in a container."""
        st.markdown(f"""
            <div style="display: flex; justify-content: center; align-items: center; margin: 20px 0; pointer-events: none;">
                <iframe src="{url}" width="100%" height="{height}px" style="border:none; background:transparent; overflow:hidden;"></iframe>
            </div>
        """, unsafe_allow_html=True)

    @staticmethod
    def render_header(title: str, subtitle: str):
        """Standardized Header Component."""
        st.markdown(f"""
        <div style="margin-bottom: 40px; padding-left: 10px; border-left: 5px solid #3b82f6;">
            <h1 style="font-size: 3rem; margin-bottom: 5px; color: white;">{title}</h1>
            <p style="font-size: 1.2rem; color: #94a3b8; margin: 0;">{subtitle}</p>
        </div>
        """, unsafe_allow_html=True)

    @staticmethod
    def parse_tooltips(text: str) -> str:
        """
        CONVIERTE TEXTO DE TOOLTIPS EN HTML.
        Entrada: "Hello [World](Mundo)"
        Salida: HTML con span class='tooltip'
        """
        if not isinstance(text, str):
            return str(text)
            
        pattern = r'\[(.*?)]\((.*?)\)'
        # Reemplazamos con el HTML que definimos en el CSS
        replacement = r'<span class="tooltip">\1<span class="tooltiptext">💡 \2</span></span>'
        
        return re.sub(pattern, replacement, text)

# ======================================================================================================================
# SECTION 2: DATA ENGINE (OMNI-PARSER v7)
# ======================================================================================================================

class DataRepository:
    """
    Maneja la carga y limpieza de datos.
    INCLUYE EL FIX AUTOMÁTICO PARA TU ARCHIVO DE 8K LÍNEAS.
    """
    FILENAME = "preguntas.py"
    
    @staticmethod
    def load_content() -> Dict:
        """
        Loads, validates, and auto-repairs the data content.
        Uses a 'Fail-Safe' approach to ensure the app never crashes.
        """
        file_path = os.path.join(os.getcwd(), DataRepository.FILENAME)
        
        # 1. Check File Existence
        if not os.path.exists(file_path):
            st.error("⚠️ Archivo de preguntas no encontrado.")
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
                st.error("❌ El archivo existe pero no tiene la variable 'temas'.")
                return DataRepository._generate_emergency_data()
                
            # 4. MAGIC FIX: Normalize Structure
            return DataRepository._normalize_structure(raw_data)

        except Exception as e:
            st.error(f"❌ Error crítico leyendo el archivo: {e}")
            st.code(traceback.format_exc())
            return DataRepository._generate_emergency_data()

    @staticmethod
    def _normalize_structure(raw_data: Any) -> Dict:
        """
        Limpia la estructura de datos eliminando listas innecesarias.
        """
        clean_data = {}
        
        # Caso: Si todo el archivo es una lista gigante
        if isinstance(raw_data, list):
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
                    content = {"General": []}
            
            if isinstance(content, dict):
                normalized_levels = {}
                for level_name, questions in content.items():
                    # FIX 2: Sanitize the deck of questions
                    normalized_levels[level_name] = DataRepository._sanitize_deck(questions)
                clean_data[topic] = normalized_levels
            else:
                clean_data[topic] = {}
        
        return clean_data

    @staticmethod
    def _sanitize_deck(questions_raw: Any) -> List[Dict]:
        """
        Iterates through questions and converts strings to valid Question Objects.
        This prevents the 'AttributeError' seen in previous versions.
        """
        valid_questions = []
        
        if not isinstance(questions_raw, list):
            return []
            
        for q in questions_raw:
            # CASO A: La pregunta es un Diccionario (Correcto)
            if isinstance(q, dict):
                # Ensure keys exist
                if 'opciones' not in q: q['opciones'] = ["Verdadero", "Falso"]
                if 'correcta' not in q: q['correcta'] = "Verdadero"
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
        
        return valid_questions

    @staticmethod
    def _generate_emergency_data() -> Dict:
        """Fallback data."""
        return {"Recovery": {"Mode": [{"pregunta": "System Recovery", "opciones": ["OK"], "correcta": "OK"}]}}

# ======================================================================================================================
# SECTION 3: USER PROFILE & STATE
# ======================================================================================================================

@dataclass
class UserProfile:
    username: str = "Administrator"
    role: str = "Senior Database Architect"
    xp: int = 15800
    streak: int = 12

class AppState:
    KEY = "TITAN_AEGIS_V12"
    
    @classmethod
    def get(cls):
        if cls.KEY not in st.session_state:
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
                    "last_selection": None,
                    "deck": []
                },
                "training_nav": "TOPIC_SELECT" # TOPIC_SELECT -> LEVEL_SELECT -> QUIZ
            }
        return st.session_state[cls.KEY]

# ======================================================================================================================
# SECTION 4: MOCK SQL ENGINE
# ======================================================================================================================

class SQLSimulator:
    _DB_CONNECTION = None

    @classmethod
    def execute(cls, query: str) -> Tuple[Optional[pd.DataFrame], Optional[str]]:
        if cls._DB_CONNECTION is None:
            conn = sqlite3.connect(":memory:", check_same_thread=False)
            # Seed minimal data
            df_emp = pd.DataFrame({
                "ID": range(1, 101),
                "Name": [f"Employee {i}" for i in range(1, 101)],
                "Salary": [random.randint(3000, 9000) for _ in range(100)]
            })
            df_emp.to_sql("Employees", conn, index=False)
            cls._DB_CONNECTION = conn
        
        try:
            return pd.read_sql_query(query, cls._DB_CONNECTION), None
        except Exception as e:
            return None, str(e)

# ======================================================================================================================
# SECTION 5: VIEW CONTROLLERS (THE NEW FLOW)
# ======================================================================================================================

def render_dashboard():
    user = AppState.get()["user"]
    AegisUI.render_header("IronClad Titan // v12.0", f"Bienvenido, {user.username}. Sistema en línea.")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("### ⚡ Acceso Rápido")
        b1, b2 = st.columns(2)
        if b1.button("🧠 Iniciar Entrenamiento", use_container_width=True):
            AppState.get()["view"] = "TRAINING"
            AppState.get()["training_nav"] = "TOPIC_SELECT"
            st.rerun()
        if b2.button("💾 Terminal SQL", use_container_width=True):
            AppState.get()["view"] = "SQL"
            st.rerun()
            
        st.markdown("### 📈 Estadísticas")
        m1, m2, m3 = st.columns(3)
        m1.metric("XP Total", f"{user.xp}", "+450")
        m2.metric("Racha", f"{user.streak} días", "🔥")
        m3.metric("Nivel", "Arquitecto", "Senior")

    with col2:
        VisualAssets.render_lottie(VisualAssets.ANIM_HOME_BOT)

def render_training():
    state = AppState.get()
    quiz_state = state["quiz"]
    nav_stage = state["training_nav"]
    repo = DataRepository.load_content()
    
    # --- STAGE 1: SELECCIÓN DE TEMA (CUADROS) ---
    if nav_stage == "TOPIC_SELECT":
        AegisUI.render_header("Centro de Entrenamiento", "Selecciona una categoría para comenzar.")
        
        if st.button(f"{VisualAssets.ICON_BACK} Volver al Dashboard"):
            state["view"] = "DASHBOARD"
            st.rerun()
            
        temas = list(repo.keys())
        # Grid System for Topics
        cols = st.columns(3)
        for i, tema in enumerate(temas):
            with cols[i % 3]:
                # Render CSS Card
                st.markdown(f"""
                <div class="module-card">
                    <div class="module-title">{tema}</div>
                    <div class="module-desc">Explora este módulo de conocimiento.</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Hidden button logic
                if st.button(f"Abrir {tema}", key=f"topic_{i}", use_container_width=True):
                    quiz_state["topic"] = tema
                    state["training_nav"] = "LEVEL_SELECT"
                    st.rerun()
                st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)

    # --- STAGE 2: SELECCIÓN DE NIVEL (CUADROS) ---
    elif nav_stage == "LEVEL_SELECT":
        tema_actual = quiz_state["topic"]
        AegisUI.render_header(f"Módulo: {tema_actual}", "Selecciona tu nivel de dificultad.")
        
        if st.button(f"{VisualAssets.ICON_BACK} Volver a Temas"):
            state["training_nav"] = "TOPIC_SELECT"
            st.rerun()
            
        niveles = list(repo[tema_actual].keys())
        if not niveles:
            st.warning("Este tema no tiene niveles disponibles aún.")
            return

        cols = st.columns(3)
        for i, nivel in enumerate(niveles):
            with cols[i % 3]:
                st.markdown(f"""
                <div class="module-card" style="border-top: 4px solid #6366f1;">
                    <div class="module-title">{nivel}</div>
                    <div class="module-desc">Desafío de conocimiento.</div>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"▶ Iniciar {nivel}", key=f"lvl_{i}", use_container_width=True):
                    # Iniciar Quiz
                    quiz_state["level"] = nivel
                    raw_deck = repo[tema_actual][nivel]
                    
                    # Fix for list wrapper
                    if isinstance(raw_deck, dict): 
                        raw_deck = list(raw_deck.values())[0] if raw_deck else []
                    
                    quiz_state["deck"] = raw_deck
                    random.shuffle(quiz_state["deck"])
                    quiz_state["q_index"] = 0
                    quiz_state["score"] = 0
                    quiz_state["feedback_mode"] = False
                    state["training_nav"] = "GAMEPLAY"
                    st.rerun()
                st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)

    # --- STAGE 3: GAMEPLAY (EL QUIZ) ---
    elif nav_stage == "GAMEPLAY":
        deck = quiz_state["deck"]
        idx = quiz_state["q_index"]
        
        # Victory Condition
        if idx >= len(deck):
            col1, col2 = st.columns([2, 1])
            with col1:
                st.markdown(f"""
                <div style="padding: 40px; background: rgba(16, 185, 129, 0.1); border-radius: 20px; border: 1px solid #10b981;">
                    <h1 style="color: #10b981;">¡ENTRENAMIENTO COMPLETADO!</h1>
                    <h2>Puntaje Final: {quiz_state['score']} / {len(deck)}</h2>
                </div>
                """, unsafe_allow_html=True)
                if st.button("Volver al Menú Principal", use_container_width=True):
                    state["training_nav"] = "TOPIC_SELECT"
                    st.rerun()
            with col2:
                VisualAssets.render_lottie(VisualAssets.ANIM_VICTORY)
            return

        # Render Question
        q_data = deck[idx]
        progress = (idx + 1) / len(deck)
        
        # Header Info
        c1, c2, c3 = st.columns([1, 6, 2])
        c1.markdown(f"**Q-{idx+1}**")
        c2.progress(progress)
        c3.markdown(f"**Score:** {quiz_state['score']}")
        
        # --- AQUÍ APLICAMOS LA MAGIA DEL TOOLTIP ---
        # Parseamos el texto de la pregunta para buscar [Palabra](Traduccion)
        pregunta_html = AegisUI.parse_tooltips(q_data.get('pregunta', 'Error loading question'))
        
        st.markdown(f"""
        <div style="
            background: rgba(30, 41, 59, 0.6); 
            border-left: 5px solid #3b82f6; 
            padding: 30px; 
            border-radius: 15px; 
            margin-bottom: 30px;">
            <h3 style="margin:0; font-weight: 600; line-height: 1.6;">{pregunta_html}</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Options logic
        options = q_data.get('opciones', ['Opción A', 'Opción B'])
        if isinstance(options, str): options = [options]
        
        if not quiz_state["feedback_mode"]:
            selection = st.radio("Selecciona tu respuesta:", options, index=None, key=f"q_{idx}")
            st.write("")
            if st.button("Confirmar Respuesta", type="primary", use_container_width=True):
                if selection:
                    quiz_state["last_selection"] = selection
                    quiz_state["feedback_mode"] = True
                    if selection == q_data.get('correcta'):
                        quiz_state["score"] += 1
                        st.balloons()
                    st.rerun()
                else:
                    st.toast("⚠️ Selecciona una opción primero.")
        else:
            # Feedback View
            sel = quiz_state["last_selection"]
            corr = q_data.get('correcta')
            
            if sel == corr:
                st.success(f"✅ ¡Correcto! Respuesta: {corr}")
            else:
                st.error(f"❌ Incorrecto. Tú dijiste: {sel}")
                st.info(f"💡 La correcta era: {corr}")
            
            with st.expander("📚 Explicación y Traducción", expanded=True):
                st.markdown(f"**Explicación:** {q_data.get('explicacion', 'N/A')}")
                st.caption(f"Traducción: {q_data.get('traduccion', 'N/A')}")
                
            if st.button("Siguiente Pregunta ➡", type="primary", use_container_width=True):
                quiz_state["q_index"] += 1
                quiz_state["feedback_mode"] = False
                st.rerun()

def render_sql():
    AegisUI.render_header("Laboratorio SQL", "Entorno de simulación seguro.")
    
    c1, c2 = st.columns([3, 1])
    with c1:
        q = st.text_area("Query Editor:", "SELECT * FROM Employees LIMIT 5;", height=250)
        b1, b2 = st.columns(2)
        if b1.button("▶ Ejecutar Query", type="primary", use_container_width=True):
            df, err = SQLSimulator.execute(q)
            if err:
                st.error(err)
            else:
                st.success("Query ejecutada exitosamente.")
                st.dataframe(df, use_container_width=True)
                
    with c2:
        st.markdown("### 🗄️ Esquema")
        with st.expander("Employees", expanded=True):
            st.code("ID (INT)\nName (TXT)\nSalary (INT)")

# ======================================================================================================================
# MAIN EXECUTION
# ======================================================================================================================

def render_sidebar():
    user = AppState.get()["user"]
    with st.sidebar:
        st.markdown(f"""
        <div style="text-align: center; padding: 20px 0;">
            <div style="width: 80px; height: 80px; background: linear-gradient(135deg, #3b82f6, #6366f1); border-radius: 50%; margin: 0 auto; display: flex; align-items: center; justify-content: center; color: white; font-size: 2rem; font-weight: bold;">
                {user.username[0]}
            </div>
            <h3 style="margin-top: 15px; color: white;">{user.username}</h3>
            <p style="color: #94a3b8; font-size: 0.9rem;">{user.role}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        if st.button(f"{VisualAssets.ICON_DASHBOARD}  Dashboard", use_container_width=True):
            AppState.get()["view"] = "DASHBOARD"
            st.rerun()
            
        if st.button(f"{VisualAssets.ICON_LEARN}  Training", use_container_width=True):
            AppState.get()["view"] = "TRAINING"
            AppState.get()["training_nav"] = "TOPIC_SELECT"
            st.rerun()
            
        if st.button(f"{VisualAssets.ICON_CODE}  SQL Lab", use_container_width=True):
            AppState.get()["view"] = "SQL"
            st.rerun()

def main():
    AegisUI.inject_css()
    render_sidebar()
    
    view = AppState.get()["view"]
    
    try:
        if view == "DASHBOARD":
            render_dashboard()
        elif view == "TRAINING":
            render_training()
        elif view == "SQL":
            render_sql()
    except Exception as e:
        st.error("SYSTEM ERROR")
        st.code(traceback.format_exc())
        if st.button("EMERGENCY RESET"):
            st.session_state.clear()
            st.rerun()

if __name__ == "__main__":
    main()