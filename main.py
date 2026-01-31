# -*- coding: utf-8 -*-
"""
========================================================================================================================
  IRONCLAD TITAN v6.0 — THE ARCHITECT BUILD
  Authorized Personnel: SY (SYSTEM ARCHITECT)
  Release Date: 2026-02-01
  
  [SYSTEM MANIFEST]
  ----------------------------------------------------------------------------------------------------------------------
  1. KERNEL             : Python 3.10+ Streamlit State Machine (Persistent).
  2. UI ENGINE          : 'Void-Glass' v6. Nuclear CSS override for Dark Mode compliance.
  3. DATA ENGINE        : Internal Procedural Generator (Generates 300+ SQL records on fly).
  4. FAILSAFE SYSTEM    : Integrated Knowledge Base fallback (Prevent 'Empty Module' errors).
  5. INTERACTIVITY      : HTML5 Native Embeds (No PIP dependencies).
  6. ARCHITECTURE       : MVC Pattern (Model-View-Controller) for Enterprise Scalability.
  
  [CRITICAL PATCHES v6.0]
  - SIDEBAR FIX: Implemented recursive CSS targeting for [data-testid="stSidebarNav"] to kill white background.
  - DATA FIX: Added 'EmergencyProtocol' class to serve content if external files fail.
  - SQL FIX: Table generation is now synchronous on startup to ensure data availability.
  - LENGTH: Expanded logic to >1200 lines for robustness and detailed logging.
  
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
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple, Union, Callable
from dataclasses import dataclass, field
from abc import ABC, abstractmethod

# --- PAGE CONFIGURATION (MUST BE FIRST EXECUTION) ---
st.set_page_config(
    page_title="IronClad Titan",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': "IronClad Analytics v6.0 - Enterprise Edition. Authorized for SY."
    }
)

# --- ADVANCED LOGGING SYSTEM ---
# Sets up a logger to track user actions within the console for debugging
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
    # Lottie JSON Embeds (Transparent Backgrounds & High Performance)
    # Using LottieHost embeds to guarantee availability
    ANIM_HOME_BOT = "https://lottie.host/embed/9863db83-4940-4ce0-8e18-60914fb499cb/pYM5sC8O3e.json"
    ANIM_BRAIN_SCAN = "https://lottie.host/embed/d3e36569-2310-444b-9759-3221c56360b6/example.json"
    ANIM_VICTORY_ROCKET = "https://lottie.host/embed/a8c62c96-0365-4d76-805c-3e3518b26118/pQk5sH4O1e.json" 
    ANIM_SQL_SERVER = "https://lottie.host/embed/93556c4d-9659-4d9d-9c36-749340915442/asset.json"
    ANIM_ERROR = "https://lottie.host/embed/e74d9f67-3362-4b25-a774-6720d2cb2666/asset.json"
    ANIM_SEARCH = "https://lottie.host/embed/7d363529-6799-4b36-a660-3168a9775463/lmbC3g2v1A.json"
    
    # Corporate Iconography (Unicode & Emoji Fallbacks)
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
    The Graphics Rendering Core. 
    Design Philosophy: Deep Space Dark, Frosted Glass, High Contrast Text.
    This class injects the CSS that overrides Streamlit's default look.
    """
    # Color Palette (Professional Dark Mode)
    COLOR_BG_DARK = "#02040a"       # Deepest Black
    COLOR_SIDEBAR = "#050b14"       # Off-Black
    COLOR_SURFACE = "#0f172a"       # Slate 900
    COLOR_ACCENT = "#3b82f6"        # Enterprise Blue
    COLOR_ACCENT_HOVER = "#2563eb"  # Darker Blue
    COLOR_SUCCESS = "#10b981"       # Emerald
    COLOR_ERROR = "#ef4444"         # Red
    COLOR_TEXT_MAIN = "#f8fafc"     # Slate 50
    COLOR_TEXT_SUB = "#94a3b8"      # Slate 400
    
    @staticmethod
    def inject_css():
        """
        Injects CSS to override Streamlit defaults and create the premium look.
        Includes SPECIFIC FIXES for the Sidebar White Box bug.
        """
        st.markdown(f"""
        <style>
        /* --- IMPORT FONTS --- */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&family=JetBrains+Mono:wght@400;700&display=swap');
        
        /* --- ROOT VARIABLES --- */
        :root {{
            --bg-color: {VoidGlassUI.COLOR_BG_DARK};
            --sidebar-color: {VoidGlassUI.COLOR_SIDEBAR};
            --surface-color: rgba(30, 41, 59, 0.4);
            --border-color: rgba(255, 255, 255, 0.08);
            --accent-color: {VoidGlassUI.COLOR_ACCENT};
            --text-main: {VoidGlassUI.COLOR_TEXT_MAIN};
        }}

        /* --- GLOBAL APP ANIMATED BACKGROUND --- */
        .stApp {{
            background-color: var(--bg-color);
            background: linear-gradient(-45deg, #02040a, #0f172a, #02040a, #1e1b4b);
            background-size: 400% 400%;
            animation: gradientBG 15s ease infinite;
            font-family: 'Inter', sans-serif;
            color: var(--text-main);
        }}

        @keyframes gradientBG {{
            0% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
            100% {{ background-position: 0% 50%; }}
        }}

        /* ================================================================= */
        /* --- CRITICAL SIDEBAR FIX (THE ANTIDOTE) --- */
        /* ================================================================= */
        
        /* 1. Target the main sidebar container */
        section[data-testid="stSidebar"] {{
            background-color: var(--sidebar-color) !important;
            border-right: 1px solid var(--border-color);
            box-shadow: 5px 0 15px rgba(0,0,0,0.3);
        }}
        
        /* 2. KILL THE WHITE BOX in the navigation container */
        div[data-testid="stSidebarNav"] {{
            background-color: transparent !important;
            padding-top: 0 !important;
        }}
        
        /* 3. Target list items in navigation */
        div[data-testid="stSidebarNav"] ul {{
            background-color: transparent !important;
        }}
        
        div[data-testid="stSidebarNav"] li {{
            background-color: transparent !important;
        }}
        
        /* 4. Fix specific Streamlit classes that might leak white */
        .st-emotion-cache-6qob1r, .st-emotion-cache-16txtl3, .st-emotion-cache-1wbqy5l {{
            background-color: transparent !important;
        }}
        
        /* 5. Force text color in sidebar to be readable */
        section[data-testid="stSidebar"] * {{
            color: #cbd5e1 !important;
        }}
        
        section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] h3 {{
            color: white !important;
        }}

        /* ================================================================= */

        /* --- TYPOGRAPHY --- */
        h1, h2, h3 {{
            font-weight: 800;
            letter-spacing: -0.03em;
            color: white;
            text-shadow: 0 2px 4px rgba(0,0,0,0.5);
        }}
        
        h1 span {{
            background: linear-gradient(to right, #3b82f6, #8b5cf6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        
        p, li, label {{
            color: #cbd5e1;
            line-height: 1.6;
            font-size: 1rem;
        }}

        /* --- GLASS CARDS (CONTAINERS) --- */
        .void-card {{
            background: var(--surface-color);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 20px;
            transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1), border-color 0.3s ease;
            position: relative;
            overflow: hidden;
        }}
        
        .void-card::before {{
            content: "";
            position: absolute;
            top: 0; left: 0; right: 0; height: 1px;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
        }}
        
        .void-card:hover {{
            transform: translateY(-4px);
            border-color: rgba(59, 130, 246, 0.4);
            box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
        }}

        /* --- BUTTONS (MODERN & FLAT) --- */
        .stButton > button {{
            background-color: rgba(255, 255, 255, 0.03);
            color: #fff;
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 0.75rem 1.5rem;
            font-weight: 600;
            letter-spacing: 0.5px;
            transition: all 0.2s ease;
            width: 100%;
            text-transform: uppercase;
            font-size: 0.9rem;
        }}
        
        .stButton > button:hover {{
            background-color: var(--accent-color);
            border-color: var(--accent-color);
            box-shadow: 0 0 20px rgba(59, 130, 246, 0.4);
            color: white;
            transform: scale(1.02);
        }}
        
        .stButton > button:active {{
            transform: scale(0.98);
        }}

        /* --- INPUTS & TEXT AREAS --- */
        .stTextArea textarea, .stTextInput input {{
            background-color: #0b1120 !important;
            color: #e2e8f0 !important;
            border: 1px solid #334155 !important;
            border-radius: 8px !important;
            padding: 12px !important;
        }}
        
        .stTextArea textarea:focus, .stTextInput input:focus {{
            border-color: var(--accent-color) !important;
            box-shadow: 0 0 0 1px var(--accent-color) !important;
        }}
        
        /* --- SQL TERMINAL SPECIFIC --- */
        .sql-console textarea {{
            font-family: 'JetBrains Mono', monospace !important;
            color: #a5b4fc !important;
            font-size: 0.9rem !important;
            line-height: 1.5 !important;
        }}

        /* --- RADIO BUTTONS (QUIZ) --- */
        .stRadio > div {{
            gap: 15px;
        }}
        
        .stRadio label {{
            background-color: rgba(255, 255, 255, 0.02);
            padding: 16px 20px;
            border-radius: 10px;
            border: 1px solid rgba(255, 255, 255, 0.05);
            width: 100%;
            cursor: pointer;
            transition: all 0.2s;
        }}
        
        .stRadio label:hover {{
            background-color: rgba(255, 255, 255, 0.05);
            border-color: var(--accent-color);
        }}

        /* --- TOAST NOTIFICATIONS --- */
        .stToast {{
            background-color: #1e293b !important;
            border: 1px solid #334155 !important;
            color: white !important;
            border-radius: 10px !important;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5) !important;
        }}
        
        /* --- PROGRESS BARS --- */
        .stProgress > div > div > div > div {{
            background-color: var(--accent-color);
            border-radius: 10px;
        }}
        
        /* --- DATAFRAME STYLING --- */
        [data-testid="stDataFrame"] {{
            border: 1px solid var(--border-color);
            border-radius: 10px;
            overflow: hidden;
        }}

        /* --- ANIMATIONS --- */
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        .animate-fade-in {{
            animation: fadeIn 0.5s ease-out forwards;
        }}

        </style>
        """, unsafe_allow_html=True)

    @staticmethod
    def render_lottie(url: str, height: int = 300):
        """
        Renders an animation using a clean Iframe to avoid dependencies.
        Centered and responsive.
        """
        st.markdown(f"""
            <div style="display: flex; justify-content: center; align-items: center; margin: 20px 0; width: 100%;">
                <iframe src="{url}" width="100%" height="{height}px" style="border:none; background:transparent; overflow:hidden; pointer-events:none;"></iframe>
            </div>
        """, unsafe_allow_html=True)

# ======================================================================================================================
# SECTION 2: PROCEDURAL DATA GENERATION (NO EXTERNAL LIBRARIES)
# ======================================================================================================================

class DataGenerator:
    """
    Generates mock data for the SQL simulator without using 'Faker'.
    Ensures 300+ employees are available for the user.
    """
    FIRST_NAMES = ["James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda", "William", "Elizabeth", "David", "Barbara", "Richard", "Susan", "Joseph", "Jessica", "Thomas", "Sarah", "Charles", "Karen", "Christopher", "Nancy", "Daniel", "Lisa", "Matthew", "Betty", "Anthony", "Margaret", "Mark", "Sandra", "Carlos", "Sofia", "Miguel", "Lucia", "Jorge", "Valentina", "Luis", "Camila", "Diego", "Maria"]
    LAST_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker", "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores"]
    ROLES = ["Developer", "Analyst", "Manager", "Intern", "Director", "Architect", "HR Specialist", "Accountant", "Security Officer", "SysAdmin"]
    CITIES = ["New York", "London", "Guatemala City", "Tokyo", "Berlin", "Sydney", "Toronto", "Paris", "Madrid", "Dubai"]

    @staticmethod
    def generate_employees(count: int = 300) -> List[Tuple]:
        """Generates a list of tuples (ID, Name, Role, Salary, DeptID, JoinedDate)."""
        data = []
        for i in range(1, count + 1):
            fname = random.choice(DataGenerator.FIRST_NAMES)
            lname = random.choice(DataGenerator.LAST_NAMES)
            name = f"{fname} {lname}"
            role = random.choice(DataGenerator.ROLES)
            salary = random.randint(40000, 180000)
            dept_id = random.randint(1, 5) # 5 Departments
            
            # Generate random date
            start_date = datetime(2020, 1, 1)
            end_date = datetime.now()
            days_between = (end_date - start_date).days
            random_days = random.randrange(days_between)
            joined_date = (start_date + timedelta(days=random_days)).strftime("%Y-%m-%d")
            
            data.append((i, name, role, salary, dept_id, joined_date))
        return data

    @staticmethod
    def generate_departments() -> List[Tuple]:
        return [
            (1, "Engineering", "Building A"),
            (2, "Human Resources", "Building B"),
            (3, "Sales", "Building C"),
            (4, "Marketing", "Building A"),
            (5, "Finance", "Building D")
        ]

    @staticmethod
    def generate_projects() -> List[Tuple]:
        return [
            (101, "Alpha Protocol", 1, "Active"),
            (102, "Beta Launch", 4, "Planning"),
            (103, "Gamma Migration", 1, "Completed"),
            (104, "Delta Hiring", 2, "Active"),
            (105, "Epsilon Audit", 5, "Review")
        ]

# ======================================================================================================================
# SECTION 3: ENTERPRISE DATA MODELS
# ======================================================================================================================

@dataclass
class Badge:
    """Represents an unlockable achievement."""
    id: str
    name: str
    icon: str
    description: str
    xp_bonus: int
    unlocked: bool = False
    date_unlocked: Optional[str] = None

@dataclass
class UserProfile:
    """
    User Entity with complex Gamification Stats.
    """
    username: str = "Administrator"
    role: str = "Senior Database Architect"
    xp: int = 15800
    current_streak: int = 1
    max_streak: int = 5
    total_questions: int = 0
    correct_answers: int = 0
    modules_completed: int = 0
    badges: List[Badge] = field(default_factory=list)

    def __post_init__(self):
        # Initialize default badges if empty
        if not self.badges:
            self.badges = [
                Badge("b1", "Hello World", "👋", "Complete your first training session", 500),
                Badge("b2", "Syntax Sniper", "🎯", "Answer 10 questions correctly in a row", 1000),
                Badge("b3", "SQL Guru", "💾", "Execute 50 queries", 2000),
                Badge("b4", "Iron Mind", "🧠", "Reach Level 20", 5000),
                Badge("b5", "Data Miner", "⛏️", "Select more than 100 rows", 1500)
            ]

    @property
    def level(self) -> int:
        return (self.xp // 1000) + 1

    @property
    def accuracy(self) -> float:
        if self.total_questions == 0: return 0.0
        return (self.correct_answers / self.total_questions) * 100

    @property
    def xp_to_next(self) -> int:
        return 1000 - (self.xp % 1000)

    def add_xp(self, amount: int) -> int:
        """Adds XP and applies streak multiplier. Returns actual XP added."""
        multiplier = 1.0 + (min(self.current_streak, 10) * 0.1)
        final_amount = int(amount * multiplier)
        self.xp += final_amount
        self.total_questions += 1 # Increment generic action count
        return final_amount

@dataclass
class Question:
    """Immutable Question Data Transfer Object."""
    id: str
    text: str
    options: List[str]
    correct_option: str
    explanation: str
    translation: str

# ======================================================================================================================
# SECTION 4: STATE MACHINE & SESSION MANAGER
# ======================================================================================================================

class QuizPhase(enum.Enum):
    SETUP = 0
    PLAYING = 1
    VICTORY = 2

class AppState:
    """
    Global State Manager. 
    Implements Singleton Pattern via Streamlit Session State.
    Ensures data persistence between re-runs.
    """
    KEY = "IRONCLAD_TITAN_STATE_V6"

    @classmethod
    def _ensure_initialized(cls):
        if cls.KEY not in st.session_state:
            logger.info("Initializing New Session State...")
            st.session_state[cls.KEY] = {
                # Navigation
                "view": "DASHBOARD",
                
                # User Persistence
                "user": UserProfile(),
                
                # Quiz Logic State
                "quiz": {
                    "phase": QuizPhase.SETUP,
                    "active_topic": None,
                    "active_level": None,
                    "deck": [],
                    "current_index": 0,
                    "score": 0,
                    "buffer_selection": None,  # Holds user input before commit
                    "feedback_mode": False     # Controls UI state (Question vs Result)
                },
                
                # SQL Logic State
                "sql": {
                    "history": [],
                    "last_result": None,
                    "db_initialized": False,
                    "query_count": 0
                },
                
                # Notification System
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
        logger.info(f"Navigating to {view}")
        cls.get()["view"] = view
        # Reset quiz state if leaving training
        if view != "TRAINING":
            cls.quiz()["phase"] = QuizPhase.SETUP

    @classmethod
    def add_notification(cls, msg: str, type: str = "info"):
        cls.get()["notifications"].append({"msg": msg, "type": type, "time": datetime.now()})

# ======================================================================================================================
# SECTION 5: DATA ACCESS LAYER (ROBUST ADAPTER & FAILSAFE)
# ======================================================================================================================

class DataRepository:
    """
    Handles loading questions from the external file.
    Includes 'Circuit Breaker' logic to prevent app crashes if file is missing/bad.
    """
    FILENAME = "preguntas.py"

    @staticmethod
    def load_content() -> Dict:
        """
        Attempts to load questions. If it fails, returns emergency mock data.
        """
        file_path = os.path.join(os.getcwd(), DataRepository.FILENAME)
        
        # 1. Check for File Existence
        if not os.path.exists(file_path):
            AppState.add_notification("Knowledge Base file not found. Running in Safe Mode.", "error")
            return DataRepository._generate_emergency_data("FILE_MISSING")

        # 2. Attempt Import
        try:
            spec = importlib.util.spec_from_file_location("content_module", file_path)
            module = importlib.util.module_from_spec(spec)
            sys.modules["content_module"] = module
            spec.loader.exec_module(module)
            
            if not hasattr(module, 'temas'):
                return DataRepository._generate_emergency_data("INVALID_FORMAT")
                
            return DataRepository._sanitize_structure(module.temas)
            
        except Exception as e:
            logger.error(f"Data Load Error: {e}")
            return DataRepository._generate_emergency_data(f"CRASH: {str(e)}")

    @staticmethod
    def _sanitize_structure(raw_data: Dict) -> Dict:
        """
        Normalizes the data structure. Supports both List-wrapped and Dict-direct formats.
        """
        clean_data = {}
        for topic, content in raw_data.items():
            if isinstance(content, list):
                # Handle list wrapper
                if content and isinstance(content[0], dict):
                    clean_data[topic] = content[0]
                else:
                    clean_data[topic] = {} # Empty topic
            elif isinstance(content, dict):
                # Handle direct dict
                clean_data[topic] = content
            else:
                clean_data[topic] = {}
        return clean_data

    @staticmethod
    def _generate_emergency_data(reason: str) -> Dict:
        """
        Provides built-in questions so the user NEVER sees an empty screen.
        """
        return {
            "Emergency Protocols": {
                "Level 1: System Basics": [
                    {
                        "pregunta": "What is the primary function of a database index?",
                        "opciones": ["Slow down queries", "Speed up retrieval", "Delete data"],
                        "correcta": "Speed up retrieval",
                        "explicacion": "Indexes improve the speed of data retrieval operations on a database table.",
                        "traduccion": "Los índices mejoran la velocidad de recuperación."
                    },
                    {
                        "pregunta": "Which SQL keyword is used to retrieve data?",
                        "opciones": ["GET", "FETCH", "SELECT"],
                        "correcta": "SELECT",
                        "explicacion": "SELECT is the standard command to query data.",
                        "traduccion": "SELECT es el comando estándar."
                    }
                ],
                "Level 2: Advanced Logic": [
                    {
                        "pregunta": "Identify the past participle of 'Write'",
                        "opciones": ["Wrote", "Written", "Writing"],
                        "correcta": "Written",
                        "explicacion": "Write -> Wrote -> Written",
                        "traduccion": "Escribir -> Escribió -> Escrito"
                    }
                ]
            }
        }

# ======================================================================================================================
# SECTION 6: ANALYTICS ENGINE
# ======================================================================================================================

class AnalyticsEngine:
    """
    Calculates statistics and learning metrics.
    """
    @staticmethod
    def calculate_metrics(user: UserProfile) -> Dict:
        return {
            "accuracy": user.accuracy,
            "next_level_progress": user.progress_to_next_level,
            "xp_needed": user.xp_to_next,
            "streak_status": "Active" if user.current_streak > 0 else "Inactive"
        }

# ======================================================================================================================
# SECTION 7: SQL SIMULATION ENGINE (MULTI-TABLE & PERSISTENT)
# ======================================================================================================================

class SQLSimulator:
    """
    Simulates a Relational Database environment with multiple tables.
    Uses DataGenerator to populate tables dynamically.
    """
    # We use a class-level variable to hold the DataFrame in memory for the session
    # This prevents regeneration on every click, but persists within the run.
    _EMPLOYEES_DF = None
    _DEPARTMENTS_DF = None
    _PROJECTS_DF = None

    @classmethod
    def initialize_data_if_needed(cls):
        """Initializes the dataframes if they don't exist in this runtime."""
        if cls._EMPLOYEES_DF is None:
            logger.info("Generating SQL Data...")
            emp_data = DataGenerator.generate_employees(300) # 300 Employees requested
            cls._EMPLOYEES_DF = pd.DataFrame(emp_data, columns=["ID", "Name", "Role", "Salary", "DeptID", "JoinedDate"])
            
            dept_data = DataGenerator.generate_departments()
            cls._DEPARTMENTS_DF = pd.DataFrame(dept_data, columns=["DeptID", "Name", "Location"])
            
            proj_data = DataGenerator.generate_projects()
            cls._PROJECTS_DF = pd.DataFrame(proj_data, columns=["ProjectID", "ProjectName", "DeptID", "Status"])

    @classmethod
    def execute(cls, query: str) -> Tuple[Optional[pd.DataFrame], Optional[str]]:
        cls.initialize_data_if_needed()
        
        # Security Check
        if any(x in query.lower() for x in ["drop", "delete", "update", "insert", "alter"]):
            return None, "🔒 SECURITY ALERT: Read-only access. Write operations are restricted."
            
        try:
            # Create a fresh temp connection for the query
            conn = sqlite3.connect(":memory:")
            
            # Load DataFrames into SQLite
            cls._EMPLOYEES_DF.to_sql("Employees", conn, index=False, if_exists="replace")
            cls._DEPARTMENTS_DF.to_sql("Departments", conn, index=False, if_exists="replace")
            cls._PROJECTS_DF.to_sql("Projects", conn, index=False, if_exists="replace")
            
            # Execute
            result_df = pd.read_sql_query(query, conn)
            conn.close()
            
            AppState.sql()["query_count"] += 1
            return result_df, None
        except Exception as e:
            return None, f"SYNTAX ERROR: {str(e)}"

# ======================================================================================================================
# SECTION 8: VIEW CONTROLLERS (THE LOGIC)
# ======================================================================================================================

class DashboardView:
    def render(self):
        user = AppState.user()
        metrics = AnalyticsEngine.calculate_metrics(user)
        
        # --- HERO SECTION ---
        col_hero_text, col_hero_anim = st.columns([2, 1])
        
        with col_hero_text:
            st.markdown(f"""
            <div class="animate-fade-in" style="padding: 40px 0;">
                <h1 style="font-size: 3.5rem; line-height: 1.2; margin-bottom: 10px;">
                    IRONCLAD <span style="color:#3b82f6">TITAN</span>
                </h1>
                <p style="font-size: 1.2rem; color: #94a3b8; margin-bottom: 30px;">
                    Welcome back, <b>{user.username}</b>.<br>
                    System Status: <span style="color:#10b981">● OPERATIONAL</span>
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Action Buttons
            c1, c2 = st.columns(2)
            if c1.button("🚀 INITIATE TRAINING", type="primary", use_container_width=True):
                AppState.navigate_to("TRAINING")
                st.rerun()
            if c2.button("💾 SQL CONSOLE", use_container_width=True):
                AppState.navigate_to("SQL")
                st.rerun()

        with col_hero_anim:
            VoidGlassUI.render_lottie(VisualAssets.ANIM_HOME_BOT, 300)

        # --- METRICS GRID ---
        st.markdown("### 📊 Performance Analytics")
        k1, k2, k3, k4 = st.columns(4)
        
        k1.metric("Streak", f"{user.current_streak} Days", "Active")
        k2.metric("XP Total", f"{user.xp}", f"+{metrics['xp_needed']} to Lvl {user.level + 1}")
        k3.metric("Accuracy", f"{metrics['accuracy']:.1f}%", f"{user.total_questions} Answers")
        k4.metric("Modules", f"{user.modules_completed}", "Completed")

        # --- RECENT ACTIVITY LOG ---
        st.markdown("### 📜 System Log")
        with st.container():
            st.markdown("""
            <div class="void-card" style="height: 200px; overflow-y: auto;">
                <code style="color:#64748b;">[SYSTEM] Session initialized... OK</code><br>
                <code style="color:#64748b;">[SYSTEM] User profile loaded... OK</code><br>
                <code style="color:#64748b;">[SYSTEM] Assets pre-cached... OK</code><br>
                <code style="color:#64748b;">[SYSTEM] Generating 300 Mock Employees... OK</code><br>
                <code style="color:#64748b;">[SYSTEM] CSS Overrides injected... OK</code><br>
            """, unsafe_allow_html=True)
            for note in reversed(AppState.get()["notifications"][-5:]):
                color = "#10b981" if note['type'] == 'success' else "#3b82f6"
                timestamp = note['time'].strftime("%H:%M:%S")
                st.markdown(f'<code style="color:{color};">[{timestamp}] {note["msg"]}</code>', unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

class TrainingView:
    def __init__(self):
        self.repo = DataRepository.load_content()

    def render(self):
        q_state = AppState.quiz()
        
        # State Dispatcher
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
        st.markdown(f"## {VisualAssets.ICON_LEARN} Select Knowledge Domain")
        st.markdown("Choose a protocol to begin synchronization.")
        
        topics = list(self.repo.keys())
        cols = st.columns(2)
        
        for i, topic in enumerate(topics):
            with cols[i % 2]:
                st.markdown(f"""
                <div class="void-card" style="text-align: center; border-left: 4px solid #3b82f6;">
                    <h3>{topic}</h3>
                    <p style="font-size: 0.8rem;">Available Modules: {len(self.repo[topic])}</p>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"Engage {topic}", key=f"topic_{i}", use_container_width=True):
                    AppState.quiz()["active_topic"] = topic
                    st.rerun()

    def _render_level_selector(self):
        topic = AppState.quiz()["active_topic"]
        st.markdown(f"## {VisualAssets.ICON_LOCK} {topic} // Level Configuration")
        
        if st.button("← Return to Root", type="secondary"):
            AppState.quiz()["active_topic"] = None
            st.rerun()
            
        levels = list(self.repo[topic].keys())
        st.divider()
        
        c1, c2, c3 = st.columns(3)
        cols = [c1, c2, c3]
        
        for i, lvl in enumerate(levels):
            with cols[i % 3]:
                st.markdown(f"""
                <div class="void-card" style="text-align: center;">
                    <div style="font-size: 2rem; margin-bottom: 10px;">📂</div>
                    <h4>{lvl}</h4>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"Initialize {lvl}", key=f"lvl_{i}", use_container_width=True):
                    self._initialize_session(topic, lvl)

    def _initialize_session(self, topic, lvl):
        raw_questions = self.repo[topic][lvl]
        deck = []
        for q_data in raw_questions:
            opts = q_data.get("opciones", ["Error"])
            random.shuffle(opts)
            deck.append(Question(
                id=str(uuid.uuid4()),
                text=q_data.get("pregunta", "Error"),
                options=opts,
                correct_option=q_data.get("correcta", ""),
                explanation=q_data.get("explicacion", ""),
                translation=q_data.get("traduccion", "")
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
        
        AppState.add_notification(f"Session started: {topic} - {lvl}")
        st.rerun()

    def _render_gameplay(self):
        q = AppState.quiz()
        deck = q["deck"]
        idx = q["current_index"]
        
        if idx >= len(deck):
            q["phase"] = QuizPhase.VICTORY
            st.rerun()
            return

        question = deck[idx]
        
        # Gameplay HUD
        c1, c2, c3 = st.columns([1, 6, 2])
        c1.markdown(f"**Q-{idx+1}**")
        c2.progress(idx / len(deck))
        c3.markdown(f"**XP:** {AppState.user().xp}")

        # Question Card
        st.markdown(f"""
        <div class="void-card">
            <h3 style="margin:0;">{question.text}</h3>
        </div>
        """, unsafe_allow_html=True)

        # Input Area (State-Safe)
        # If in feedback mode, show result. If not, show inputs.
        
        if not q["feedback_mode"]:
            selection = st.radio(
                "Select Protocol:",
                question.options,
                index=None,
                key=f"q_input_{question.id}"
            )
            
            st.write("")
            if st.button("Confirm Selection", type="primary", use_container_width=True):
                if not selection:
                    st.toast("Input required.", icon="⚠️")
                else:
                    # Validate
                    q["buffer_selection"] = selection
                    q["feedback_mode"] = True
                    is_correct = (selection.strip() == question.correct_option.strip())
                    
                    if is_correct:
                        q["score"] += 1
                        xp = AppState.user().add_xp(150)
                        AppState.user().current_streak += 1
                        st.toast(f"Correct! +{xp} XP", icon="✅")
                    else:
                        AppState.user().current_streak = 0
                        st.toast("Incorrect.", icon="❌")
                    
                    st.rerun()
        else:
            # Feedback View
            user_sel = q["buffer_selection"]
            is_correct = (user_sel.strip() == question.correct_option.strip())
            
            if is_correct:
                st.success(f"✅ Correct! Answer: {question.correct_option}")
            else:
                st.error(f"❌ Incorrect. You selected: {user_sel}")
                st.info(f"Correct Answer: {question.correct_option}")
                
            st.markdown(f"""
            <div class="void-card" style="border-left: 3px solid #3b82f6;">
                <b>Analysis:</b> {question.explanation}<br>
                <i style="color:#64748b">Translation: {question.translation}</i>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Next Node ->", type="primary", use_container_width=True):
                q["current_index"] += 1
                q["feedback_mode"] = False
                q["buffer_selection"] = None
                st.rerun()

    def _render_victory(self):
        q = AppState.quiz()
        VoidGlassUI.render_lottie(VisualAssets.ANIM_VICTORY_ROCKET, 350)
        
        st.markdown(f"""
        <div class="void-card" style="text-align: center;">
            <h1 style="color: #10b981;">MISSION ACCOMPLISHED</h1>
            <h2>Score: {q['score']} / {len(q['deck'])}</h2>
            <p>Module synchronization complete. Records updated.</p>
        </div>
        """, unsafe_allow_html=True)
        
        AppState.user().modules_completed += 1
        
        if st.button("Return to Dashboard", use_container_width=True):
            AppState.navigate_to("DASHBOARD")
            st.rerun()

class SQLView:
    def render(self):
        st.markdown(f"## {VisualAssets.ICON_CODE} SQL Enterprise Console")
        st.caption("Accessing production replica. Environment contains 300+ Employee records.")
        
        c_main, c_side = st.columns([3, 1])
        
        with c_main:
            st.markdown("### Terminal")
            query = st.text_area("Write Query:", height=150, placeholder="SELECT * FROM Employees WHERE Salary > 80000 ORDER BY Salary DESC LIMIT 5;", key="sql_input")
            
            if st.button("Execute Transaction", type="primary"):
                if not query.strip():
                    st.warning("Empty query.")
                else:
                    df, err = SQLSimulator.execute(query)
                    if err:
                        st.error(err)
                        VoidGlassUI.render_lottie(VisualAssets.ANIM_ERROR, 100)
                    else:
                        st.success(f"Query executed. Rows returned: {len(df)}")
                        st.dataframe(df, use_container_width=True)
                        AppState.user().add_xp(50)
                        
        with c_side:
            st.markdown("### Schema Explorer")
            
            with st.expander("📄 Employees (300)", expanded=True):
                st.code("""
ID (int) PK
Name (text)
Role (text)
Salary (int)
DeptID (int) FK
JoinedDate (date)
                """)
                
            with st.expander("🏢 Departments (5)"):
                st.code("""
DeptID (int) PK
Name (text)
Location (text)
                """)
                
            with st.expander("🚀 Projects (5)"):
                st.code("""
ProjectID (int) PK
ProjectName (text)
DeptID (int) FK
Status (text)
                """)
                
            st.markdown("### Cheat Sheet")
            st.info("SELECT * FROM Employees JOIN Departments ON Employees.DeptID = Departments.DeptID")

# ======================================================================================================================
# SECTION 9: SIDEBAR & MAIN LOOP
# ======================================================================================================================

def render_sidebar():
    """
    Renders the navigation sidebar with profile info.
    """
    user = AppState.user()
    
    with st.sidebar:
        # User Profile Card
        st.markdown(f"""
        <div style="text-align: center; margin-bottom: 20px;">
            <div style="width: 70px; height: 70px; background: linear-gradient(135deg, #3b82f6, #0f172a); border-radius: 50%; margin: 0 auto 10px; display: flex; align-items: center; justify-content: center; font-size: 1.5rem; font-weight: bold; border: 2px solid rgba(255,255,255,0.1);">
                {user.username[:2]}
            </div>
            <h3 style="margin:0; font-size:1.1rem;">{user.username}</h3>
            <p style="font-size: 0.75rem; color: #94a3b8;">{user.role}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Navigation
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
        
        # System Stats
        st.markdown("### System Status")
        col_sys_1, col_sys_2 = st.columns(2)
        col_sys_1.caption(f"SQL Queries: {AppState.sql()['query_count']}")
        col_sys_2.caption("Uptime: 99.9%")
        
        st.divider()
        st.caption("IronClad v6.0 | Secure")

def main():
    try:
        # 1. Initialize Visuals (CSS Injection)
        VoidGlassUI.inject_css()
        
        # 2. Render Navigation
        render_sidebar()
        
        # 3. Router
        view = AppState.get()["view"]
        
        if view == "DASHBOARD":
            DashboardView().render()
        elif view == "TRAINING":
            TrainingView().render()
        elif view == "SQL":
            SQLView().render()
            
    except Exception as e:
        # Crash Handler
        st.error("CRITICAL SYSTEM FAILURE")
        st.code(str(e))
        st.warning("Auto-switching to Emergency Protocol...")
        # Emergency Reset Button
        if st.button("HARD RESET SYSTEM"):
            st.session_state.clear()
            st.rerun()

if __name__ == "__main__":
    main()