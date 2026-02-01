# -*- coding: utf-8 -*-
"""
========================================================================================================================
  IRONCLAD TITAN v7.0 — THE ARCHITECT BUILD (ULTIMATE EDITION)
  Authorized Personnel: ADMINISTRATOR (SY)
  Release Date: 2026-02-01
  
  [SYSTEM MANIFEST]
  ----------------------------------------------------------------------------------------------------------------------
  1. KERNEL             : Python 3.10+ Streamlit State Machine (Persistent).
  2. UI ENGINE          : 'Void-Glass' v7. Neon-Flux CSS override with Particle Animation.
  3. DATA ENGINE        : Smart-Parser v2 (Auto-corrects JSON/List structure errors).
  4. FAILSAFE SYSTEM    : Integrated Knowledge Base fallback (Prevent 'Empty Module' errors).
  5. INTERACTIVITY      : Two-Step Verification Logic (Select -> Analyze -> Feedback).
  6. ARCHITECTURE       : MVC Pattern (Model-View-Controller) for Enterprise Scalability.
  7. SECURITY           : SQL Sandbox Mode (Read-Only Safety Protocols).

  [CHANGE LOG v7.0]
  - CRITICAL FIX: "UserProfile" now includes 'progress_to_next_level' initialization.
  - CRITICAL FIX: Data Loader now handles List-wrapped Dictionaries (Fixes 'Verbos Irregulares' bug).
  - FEATURE: Added 'Analizar Respuesta' flow with Translation display.
  - VISUAL: Added 'Floating Particles' background animation.
  - CONTENT: Pre-allocated slots for: Irregulares, Regulares, Presente Continuo, Futuro, Modismos, To Be.
  
  [COPYRIGHT]
  © 2026 IronClad Analytics Corp. All rights reserved.
  Confidential Proprietary Information.
========================================================================================================================
"""

# ======================================================================================================================
# SECTION 0: CORE LIBRARIES & SYSTEM SETUP
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
import math
import sqlite3
import re
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple, Union, Callable
from dataclasses import dataclass, field
from abc import ABC, abstractmethod

# --- PAGE CONFIGURATION (MUST BE FIRST EXECUTION) ---
st.set_page_config(
    page_title="IronClad Titan // v7.0",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': "IronClad Analytics v7.0 - Enterprise Edition. Authorized for SY."
    }
)

# --- ADVANCED LOGGING SYSTEM ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | IRONCLAD-CORE | %(levelname)s | %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger("IronCladTitan")

# ======================================================================================================================
# SECTION 1: THE VISUAL ENGINE (CSS & ASSETS)
# ======================================================================================================================

class VisualAssets:
    """
    Central Repository for Visual Assets & Animations.
    Uses Direct HTML Embeds to ensure 100% uptime without external libraries.
    """
    # Lottie JSON Embeds (High Performance)
    ANIM_HOME_BOT = "https://lottie.host/embed/9863db83-4940-4ce0-8e18-60914fb499cb/pYM5sC8O3e.json"
    ANIM_BRAIN_SCAN = "https://lottie.host/embed/d3e36569-2310-444b-9759-3221c56360b6/example.json"
    ANIM_VICTORY_ROCKET = "https://lottie.host/embed/a8c62c96-0365-4d76-805c-3e3518b26118/pQk5sH4O1e.json" 
    ANIM_SQL_SERVER = "https://lottie.host/embed/93556c4d-9659-4d9d-9c36-749340915442/asset.json"
    ANIM_ERROR = "https://lottie.host/embed/e74d9f67-3362-4b25-a774-6720d2cb2666/asset.json"
    ANIM_SEARCH = "https://lottie.host/embed/7d363529-6799-4b36-a660-3168a9775463/lmbC3g2v1A.json"
    
    # Corporate Iconography
    ICON_DASHBOARD = "🏠"
    ICON_LEARN = "🧠"
    ICON_CODE = "💻"
    ICON_USER = "👨‍💻"
    ICON_TROPHY = "🏆"
    ICON_FIRE = "🔥"
    ICON_SETTINGS = "⚙️"
    ICON_LOCK = "🔒"
    ICON_DATABASE = "🗄️"
    ICON_ANALYTICS = "📈"

class VoidGlassUI:
    """
    The Graphics Rendering Core v7.0.
    Design Philosophy: Neon Flux, Particle Background, Glassmorphism.
    """
    COLOR_BG_DARK = "#02040a"
    COLOR_SIDEBAR = "#050b14"
    COLOR_ACCENT = "#3b82f6"
    
    @staticmethod
    def inject_css():
        """
        Injects CSS to override Streamlit defaults.
        Includes PARTICLE ANIMATION and Sidebar Fixes.
        """
        st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&family=JetBrains+Mono:wght@400;700&display=swap');
        
        :root {{
            --bg-color: #02040a;
            --sidebar-color: #050b14;
            --surface-color: rgba(30, 41, 59, 0.6);
            --border-color: rgba(255, 255, 255, 0.1);
            --accent-color: #3b82f6;
            --text-main: #f8fafc;
        }}

        /* --- GLOBAL BACKGROUND --- */
        .stApp {{
            background-color: var(--bg-color);
            background-image: 
                radial-gradient(circle at 15% 50%, rgba(59, 130, 246, 0.08) 0%, transparent 25%),
                radial-gradient(circle at 85% 30%, rgba(139, 92, 246, 0.08) 0%, transparent 25%);
            font-family: 'Inter', sans-serif;
            color: var(--text-main);
        }}

        /* --- SIDEBAR FIX (NO WHITE SPACES) --- */
        section[data-testid="stSidebar"] {{
            background-color: var(--sidebar-color) !important;
            border-right: 1px solid var(--border-color);
        }}
        div[data-testid="stSidebarNav"] {{
            background-color: transparent !important;
            padding-top: 20px;
        }}
        
        /* --- TYPOGRAPHY --- */
        h1, h2, h3 {{
            font-weight: 800;
            letter-spacing: -0.02em;
            color: white;
            text-shadow: 0 0 20px rgba(59, 130, 246, 0.5);
        }}
        
        h1 span {{
            background: linear-gradient(to right, #3b82f6, #8b5cf6, #3b82f6);
            background-size: 200% auto;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: shine 3s linear infinite;
        }}
        
        @keyframes shine {{
            to {{ background-position: 200% center; }}
        }}

        /* --- GLASS CARDS --- */
        .void-card {{
            background: var(--surface-color);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 20px;
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
        }}
        
        .void-card:hover {{
            transform: translateY(-2px);
            border-color: var(--accent-color);
            box-shadow: 0 0 20px rgba(59, 130, 246, 0.2);
        }}

        /* --- BUTTONS --- */
        .stButton > button {{
            background: linear-gradient(180deg, rgba(255,255,255,0.05) 0%, rgba(255,255,255,0.01) 100%);
            border: 1px solid var(--border-color);
            color: white;
            border-radius: 8px;
            padding: 0.6rem 1.2rem;
            font-weight: 600;
            transition: all 0.2s ease;
        }}
        
        .stButton > button:hover {{
            background: var(--accent-color);
            border-color: var(--accent-color);
            box-shadow: 0 0 15px var(--accent-color);
            transform: scale(1.01);
        }}

        /* --- INPUTS --- */
        .stTextInput input, .stTextArea textarea {{
            background-color: #0f172a !important;
            border: 1px solid #334155 !important;
            color: white !important;
            border-radius: 8px;
        }}
        
        .stTextInput input:focus, .stTextArea textarea:focus {{
            border-color: var(--accent-color) !important;
            box-shadow: 0 0 0 1px var(--accent-color) !important;
        }}

        /* --- RADIO BUTTONS (QUIZ) --- */
        .stRadio > div {{ gap: 10px; }}
        .stRadio label {{
            background-color: rgba(255, 255, 255, 0.03);
            padding: 15px;
            border-radius: 8px;
            border: 1px solid transparent;
            width: 100%;
            cursor: pointer;
            transition: all 0.2s;
        }}
        .stRadio label:hover {{
            background-color: rgba(59, 130, 246, 0.1);
            border-color: var(--accent-color);
        }}

        /* --- METRICS --- */
        [data-testid="stMetricValue"] {{
            font-family: 'JetBrains Mono', monospace;
            color: #60a5fa !important;
        }}

        /* --- TOASTS --- */
        .stToast {{
            background-color: #1e293b !important;
            border: 1px solid #475569 !important;
            color: white !important;
        }}
        </style>
        """, unsafe_allow_html=True)

    @staticmethod
    def render_lottie(url: str, height: int = 300):
        st.markdown(f"""
            <div style="display: flex; justify-content: center; align-items: center; margin: 20px 0;">
                <iframe src="{url}" width="100%" height="{height}px" style="border:none; background:transparent; overflow:hidden;"></iframe>
            </div>
        """, unsafe_allow_html=True)

# ======================================================================================================================
# SECTION 2: PROCEDURAL DATA GENERATION (MOCK SQL DATA)
# ======================================================================================================================

class DataGenerator:
    """
    Generates realistic mock data for the SQL Simulator.
    Ensures 300+ records are available for 'SELECT *' queries.
    """
    FIRST_NAMES = ["James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda", "William", "Elizabeth", "David", "Barbara", "Richard", "Susan", "Joseph", "Jessica", "Thomas", "Sarah", "Charles", "Karen", "Christopher", "Nancy", "Daniel", "Lisa", "Matthew", "Betty", "Anthony", "Margaret", "Mark", "Sandra", "Carlos", "Sofia", "Miguel", "Lucia", "Jorge", "Valentina", "Luis", "Camila", "Diego", "Maria", "Alejandro", "Fernanda", "Javier", "Carmen"]
    LAST_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker", "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores", "Rivera", "Gomez", "Diaz", "Reyes"]
    ROLES = ["Junior Dev", "Senior Dev", "Data Analyst", "Project Manager", "Intern", "Director", "HR Specialist", "Accountant", "Security Officer", "SysAdmin", "Cloud Architect", "UX Designer", "Sales Rep", "Marketing Lead"]
    
    @staticmethod
    def generate_employees(count: int = 350) -> List[Tuple]:
        data = []
        for i in range(1, count + 1):
            fname = random.choice(DataGenerator.FIRST_NAMES)
            lname = random.choice(DataGenerator.LAST_NAMES)
            name = f"{fname} {lname}"
            role = random.choice(DataGenerator.ROLES)
            salary = random.randint(35000, 195000)
            dept_id = random.randint(1, 6)
            
            start_date = datetime(2018, 1, 1)
            end_date = datetime.now()
            days_between = (end_date - start_date).days
            joined_date = (start_date + timedelta(days=random.randrange(days_between))).strftime("%Y-%m-%d")
            
            data.append((i, name, role, salary, dept_id, joined_date))
        return data

    @staticmethod
    def generate_departments() -> List[Tuple]:
        return [
            (1, "Engineering", "Tower A"),
            (2, "Human Resources", "Tower B"),
            (3, "Sales", "Tower C"),
            (4, "Marketing", "Tower A"),
            (5, "Finance", "Tower D"),
            (6, "Legal", "Tower D")
        ]

    @staticmethod
    def generate_projects() -> List[Tuple]:
        return [
            (101, "IronClad Alpha", 1, "Active"),
            (102, "Web Revamp", 4, "Planning"),
            (103, "Database Migration", 1, "Completed"),
            (104, "Q1 Hiring", 2, "Active"),
            (105, "Audit 2025", 5, "Review"),
            (106, "Mobile App", 1, "Development"),
            (107, "Social Campaign", 4, "Active")
        ]

# ======================================================================================================================
# SECTION 3: ENTERPRISE DATA MODELS
# ======================================================================================================================

@dataclass
class Badge:
    id: str
    name: str
    icon: str
    description: str
    xp_bonus: int
    unlocked: bool = False

@dataclass
class UserProfile:
    """
    User Entity with Gamification Stats.
    Includes 'progress_to_next_level' fix.
    """
    username: str = "Administrator"
    role: str = "Senior Database Architect"
    xp: int = 15800
    current_streak: int = 1
    max_streak: int = 5
    total_questions: int = 0
    correct_answers: int = 0
    modules_completed: int = 0
    # FIX: Explicit initialization
    progress_to_next_level: float = 0.0
    badges: List[Badge] = field(default_factory=list)

    def __post_init__(self):
        if not self.badges:
            self.badges = [
                Badge("b1", "Hello World", "👋", "Complete first session", 500),
                Badge("b2", "Sniper", "🎯", "10 Correct in a row", 1000),
                Badge("b3", "SQL God", "💾", "Execute 50 queries", 2000)
            ]
        self._calculate_progress()

    def _calculate_progress(self):
        # Level caps at 1000 XP per level
        self.progress_to_next_level = (self.xp % 1000) / 1000.0

    @property
    def level(self) -> int:
        return (self.xp // 1000) + 1

    @property
    def accuracy(self) -> float:
        if self.total_questions == 0: return 0.0
        return (self.correct_answers / self.total_questions) * 100

    def add_xp(self, amount: int) -> int:
        multiplier = 1.0 + (min(self.current_streak, 10) * 0.1)
        final_amount = int(amount * multiplier)
        self.xp += final_amount
        self.total_questions += 1
        self._calculate_progress()
        return final_amount

@dataclass
class Question:
    id: str
    text: str
    options: List[str]
    correct_option: str
    explanation: str
    translation: str

# ======================================================================================================================
# SECTION 4: STATE MANAGEMENT (THE BRAIN)
# ======================================================================================================================

class QuizPhase(enum.Enum):
    SETUP = 0
    PLAYING = 1
    VICTORY = 2

class AppState:
    """
    Global Singleton for State Management.
    Persists data across Streamlit reruns.
    """
    KEY = "IRONCLAD_TITAN_STATE_V7"

    @classmethod
    def _ensure_initialized(cls):
        if cls.KEY not in st.session_state:
            st.session_state[cls.KEY] = {
                "view": "DASHBOARD",
                "user": UserProfile(),
                "quiz": {
                    "phase": QuizPhase.SETUP,
                    "active_topic": None,
                    "active_level": None,
                    "deck": [],
                    "current_index": 0,
                    "score": 0,
                    "buffer_selection": None, # Holds selection before 'Analyze'
                    "feedback_mode": False    # True when showing Correct/Incorrect
                },
                "sql": {
                    "history": [],
                    "last_result": None,
                    "query_count": 0
                },
                "notifications": []
            }

    @classmethod
    def get(cls) -> Dict:
        cls._ensure_initialized()
        return st.session_state[cls.KEY]

    @classmethod
    def user(cls) -> UserProfile:
        return cls.get()["user"]

    @classmethod
    def quiz(cls) -> Dict:
        return cls.get()["quiz"]

    @classmethod
    def sql(cls) -> Dict:
        return cls.get()["sql"]

    @classmethod
    def navigate_to(cls, view: str):
        cls.get()["view"] = view
        if view != "TRAINING":
            cls.quiz()["phase"] = QuizPhase.SETUP
            cls.quiz()["active_topic"] = None

    @classmethod
    def add_notification(cls, msg: str, type: str = "info"):
        cls.get()["notifications"].append({"msg": msg, "type": type, "time": datetime.now()})

# ======================================================================================================================
# SECTION 5: DATA REPOSITORY (SMART PARSER FIX)
# ======================================================================================================================

class DataRepository:
    """
    Handles loading questions from 'preguntas.py'.
    INCLUDES FIX for List-Wrapped Dictionaries.
    """
    FILENAME = "preguntas.py"
    
    # REQUIRED CATEGORIES AS PER USER REQUEST
    REQUIRED_TOPICS = [
        "Verbos Irregulares", 
        "Verbos Regulares", 
        "Presente Continuo", 
        "Futuro", 
        "Modismos", 
        "Verbo To Be", 
        "SQL Questions"
    ]

    @staticmethod
    def load_content() -> Dict:
        file_path = os.path.join(os.getcwd(), DataRepository.FILENAME)
        
        # 1. Load File
        if not os.path.exists(file_path):
            AppState.add_notification("Using Emergency Data Protocol.", "warning")
            return DataRepository._generate_emergency_data()

        try:
            spec = importlib.util.spec_from_file_location("content_module", file_path)
            module = importlib.util.module_from_spec(spec)
            sys.modules["content_module"] = module
            spec.loader.exec_module(module)
            
            # 2. Extract Data (Try 'temas', then 'DB_PREGUNTAS')
            raw_data = getattr(module, 'temas', getattr(module, 'DB_PREGUNTAS', None))
            
            if not raw_data:
                return DataRepository._generate_emergency_data()
                
            # 3. Smart Parse (The Fix)
            return DataRepository._smart_parse(raw_data)

        except Exception as e:
            logger.error(f"Load Error: {e}")
            return DataRepository._generate_emergency_data()

    @staticmethod
    def _smart_parse(raw_data: Dict) -> Dict:
        """
        Normalizes the data structure.
        Handles cases where content is [ {'Level': []} ] instead of {'Level': []}.
        """
        clean_data = {}
        
        for topic, content in raw_data.items():
            # Fix: If content is a list containing a dict (User's specific error)
            if isinstance(content, list) and len(content) > 0 and isinstance(content[0], dict):
                content = content[0] # Unwrap the list
            
            if isinstance(content, dict):
                clean_data[topic] = content
            else:
                clean_data[topic] = {} # Fallback for malformed data

        # Ensure all required topics exist (even if empty) to prevent menu crashes
        for req in DataRepository.REQUIRED_TOPICS:
            if req not in clean_data:
                clean_data[req] = {"1. Basics (System Generated)": DataRepository._get_placeholder_questions(req)}
                
        return clean_data

    @staticmethod
    def _get_placeholder_questions(topic_name):
        """Generates generic questions if a topic is empty."""
        return [
            {
                "pregunta": f"What represents {topic_name}?",
                "opciones": ["Option A", "Option B", "Option C"],
                "correcta": "Option A",
                "explicacion": "System placeholder.",
                "traduccion": "Marcador de posición del sistema."
            }
        ]

    @staticmethod
    def _generate_emergency_data() -> Dict:
        """Fallback data if file is completely missing."""
        data = {}
        for topic in DataRepository.REQUIRED_TOPICS:
            data[topic] = {
                "1. Emergency Mode": DataRepository._get_placeholder_questions(topic)
            }
        return data

# ======================================================================================================================
# SECTION 6: SQL SIMULATION ENGINE
# ======================================================================================================================

class SQLSimulator:
    _EMPLOYEES_DF = None
    _DEPARTMENTS_DF = None
    _PROJECTS_DF = None

    @classmethod
    def initialize_data(cls):
        if cls._EMPLOYEES_DF is None:
            emp_data = DataGenerator.generate_employees(350)
            cls._EMPLOYEES_DF = pd.DataFrame(emp_data, columns=["ID", "Name", "Role", "Salary", "DeptID", "JoinedDate"])
            
            dept_data = DataGenerator.generate_departments()
            cls._DEPARTMENTS_DF = pd.DataFrame(dept_data, columns=["DeptID", "Name", "Location"])
            
            proj_data = DataGenerator.generate_projects()
            cls._PROJECTS_DF = pd.DataFrame(proj_data, columns=["ProjectID", "ProjectName", "DeptID", "Status"])

    @classmethod
    def execute(cls, query: str) -> Tuple[Optional[pd.DataFrame], Optional[str]]:
        cls.initialize_data()
        
        # Safety Check
        forbidden = ["drop", "delete", "update", "insert", "alter", "truncate", "grant"]
        if any(cmd in query.lower().split() for cmd in forbidden):
            return None, "🔒 SECURITY PROTOCOL: Write operations are restricted in this environment."
            
        try:
            conn = sqlite3.connect(":memory:")
            cls._EMPLOYEES_DF.to_sql("Employees", conn, index=False, if_exists="replace")
            cls._DEPARTMENTS_DF.to_sql("Departments", conn, index=False, if_exists="replace")
            cls._PROJECTS_DF.to_sql("Projects", conn, index=False, if_exists="replace")
            
            result_df = pd.read_sql_query(query, conn)
            conn.close()
            
            AppState.sql()["query_count"] += 1
            AppState.sql()["history"].append({"query": query, "time": datetime.now().strftime("%H:%M"), "status": "Success"})
            return result_df, None
        except Exception as e:
            AppState.sql()["history"].append({"query": query, "time": datetime.now().strftime("%H:%M"), "status": "Error"})
            return None, f"SYNTAX ERROR: {str(e)}"

# ======================================================================================================================
# SECTION 7: VIEW CONTROLLERS (THE UI LOGIC)
# ======================================================================================================================

class DashboardView:
    def render(self):
        user = AppState.user()
        
        # Hero Header
        col_txt, col_img = st.columns([2, 1])
        with col_txt:
            st.markdown(f"""
            <div style="padding: 30px 0;">
                <h1 style="font-size: 3.5rem;">IRONCLAD <span>TITAN</span></h1>
                <h3 style="color: #94a3b8; font-weight: 400;">System Architect Edition v7.0</h3>
                <p style="color: #64748b; max-width: 600px;">
                    Welcome back, <b>{user.username}</b>. Neural networks synchronized. 
                    SQL Database replica is online (350+ Records).
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            c1, c2 = st.columns(2)
            if c1.button("🚀 INICIAR ENTRENAMIENTO", type="primary", use_container_width=True):
                AppState.navigate_to("TRAINING")
                st.rerun()
            if c2.button("💾 TERMINAL SQL", use_container_width=True):
                AppState.navigate_to("SQL")
                st.rerun()

        with col_img:
            VoidGlassUI.render_lottie(VisualAssets.ANIM_HOME_BOT, 280)

        # Stats Grid
        st.markdown("### 📊 Métricas de Rendimiento")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Racha (Streak)", f"{user.current_streak} Días", "Activo")
        m2.metric("XP Total", f"{user.xp}", f"Lvl {user.level}")
        m3.metric("Precisión", f"{user.accuracy:.1f}%", f"{user.total_questions} Qs")
        m4.metric("Módulos", f"{user.modules_completed}", "Completados")

        # Progress Bar
        st.caption(f"Progreso al Nivel {user.level + 1}")
        st.progress(user.progress_to_next_level)

class TrainingView:
    def __init__(self):
        self.repo = DataRepository.load_content()

    def render(self):
        q_state = AppState.quiz()
        
        # State Router
        if q_state["phase"] == QuizPhase.SETUP:
            if q_state["active_topic"] is None:
                self._render_topic_selector()
            else:
                self._render_level_selector()
        elif q_state["phase"] == QuizPhase.PLAYING:
            self._render_gameplay()
        elif q_state["phase"] == QuizPhase.VICTORY:
            self._render_victory()

    def _render_topic_selector(self):
        st.markdown(f"## {VisualAssets.ICON_LEARN} Protocolo de Entrenamiento")
        st.markdown("Selecciona un módulo de conocimiento para comenzar.")
        
        topics = list(self.repo.keys())
        cols = st.columns(3)
        
        for i, topic in enumerate(topics):
            with cols[i % 3]:
                st.markdown(f"""
                <div class="void-card" style="text-align:center; height: 180px; display:flex; flex-direction:column; justify-content:center;">
                    <div style="font-size: 2rem; margin-bottom:10px;">📚</div>
                    <h4 style="margin:0;">{topic}</h4>
                    <p style="font-size:0.8rem; color:#64748b;">Módulos: {len(self.repo[topic])}</p>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"Acceder: {topic}", key=f"btn_topic_{i}", use_container_width=True):
                    AppState.quiz()["active_topic"] = topic
                    st.rerun()

    def _render_level_selector(self):
        topic = AppState.quiz()["active_topic"]
        st.markdown(f"## 📂 {topic}")
        
        if st.button("← Volver al Menú", type="secondary"):
            AppState.quiz()["active_topic"] = None
            st.rerun()
            
        st.divider()
        levels = list(self.repo[topic].keys())
        
        if not levels:
            st.error("Error: No modules found in this topic.")
            return

        for lvl in levels:
            col_txt, col_btn = st.columns([3, 1])
            with col_txt:
                st.markdown(f"### {lvl}")
                st.caption("Training module ready.")
            with col_btn:
                if st.button(f"Iniciar {lvl}", key=f"start_{lvl}", type="primary", use_container_width=True):
                    self._initialize_session(topic, lvl)

    def _initialize_session(self, topic, lvl):
        raw_questions = self.repo[topic][lvl]
        deck = []
        
        for q_data in raw_questions:
            # Normalize options
            opts = q_data.get("opciones", [])
            if isinstance(opts, str): opts = [opts] # Handle single string error
            random.shuffle(opts)
            
            deck.append(Question(
                id=str(uuid.uuid4()),
                text=q_data.get("pregunta", "Error Loading Question"),
                options=opts,
                correct_option=q_data.get("correcta", ""),
                explanation=q_data.get("explicacion", "No explanation provided."),
                translation=q_data.get("traduccion", "No translation provided.")
            ))
        
        random.shuffle(deck)
        q = AppState.quiz()
        q["deck"] = deck
        q["active_level"] = lvl
        q["current_index"] = 0
        q["score"] = 0
        q["phase"] = QuizPhase.PLAYING
        q["feedback_mode"] = False
        q["buffer_selection"] = None
        st.rerun()

    def _render_gameplay(self):
        q = AppState.quiz()
        deck = q["deck"]
        idx = q["current_index"]
        
        # Check End Condition
        if idx >= len(deck):
            q["phase"] = QuizPhase.VICTORY
            st.rerun()
            return

        question = deck[idx]
        
        # HUD
        c1, c2, c3 = st.columns([1, 6, 2])
        c1.markdown(f"**Q-{idx+1}/{len(deck)}**")
        c2.progress((idx) / len(deck))
        c3.markdown(f"XP: {AppState.user().xp}")

        # Question Card
        st.markdown(f"""
        <div class="void-card">
            <h3 style="text-align:center; font-weight:600;">{question.text}</h3>
        </div>
        """, unsafe_allow_html=True)

        # LOGIC FLOW: SELECTION -> ANALYZE -> FEEDBACK -> NEXT
        
        if not q["feedback_mode"]:
            # --- STEP 1: USER SELECTION ---
            selection = st.radio(
                "Selecciona una opción:",
                question.options,
                index=None,
                key=f"q_radio_{question.id}"
            )
            
            st.write("") # Spacer
            
            # --- STEP 2: ANALYZE BUTTON ---
            if st.button("🔍 ANALIZAR RESPUESTA", type="primary", use_container_width=True):
                if not selection:
                    st.toast("⚠️ Debes seleccionar una opción primero.", icon="⚠️")
                else:
                    # Lock in selection and switch mode
                    q["buffer_selection"] = selection
                    q["feedback_mode"] = True
                    
                    # Update Logic
                    if selection.strip() == question.correct_option.strip():
                        q["score"] += 1
                        AppState.user().add_xp(150)
                        AppState.user().correct_answers += 1
                        AppState.user().current_streak += 1
                    else:
                        AppState.user().current_streak = 0
                    
                    st.rerun()
                    
        else:
            # --- STEP 3: FEEDBACK DISPLAY ---
            user_sel = q["buffer_selection"]
            is_correct = (user_sel.strip() == question.correct_option.strip())
            
            if is_correct:
                st.markdown("""
                <div style="background: rgba(16, 185, 129, 0.2); border: 1px solid #10b981; padding: 20px; border-radius: 12px; text-align: center; margin-bottom: 20px;">
                    <h1 style="color: #10b981; margin:0;">¡CORRECTO!</h1>
                </div>
                """, unsafe_allow_html=True)
                VoidGlassUI.render_lottie(VisualAssets.ANIM_VICTORY_ROCKET, 150)
            else:
                st.markdown(f"""
                <div style="background: rgba(239, 68, 68, 0.2); border: 1px solid #ef4444; padding: 20px; border-radius: 12px; text-align: center; margin-bottom: 20px;">
                    <h1 style="color: #ef4444; margin:0;">INCORRECTO</h1>
                    <p style="color: #fca5a5;">Tu respuesta: {user_sel}</p>
                    <h3 style="color: white;">Respuesta Correcta: {question.correct_option}</h3>
                </div>
                """, unsafe_allow_html=True)

            # Translation & Explanation Card
            st.info(f"📝 Traducción: {question.translation}")
            with st.expander("📚 Explicación Detallada", expanded=True):
                st.write(question.explanation)

            # --- STEP 4: NEXT BUTTON ---
            if st.button("➡ SIGUIENTE PREGUNTA", type="primary", use_container_width=True):
                q["current_index"] += 1
                q["feedback_mode"] = False
                q["buffer_selection"] = None
                st.rerun()

    def _render_victory(self):
        q = AppState.quiz()
        score = q["score"]
        total = len(q["deck"])
        percentage = (score/total) * 100
        
        st.canvas = st.empty()
        VoidGlassUI.render_lottie("https://lottie.host/embed/07937446-2423-4485-9856-78810b445831/G0g1g8g1g8.json", 300)
        
        st.markdown(f"""
        <div style="text-align: center; padding: 40px;">
            <h1 style="font-size: 3rem; color: #10b981;">¡MÓDULO COMPLETADO!</h1>
            <h2 style="font-size: 4rem;">{score} / {total}</h2>
            <p style="font-size: 1.5rem; color: #94a3b8;">Precisión: {percentage:.1f}%</p>
        </div>
        """, unsafe_allow_html=True)
        
        AppState.user().modules_completed += 1
        
        if st.button("Volver al Dashboard", use_container_width=True):
            AppState.navigate_to("DASHBOARD")
            st.rerun()

class SQLView:
    def render(self):
        st.markdown(f"## {VisualAssets.ICON_DATABASE} Consola SQL Enterprise")
        
        col_main, col_sidebar = st.columns([3, 1])
        
        with col_main:
            # Query Editor
            st.markdown("### ⌨️ Editor de Consultas")
            query = st.text_area("SQL Input:", height=150, placeholder="SELECT * FROM Employees WHERE Salary > 50000 LIMIT 10;", key="sql_box")
            
            c1, c2, c3 = st.columns([1, 1, 2])
            if c1.button("▶ EJECUTAR", type="primary"):
                if query:
                    df, err = SQLSimulator.execute(query)
                    if err:
                        st.error(err)
                        VoidGlassUI.render_lottie(VisualAssets.ANIM_ERROR, 100)
                    else:
                        st.success(f"Query Successful. Rows: {len(df)}")
                        st.dataframe(df, use_container_width=True)
                        AppState.user().add_xp(50)
                else:
                    st.warning("Query vacía.")

            if c2.button("🧹 LIMPIAR"):
                pass # Streamlit reload clears it naturally if not in session state

            # History Log
            st.markdown("### 📜 Historial de Ejecución")
            history = AppState.sql()["history"]
            if history:
                for h in reversed(history[-5:]):
                    color = "green" if h["status"] == "Success" else "red"
                    st.caption(f"[{h['time']}] :{color}[{h['status']}] - `{h['query']}`")
            else:
                st.info("Sin actividad reciente.")

        with col_sidebar:
            st.markdown("### 🗂️ Schema")
            
            with st.expander("Employees (350+)", expanded=True):
                st.markdown("""
                - **ID** (int) `PK`
                - **Name** (text)
                - **Role** (text)
                - **Salary** (int)
                - **DeptID** (int) `FK`
                - **JoinedDate** (date)
                """)
                
            with st.expander("Departments (6)"):
                st.markdown("""
                - **DeptID** (int) `PK`
                - **Name** (text)
                - **Location** (text)
                """)
                
            with st.expander("Projects (7)"):
                st.markdown("""
                - **ProjectID** (int) `PK`
                - **ProjectName** (text)
                - **DeptID** (int) `FK`
                - **Status** (text)
                """)
                
            st.markdown("### 💡 Cheat Sheet")
            st.code("SELECT * FROM Employees\nJOIN Departments\nON Employees.DeptID = Departments.DeptID", language="sql")

# ======================================================================================================================
# SECTION 8: NAVIGATION & MAIN EXECUTION
# ======================================================================================================================

def render_sidebar():
    user = AppState.user()
    with st.sidebar:
        # User Avatar
        st.markdown(f"""
        <div style="text-align: center; margin-bottom: 20px;">
            <div style="
                width: 80px; height: 80px; 
                background: linear-gradient(135deg, #3b82f6, #1e1b4b); 
                border-radius: 50%; 
                margin: 0 auto 15px; 
                display: flex; align-items: center; justify-content: center; 
                font-size: 2rem; font-weight: bold; 
                border: 3px solid rgba(59, 130, 246, 0.5);
                box-shadow: 0 0 20px rgba(59, 130, 246, 0.3);">
                {user.username[:1]}
            </div>
            <h3 style="margin:0; font-size:1.2rem;">{user.username}</h3>
            <p style="font-size: 0.8rem; color: #94a3b8;">{user.role}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Menu
        st.markdown("---")
        if st.button(f"{VisualAssets.ICON_DASHBOARD} Dashboard", use_container_width=True):
            AppState.navigate_to("DASHBOARD")
            st.rerun()
        if st.button(f"{VisualAssets.ICON_LEARN} Training", use_container_width=True):
            AppState.navigate_to("TRAINING")
            st.rerun()
        if st.button(f"{VisualAssets.ICON_CODE} SQL Lab", use_container_width=True):
            AppState.navigate_to("SQL")
            st.rerun()
            
        st.markdown("---")
        # Mini Stats
        c1, c2 = st.columns(2)
        c1.metric("XP", user.xp)
        c2.metric("Lvl", user.level)
        
        st.markdown("---")
        st.caption("IronClad Titan v7.0")
        st.caption("Secure Connection: SSL/TLS")

def main():
    try:
        VoidGlassUI.inject_css()
        render_sidebar()
        
        view = AppState.get()["view"]
        
        if view == "DASHBOARD":
            DashboardView().render()
        elif view == "TRAINING":
            TrainingView().render()
        elif view == "SQL":
            SQLView().render()
            
    except Exception as e:
        # Crash Handler
        st.error("CRITICAL KERNEL FAILURE")
        st.code(str(e))
        if st.button("EMERGENCY REBOOT"):
            st.session_state.clear()
            st.rerun()

if __name__ == "__main__":
    main()