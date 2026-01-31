# -*- coding: utf-8 -*-
"""
====================================================================================================
  APEX SOVEREIGN SUITE v16.0 — THE LEVIATHAN BUILD
  Target User: SY (Carlos) | INTECAP DATABASE SPECIALIST
  Release Date: 2026-01-31
  Architecture: Hexagonal Enterprise (Domain-Driven Design)
  
  [SYSTEM MANIFEST]
  --------------------------------------------------------------------------------------------------
  1. CORE KERNEL      : Python 3.10+ Streamlit Framework (Session State Level 5).
  2. DATA INGESTION   : 'Universal Adapter' pattern for 'preguntas.py' (List/Dict Agnostic).
  3. FEEDBACK HUD     : FIXED. Requires explicit validation trigger. No premature failures.
  4. UI ENGINE        : 'Nebula-X' CSS with forced 220px+ height on action cards.
  5. SQL EMULATOR     : In-Memory T-SQL Simulation with RBAC (Role Based Access Control).
  6. TELEMETRY        : Verbose logging for every user interaction.
  --------------------------------------------------------------------------------------------------
  
  WARNING: THIS SOURCE CODE CONTAINS ADVANCED CLASS STRUCTURES.
  DO NOT MODIFY THE 'SESSION_GUARD' WITHOUT AUTHORIZATION.
====================================================================================================
"""

# ==================================================================================================
# MODULE 1: SYSTEM IMPORTS & ENVIRONMENT SETUP
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
import uuid
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple, Union, Callable, Type
from dataclasses import dataclass, field
from abc import ABC, abstractmethod

# ==================================================================================================
# MODULE 2: INDUSTRIAL LOGGING & TELEMETRY
# ==================================================================================================

# Configure Industrial Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | APEX-CORE | %(levelname)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("ApexLeviathan")

class TelemetryService:
    """
    Service responsible for tracking user interactions and system health.
    Implements a Singleton pattern to ensure one logger instance.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TelemetryService, cls).__new__(cls)
            cls._instance.session_id = str(uuid.uuid4())
            logger.info(f"Telemetry Service Initialized. Session ID: {cls._instance.session_id}")
        return cls._instance

    def log_interaction(self, component: str, action: str, metadata: Dict = None):
        """Logs a user interaction with timestamp."""
        meta_str = json.dumps(metadata) if metadata else "{}"
        logger.info(f"INTERACTION | Component: {component} | Action: {action} | Meta: {meta_str}")

    def log_error(self, source: str, error_msg: str):
        """Logs a critical system error."""
        logger.error(f"CRITICAL FAILURE | Source: {source} | Error: {error_msg}")

# Initialize Telemetry
TELEMETRY = TelemetryService()

# ==================================================================================================
# MODULE 3: THE NEBULA DESIGN SYSTEM (CSS ENGINE)
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
            font-weight: 800;
            letter-spacing: -0.5px;
            color: #ffffff;
            text-transform: uppercase;
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
            min-height: 220px !important;
            width: 100% !important;
            border-radius: 24px !important;
            background: linear-gradient(160deg, #1e293b 0%, #0f172a 100%) !important;
            border: 1px solid rgba(255,255,255,0.08) !important;
            color: #ffffff !important;
            font-size: 1.6rem !important;
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

        /* --- FEEDBACK STATUS BOXES (HUD) --- */
        .feedback-box-success {{
            background: rgba(16, 185, 129, 0.1);
            border: 2px solid {cls.COLOR_SUCCESS};
            color: {cls.COLOR_SUCCESS};
            padding: 30px;
            border-radius: 16px;
            text-align: center;
            font-weight: 900;
            font-size: 2rem;
            margin: 20px 0;
            animation: popIn 0.4s ease;
            box-shadow: 0 0 40px rgba(16, 185, 129, 0.2);
        }}
        
        .feedback-box-error {{
            background: rgba(239, 68, 68, 0.1);
            border: 2px solid {cls.COLOR_DANGER};
            color: {cls.COLOR_DANGER};
            padding: 30px;
            border-radius: 16px;
            text-align: center;
            font-weight: 900;
            font-size: 2rem;
            margin: 20px 0;
            animation: shake 0.4s ease;
            box-shadow: 0 0 40px rgba(239, 68, 68, 0.2);
        }}
        
        .explanation-card {{
            background: rgba(255,255,255,0.03);
            border-left: 6px solid {cls.COLOR_PRIMARY};
            padding: 25px;
            margin-top: 15px;
            border-radius: 12px;
            border: 1px solid rgba(255,255,255,0.05);
        }}

        /* --- RADIO BUTTON STYLING --- */
        .stRadio > div {{
            background: transparent;
        }}
        .stRadio label {{
            background: rgba(255,255,255,0.05);
            padding: 15px 20px;
            border-radius: 10px;
            margin-bottom: 10px;
            border: 1px solid rgba(255,255,255,0.1);
            transition: all 0.2s;
            width: 100%;
        }}
        .stRadio label:hover {{
            background: rgba(99, 102, 241, 0.2);
            border-color: {cls.COLOR_PRIMARY};
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
            font-size: 1rem;
        }}
        </style>
        """, unsafe_allow_html=True)

# ==================================================================================================
# MODULE 4: DOMAIN ENTITIES & INTERFACES
# ==================================================================================================

@dataclass
class QuestionEntity:
    """
    Represents a single atomic unit of assessment.
    Contains validation logic and metadata.
    """
    id: str
    text: str
    options: List[str]
    correct_option: str
    explanation: str
    translation: str
    
    def validate(self, selected: str) -> bool:
        """Determines if the selected option matches the correct one."""
        if not selected: return False
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
    badges: List[str] = field(default_factory=list)
    
    def award_xp(self, amount: int):
        self.xp_points += amount
        self.current_streak += 1
        TELEMETRY.log_interaction("UserContext", "XP Awarded", {"amount": amount, "total": self.xp_points})

class FeedbackState(enum.Enum):
    """Enumeration for the state of the answer feedback mechanism."""
    WAITING_FOR_INPUT = 0
    VALIDATING = 1  # Transient state
    SUCCESS = 2
    FAILURE = 3

# ==================================================================================================
# MODULE 5: SESSION VAULT (STATE MANAGEMENT)
# ==================================================================================================

class SessionGuardian:
    """
    The Single Source of Truth for the application state.
    Implements strict getters and setters to prevent 'KeyError'.
    Manages the lifecycle of the Quiz State Machine.
    """
    VAULT_ID = "apex_v16_leviathan"

    @classmethod
    def boot(cls):
        """Initializes the session state dictionary if it doesn't exist."""
        if cls.VAULT_ID not in st.session_state:
            logger.info("Initializing Apex Vault v16...")
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
                "quiz_state_machine": FeedbackState.WAITING_FOR_INPUT,
                "quiz_last_selected_option": None,
                
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
        """
        CRITICAL: Resets the state machine for the next question.
        Ensures the UI does not show feedback prematurely.
        """
        cls.set("quiz_state_machine", FeedbackState.WAITING_FOR_INPUT)
        cls.set("quiz_last_selected_option", None)
        TELEMETRY.log_interaction("SessionGuardian", "Quiz Flags Reset")

# Initialize Session Immediately
SessionGuardian.boot()

# ==================================================================================================
# MODULE 6: DATA INGESTION (ADAPTER PATTERN)
# ==================================================================================================

class DataIngestionService:
    """
    Handlers for external files, specifically 'preguntas.py'.
    Includes robust error handling and structure normalization.
    """
    FILE_TARGET = "preguntas.py"

    @staticmethod
    def _load_module_dynamic():
        """Attempts to load the python file as a module using importlib."""
        path = os.path.join(os.getcwd(), DataIngestionService.FILE_TARGET)
        if not os.path.exists(path):
            TELEMETRY.log_error("DataIngestion", f"File not found: {path}")
            return None
        
        try:
            # Force reload logic to ensure updates in preguntas.py are reflected
            spec = importlib.util.spec_from_file_location("dynamic_preguntas_v16", path)
            mod = importlib.util.module_from_spec(spec)
            sys.modules["dynamic_preguntas_v16"] = mod
            spec.loader.exec_module(mod)
            if hasattr(mod, 'temas'):
                return mod.temas
        except Exception as e:
            TELEMETRY.log_error("DataIngestion", f"Import Error: {e}")
            logger.error(traceback.format_exc())
        return None

    @classmethod
    def fetch_knowledge_base(cls) -> Dict:
        """
        Retrieves and normalizes the data. 
        CRITICAL: Handles the list vs dict structure variation.
        """
        raw_data = cls._load_module_dynamic()
        if not raw_data:
            return {} # Return empty dict instead of mock data to force error if file missing

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
# MODULE 7: SQL EMULATION ENGINE (LOGIC LAYER)
# ==================================================================================================

class SQLEngine:
    """
    Simulates a T-SQL Environment using SQLite memory.
    """
    @staticmethod
    def _seed_database() -> pd.DataFrame:
        """Generates 300+ mock employee records for the simulation."""
        if SessionGuardian.get("db_dataframe") is None:
            data = []
            roles = ["DBA", "DevOps Engineer", "Backend Developer", "Frontend Developer", "QA Analyst", "Project Manager", "CTO"]
            depts = ["IT Infrastructure", "Human Resources", "Global Sales", "Operations", "Cybersecurity"]
            cities = ["Guatemala City", "Quetzaltenango", "Escuintla", "Antigua", "Flores"]
            
            for i in range(1, 350):
                data.append({
                    "EmployeeID": i,
                    "FullName": f"Apex_User_{i:03d}",
                    "Role": random.choice(roles),
                    "Department": random.choice(depts),
                    "Location": random.choice(cities),
                    "Salary_USD": random.randint(40000, 150000),
                    "IsActive": random.choice([1, 1, 1, 1, 0]),
                    "HireDate": (datetime.now() - timedelta(days=random.randint(0, 3650))).strftime("%Y-%m-%d")
                })
            df = pd.DataFrame(data)
            SessionGuardian.set("db_dataframe", df)
        return SessionGuardian.get("db_dataframe")

    @classmethod
    def execute(cls, query: str) -> Tuple[Optional[pd.DataFrame], str]:
        """Runs the query and returns (Result, ErrorMessage)."""
        df = cls._seed_database()
        
        # Security Guard
        if not query.lower().strip().startswith("select"):
            return None, "🚫 PERMISSION DENIED: Only SELECT statements are permitted in this sandbox environment."
            
        try:
            conn = sqlite3.connect(":memory:")
            df.to_sql("Employees", conn, index=False, if_exists="replace")
            
            start_t = time.time()
            res = pd.read_sql_query(query, conn)
            exec_time = time.time() - start_t
            
            conn.close()
            TELEMETRY.log_interaction("SQLEngine", "Query Executed", {"time": exec_time, "rows": len(res)})
            return res, ""
        except Exception as e:
            return None, f"SQL SYNTAX ERROR: {str(e)}"

# ==================================================================================================
# MODULE 8: UI CONTROLLERS (PRESENTATION LAYER)
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
                
            st.markdown("---")
            st.caption(f"Session: {TELEMETRY.session_id[:8]}")
            st.caption("INTECAP SENIOR LABS")

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
            st.error("⚠️ CRITICAL: 'preguntas.py' is missing or has invalid structure.")
            st.code("Expected format: temas = {'Topic': ...}")
            return

        # MEGA GRID RENDER
        cols = st.columns(3)
        for i, topic in enumerate(topics):
            with cols[i % 3]:
                # Unique keys for buttons are essential
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
            
        if topic not in self.kb:
            st.error("Topic Data Lost. Please restart.")
            return

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
            # Shuffle options carefully creating a new list
            opts_shuffled = list(opts)
            random.shuffle(opts_shuffled)
            
            entity = QuestionEntity(
                id=str(uuid.uuid4()),
                text=q.get("pregunta", "Error loading text"),
                options=opts_shuffled,
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
        """
        The main quiz interface logic.
        FIX: Implements the waiting state properly.
        """
        deck = SessionGuardian.get("quiz_deck")
        idx = SessionGuardian.get("quiz_pointer")
        
        # End of Quiz Handler
        if idx >= len(deck):
            self._view_summary()
            return
            
        current_q = deck[idx]
        state = SessionGuardian.get("quiz_state_machine")
        
        # --- HEADER AREA ---
        c1, c2 = st.columns([5,1])
        with c1:
            st.markdown(f"## Question {idx + 1} / {len(deck)}")
        with c2:
            if st.button("❌ EXIT", use_container_width=True):
                SessionGuardian.set("training_step", 1)
                st.rerun()
        
        # Progress Bar
        st.progress((idx) / len(deck))
        
        # --- QUESTION CARD ---
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.05); padding: 30px; border-radius: 16px; margin-bottom: 20px;">
            <h3 style="margin:0; font-size: 1.5rem;">{current_q.text}</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # --- INTERACTION AREA ---
        # The key is crucial. It must change with the question ID to reset the selection.
        # We also default index to None so nothing is selected initially.
        selected_option = st.radio(
            "Select Answer:", 
            current_q.options, 
            key=f"radio_{current_q.id}", 
            label_visibility="collapsed",
            index=None,
            disabled=(state != FeedbackState.WAITING_FOR_INPUT) # Disable if already answered
        )
        
        # --- ACTION & FEEDBACK LOGIC ---
        
        if state == FeedbackState.WAITING_FOR_INPUT:
            # Only show Validate button here
            # Logic: If nothing selected, disable button (visual cue) or show warning on click
            
            if st.button("✅ VALIDATE ANSWER", type="primary", use_container_width=True):
                if selected_option is None:
                    st.warning("⚠️ Please select an option before validating.")
                else:
                    # Transition State
                    is_correct = current_q.validate(selected_option)
                    
                    if is_correct:
                        SessionGuardian.set("quiz_state_machine", FeedbackState.SUCCESS)
                        SessionGuardian.set("quiz_score", SessionGuardian.get("quiz_score") + 1)
                        SessionGuardian.get_user().award_xp(100)
                        st.toast("CORRECT! +100 XP", icon="✅")
                    else:
                        SessionGuardian.set("quiz_state_machine", FeedbackState.FAILURE)
                        st.toast("INCORRECT", icon="❌")
                    
                    # Save what was selected to keep context
                    SessionGuardian.set("quiz_last_selected_option", selected_option)
                    st.rerun()

        else:
            # STATE IS SUCCESS OR FAILURE -> SHOW FEEDBACK
            
            if state == FeedbackState.SUCCESS:
                st.markdown(f"""
                <div class="feedback-box-success">
                    ✨ EXCELLENT! CORRECT ANSWER
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="feedback-box-error">
                    ❌ INCORRECT
                    <div style="font-size: 1rem; margin-top: 10px; color: #fca5a5; font-weight: 400;">
                        Correct Option: <b>{current_q.correct_option}</b>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # Show Explanation (Always visible in feedback state)
            st.markdown(f"""
            <div class="explanation-card">
                <h4 style="color:#6366f1; margin:0;">Technical Analysis</h4>
                <p style="color:#e2e8f0; font-size: 1.1rem; margin-top: 10px;">{current_q.explanation}</p>
                <hr style="border-color: rgba(255,255,255,0.1); margin: 15px 0;">
                <p style="color:#94a3b8; font-style:italic;">Translation: {current_q.translation}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Next Button
            if st.button("NEXT DATA POINT ➡️", type="primary", use_container_width=True):
                SessionGuardian.set("quiz_pointer", idx + 1)
                SessionGuardian.reset_quiz_flags()
                st.rerun()

    def _view_summary(self):
        score = SessionGuardian.get("quiz_score")
        total = len(SessionGuardian.get("quiz_deck"))
        accuracy = (score / total) * 100 if total > 0 else 0
        
        st.balloons()
        st.markdown(f"""
        <div style="text-align: center; padding: 50px; background: rgba(255,255,255,0.02); border-radius: 20px;">
            <h1 style="font-size: 4rem; color: #ffffff;">SESSION COMPLETE</h1>
            <h2 style="color: #10b981; font-size: 3rem;">SCORE: {score} / {total}</h2>
            <p style="color: #94a3b8; font-size: 1.5rem;">Accuracy: {accuracy:.1f}%</p>
        </div>
        """, unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🔄 RESTART LEVEL", use_container_width=True):
                SessionGuardian.set("training_step", 1)
                st.rerun()
        with c2:
            if st.button("🏠 DASHBOARD", use_container_width=True):
                SessionGuardian.set("view", "welcome")
                st.rerun()

# ==================================================================================================
# MODULE 9: MAIN APP LAUNCHER
# ==================================================================================================

def main():
    """System Entry Point."""
    st.set_page_config(
        page_title="APEX SOVEREIGN v16", 
        page_icon="💠", 
        layout="wide",
        initial_sidebar_state="expanded"
    )
    ApexTheme.inject_css()
    NavigationController.render()
    
    view = SessionGuardian.get("view")
    
    if view == "welcome":
        st.markdown('<div style="text-align: center; margin-top: 50px;">', unsafe_allow_html=True)
        st.title("APEX SOVEREIGN SUITE v16.0")
        st.markdown(f"<h3 style='color: #94a3b8;'>{datetime.now().strftime('%A, %d %B %Y')}</h3>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            st.info("System Status: OPERATIONAL. All modules loaded correctly.")
            st.write("""
            Welcome back, SY. 
            This environment is optimized for High-Performance Learning.
            - **Training Hub**: Validated logic with explicit feedback steps.
            - **SQL Console**: Full T-SQL emulation engine.
            - **Design**: Nebula-X Interface enabled.
            """)
            
            if st.button("INITIATE SEQUENCE", type="primary", use_container_width=True):
                SessionGuardian.set("view", "training")
                st.rerun()
            
    elif view == "training":
        ctrl = QuizController()
        ctrl.router()
        
    elif view == "sql":
        st.title("SQL Enterprise Workbench")
        st.markdown("Write and execute queries against the `Employees` table.")
        
        c_code, c_meta = st.columns([3, 1])
        with c_meta:
            st.markdown("#### Schema")
            st.code("""
EmployeeID (INT)
FullName (TXT)
Role (TXT)
Department (TXT)
Location (TXT)
Salary_USD (INT)
IsActive (BIT)
HireDate (DATE)
            """)
        
        with c_code:
            query = st.text_area("Query Editor", "SELECT * FROM Employees WHERE Salary_USD > 100000 LIMIT 5;", height=200)
            if st.button("Execute Query", type="primary"):
                res, err = SQLEngine.execute(query)
                if err:
                    st.error(err)
                else:
                    st.success(f"Query Successful. Returned {len(res)} rows.")
                    st.dataframe(res, use_container_width=True)

if __name__ == "__main__":
    main()