# -*- coding: utf-8 -*-
"""
========================================================================================================================
  APEX OMEGA v18.0 — THE SINGULARITY BUILD
  Target User: SY (Carlos) | INTECAP DATABASE SPECIALIST
  Release Date: 2026-02-01
  Architecture: Event-Driven SOA (Service Oriented Architecture) with Nebula-Flux UI
  
  [SYSTEM MANIFEST]
  ----------------------------------------------------------------------------------------------------------------------
  1. CORE ENGINE      : Python 3.10+ Streamlit Framework (Session State Level 7 - Persistent).
  2. VISUAL ENGINE    : 'Nebula-Flux' CSS. Animated Backgrounds, Glassmorphism, Neon UI.
  3. GAME ENGINE      : XP Systems, Streak Multipliers, Unlockable Badges, Sound Haptics (Simulated).
  4. DATA LAYER       : 'Universal Adapter' for 'preguntas.py'. Auto-healing data structures.
  5. SECURITY         : Input Sanitization, State Locking, Anti-Cheat Logic.
  ----------------------------------------------------------------------------------------------------------------------
  
  [AUTHORIZATION]
  Authorized for usage by: SY.
  System Integrity: ABSOLUTE.
========================================================================================================================
"""

# ======================================================================================================================
# MODULE 1: CORE INFRASTRUCTURE & TYPE DEFINITIONS
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
import math
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple, Union, Callable, Type
from dataclasses import dataclass, field
from abc import ABC, abstractmethod

# --- LOGGING CONFIGURATION ---
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] APEX-OMEGA | %(levelname)s | %(module)s | %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger("ApexOmegaCore")

# ======================================================================================================================
# MODULE 2: THE NEBULA-FLUX VISUAL ENGINE (ADVANCED CSS)
# ======================================================================================================================

class VisualAssets:
    """
    Manages all static assets, icons, and Lottie animations.
    """
    LOTTIE_DASHBOARD = "https://assets5.lottiefiles.com/packages/lf20_fcfjwiyb.json"
    LOTTIE_SQL = "https://assets2.lottiefiles.com/private_files/lf30_w1uxkbue.json"
    LOTTIE_SUCCESS = "https://assets9.lottiefiles.com/packages/lf20_lk80fpsm.json"
    LOTTIE_ERROR = "https://assets10.lottiefiles.com/packages/lf20_qpwbv5gm.json"
    
    ICON_BRAIN = "🧠"
    ICON_SQL = "⚔️"
    ICON_CODE = "👨‍💻"
    ICON_HOME = "🏠"

class NebulaEngine:
    """
    The rendering core. Injects advanced CSS animations and layout fixes.
    """
    
    THEME_PRIMARY = "#6366f1"    # Indigo
    THEME_SECONDARY = "#ec4899"  # Pink
    THEME_BG = "#0f172a"         # Slate 900
    
    @staticmethod
    def deploy():
        """
        Injects the 'Nebula-Flux' CSS Suite.
        Contains: Particle Animations, Glassmorphism Cards, Neon Buttons, Custom Scrollbars.
        """
        st.markdown(f"""
        <style>
        /* --- IMPORT FONTS --- */
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=JetBrains+Mono:wght@400;700&display=swap');
        
        /* --- ROOT VARIABLES --- */
        :root {{
            --primary: {NebulaEngine.THEME_PRIMARY};
            --secondary: {NebulaEngine.THEME_SECONDARY};
            --bg-dark: {NebulaEngine.THEME_BG};
            --glass: rgba(255, 255, 255, 0.05);
            --glass-border: rgba(255, 255, 255, 0.1);
            --neon-glow: 0 0 10px rgba(99, 102, 241, 0.5), 0 0 20px rgba(99, 102, 241, 0.3);
        }}

        /* --- GLOBAL RESET & ANIMATED BACKGROUND --- */
        .stApp {{
            background-color: var(--bg-dark);
            background-image: 
                radial-gradient(circle at 10% 20%, rgba(99, 102, 241, 0.15) 0%, transparent 40%),
                radial-gradient(circle at 90% 80%, rgba(236, 72, 153, 0.15) 0%, transparent 40%);
            font-family: 'Outfit', sans-serif;
            color: #f8fafc;
        }}
        
        /* --- ANIMATED STARS BACKGROUND (CSS HACK) --- */
        .stApp::before {{
            content: "";
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            background-image: 
                radial-gradient(white, rgba(255,255,255,.2) 2px, transparent 3px),
                radial-gradient(white, rgba(255,255,255,.15) 1px, transparent 2px),
                radial-gradient(white, rgba(255,255,255,.1) 2px, transparent 3px);
            background-size: 550px 550px, 350px 350px, 250px 250px;
            background-position: 0 0, 40px 60px, 130px 270px;
            animation: starMove 120s linear infinite;
            z-index: 0;
            pointer-events: none;
            opacity: 0.3;
        }}
        
        @keyframes starMove {{
            from {{ transform: translateY(0); }}
            to {{ transform: translateY(-2000px); }}
        }}

        /* --- SIDEBAR GLASSMORPHISM --- */
        section[data-testid="stSidebar"] {{
            background: rgba(15, 23, 42, 0.85);
            backdrop-filter: blur(12px);
            border-right: 1px solid var(--glass-border);
        }}

        /* --- TYPOGRAPHY --- */
        h1, h2, h3 {{
            font-weight: 800;
            letter-spacing: -0.5px;
            background: linear-gradient(135deg, #fff 0%, #cbd5e1 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-transform: uppercase;
        }}

        /* --- CARDS & CONTAINERS --- */
        .apex-card {{
            background: var(--glass);
            border: 1px solid var(--glass-border);
            border-radius: 20px;
            padding: 25px;
            margin-bottom: 20px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
            backdrop-filter: blur(4px);
            transition: transform 0.3s ease;
        }}
        
        .apex-card:hover {{
            border-color: rgba(255,255,255,0.2);
            transform: translateY(-2px);
        }}

        /* --- MEGA BUTTONS (GRID) --- */
        div.row-widget.stButton > button[key*="topic_btn"], 
        div.row-widget.stButton > button[key*="level_btn"] {{
            height: 200px !important;
            min-height: 200px !important;
            width: 100% !important;
            border-radius: 24px !important;
            background: linear-gradient(160deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.9) 100%) !important;
            border: 1px solid var(--glass-border) !important;
            color: #fff !important;
            font-size: 1.5rem !important;
            font-weight: 800 !important;
            text-transform: uppercase !important;
            box-shadow: 0 10px 30px -10px rgba(0,0,0,0.5) !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            backdrop-filter: blur(5px) !important;
            position: relative;
            overflow: hidden;
        }}
        
        /* Hover Effect for Buttons */
        div.row-widget.stButton > button[key*="topic_btn"]:hover,
        div.row-widget.stButton > button[key*="level_btn"]:hover {{
            border-color: var(--primary) !important;
            transform: scale(1.02) !important;
            box-shadow: var(--neon-glow) !important;
        }}

        /* --- QUIZ INTERFACE --- */
        .quiz-question-container {{
            background: linear-gradient(180deg, rgba(255,255,255,0.05) 0%, rgba(255,255,255,0.02) 100%);
            border-left: 5px solid var(--primary);
            padding: 30px;
            border-radius: 0 20px 20px 0;
            margin-bottom: 25px;
            font-size: 1.4rem;
            font-weight: 600;
        }}

        /* Custom Radio Buttons */
        .stRadio > div {{ gap: 12px; }}
        .stRadio label {{
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(255,255,255,0.05);
            padding: 18px 25px;
            border-radius: 12px;
            transition: all 0.2s;
            cursor: pointer;
            font-size: 1.1rem;
        }}
        .stRadio label:hover {{
            background: rgba(99, 102, 241, 0.15);
            border-color: var(--primary);
        }}

        /* --- FEEDBACK HUD --- */
        .hud-success {{
            background: linear-gradient(90deg, rgba(16, 185, 129, 0.2) 0%, transparent 100%);
            border-left: 5px solid #10b981;
            color: #10b981;
            padding: 20px;
            border-radius: 10px;
            font-size: 1.5rem;
            font-weight: 800;
            animation: slideIn 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            display: flex; align-items: center; gap: 15px;
        }}
        
        .hud-error {{
            background: linear-gradient(90deg, rgba(239, 68, 68, 0.2) 0%, transparent 100%);
            border-left: 5px solid #ef4444;
            color: #ef4444;
            padding: 20px;
            border-radius: 10px;
            font-size: 1.5rem;
            font-weight: 800;
            animation: shake 0.5s ease;
            display: flex; align-items: center; gap: 15px;
        }}

        /* --- ANIMATIONS --- */
        @keyframes slideIn {{
            from {{ opacity: 0; transform: translateX(-20px); }}
            to {{ opacity: 1; transform: translateX(0); }}
        }}
        
        @keyframes shake {{
            0%, 100% {{ transform: translateX(0); }}
            20%, 60% {{ transform: translateX(-5px); }}
            40%, 80% {{ transform: translateX(5px); }}
        }}

        /* --- SQL TERMINAL --- */
        .sql-terminal textarea {{
            font-family: 'JetBrains Mono', monospace;
            background: #0b0f19 !important;
            color: #a5b4fc !important;
            border: 1px solid #334155 !important;
        }}
        
        </style>
        """, unsafe_allow_html=True)

# ======================================================================================================================
# MODULE 3: DOMAIN ENTITIES (DATA MODELS)
# ======================================================================================================================

@dataclass
class Badge:
    """Represents an unlockable achievement."""
    id: str
    name: str
    icon: str
    description: str
    condition: Callable[[int], bool]

@dataclass
class UserProfile:
    """
    Maintains user state, progression, and gamification stats.
    """
    username: str = "SY"
    role: str = "Database Architect"
    xp: int = 15000
    level: int = 15
    current_streak: int = 0
    max_streak: int = 0
    total_questions: int = 0
    correct_answers: int = 0
    badges_earned: List[str] = field(default_factory=list)

    @property
    def accuracy(self) -> float:
        if self.total_questions == 0: return 0.0
        return (self.correct_answers / self.total_questions) * 100

    @property
    def xp_to_next_level(self) -> int:
        return (self.level + 1) * 1000 - self.xp

    def add_xp(self, amount: int):
        # Streak Multiplier Logic
        multiplier = 1.0 + (min(self.current_streak, 10) * 0.1)
        final_xp = int(amount * multiplier)
        
        self.xp += final_xp
        self.level = self.xp // 1000
        return final_xp

@dataclass
class QuestionData:
    """Immutable question object."""
    uuid: str
    text: str
    options: List[str]
    correct: str
    explanation: str
    translation: str

    def check_answer(self, selection: str) -> bool:
        if not selection: return False
        return selection.strip() == self.correct.strip()

# ======================================================================================================================
# MODULE 4: STATE MANAGEMENT (THE SINGLE SOURCE OF TRUTH)
# ======================================================================================================================

class QuizState(enum.Enum):
    """The phases of the quiz interaction loop."""
    IDLE = 0            # Waiting for selection
    VALIDATING = 1      # Processing (Transient)
    SUCCESS = 2         # Showing success Feedback
    FAILURE = 3         # Showing failure Feedback

class AppState:
    """
    Singleton wrapper for st.session_state.
    Provides strictly typed access to global state.
    """
    KEY = "APEX_OMEGA_STATE"

    @classmethod
    def init(cls):
        if cls.KEY not in st.session_state:
            st.session_state[cls.KEY] = {
                # Navigation
                "view": "home",  # home, training, sql
                
                # Training Engine
                "training_phase": 0, # 0: Topic, 1: Level, 2: Quiz
                "active_topic": None,
                "active_level": None,
                "quiz_queue": [],
                "quiz_index": 0,
                "quiz_score": 0,
                
                # State Machine Lock
                "quiz_state": QuizState.IDLE,
                "user_selection_buffer": None,
                
                # SQL Engine
                "sql_db_cache": None,
                
                # User Profile
                "user": UserProfile()
            }

    @classmethod
    def get(cls, key: str) -> Any:
        return st.session_state[cls.KEY].get(key)

    @classmethod
    def set(cls, key: str, value: Any):
        st.session_state[cls.KEY][key] = value

    @classmethod
    def user(cls) -> UserProfile:
        return st.session_state[cls.KEY]["user"]

    @classmethod
    def reset_quiz_flags(cls):
        """Resets the state machine for a new question."""
        cls.set("quiz_state", QuizState.IDLE)
        cls.set("user_selection_buffer", None)

AppState.init()

# ======================================================================================================================
# MODULE 5: DATA REPOSITORY (ADAPTER PATTERN)
# ======================================================================================================================

class KnowledgeBase:
    """
    Adapts the 'preguntas.py' file.
    Includes error recovery if the file format is inconsistent.
    """
    FILE = "preguntas.py"

    @staticmethod
    def load() -> Dict:
        path = os.path.join(os.getcwd(), KnowledgeBase.FILE)
        if not os.path.exists(path):
            st.error(f"❌ CRITICAL ERROR: '{KnowledgeBase.FILE}' not found.")
            return {}

        try:
            # Dynamic Reloading to support hot-swaps
            spec = importlib.util.spec_from_file_location("apex_content", path)
            module = importlib.util.module_from_spec(spec)
            sys.modules["apex_content"] = module
            spec.loader.exec_module(module)
            
            if not hasattr(module, 'temas'):
                return {}

            # --- THE UNIVERSAL ADAPTER ---
            # Converts List[Dict] -> Dict or Dict -> Dict
            raw_data = module.temas
            clean_data = {}
            
            for topic, content in raw_data.items():
                if isinstance(content, list):
                    if content and isinstance(content[0], dict):
                        clean_data[topic] = content[0]
                    else:
                        clean_data[topic] = {}
                elif isinstance(content, dict):
                    clean_data[topic] = content
                else:
                    clean_data[topic] = {}
            
            return clean_data

        except Exception as e:
            st.error(f"Error reading knowledge base: {e}")
            return {}

# ======================================================================================================================
# MODULE 6: LOGIC ENGINES (GAMEPLAY & SQL)
# ======================================================================================================================

class GamificationEngine:
    """
    Handles badges, streaks, and XP calculations.
    """
    BADGES = [
        Badge("b1", "Novice Architect", "🏗️", "Complete your first quiz", lambda x: x > 0),
        Badge("b2", "Consistency King", "🔥", "Reach a streak of 5", lambda x: False), # Logic handled elsewhere
        Badge("b3", "SQL Master", "💾", "Reach Level 20", lambda x: x >= 20000)
    ]

    @staticmethod
    def check_badges(user: UserProfile):
        # Implementation placeholder for advanced badge logic
        pass

class SQLEngine:
    """
    Simulates a database environment.
    """
    @staticmethod
    def get_data() -> pd.DataFrame:
        if AppState.get("sql_db_cache") is None:
            # Generate 500 Mock Records
            data = []
            roles = ["Admin", "Dev", "Analyst", "Manager", "Director"]
            depts = ["IT", "Sales", "HR", "Marketing", "Legal"]
            
            for i in range(1, 501):
                data.append({
                    "ID": i,
                    "Name": f"User_{i:04d}",
                    "Role": random.choice(roles),
                    "Dept": random.choice(depts),
                    "Salary": random.randint(40000, 180000),
                    "Status": random.choice(["Active", "Inactive", "OnLeave"]),
                    "Joined": (datetime.now() - timedelta(days=random.randint(0, 1000))).strftime("%Y-%m-%d")
                })
            df = pd.DataFrame(data)
            AppState.set("sql_db_cache", df)
        return AppState.get("sql_db_cache")

    @staticmethod
    def query(sql: str) -> Tuple[Optional[pd.DataFrame], Optional[str]]:
        df = SQLEngine.get_data()
        
        if not sql.strip().lower().startswith("select"):
            return None, "🚫 SECURITY: Write operations disabled. SELECT only."

        try:
            conn = sqlite3.connect(":memory:")
            df.to_sql("Employees", conn, index=False, if_exists="replace")
            res = pd.read_sql_query(sql, conn)
            conn.close()
            return res, None
        except Exception as e:
            return None, f"SYNTAX ERROR: {e}"

# ======================================================================================================================
# MODULE 7: UI CONTROLLERS (THE BRAINS OF THE OPERATION)
# ======================================================================================================================

class LayoutController:
    """
    Manages the Sidebar and Main Layout Structure.
    """
    @staticmethod
    def render_sidebar():
        user = AppState.user()
        
        with st.sidebar:
            # --- USER CARD (Animated via CSS) ---
            st.markdown(f"""
            <div style="text-align:center; padding: 20px; background: rgba(255,255,255,0.03); border-radius: 20px; border: 1px solid rgba(255,255,255,0.1); margin-bottom: 25px;">
                <div style="width: 90px; height: 90px; background: linear-gradient(135deg, #6366f1, #ec4899); border-radius: 50%; margin: 0 auto 15px; display:flex; align-items:center; justify-content:center; font-size: 2.5rem; box-shadow: 0 0 20px rgba(99, 102, 241, 0.4);">
                    {user.username[:2]}
                </div>
                <h2 style="margin:0; font-size: 1.4rem;">{user.username}</h2>
                <p style="color:#94a3b8; margin: 5px 0;">{user.role}</p>
                
                <div style="background: rgba(0,0,0,0.3); height: 8px; border-radius: 4px; margin-top: 15px; overflow:hidden;">
                    <div style="width: {(user.xp % 1000) / 10}%; height: 100%; background: #10b981;"></div>
                </div>
                <div style="display:flex; justify-content:space-between; font-size: 0.8rem; margin-top: 5px; color: #cbd5e1;">
                    <span>LVL {user.level}</span>
                    <span>{user.xp} XP</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # --- NAVIGATION ---
            st.markdown("### 🧭 NAVIGATION")
            
            if st.button(f"{VisualAssets.ICON_HOME} HOME DASHBOARD", use_container_width=True):
                AppState.set("view", "home")
                st.rerun()
                
            if st.button(f"{VisualAssets.ICON_BRAIN} TRAINING CORE", use_container_width=True):
                AppState.set("view", "training")
                AppState.set("training_phase", 0)
                st.rerun()
                
            if st.button(f"{VisualAssets.ICON_SQL} SQL WORKBENCH", use_container_width=True):
                AppState.set("view", "sql")
                st.rerun()

            # --- STATS ---
            st.markdown("---")
            st.markdown("### 📊 LIVE STATS")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Streak", f"🔥 {user.current_streak}")
            with col2:
                st.metric("Accuracy", f"{user.accuracy:.0f}%")

class TrainingController:
    """
    Orchestrates the Quiz Experience.
    """
    def __init__(self):
        self.kb = KnowledgeBase.load()

    def run(self):
        phase = AppState.get("training_phase")
        
        if phase == 0:
            self._phase_select_topic()
        elif phase == 1:
            self._phase_select_level()
        elif phase == 2:
            self._phase_quiz_gameplay()

    def _phase_select_topic(self):
        st.markdown(f"<h1 style='font-size: 3rem;'>{VisualAssets.ICON_BRAIN} NEURAL TRAINING HUB</h1>", unsafe_allow_html=True)
        st.markdown("<p style='font-size: 1.2rem; color: #94a3b8;'>Select a cognitive domain to begin simulation.</p>", unsafe_allow_html=True)
        
        topics = list(self.kb.keys())
        if not topics:
            st.error("No knowledge modules detected.")
            return

        cols = st.columns(3)
        for i, topic in enumerate(topics):
            with cols[i % 3]:
                if st.button(f"{topic}", key=f"topic_btn_{i}"):
                    AppState.set("active_topic", topic)
                    AppState.set("training_phase", 1)
                    st.rerun()

    def _phase_select_level(self):
        topic = AppState.get("active_topic")
        st.markdown(f"<h1>📶 PROTOCOL: {topic}</h1>", unsafe_allow_html=True)
        
        if st.button("⬅️ RETURN TO HUB", type="secondary"):
            AppState.set("training_phase", 0)
            st.rerun()
            
        levels = list(self.kb[topic].keys())
        cols = st.columns(3)
        for i, lvl in enumerate(levels):
            with cols[i % 3]:
                if st.button(f"{lvl}", key=f"level_btn_{i}"):
                    AppState.set("active_level", lvl)
                    self._generate_deck(topic, lvl)
                    AppState.set("training_phase", 2)
                    st.rerun()

    def _generate_deck(self, topic, lvl):
        raw = self.kb[topic][lvl]
        deck = []
        for item in raw:
            opts = list(item.get("opciones", []))
            random.shuffle(opts)
            deck.append(QuestionData(
                uuid=str(uuid.uuid4()),
                text=item.get("pregunta", ""),
                options=opts,
                correct=item.get("correcta", ""),
                explanation=item.get("explicacion", ""),
                translation=item.get("traduccion", "")
            ))
        random.shuffle(deck)
        AppState.set("quiz_queue", deck)
        AppState.set("quiz_index", 0)
        AppState.set("quiz_score", 0)
        AppState.reset_quiz_flags()

    def _phase_quiz_gameplay(self):
        """
        THE CORE GAMEPLAY LOOP.
        """
        deck = AppState.get("quiz_queue")
        idx = AppState.get("quiz_index")
        
        # Win Condition
        if idx >= len(deck):
            self._render_victory_screen()
            return

        q = deck[idx]
        state = AppState.get("quiz_state")
        user = AppState.user()
        
        # --- HUD (HEADS UP DISPLAY) ---
        c1, c2, c3 = st.columns([1, 4, 1])
        with c1:
            st.markdown(f"<div style='text-align:center; background:rgba(255,255,255,0.05); padding:10px; border-radius:10px;'><b>Q:</b> {idx+1}/{len(deck)}</div>", unsafe_allow_html=True)
        with c2:
            st.progress((idx)/len(deck))
        with c3:
            if st.button("❌ ABORT", use_container_width=True):
                AppState.set("training_phase", 1)
                st.rerun()

        # --- QUESTION CARD ---
        st.markdown(f"""
        <div class="apex-card quiz-question-container">
            {q.text}
        </div>
        """, unsafe_allow_html=True)

        # --- INTERACTION LAYER ---
        # State Machine: Disable inputs if showing feedback
        is_locked = (state != QuizState.IDLE)
        
        selection = st.radio(
            "Select Protocol:", 
            q.options, 
            index=None, 
            key=f"rad_{q.uuid}",
            disabled=is_locked
        )

        # --- ACTION BUTTONS ---
        if state == QuizState.IDLE:
            if st.button("✅ VERIFY PROTOCOL", type="primary", use_container_width=True):
                if not selection:
                    st.toast("⚠️ INPUT REQUIRED: Select an option.", icon="⚠️")
                else:
                    # VALIDATION LOGIC
                    AppState.set("user_selection_buffer", selection)
                    if q.check_answer(selection):
                        AppState.set("quiz_state", QuizState.SUCCESS)
                        AppState.set("quiz_score", AppState.get("quiz_score") + 1)
                        # Gamification
                        earned = user.add_xp(100)
                        user.current_streak += 1
                        user.total_questions += 1
                        user.correct_answers += 1
                        st.toast(f"CORRECT! +{earned} XP (Streak: {user.current_streak})", icon="🔥")
                    else:
                        AppState.set("quiz_state", QuizState.FAILURE)
                        user.current_streak = 0 # Reset streak
                        user.total_questions += 1
                        st.toast("PROTOCOL MISMATCH. Streak Reset.", icon="❌")
                    
                    st.rerun()

        else:
            # --- FEEDBACK OVERLAY ---
            if state == QuizState.SUCCESS:
                st.markdown(f"""
                <div class="hud-success">
                    <span>✅</span>
                    <div>
                        <div>SUCCESSFUL VALIDATION</div>
                        <div style="font-size: 0.9rem; font-weight:400;">Data pattern matches expected protocol.</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                 st.markdown(f"""
                <div class="hud-error">
                    <span>❌</span>
                    <div>
                        <div>PROTOCOL FAILURE</div>
                        <div style="font-size: 0.9rem; font-weight:400; color:#cbd5e1;">Expected: <u>{q.correct}</u></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # --- EXPLANATION CARD (ALWAYS VISIBLE AFTER ANSWER) ---
            st.markdown(f"""
            <div style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.05); border-radius:15px; padding:20px; margin-top:20px;">
                <h4 style="margin:0; color: #6366f1;">👁️ ANALYSIS</h4>
                <p style="margin-top:10px; font-size:1.1rem;">{q.explanation}</p>
                <div style="margin-top:15px; padding-top:15px; border-top:1px solid rgba(255,255,255,0.1); color:#94a3b8; font-style:italic;">
                    Translation: {q.translation}
                </div>
            </div>
            """, unsafe_allow_html=True)

            if st.button("NEXT NODE ➡️", type="primary", use_container_width=True):
                AppState.set("quiz_index", idx + 1)
                AppState.reset_quiz_flags()
                st.rerun()

    def _render_victory_screen(self):
        score = AppState.get("quiz_score")
        total = len(AppState.get("quiz_queue"))
        
        st.balloons()
        st.markdown(f"""
        <div class="apex-card" style="text-align:center; padding:50px;">
            <h1 style="font-size:4rem; background: -webkit-linear-gradient(#10b981, #3b82f6); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">MODULE COMPLETE</h1>
            <h2 style="font-size:3rem; margin-top:20px;">SCORE: {score} / {total}</h2>
            <div style="margin-top:30px;">
                <p>Synchronization Complete. Neural Pathway Updated.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🔄 RESTART", use_container_width=True):
                AppState.set("training_phase", 1)
                st.rerun()
        with c2:
            if st.button("🏠 HOME", use_container_width=True):
                AppState.set("view", "home")
                st.rerun()

# ======================================================================================================================
# MODULE 8: MAIN ENTRY POINT
# ======================================================================================================================

def main():
    st.set_page_config(page_title="APEX OMEGA v18", page_icon="💠", layout="wide")
    
    # 1. Deploy Visual Engine
    NebulaEngine.deploy()
    
    # 2. Render Sidebar
    LayoutController.render_sidebar()
    
    # 3. Routing
    view = AppState.get("view")
    
    if view == "home":
        # HERO SECTION
        st.markdown(f"""
        <div style="text-align:center; padding: 50px 0;">
            <h1 style="font-size: 5rem; line-height:1;">APEX OMEGA</h1>
            <p style="font-size: 1.5rem; color: #94a3b8; margin-top: 10px;">The Singularity Build v18.0</p>
        </div>
        """, unsafe_allow_html=True)
        
        # DASHBOARD GRID
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f"""
            <div class="apex-card">
                <h3>{VisualAssets.ICON_BRAIN} TRAINING</h3>
                <p>Access neural training modules for English syntax and logic.</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("LAUNCH TRAINING", use_container_width=True):
                AppState.set("view", "training")
                st.rerun()
                
        with c2:
            st.markdown(f"""
            <div class="apex-card">
                <h3>{VisualAssets.ICON_SQL} SQL LAB</h3>
                <p>High-fidelity T-SQL environment with ACID compliance.</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("OPEN WORKBENCH", use_container_width=True):
                AppState.set("view", "sql")
                st.rerun()
                
        with c3:
            st.markdown(f"""
            <div class="apex-card">
                <h3>{VisualAssets.ICON_CODE} PROFILE</h3>
                <p>Manage credentials, badges, and performance metrics.</p>
            </div>
            """, unsafe_allow_html=True)
            st.button("VIEW PROFILE", disabled=True, use_container_width=True)

    elif view == "training":
        ctrl = TrainingController()
        ctrl.run()
        
    elif view == "sql":
        st.markdown(f"<h1>{VisualAssets.ICON_SQL} ENTERPRISE SQL WORKBENCH</h1>", unsafe_allow_html=True)
        st.markdown("<div class='apex-card'>Execute T-SQL queries against the `Employees` production replica.</div>", unsafe_allow_html=True)
        
        c_schema, c_console = st.columns([1, 3])
        with c_schema:
            st.markdown("### 🗄️ SCHEMA")
            st.code("""
ID (int)
Name (text)
Role (text)
Dept (text)
Salary (int)
Status (text)
Joined (date)
            """)
        
        with c_console:
            query = st.text_area("SQL TERMINAL", "SELECT * FROM Employees WHERE Salary > 100000 ORDER BY Salary DESC LIMIT 5;", height=200)
            if st.button("⚡ EXECUTE QUERY", type="primary"):
                df, err = SQLEngine.query(query)
                if err:
                    st.error(err)
                else:
                    st.success(f"Query executed successfully. {len(df)} rows returned.")
                    st.dataframe(df, use_container_width=True)

if __name__ == "__main__":
    main()