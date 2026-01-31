# -*- coding: utf-8 -*-
"""
========================================================================================================================
  IRONCLAD ANALYTICS v3.0 — TITAN EDITION (THE MONOLITH)
  Authorized Personnel: SY (ARCHITECT)
  Release Date: 2026-02-01
  
  [SYSTEM MANIFEST & ARCHITECTURE]
  ----------------------------------------------------------------------------------------------------------------------
  1. CORE KERNEL      : Python 3.10+ Streamlit (State Machine v3).
  2. VISUAL ENGINE    : 'Neon-Flux' CSS. Animated Gradients, Glassmorphism, 3D Hover Effects.
  3. RENDERING        : Direct HTML5 Embeds for Lottie Animations (Zero-Dependency).
  4. DATA LAYER       : Fault-Tolerant JSON Adapter with Auto-Recovery.
  5. QUIZ ENGINE      : Two-Stage Validation Logic (Selection -> Buffer -> Commit -> Feedback).
  ----------------------------------------------------------------------------------------------------------------------
  
  [COPYRIGHT]
  © 2026 IronClad Analytics Corp. All rights reserved.
  Confidential Proprietary Information.
========================================================================================================================
"""

import streamlit as st
import pandas as pd
import random
import sqlite3
import time
import os
import sys
import importlib.util
import uuid
import enum
import logging
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field

# --- SYSTEM CONFIGURATION ---
st.set_page_config(
    page_title="IronClad Titan v3.0",
    page_icon="💠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- LOGGING CORE ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("IronCladTitan")

# ======================================================================================================================
# SECTION 1: THE NEON-FLUX VISUAL ENGINE (CSS & ASSETS)
# ======================================================================================================================

class VisualAssets:
    """
    Central Repository for Visual Assets & Animations.
    Uses Direct Embeds to ensure 100% uptime without external libraries.
    """
    # High-Performance Embeds
    ANIM_MAIN_ROBOT = "https://lottie.host/embed/9863db83-4940-4ce0-8e18-60914fb499cb/pYM5sC8O3e.json"
    ANIM_VICTORY = "https://lottie.host/embed/a8c62c96-0365-4d76-805c-3e3518b26118/pQk5sH4O1e.json" # Generic Trophy Placeholder
    ANIM_PROCESSING = "https://lottie.host/embed/d3e36569-2310-444b-9759-3221c56360b6/example.json" # Abstract loading
    
    # Icons
    ICON_HQ = "🏢"
    ICON_BRAIN = "🧠"
    ICON_DB = "💽"
    ICON_SECURE = "🔐"
    ICON_ALERT = "⚠️"
    ICON_USER = "👨‍🚀"

class NeonEngine:
    """
    The Graphics Rendering Core. Injects 150+ lines of CSS.
    """
    PRIMARY_COLOR = "#00f2ff"   # Cyan Neon
    SECONDARY_COLOR = "#7000ff" # Purple Neon
    BG_COLOR = "#050510"        # Deep Space Black
    
    @staticmethod
    def inject_css():
        st.markdown(f"""
        <style>
        /* --- FONTS & BASICS --- */
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;500;700&display=swap');
        
        :root {{
            --neon-cyan: {NeonEngine.PRIMARY_COLOR};
            --neon-purple: {NeonEngine.SECONDARY_COLOR};
            --bg-dark: {NeonEngine.BG_COLOR};
            --glass: rgba(255, 255, 255, 0.05);
            --glass-border: rgba(255, 255, 255, 0.1);
        }}

        .stApp {{
            background-color: var(--bg-dark);
            background-image: 
                radial-gradient(circle at 10% 20%, rgba(112, 0, 255, 0.15) 0%, transparent 40%),
                radial-gradient(circle at 90% 80%, rgba(0, 242, 255, 0.15) 0%, transparent 40%);
            color: #e0e0e0;
            font-family: 'Rajdhani', sans-serif;
        }}

        /* --- HEADERS --- */
        h1, h2, h3 {{
            font-family: 'Orbitron', sans-serif;
            text-transform: uppercase;
            letter-spacing: 2px;
            background: linear-gradient(90deg, #fff, var(--neon-cyan));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 0 20px rgba(0, 242, 255, 0.3);
        }}

        /* --- TITAN CARDS --- */
        .titan-card {{
            background: rgba(10, 10, 25, 0.7);
            border: 1px solid var(--glass-border);
            border-left: 4px solid var(--neon-purple);
            border-radius: 16px;
            padding: 25px;
            backdrop-filter: blur(10px);
            box-shadow: 0 10px 30px -10px rgba(0,0,0,0.8);
            transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
            margin-bottom: 20px;
        }}
        
        .titan-card:hover {{
            transform: translateY(-5px) scale(1.01);
            border-color: var(--neon-cyan);
            box-shadow: 0 0 20px rgba(0, 242, 255, 0.2);
        }}

        /* --- BUTTONS (CYBERPUNK STYLE) --- */
        .stButton > button {{
            background: linear-gradient(45deg, #1a1a2e, #16213e);
            border: 1px solid var(--neon-cyan);
            color: var(--neon-cyan);
            font-family: 'Orbitron', sans-serif;
            text-transform: uppercase;
            letter-spacing: 1px;
            padding: 12px 24px;
            border-radius: 4px;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }}
        
        .stButton > button:hover {{
            background: var(--neon-cyan);
            color: #000;
            box-shadow: 0 0 30px var(--neon-cyan);
        }}

        /* --- SIDEBAR --- */
        section[data-testid="stSidebar"] {{
            background: #020205;
            border-right: 1px solid #1f1f3a;
        }}

        /* --- QUIZ INTERFACE --- */
        .quiz-box {{
            background: rgba(255,255,255,0.03);
            border: 1px solid var(--glass-border);
            padding: 30px;
            border-radius: 20px;
            margin: 20px 0;
            position: relative;
        }}
        
        .quiz-box::before {{
            content: "SECURE PROTOCOL";
            position: absolute;
            top: -10px;
            right: 20px;
            background: var(--neon-purple);
            color: white;
            font-size: 0.7rem;
            padding: 2px 10px;
            border-radius: 10px;
            font-family: 'Orbitron', sans-serif;
        }}

        /* --- SQL TERMINAL --- */
        .sql-console textarea {{
            background-color: #0a0a12 !important;
            color: #00ff9d !important;
            font-family: 'Courier New', monospace !important;
            border: 1px solid #333 !important;
        }}

        /* --- FEEDBACK HUD --- */
        .hud-pass {{
            border: 1px solid #00ff9d;
            background: rgba(0, 255, 157, 0.1);
            color: #00ff9d;
            padding: 15px;
            border-radius: 8px;
            font-weight: bold;
            animation: pulse 1s infinite alternate;
        }}
        
        .hud-fail {{
            border: 1px solid #ff0055;
            background: rgba(255, 0, 85, 0.1);
            color: #ff0055;
            padding: 15px;
            border-radius: 8px;
            font-weight: bold;
        }}

        @keyframes pulse {{
            from {{ box-shadow: 0 0 10px rgba(0,255,157,0.1); }}
            to {{ box-shadow: 0 0 20px rgba(0,255,157,0.4); }}
        }}

        </style>
        """, unsafe_allow_html=True)

    @staticmethod
    def render_anim(url: str, height: int = 300):
        st.markdown(f"""
            <div style="width: 100%; display: flex; justify-content: center; margin: 20px 0;">
                <iframe src="{url}" width="100%" height="{height}" style="border: none; background: transparent;"></iframe>
            </div>
        """, unsafe_allow_html=True)

# ======================================================================================================================
# SECTION 2: DATA MODELS & STATE ARCHITECTURE
# ======================================================================================================================

@dataclass
class UserStats:
    """User Progression Tracking."""
    username: str = "Administrator"
    role: str = "System Architect"
    xp: int = 15800
    streak: int = 0
    total_ops: int = 0
    successful_ops: int = 0

    def add_xp(self, base_xp: int = 100):
        bonus = min(self.streak * 10, 50)
        self.xp += (base_xp + bonus)
        self.total_ops += 1
        self.successful_ops += 1
        self.streak += 1

    def reset_streak(self):
        self.streak = 0
        self.total_ops += 1

@dataclass
class Question:
    """Immutable Question Entity."""
    id: str
    text: str
    options: List[str]
    correct_option: str
    explanation: str
    translation: str

class AppState:
    """
    The Monolith State Manager.
    Ensures persistence across reruns to PREVENT bugs.
    """
    KEY = "TITAN_STATE"

    @classmethod
    def _init(cls):
        if cls.KEY not in st.session_state:
            st.session_state[cls.KEY] = {
                "view": "DASHBOARD",
                "user": UserStats(),
                "quiz": {
                    "active": False,
                    "topic": None,
                    "level": None,
                    "queue": [],
                    "current_idx": 0,
                    "score": 0,
                    "state": "WAITING_INPUT", # WAITING_INPUT | SHOWING_RESULT
                    "last_selected_option": None
                },
                "sql": {
                    "history": [],
                    "cache": None
                }
            }

    @classmethod
    def get(cls):
        cls._init()
        return st.session_state[cls.KEY]

    @classmethod
    def user(cls) -> UserStats:
        return cls.get()["user"]

    @classmethod
    def quiz_state(cls):
        return cls.get()["quiz"]

    @classmethod
    def reset_question_state(cls):
        """Crucial for fixing the selection bug."""
        q = cls.quiz_state()
        q["state"] = "WAITING_INPUT"
        q["last_selected_option"] = None

# ======================================================================================================================
# SECTION 3: ROBUST DATA ADAPTER
# ======================================================================================================================

class DataCore:
    """
    Handles data ingestion from preguntas.py with Fallback Safety.
    """
    FILE_PATH = "preguntas.py"

    @staticmethod
    def fetch_knowledge_base() -> Dict:
        path = os.path.join(os.getcwd(), DataCore.FILE_PATH)
        
        # 1. Check Existence
        if not os.path.exists(path):
            return DataCore._generate_emergency_data("FILE_NOT_FOUND")

        # 2. Dynamic Import
        try:
            spec = importlib.util.spec_from_file_location("dynamic_content", path)
            module = importlib.util.module_from_spec(spec)
            sys.modules["dynamic_content"] = module
            spec.loader.exec_module(module)
            
            raw = getattr(module, 'temas', None)
            if not raw: return DataCore._generate_emergency_data("EMPTY_MODULE")
            
            return DataCore._sanitize(raw)
        except Exception as e:
            st.sidebar.error(f"Data Corrupted: {str(e)}")
            return DataCore._generate_emergency_data("CORRUPTION")

    @staticmethod
    def _sanitize(raw_data: Dict) -> Dict:
        clean = {}
        for topic, content in raw_data.items():
            # Handle List vs Dict inconsistencies
            if isinstance(content, list):
                if content and isinstance(content[0], dict):
                    clean[topic] = content[0]
                else:
                    clean[topic] = {}
            elif isinstance(content, dict):
                clean[topic] = content
            else:
                clean[topic] = {}
        return clean

    @staticmethod
    def _generate_emergency_data(reason: str) -> Dict:
        """Generates mock data so the app NEVER crashes."""
        return {
            f"EMERGENCY MODE ({reason})": {
                "Level 1": [
                    {"pregunta": "System Integrity Check?", "opciones": ["Stable", "Unstable", "Critical"], "correcta": "Stable", "explicacion": "Fallback active.", "traduccion": "Prueba de sistema."}
                ]
            }
        }

# ======================================================================================================================
# SECTION 4: ENGINE CONTROLLERS (THE BRAIN)
# ======================================================================================================================

class QuizController:
    """
    The Logic that runs the Training Modules.
    IMPROVED: Separates selection from submission to avoid state loss.
    """
    def __init__(self):
        self.kb = DataCore.fetch_knowledge_base()

    def render_selector(self):
        st.markdown(f"## {VisualAssets.ICON_BRAIN} NEURAL TRAINING HUB")
        st.markdown("Authenticate domain to proceed.")
        
        topics = list(self.kb.keys())
        cols = st.columns(2)
        for i, topic in enumerate(topics):
            with cols[i % 2]:
                st.markdown(f"""
                <div class="titan-card" style="text-align:center;">
                    <h3 style="color:var(--neon-cyan);">{topic}</h3>
                    <p style="color:#888;">Protocol Set {i+1}</p>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"ENGAGE {topic}", key=f"topic_{i}", use_container_width=True):
                    q_state = AppState.quiz_state()
                    q_state["active"] = True
                    q_state["topic"] = topic
                    q_state["level"] = None
                    st.rerun()

    def render_level_selector(self):
        state = AppState.quiz_state()
        topic = state["topic"]
        
        st.markdown(f"## {VisualAssets.ICON_SECURE} ACCESS LEVEL: {topic}")
        if st.button("<< ABORT SEQUENCE", type="secondary"):
            state["active"] = False
            state["topic"] = None
            st.rerun()

        levels = list(self.kb[topic].keys())
        c1, c2, c3 = st.columns(3)
        cols = [c1, c2, c3]
        
        for i, lvl in enumerate(levels):
            with cols[i % 3]:
                st.markdown(f"""
                <div class="titan-card" style="height: 150px; display:flex; flex-direction:column; justify-content:center; align-items:center;">
                    <h1>{i+1}</h1>
                    <p>{lvl}</p>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"INITIATE {lvl}", key=f"lvl_{i}", use_container_width=True):
                    self._start_quiz(topic, lvl)

    def _start_quiz(self, topic, lvl):
        # 1. Load Data
        raw_questions = self.kb[topic][lvl]
        deck = []
        for item in raw_questions:
            # Create Safe Object
            opts = item.get("opciones", ["Error"])
            random.shuffle(opts)
            deck.append(Question(
                id=str(uuid.uuid4()),
                text=item.get("pregunta", "Data Error"),
                options=opts,
                correct_option=item.get("correcta", ""),
                explanation=item.get("explicacion", ""),
                translation=item.get("traduccion", "")
            ))
        
        # 2. Reset State
        qs = AppState.quiz_state()
        qs["level"] = lvl
        qs["queue"] = deck
        qs["current_idx"] = 0
        qs["score"] = 0
        AppState.reset_question_state()
        st.rerun()

    def render_gameplay(self):
        qs = AppState.quiz_state()
        deck = qs["queue"]
        idx = qs["current_idx"]
        
        # Victory Condition
        if idx >= len(deck):
            self._render_victory()
            return

        q = deck[idx]
        
        # --- HUD ---
        c1, c2, c3 = st.columns([1, 6, 2])
        c1.markdown(f"### Q{idx+1}")
        c2.progress((idx) / len(deck))
        c3.metric("SCORE", f"{qs['score']} PTS")

        # --- QUESTION DISPLAY ---
        st.markdown(f"""
        <div class="quiz-box">
            <h2 style="margin:0;">{q.text}</h2>
        </div>
        """, unsafe_allow_html=True)

        # --- LOGIC CORE (BUG FIX) ---
        # If we are waiting for input, show radio.
        # If we showed result, show static info.
        
        if qs["state"] == "WAITING_INPUT":
            # Input Phase
            selection = st.radio(
                "SELECT ANSWER PROTOCOL:",
                q.options,
                index=None,
                key=f"radio_{q.id}"
            )
            
            st.write("")
            if st.button("VERIFY PROTOCOL >>", use_container_width=True, type="primary"):
                if not selection:
                    st.toast("⛔ INPUT REQUIRED: Please select an option!", icon="⛔")
                else:
                    # COMMIT ANSWER
                    qs["last_selected_option"] = selection
                    qs["state"] = "SHOWING_RESULT"
                    
                    if selection.strip() == q.correct_option.strip():
                        qs["score"] += 1
                        AppState.user().add_xp(150)
                    else:
                        AppState.user().reset_streak()
                    
                    st.rerun()

        elif qs["state"] == "SHOWING_RESULT":
            # Result Phase (Input Locked)
            user_choice = qs["last_selected_option"]
            is_correct = (user_choice.strip() == q.correct_option.strip())
            
            if is_correct:
                st.markdown(f"""
                <div class="hud-pass">
                    ACCESS GRANTED. <br>
                    Correct Protocol: {q.correct_option}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="hud-fail">
                    ACCESS DENIED. <br>
                    Selected: {user_choice} <br>
                    Required: {q.correct_option}
                </div>
                """, unsafe_allow_html=True)

            # Explanation
            st.info(f"📋 **ANALYSIS:** {q.explanation}")
            st.caption(f"🌐 Translation: {q.translation}")
            
            # Next Button
            if st.button("NEXT NODE >>", use_container_width=True):
                qs["current_idx"] += 1
                AppState.reset_question_state()
                st.rerun()

    def _render_victory(self):
        qs = AppState.quiz_state()
        score = qs["score"]
        total = len(qs["queue"])
        
        NeonEngine.render_anim(VisualAssets.ANIM_VICTORY, 400)
        
        st.markdown(f"""
        <div class="titan-card" style="text-align:center; border-color: #00ff9d;">
            <h1 style="font-size: 4rem;">MISSION COMPLETE</h1>
            <h2>Efficiency: {score}/{total}</h2>
            <p>Neural pathways updated successfully.</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("RETURN TO DASHBOARD", use_container_width=True):
            qs["active"] = False
            qs["topic"] = None
            st.rerun()

class SQLLabController:
    """
    Mock SQL Environment for Practice.
    """
    def render(self):
        st.markdown(f"## {VisualAssets.ICON_DB} SQL TITAN WORKBENCH")
        
        c_main, c_help = st.columns([3, 1])
        
        with c_main:
            st.markdown("### TERMINAL")
            query = st.text_area("QUERY INPUT", height=150, placeholder="SELECT * FROM Employees WHERE...", key="sql_input")
            
            if st.button("EXECUTE QUERY", type="primary"):
                self._execute_fake_query(query)
                
        with c_help:
            st.markdown("### SCHEMA")
            st.code("""
TABLE Employees (
  ID int PK,
  Name varchar,
  Role varchar,
  Salary int,
  Joined date
)
            """, language="sql")
            
            with st.expander("CHEAT SHEET"):
                st.markdown("""
                - **SELECT** `col` FROM `table`
                - **WHERE** `col` > 100
                - **ORDER BY** `col` DESC
                - **LIMIT** 5
                """)

    def _execute_fake_query(self, sql):
        if not sql.strip():
            st.warning("Empty buffer.")
            return
            
        if "select" not in sql.lower():
            st.error("SECURITY ALERT: Only SELECT allowed.")
            return
            
        # Mock Data Generation
        data = []
        roles = ["Engineer", "Architect", "Manager", "Intern"]
        for i in range(5):
            data.append({
                "ID": i+100,
                "Name": f"Operative_{i}",
                "Role": random.choice(roles),
                "Salary": random.randint(50000, 150000),
                "Joined": "2024-01-01"
            })
        
        st.success(f"Query executed in 0.0{random.randint(1,9)}s")
        st.dataframe(pd.DataFrame(data), use_container_width=True)

# ======================================================================================================================
# SECTION 5: MAIN LAYOUT & ROUTING
# ======================================================================================================================

def render_sidebar():
    user = AppState.user()
    with st.sidebar:
        st.image("https://img.icons8.com/fluency/96/data-protection.png", width=80)
        st.markdown(f"## {user.username}")
        st.caption(f"Role: {user.role}")
        
        # XP Bar
        st.progress((user.xp % 1000) / 1000)
        st.markdown(f"**LVL {user.xp // 1000}** | {user.xp} XP")
        
        st.divider()
        st.markdown("### 🧭 NAVIGATION")
        
        if st.button("DASHBOARD", use_container_width=True):
            AppState.get()["view"] = "DASHBOARD"
            st.rerun()
            
        if st.button("NEURAL TRAINING", use_container_width=True):
            AppState.get()["view"] = "TRAINING"
            st.rerun()
            
        if st.button("SQL LAB", use_container_width=True):
            AppState.get()["view"] = "SQL"
            st.rerun()
            
        st.divider()
        st.markdown("### ⚙️ SYSTEM STATUS")
        st.code(f"""
UPTIME: 99.9%
LATENCY: 12ms
STREAK: {user.streak}
        """)

def render_dashboard():
    st.markdown(f"# {VisualAssets.ICON_HQ} IRONCLAD DASHBOARD")
    st.markdown("Welcome back, Architect. Systems are nominal.")
    
    # Hero Animation
    NeonEngine.render_anim(VisualAssets.ANIM_MAIN_ROBOT, 350)
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        <div class="titan-card">
            <h3>ENGLISH CORE</h3>
            <p>Status: ACTIVE</p>
            <p>Modules: Loaded</p>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="titan-card">
            <h3>SQL ENGINE</h3>
            <p>Status: STANDBY</p>
            <p>Connection: Secure</p>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="titan-card">
            <h3>USER METRICS</h3>
            <p>Performance: Optimal</p>
            <p>Sync: Complete</p>
        </div>
        """, unsafe_allow_html=True)

def main_loop():
    # 1. Inject CSS
    NeonEngine.inject_css()
    
    # 2. Sidebar
    render_sidebar()
    
    # 3. Router
    view = AppState.get()["view"]
    
    if view == "DASHBOARD":
        render_dashboard()
        
    elif view == "TRAINING":
        ctrl = QuizController()
        q_state = AppState.quiz_state()
        
        if not q_state["active"]:
            ctrl.render_selector()
        elif q_state["topic"] and not q_state["level"]:
            ctrl.render_level_selector()
        elif q_state["level"]:
            ctrl.render_gameplay()
            
    elif view == "SQL":
        sql_ctrl = SQLLabController()
        sql_ctrl.render()

if __name__ == "__main__":
    main_loop()