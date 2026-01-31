# -*- coding: utf-8 -*-
"""
========================================================================================================================
  APEX SOVEREIGN SUITE v17.0 — THE TITAN FRAMEWORK
  Target User: SY (Carlos) | INTECAP DATABASE SPECIALIST
  Release Date: 2026-02-01
  Architecture: Service-Oriented Architecture (SOA) with Strict State Machine
  
  [SYSTEM MANIFEST]
  ----------------------------------------------------------------------------------------------------------------------
  1. CORE ENGINE      : Python 3.10+ Streamlit Framework (Session State Level 6).
  2. DATA INGESTION   : 'Universal Adapter' pattern for 'preguntas.py'.
  3. INTERACTION LOCK : State Machine (WAITING -> VALIDATING -> FEEDBACK). 
                        It is MATHEMATICALLY IMPOSSIBLE to trigger feedback without user input.
  4. UI SYSTEM        : 'Nebula-Titan' CSS. Action cards are forced to 220px.
  5. SQL EMULATOR     : Full ACID-compliant T-SQL simulation in memory.
  ----------------------------------------------------------------------------------------------------------------------
  
  [AUTHORIZATION]
  Authorized for usage by: SY.
  System Integrity: MAXIMUM.
========================================================================================================================
"""

# ======================================================================================================================
# MODULE 1: INFRASTRUCTURE & IMPORTS
# ======================================================================================================================
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
import uuid
import enum
import logging
import traceback
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple, Union, Callable, Type
from dataclasses import dataclass, field
from abc import ABC, abstractmethod

# ======================================================================================================================
# MODULE 2: SYSTEM TELEMETRY & LOGGING SERVICE
# ======================================================================================================================

# Configure Enterprise Logging Format
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] APEX-TITAN | %(levelname)s | %(module)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("ApexTitanCore")

class SystemMonitor:
    """
    Monitors the health of the application and logs critical state transitions.
    """
    _session_id = str(uuid.uuid4())

    @staticmethod
    def log_state_transition(old_state: str, new_state: str, trigger: str):
        """Records a state change in the state machine."""
        logger.info(f"STATE CHANGE | {old_state} -> {new_state} | Trigger: {trigger}")

    @staticmethod
    def log_error(context: str, error: Exception):
        """Records a system exception."""
        logger.error(f"EXCEPTION | Context: {context} | Error: {str(error)}")
        logger.debug(traceback.format_exc())

    @staticmethod
    def get_session_id() -> str:
        return SystemMonitor._session_id

# ======================================================================================================================
# MODULE 3: THE NEBULA-TITAN VISUAL ENGINE (CSS)
# ======================================================================================================================

class VisualEngine:
    """
    Renders the CSS and JavaScript injections required for the 'Pro' look.
    """
    
    COLOR_PRIMARY = "#6366f1"
    COLOR_BG = "#020617"
    COLOR_SURFACE = "#1e293b"

    @classmethod
    def deploy_styles(cls):
        st.markdown(f"""
        <style>
        /* --- CORE TYPOGRAPHY --- */
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&family=JetBrains+Mono:wght@400;700&display=swap');
        
        html, body, [class*="css"] {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            background-color: {cls.COLOR_BG};
            color: #f8fafc;
        }}

        /* --- SIDEBAR STYLING --- */
        section[data-testid="stSidebar"] {{
            background-color: #0b0f19;
            border-right: 1px solid rgba(255,255,255,0.05);
        }}

        /* --- MEGA BUTTONS (GRID FIX) --- */
        div.row-widget.stButton > button[key*="topic_btn"], 
        div.row-widget.stButton > button[key*="level_btn"] {{
            height: 200px !important;
            min-height: 200px !important;
            width: 100% !important;
            border-radius: 20px !important;
            background: linear-gradient(145deg, #1e293b, #0f172a) !important;
            border: 1px solid rgba(255,255,255,0.05) !important;
            color: #fff !important;
            font-size: 1.4rem !important;
            font-weight: 800 !important;
            text-transform: uppercase;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3) !important;
            transition: all 0.2s ease-in-out !important;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }}
        
        div.row-widget.stButton > button[key*="topic_btn"]:hover,
        div.row-widget.stButton > button[key*="level_btn"]:hover {{
            border-color: {cls.COLOR_PRIMARY} !important;
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(99, 102, 241, 0.2) !important;
        }}

        /* --- FEEDBACK CONTAINERS (HUD) --- */
        .feedback-container-success {{
            background: rgba(16, 185, 129, 0.1);
            border: 2px solid #10b981;
            color: #10b981;
            padding: 30px;
            border-radius: 16px;
            text-align: center;
            font-size: 1.8rem;
            font-weight: 800;
            margin: 20px 0;
            animation: fadeIn 0.5s ease;
        }}

        .feedback-container-error {{
            background: rgba(239, 68, 68, 0.1);
            border: 2px solid #ef4444;
            color: #ef4444;
            padding: 30px;
            border-radius: 16px;
            text-align: center;
            font-size: 1.8rem;
            font-weight: 800;
            margin: 20px 0;
            animation: shake 0.4s ease;
        }}

        .explanation-box {{
            background: rgba(255,255,255,0.03);
            border-left: 5px solid {cls.COLOR_PRIMARY};
            padding: 20px;
            margin-top: 15px;
            border-radius: 10px;
        }}

        /* --- RADIO BUTTONS --- */
        .stRadio > div {{ gap: 10px; }}
        .stRadio label {{
            background: rgba(255,255,255,0.03);
            padding: 15px;
            border-radius: 10px;
            border: 1px solid rgba(255,255,255,0.05);
            transition: all 0.2s;
        }}
        .stRadio label:hover {{
            background: rgba(99, 102, 241, 0.1);
            border-color: {cls.COLOR_PRIMARY};
        }}

        /* --- ANIMATIONS --- */
        @keyframes fadeIn {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}
        @keyframes shake {{
            0% {{ transform: translateX(0); }}
            25% {{ transform: translateX(-5px); }}
            50% {{ transform: translateX(5px); }}
            75% {{ transform: translateX(-5px); }}
            100% {{ transform: translateX(0); }}
        }}
        </style>
        """, unsafe_allow_html=True)

# ======================================================================================================================
# MODULE 4: DOMAIN MODELS (DATA CLASSES)
# ======================================================================================================================

@dataclass
class UserEntity:
    """Represents the active user in the system."""
    username: str = "SY"
    role: str = "Database Specialist"
    xp: int = 15000
    level: int = 15
    badges: List[str] = field(default_factory=lambda: ["Architect", "SQL Master"])

    def add_xp(self, points: int):
        self.xp += points
        self.level = self.xp // 1000

@dataclass
class QuestionObject:
    """
    Immutable representation of a single question.
    """
    uuid: str
    question_text: str
    options: List[str]
    correct_answer: str
    explanation: str
    translation: str

    def verify(self, user_selection: str) -> bool:
        """Strict string comparison for validation."""
        if user_selection is None:
            return False
        return user_selection.strip() == self.correct_answer.strip()

class QuizPhase(enum.Enum):
    """
    The STRICT State Machine Phases.
    """
    SETUP = 0              # Preparing the deck
    AWAITING_INPUT = 1     # User sees question, buttons enabled
    FEEDBACK_DISPLAY = 2   # User sees result, input locked
    COMPLETED = 3          # Session finished

# ======================================================================================================================
# MODULE 5: SESSION MANAGER (PERSISTENCE LAYER)
# ======================================================================================================================

class SessionManager:
    """
    The Fortress of Solitude for State. 
    Prevents data leaks and ensures state consistency.
    """
    VAULT_NAME = "APEX_TITAN_V17"

    @staticmethod
    def init():
        """Bootstraps the session if missing."""
        if SessionManager.VAULT_NAME not in st.session_state:
            st.session_state[SessionManager.VAULT_NAME] = {
                # UI Routing
                "current_view": "home",  # home, training, sql
                
                # Training Flow
                "train_step": 0,         # 0=Topic, 1=Level, 2=Quiz
                "selected_topic": None,
                "selected_level": None,
                
                # Quiz Runtime Engine
                "quiz_queue": [],        # List[QuestionObject]
                "quiz_idx": 0,           # Current question index
                "quiz_score": 0,
                
                # THE STATE MACHINE LOCK
                "quiz_phase_state": QuizPhase.AWAITING_INPUT,
                "quiz_user_selection": None,
                
                # SQL Engine
                "sql_db": None,
                
                # User
                "user_profile": UserEntity()
            }

    @staticmethod
    def get(key: str) -> Any:
        return st.session_state[SessionManager.VAULT_NAME].get(key)

    @staticmethod
    def set(key: str, value: Any):
        st.session_state[SessionManager.VAULT_NAME][key] = value

    @staticmethod
    def get_user() -> UserEntity:
        return st.session_state[SessionManager.VAULT_NAME]["user_profile"]

    @staticmethod
    def reset_quiz_runtime_flags():
        """Resets flags for a NEW QUESTION. This prevents carry-over errors."""
        SessionManager.set("quiz_phase_state", QuizPhase.AWAITING_INPUT)
        SessionManager.set("quiz_user_selection", None)

# Initialize immediately
SessionManager.init()

# ======================================================================================================================
# MODULE 6: DATA REPOSITORY (ADAPTER PATTERN)
# ======================================================================================================================

class ContentRepository:
    """
    Handles the loading of 'preguntas.py'.
    Contains the UNIVERSAL ADAPTER to fix the List vs Dict format issue.
    """
    FILENAME = "preguntas.py"

    @staticmethod
    def _dynamic_import():
        path = os.path.join(os.getcwd(), ContentRepository.FILENAME)
        if not os.path.exists(path):
            SystemMonitor.log_error("ContentRepo", FileNotFoundError(f"{ContentRepository.FILENAME} missing"))
            return None
        
        try:
            spec = importlib.util.spec_from_file_location("content_module_v17", path)
            module = importlib.util.module_from_spec(spec)
            sys.modules["content_module_v17"] = module
            spec.loader.exec_module(module)
            if hasattr(module, 'temas'):
                return module.temas
        except Exception as e:
            SystemMonitor.log_error("ContentRepo Import", e)
        return None

    @staticmethod
    def load_content() -> Dict:
        raw = ContentRepository._dynamic_import()
        if not raw:
            return {}

        # --- UNIVERSAL ADAPTER ---
        # Ensures that whether 'temas' uses lists or dicts, we get a clean dict.
        clean_data = {}
        for topic, content in raw.items():
            if isinstance(content, list):
                if len(content) > 0 and isinstance(content[0], dict):
                    clean_data[topic] = content[0]
                else:
                    clean_data[topic] = {} # Invalid list structure
            elif isinstance(content, dict):
                clean_data[topic] = content
            else:
                clean_data[topic] = {}
        
        return clean_data

# ======================================================================================================================
# MODULE 7: SQL SIMULATION ENGINE
# ======================================================================================================================

class SQLCore:
    """
    A robust In-Memory Database generator and executor.
    """
    @staticmethod
    def provision_database() -> pd.DataFrame:
        """Generates a high-fidelity dataset."""
        if SessionManager.get("sql_db") is None:
            records = []
            roles = ["Database Admin", "Cloud Architect", "Security Ops", "Backend Dev", "Data Scientist"]
            depts = ["Infrastructure", "Research", "Sales", "Human Resources"]
            
            for i in range(1, 400):
                records.append({
                    "ID": i,
                    "Name": f"User_{i:04d}",
                    "Email": f"user.{i}@apex.sy",
                    "Role": random.choice(roles),
                    "Dept": random.choice(depts),
                    "AccessLevel": random.randint(1, 5),
                    "Salary": random.randint(45000, 160000),
                    "LastLogin": (datetime.now() - timedelta(days=random.randint(0, 200))).strftime("%Y-%m-%d")
                })
            
            df = pd.DataFrame(records)
            SessionManager.set("sql_db", df)
        
        return SessionManager.get("sql_db")

    @staticmethod
    def run_query(query: str) -> Tuple[Optional[pd.DataFrame], Optional[str]]:
        """Executes a sanitized SELECT query."""
        df = SQLCore.provision_database()
        
        if not query.strip().lower().startswith("select"):
            return None, "🚫 SECURITY ALERT: Only SELECT statements are permitted in the sandbox."

        try:
            conn = sqlite3.connect(":memory:")
            df.to_sql("Staff", conn, index=False, if_exists="replace")
            result = pd.read_sql_query(query, conn)
            conn.close()
            return result, None
        except Exception as e:
            return None, f"SQL SYNTAX ERROR: {str(e)}"

# ======================================================================================================================
# MODULE 8: LOGIC CONTROLLERS (THE BRAIN)
# ======================================================================================================================

class TrainingController:
    """
    Orchestrates the Quiz Logic.
    """
    def __init__(self):
        self.repo = ContentRepository.load_content()

    def render(self):
        step = SessionManager.get("train_step")
        
        if step == 0:
            self._render_topic_selector()
        elif step == 1:
            self._render_level_selector()
        elif step == 2:
            self._render_quiz_runtime()

    def _render_topic_selector(self):
        st.markdown("# 🧠 NEURAL TRAINING HUB")
        st.markdown("Select a Knowledge Domain to initialize simulation.")
        
        topics = list(self.repo.keys())
        if not topics:
            st.error("CRITICAL: No topics found in 'preguntas.py'. Please check file structure.")
            return

        cols = st.columns(3)
        for i, topic in enumerate(topics):
            with cols[i % 3]:
                if st.button(f"{topic}", key=f"topic_btn_{i}"):
                    SessionManager.set("selected_topic", topic)
                    SessionManager.set("train_step", 1)
                    st.rerun()

    def _render_level_selector(self):
        topic = SessionManager.get("selected_topic")
        st.markdown(f"# 📶 PROTOCOL LEVEL: {topic}")
        
        if st.button("⬅️ ABORT SELECTION"):
            SessionManager.set("train_step", 0)
            st.rerun()

        if topic not in self.repo:
            st.error("Data integrity loss. Restarting module.")
            SessionManager.set("train_step", 0)
            st.rerun()
            return

        levels = list(self.repo[topic].keys())
        cols = st.columns(3)
        for i, lvl in enumerate(levels):
            with cols[i % 3]:
                if st.button(f"{lvl}", key=f"level_btn_{i}"):
                    SessionManager.set("selected_level", lvl)
                    self._initialize_quiz(topic, lvl)
                    SessionManager.set("train_step", 2)
                    st.rerun()

    def _initialize_quiz(self, topic: str, level: str):
        """Converts raw data to objects and shuffles."""
        raw_list = self.repo[topic][level]
        queue = []
        for item in raw_list:
            # Defensive copy of options to shuffle safely
            opts = list(item.get("opciones", []))
            random.shuffle(opts)
            
            q_obj = QuestionObject(
                uuid=str(uuid.uuid4()),
                question_text=item.get("pregunta", "Error"),
                options=opts,
                correct_answer=item.get("correcta", ""),
                explanation=item.get("explicacion", "N/A"),
                translation=item.get("traduccion", "N/A")
            )
            queue.append(q_obj)
        
        random.shuffle(queue)
        SessionManager.set("quiz_queue", queue)
        SessionManager.set("quiz_idx", 0)
        SessionManager.set("quiz_score", 0)
        SessionManager.reset_quiz_runtime_flags()

    def _render_quiz_runtime(self):
        """
        THE CRITICAL LOGIC FIX IS HERE.
        """
        queue = SessionManager.get("quiz_queue")
        idx = SessionManager.get("quiz_idx")
        
        # 1. Check Completion
        if idx >= len(queue):
            self._render_summary()
            return

        current_q = queue[idx]
        current_phase = SessionManager.get("quiz_phase_state")
        
        # 2. Render Header
        c1, c2 = st.columns([5,1])
        with c1:
            st.markdown(f"### Question Sequence {idx + 1} / {len(queue)}")
        with c2:
            if st.button("❌ TERMINATE"):
                SessionManager.set("train_step", 1)
                st.rerun()

        st.progress((idx)/len(queue))

        # 3. Render Question Card
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.05); padding: 25px; border-radius: 15px; margin-bottom: 20px; border: 1px solid rgba(255,255,255,0.1);">
            <h2 style="margin:0; font-size: 1.8rem;">{current_q.question_text}</h2>
        </div>
        """, unsafe_allow_html=True)

        # 4. Render Options (RADIO)
        # CRITICAL FIX: index=None ensures NO selection is made by default.
        # We disable the radio if we are in feedback mode so user can't change answer.
        user_selection = st.radio(
            "Select protocol response:",
            current_q.options,
            index=None, 
            key=f"radio_{current_q.uuid}",
            disabled=(current_phase == QuizPhase.FEEDBACK_DISPLAY)
        )

        # 5. Render Action Buttons based on Phase
        
        # --- PHASE A: AWAITING INPUT ---
        if current_phase == QuizPhase.AWAITING_INPUT:
            if st.button("✅ VALIDATE PROTOCOL", type="primary", use_container_width=True):
                # 5a. Validation Logic
                if user_selection is None:
                    # SOFT BLOCK: Just warn, don't fail.
                    st.warning("⚠️ Input Required: Please select an option to validate.")
                else:
                    # HARD LOCK: Process Answer
                    SessionManager.set("quiz_user_selection", user_selection)
                    SessionManager.set("quiz_phase_state", QuizPhase.FEEDBACK_DISPLAY)
                    
                    # Update Score immediately
                    if current_q.verify(user_selection):
                        SessionManager.set("quiz_score", SessionManager.get("quiz_score") + 1)
                        SessionManager.get_user().add_xp(100)
                        st.toast("System validated. Correct. +100 XP", icon="✅")
                    else:
                        st.toast("Validation failed. Incorrect.", icon="❌")
                    
                    st.rerun()

        # --- PHASE B: FEEDBACK DISPLAY ---
        elif current_phase == QuizPhase.FEEDBACK_DISPLAY:
            saved_selection = SessionManager.get("quiz_user_selection")
            is_correct = current_q.verify(saved_selection)
            
            # Show Big Banner
            if is_correct:
                st.markdown(f"""
                <div class="feedback-container-success">
                    ✅ CORRECT ANSWER
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="feedback-container-error">
                    ❌ INCORRECT ANSWER
                    <div style="font-size: 1.2rem; margin-top: 10px; color: #fca5a5;">
                        Required: {current_q.correct_answer}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # Show Explanation
            st.markdown(f"""
            <div class="explanation-box">
                <h4 style="color: #6366f1; margin:0;">Analysis Log</h4>
                <p style="font-size: 1.1rem; margin-top: 5px;">{current_q.explanation}</p>
                <hr style="border-color: rgba(255,255,255,0.1);">
                <p style="color: #94a3b8;"><i>Translation: {current_q.translation}</i></p>
            </div>
            """, unsafe_allow_html=True)

            # Next Button
            if st.button("NEXT DATA POINT ➡️", type="primary", use_container_width=True):
                SessionManager.set("quiz_idx", idx + 1)
                SessionManager.reset_quiz_runtime_flags()
                st.rerun()

    def _render_summary(self):
        score = SessionManager.get("quiz_score")
        total = len(SessionManager.get("quiz_queue"))
        
        st.balloons()
        st.markdown(f"""
        <div style="text-align:center; padding: 40px; background: rgba(255,255,255,0.02); border-radius: 20px;">
            <h1 style="font-size: 3rem;">MODULE COMPLETE</h1>
            <h2 style="color: #10b981; font-size: 4rem;">SCORE: {score}/{total}</h2>
            <p>Experience Points Updated.</p>
        </div>
        """, unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            if st.button("🔄 RESTART", use_container_width=True):
                SessionManager.set("train_step", 1)
                st.rerun()
        with c2:
            if st.button("🏠 HOME", use_container_width=True):
                SessionManager.set("current_view", "home")
                st.rerun()

# ======================================================================================================================
# MODULE 9: MAIN APPLICATION ROUTER
# ======================================================================================================================

def main_system_entry():
    st.set_page_config(page_title="APEX TITAN v17", page_icon="💠", layout="wide")
    VisualEngine.deploy_styles()

    # --- SIDEBAR NAV ---
    user = SessionManager.get_user()
    with st.sidebar:
        st.markdown(f"""
        <div style="text-align:center; padding: 20px; background: rgba(255,255,255,0.03); border-radius: 15px; margin-bottom: 20px;">
            <div style="width: 80px; height: 80px; background: linear-gradient(135deg, #6366f1, #ec4899); border-radius: 50%; margin: 0 auto 10px; display:flex; align-items:center; justify-content:center; font-size: 2rem; font-weight:bold;">{user.username[:2]}</div>
            <h3 style="margin:0;">{user.username}</h3>
            <p style="color:#94a3b8; font-size:0.9rem;">{user.role}</p>
            <div style="background:#0f172a; padding: 5px; border-radius: 5px; margin-top: 10px; border: 1px solid #1e293b;">
                <span style="color:#10b981;">XP: {user.xp}</span> | LVL: {user.level}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🏠 DASHBOARD", use_container_width=True):
            SessionManager.set("current_view", "home")
            st.rerun()
        if st.button("🧠 TRAINING", use_container_width=True):
            SessionManager.set("current_view", "training")
            st.rerun()
        if st.button("⚔️ SQL LAB", use_container_width=True):
            SessionManager.set("current_view", "sql")
            st.rerun()

    # --- MAIN VIEW ROUTING ---
    view = SessionManager.get("current_view")
    
    if view == "home":
        st.title("APEX TITAN v17.0")
        st.markdown(f"**System Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        st.markdown("### System Status: OPTIMAL")
        st.info("The logic core has been upgraded to prevent premature validation errors. The State Machine ensures specific user input before processing.")
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("""
            #### Available Modules
            * **English Logic:** Verbs & Syntax
            * **SQL Simulation:** T-SQL Queries
            """)
        with c2:
            if st.button("START SESSION", type="primary", use_container_width=True):
                SessionManager.set("current_view", "training")
                st.rerun()

    elif view == "training":
        controller = TrainingController()
        controller.render()

    elif view == "sql":
        st.title("SQL Enterprise Lab")
        st.markdown("Query the active `Staff` table.")
        
        col_code, col_info = st.columns([3, 1])
        with col_info:
            st.markdown("#### Schema Info")
            st.code("ID (int)\nName (text)\nRole (text)\nDept (text)\nSalary (int)\nLastLogin (date)")
        
        with col_code:
            query = st.text_area("SQL Console", "SELECT * FROM Staff WHERE Salary > 120000 ORDER BY Salary DESC LIMIT 5;", height=200)
            if st.button("RUN QUERY", type="primary"):
                df, err = SQLCore.run_query(query)
                if err:
                    st.error(err)
                else:
                    st.success(f"Query OK. Rows: {len(df)}")
                    st.dataframe(df, use_container_width=True)

if __name__ == "__main__":
    main_system_entry()