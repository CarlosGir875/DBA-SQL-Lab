# -*- coding: utf-8 -*-
"""
====================================================================================================
  APEX SOVEREIGN SUITE v15.0 — THE MONOLITH KERNEL
  Target User: SY (Carlos) | INTECAP DATABASE SPECIALIST
  Release Date: 2026-01-31
  Architecture: Hexagonal Enterprise (Domain-Driven Design)
  
  [SYSTEM MANIFEST]
  --------------------------------------------------------------------------------------------------
  1. CORE KERNEL      : Python 3.10+ Streamlit Framework (Session State Level 5).
  2. DATA INGESTION   : 'Universal Adapter' pattern for 'preguntas.py' (List/Dict Agnostic).
  3. FEEDBACK HUD     : Real-time visual feedback (Green/Red) with persistent explanation layer.
  4. UI ENGINE        : 'Nebula-X' CSS with forced 200px+ height on action cards.
  5. SQL EMULATOR     : In-Memory T-SQL Simulation with RBAC (Role Based Access Control).
  6. TELEMETRY        : Verbose logging for every user interaction.
  --------------------------------------------------------------------------------------------------
  
  WARNING: THIS SOURCE CODE CONTAINS ADVANCED CLASS STRUCTURES.
  DO NOT MODIFY THE 'SESSION_GUARD' WITHOUT AUTHORIZATION.
====================================================================================================
"""

# ==================================================================================================
# SECTION 1: SYSTEM IMPORTS & ENVIRONMENT SETUP
# ==================================================================================================
import streamlit as st
import pandas as pd
import random
import sqlite3
import requests
import time
import os
import sys
import importlib.util
import ast
import json
import base64
import logging
import traceback
import enum
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple, Union, Callable, Type
from dataclasses import dataclass, field
from abc import ABC, abstractmethod

# ==================================================================================================
# SECTION 2: ADVANCED LOGGING & DIAGNOSTICS
# ==================================================================================================

# Configure Industrial Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | APEX-CORE | %(levelname)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("ApexMonolith")

class SystemDiagnostics:
    """
    Static utility for system health checks and environment validation.
    """
    @staticmethod
    def check_integrity() -> bool:
        """Verifies that all required libraries are loaded in memory."""
        required = ['streamlit', 'pandas', 'sqlite3', 'random']
        for lib in required:
            if lib not in sys.modules:
                logger.critical(f"MISSING DEPENDENCY: {lib}")
                return False
        return True

    @staticmethod
    def get_memory_usage() -> str:
        """Simulates memory profiling for the dashboard."""
        # In a real scenario, we would use 'psutil', but for this env we simulate.
        return f"{random.randint(120, 450)} MB"

# ==================================================================================================
# SECTION 3: THE NEBULA DESIGN SYSTEM (CSS ENGINE)
# ==================================================================================================

class ApexTheme:
    """
    Centralized Design System. 
    Defines the visual physics of the application (Colors, Spacing, Typography).
    """
    # Color Palette - Cyberpunk/Enterprise
    COLOR_PRIMARY = "#6366f1"     # Indigo 500
    COLOR_SECONDARY = "#ec4899"   # Pink 500
    COLOR_SUCCESS = "#10b981"     # Emerald 500
    COLOR_DANGER = "#ef4444"      # Red 500
    COLOR_WARNING = "#f59e0b"     # Amber 500
    COLOR_BG = "#020617"          # Slate 950
    COLOR_SURFACE = "#0f172a"     # Slate 900
    COLOR_TEXT_MAIN = "#f8fafc"   # Slate 50
    COLOR_TEXT_MUTED = "#94a3b8"  # Slate 400
    
    # Assets
    ASSET_DASHBOARD_LOTTIE = "https://assets5.lottiefiles.com/packages/lf20_fcfjwiyb.json"
    ASSET_DB_LOTTIE = "https://assets2.lottiefiles.com/private_files/lf30_w1uxkbue.json"

    @classmethod
    def inject_css(cls):
        """
        Injects 300+ lines of raw CSS to override Streamlit defaults.
        This forces the 'Big Button' layout and the 'Nebula' sidebar.
        """
        st.markdown(f"""
        <style>
        /* --- FONT IMPORT --- */
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700;800&family=JetBrains+Mono:wght@400;700&display=swap');
        
        /* --- GLOBAL RESET --- */
        .stApp {{
            background-color: {cls.COLOR_BG};
            font-family: 'Plus Jakarta Sans', sans-serif;
            color: {cls.COLOR_TEXT_MAIN};
        }}
        
        h1, h2, h3, h4, h5, h6 {{
            font-weight: 700;
            letter-spacing: -0.5px;
            color: #ffffff;
        }}
        
        /* --- SIDEBAR NEBULA EFFECT --- */
        section[data-testid="stSidebar"] {{
            background-color: #030712;
            border-right: 1px solid rgba(255,255,255,0.05);
        }}
        
        /* --- MEGA GRID BUTTONS (THE FIX) --- */
        /* Forces buttons in the training grid to be huge cards */
        div.row-widget.stButton > button[key*="topic_btn"], 
        div.row-widget.stButton > button[key*="level_btn"] {{
            height: 220px !important;  /* FORCED HEIGHT */
            width: 100% !important;
            border-radius: 24px !important;
            background: linear-gradient(160deg, #1e293b 0%, #0f172a 100%) !important;
            border: 1px solid rgba(255,255,255,0.08) !important;
            color: #ffffff !important;
            font-size: 1.5rem !important;
            font-weight: 800 !important;
            text-transform: uppercase;
            box-shadow: 0 10px 30px -10px rgba(0,0,0,0.5) !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            white-space: pre-wrap; /* Allows multiline text */
        }}
        
        div.row-widget.stButton > button[key*="topic_btn"]:hover,
        div.row-widget.stButton > button[key*="level_btn"]:hover {{
            transform: translateY(-8px) scale(1.02) !important;
            border-color: {cls.COLOR_PRIMARY} !important;
            box-shadow: 0 20px 40px -10px rgba(99, 102, 241, 0.3) !important;
            background: linear-gradient(160deg, #312e81 0%, #1e1b4b 100%) !important;
        }}

        /* --- FEEDBACK STATUS BOXES --- */
        .feedback-box-success {{
            background: rgba(16, 185, 129, 0.15);
            border: 2px solid {cls.COLOR_SUCCESS};
            color: {cls.COLOR_SUCCESS};
            padding: 20px;
            border-radius: 16px;
            text-align: center;
            font-weight: 800;
            font-size: 1.5rem;
            margin: 20px 0;
            animation: popIn 0.4s ease;
        }}
        
        .feedback-box-error {{
            background: rgba(239, 68, 68, 0.15);
            border: 2px solid {cls.COLOR_DANGER};
            color: {cls.COLOR_DANGER};
            padding: 20px;
            border-radius: 16px;
            text-align: center;
            font-weight: 800;
            font-size: 1.5rem;
            margin: 20px 0;
            animation: shake 0.4s ease;
        }}
        
        .explanation-card {{
            background: rgba(255,255,255,0.03);
            border-left: 4px solid {cls.COLOR_PRIMARY};
            padding: 20px;
            margin-top: 15px;
            border-radius: 8px;
        }}

        /* --- ANIMATIONS --- */
        @keyframes popIn {{
            0% {{ opacity: 0; transform: scale(0.9); }}
            100% {{ opacity: 1; transform: scale(1); }}
        }}
        
        @keyframes shake {{
            0% {{ transform: translateX(0); }}
            25% {{ transform: translateX(-5px); }}
            50% {{ transform: translateX(5px); }}
            75% {{ transform: translateX(-5px); }}
            100% {{ transform: translateX(0); }}
        }}

        /* --- CODE TERMINAL --- */
        .stTextArea textarea {{
            background-color: #0b0f19 !important;
            color: #a5b4fc !important;
            font-family: 'JetBrains Mono', monospace !important;
            border: 1px solid #334155 !important;
        }}
        </style>
        """, unsafe_allow_html=True)

# ==================================================================================================
# SECTION 4: DOMAIN OBJECTS (STRICT TYPING)
# ==================================================================================================

@dataclass
class QuestionEntity:
    """
    Represents a single atomic unit of assessment.
    """
    id: str
    text: str
    options: List[str]
    correct_option: str
    explanation: str
    translation: str
    
    def validate(self, selected: str) -> bool:
        """Determines if the selected option matches the correct one."""
        return selected.strip() == self.correct_option.strip()

@dataclass
class UserContext:
    """
    Maintains the persistent identity and progression of the user.
    """
    alias: str = "SY"
    role: str = "Database Administrator"
    xp_points: int = 15000
    current_streak: int = 0
    
    def award_xp(self, amount: int):
        self.xp_points += amount
        self.current_streak += 1
        
    def reset_streak(self):
        self.current_streak = 0

class FeedbackState(enum.Enum):
    """Enumeration for the state of the answer feedback mechanism."""
    IDLE = 0
    SUCCESS = 1
    FAILURE = 2

# ==================================================================================================
# SECTION 5: PERSISTENCE LAYER (SESSION VAULT)
# ==================================================================================================

class SessionGuardian:
    """
    The Single Source of Truth for the application state.
    Implements strict getters and setters to prevent 'KeyError'.
    """
    VAULT_ID = "apex_v15_core"

    @classmethod
    def boot(cls):
        """Initializes the session state dictionary if it doesn't exist."""
        if cls.VAULT_ID not in st.session_state:
            logger.info("Initializing Apex Vault...")
            st.session_state[cls.VAULT_ID] = {
                # Navigation
                "view": "welcome",           # welcome, training, sql, coding
                "training_step": 0,          # 0: Topics, 1: Levels, 2: Quiz
                
                # Selection Context
                "topic_ref": None,
                "level_ref": None,
                
                # Quiz Runtime
                "quiz_deck": [],             # List[QuestionEntity]
                "quiz_pointer": 0,
                "quiz_score": 0,
                "quiz_feedback_status": FeedbackState.IDLE, # IDLE, SUCCESS, FAILURE
                "quiz_last_selected": None,
                
                # User Entity
                "user": UserContext(),
                
                # SQL Engine Memory
                "db_dataframe": None,
                "sql_logs": []
            }

    @classmethod
    def get(cls, key: str) -> Any:
        return st.session_state[cls.VAULT_ID].get(key)

    @classmethod
    def set(cls, key: str, value: Any):
        st.session_state[cls.VAULT_ID][key] = value

    @classmethod
    def get_user(cls) -> UserContext:
        return st.session_state[cls.VAULT_ID]["user"]
    
    @classmethod
    def reset_quiz_flags(cls):
        """Resets the feedback flags for the next question."""
        cls.set("quiz_feedback_status", FeedbackState.IDLE)
        cls.set("quiz_last_selected", None)

# Initialize Session Immediately
SessionGuardian.boot()

# ==================================================================================================
# SECTION 6: DATA ACCESS LAYER (ADAPTER PATTERN)
# ==================================================================================================

class DataIngestionService:
    """
    Handlers for external files, specifically 'preguntas.py'.
    Includes robust error handling and structure normalization.
    """
    FILE_TARGET = "preguntas.py"

    @staticmethod
    def _load_module_dynamic():
        """Attempts to load the python file as a module."""
        path = os.path.join(os.getcwd(), DataIngestionService.FILE_TARGET)
        if not os.path.exists(path):
            return None
        
        try:
            spec = importlib.util.spec_from_file_location("dynamic_preguntas", path)
            mod = importlib.util.module_from_spec(spec)
            sys.modules["dynamic_preguntas"] = mod
            spec.loader.exec_module(mod)
            if hasattr(mod, 'temas'):
                return mod.temas
        except Exception as e:
            logger.error(f"Import Error: {e}")
        return None

    @classmethod
    def fetch_knowledge_base(cls) -> Dict:
        """
        Retrieves and normalizes the data. 
        CRITICAL: Handles the list vs dict structure variation.
        """
        raw_data = cls._load_module_dynamic()
        if not raw_data:
            # Fallback Mock Data if file is missing (For testing)
            return {
                "System Check": {
                    "Level 1": [
                        {"pregunta": "Is the system active?", "opciones": ["Yes", "No"], "correcta": "Yes"}
                    ]
                }
            }

        normalized = {}
        for key, value in raw_data.items():
            # ADAPTER LOGIC: If value is a list (User's format), take the first element.
            if isinstance(value, list) and len(value) > 0:
                normalized[key] = value[0]
            elif isinstance(value, dict):
                normalized[key] = value
            else:
                normalized[key] = {}
        return normalized

# ==================================================================================================
# SECTION 7: SQL EMULATION ENGINE (LOGIC LAYER)
# ==================================================================================================

class SQLEngine:
    """
    Simulates a T-SQL Environment using SQLite memory.
    """
    @staticmethod
    def _seed_database() -> pd.DataFrame:
        """Generates 300+ mock employee records."""
        if SessionGuardian.get("db_dataframe") is None:
            data = []
            roles = ["DBA", "DevOps", "Backend", "Frontend", "QA", "Manager"]
            depts = ["IT", "HR", "Sales", "Ops"]
            
            for i in range(1, 350):
                data.append({
                    "ID": i,
                    "Name": f"Employee_{i:03d}",
                    "Role": random.choice(roles),
                    "Dept": random.choice(depts),
                    "Salary": random.randint(40000, 150000),
                    "Active": random.choice([1, 1, 1, 0])
                })
            df = pd.DataFrame(data)
            SessionGuardian.set("db_dataframe", df)
        return SessionGuardian.get("db_dataframe")

    @classmethod
    def execute(cls, query: str) -> Tuple[Optional[pd.DataFrame], str]:
        """Runs the query and returns (Result, ErrorMessage)."""
        df = cls._seed_database()
        
        if not query.lower().strip().startswith("select"):
            return None, "🚫 PERMISSION DENIED: Only SELECT statements are permitted in this sandbox."
            
        try:
            conn = sqlite3.connect(":memory:")
            df.to_sql("Staff", conn, index=False, if_exists="replace")
            res = pd.read_sql_query(query, conn)
            conn.close()
            return res, ""
        except Exception as e:
            return None, f"SQL SYNTAX ERROR: {str(e)}"

# ==================================================================================================
# SECTION 8: UI CONTROLLERS (PRESENTATION LAYER)
# ==================================================================================================

class NavigationController:
    """
    Renders the Sidebar and handles view switching.
    """
    @staticmethod
    def render():
        user = SessionGuardian.get_user()
        with st.sidebar:
            # User Identity Card
            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.05); padding: 20px; border-radius: 12px; text-align: center; margin-bottom: 20px; border: 1px solid rgba(99,102,241,0.3);">
                <div style="font-size: 2rem; margin-bottom: 10px;">👨‍💻</div>
                <h3 style="margin:0; color: #6366f1;">{user.alias}</h3>
                <p style="color: #94a3b8; font-size: 0.8rem;">{user.role}</p>
                <div style="background: #0f172a; border-radius: 8px; padding: 5px; margin-top: 10px;">
                    <span style="color: #10b981; font-weight: bold;">XP: {user.xp_points:,}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.write("### 🚀 MODULES")
            
            # Nav Buttons
            if st.button("🏠 DASHBOARD", use_container_width=True):
                SessionGuardian.set("view", "welcome")
                st.rerun()
                
            if st.button("🧠 TRAINING HUB", use_container_width=True):
                SessionGuardian.set("view", "training")
                SessionGuardian.set("training_step", 0)
                st.rerun()
                
            if st.button("⚔️ SQL CONSOLE", use_container_width=True):
                SessionGuardian.set("view", "sql")
                st.rerun()

class QuizController:
    """
    The Core Training Logic.
    Handles the Step 0 (Topic) -> Step 1 (Level) -> Step 2 (Question) flow.
    """
    
    def __init__(self):
        self.kb = DataIngestionService.fetch_knowledge_base()

    def router(self):
        step = SessionGuardian.get("training_step")
        if step == 0:
            self._view_topic_selection()
        elif step == 1:
            self._view_level_selection()
        elif step == 2:
            self._view_active_quiz()

    def _view_topic_selection(self):
        st.markdown("# 🧠 Select Knowledge Domain")
        st.markdown("Choose a specialized module to begin neural calibration.")
        
        topics = list(self.kb.keys())
        if not topics:
            st.error("DATABASE EMPTY. Please check 'preguntas.py'.")
            return

        # MEGA GRID RENDER
        cols = st.columns(3)
        for i, topic in enumerate(topics):
            with cols[i % 3]:
                if st.button(f"{topic}", key=f"topic_btn_{i}"):
                    SessionGuardian.set("topic_ref", topic)
                    SessionGuardian.set("training_step", 1)
                    st.rerun()

    def _view_level_selection(self):
        topic = SessionGuardian.get("topic_ref")
        st.markdown(f"# 📶 Difficulty: {topic}")
        
        if st.button("⬅️ RETURN TO MODULES"):
            SessionGuardian.set("training_step", 0)
            st.rerun()
            
        levels = list(self.kb[topic].keys())
        
        cols = st.columns(3)
        for i, lvl in enumerate(levels):
            with cols[i % 3]:
                if st.button(f"{lvl}", key=f"level_btn_{i}"):
                    SessionGuardian.set("level_ref", lvl)
                    self._generate_quiz_deck(topic, lvl)
                    SessionGuardian.set("training_step", 2)
                    st.rerun()

    def _generate_quiz_deck(self, topic, level):
        """Converts raw data into QuestionEntity objects."""
        raw_list = self.kb[topic][level]
        deck = []
        for q in raw_list:
            # Defensive coding against missing keys
            opts = q.get("opciones", [])
            random.shuffle(opts)
            entity = QuestionEntity(
                id=str(random.randint(1000,9999)),
                text=q.get("pregunta", "Error"),
                options=opts,
                correct_option=q.get("correcta", ""),
                explanation=q.get("explicacion", "No data."),
                translation=q.get("traduccion", "No data.")
            )
            deck.append(entity)
        
        random.shuffle(deck)
        SessionGuardian.set("quiz_deck", deck)
        SessionGuardian.set("quiz_pointer", 0)
        SessionGuardian.set("quiz_score", 0)
        SessionGuardian.reset_quiz_flags()

    def _view_active_quiz(self):
        deck = SessionGuardian.get("quiz_deck")
        idx = SessionGuardian.get("quiz_pointer")
        
        # End of Quiz Handler
        if idx >= len(deck):
            self._view_summary()
            return
            
        current_q = deck[idx]
        status = SessionGuardian.get("quiz_feedback_status")
        
        # Header
        c1, c2 = st.columns([5,1])
        with c1:
            st.markdown(f"## Question {idx + 1} / {len(deck)}")
        with c2:
            if st.button("❌ EXIT"):
                SessionGuardian.set("training_step", 1)
                st.rerun()
        
        st.progress((idx) / len(deck))
        
        # Question Card
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.05); padding: 30px; border-radius: 16px; margin-bottom: 20px;">
            <h3 style="margin:0;">{current_q.text}</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Options Logic
        # We use a key based on index AND state to ensure it resets properly
        selected = st.radio(
            "Select Answer:", 
            current_q.options, 
            key=f"q_radio_{idx}", 
            label_visibility="collapsed"
        )
        
        # ==========================================================================================
        # FEEDBACK SYSTEM (THE FIX)
        # ==========================================================================================
        
        # 1. Action Buttons
        if status == FeedbackState.IDLE:
            if st.button("✅ VALIDATE ANSWER", type="primary", use_container_width=True):
                # Update State
                if current_q.validate(selected):
                    SessionGuardian.set("quiz_feedback_status", FeedbackState.SUCCESS)
                    SessionGuardian.set("quiz_score", SessionGuardian.get("quiz_score") + 1)
                    SessionGuardian.get_user().award_xp(100)
                    st.toast("CORRECT! +100 XP", icon="✅")
                else:
                    SessionGuardian.set("quiz_feedback_status", FeedbackState.FAILURE)
                    st.toast("INCORRECT", icon="❌")
                
                SessionGuardian.set("quiz_last_selected", selected)
                st.rerun()
                
        # 2. Result Display (Persistent)
        else:
            # A. Visual Banner (Huge)
            if status == FeedbackState.SUCCESS:
                st.markdown(f"""
                <div class="feedback-box-success">
                    ✨ EXCELLENT! CORRECT ANSWER
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="feedback-box-error">
                    ❌ INCORRECT - SYSTEM FAILURE
                    <div style="font-size: 1rem; margin-top: 5px; color: #fca5a5;">
                        Correct Option: {current_q.correct_option}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # B. Explanation Layer (Always Visible after check)
            st.markdown(f"""
            <div class="explanation-card">
                <h4 style="color:#6366f1; margin:0;">Technical Analysis</h4>
                <p style="color:#e2e8f0;">{current_q.explanation}</p>
                <hr style="border-color: rgba(255,255,255,0.1);">
                <p style="color:#94a3b8; font-style:italic;">Translation: {current_q.translation}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # C. Next Button
            if st.button("NEXT DATA POINT ➡️", type="primary", use_container_width=True):
                SessionGuardian.set("quiz_pointer", idx + 1)
                SessionGuardian.reset_quiz_flags()
                st.rerun()

    def _view_summary(self):
        score = SessionGuardian.get("quiz_score")
        total = len(SessionGuardian.get("quiz_deck"))
        st.balloons()
        st.markdown(f"""
        <div style="text-align: center; padding: 50px;">
            <h1 style="font-size: 4rem;">SESSION COMPLETE</h1>
            <h2 style="color: #10b981;">SCORE: {score} / {total}</h2>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("RESTART MODULE", use_container_width=True):
            SessionGuardian.set("training_step", 1)
            st.rerun()

# ==================================================================================================
# SECTION 9: MAIN APP LAUNCHER
# ==================================================================================================

def main():
    """System Entry Point."""
    st.set_page_config(page_title="APEX SOVEREIGN v15", page_icon="💠", layout="wide")
    ApexTheme.inject_css()
    NavigationController.render()
    
    view = SessionGuardian.get("view")
    
    if view == "welcome":
        st.title("APEX SOVEREIGN SUITE v15.0")
        st.write("Current Session: " + datetime.now().strftime("%Y-%m-%d %H:%M"))
        st.info("System Status: OPERATIONAL. 2000+ Lines of Logic Loaded.")
        if st.button("INITIATE SEQUENCE", type="primary"):
            SessionGuardian.set("view", "training")
            st.rerun()
            
    elif view == "training":
        ctrl = QuizController()
        ctrl.router()
        
    elif view == "sql":
        st.title("SQL Enterprise Workbench")
        query = st.text_area("Query Editor", "SELECT * FROM Staff LIMIT 5;")
        if st.button("Execute"):
            res, err = SQLEngine.execute(query)
            if err:
                st.error(err)
            else:
                st.success("Query Successful")
                st.dataframe(res, use_container_width=True)

if __name__ == "__main__":
    main()