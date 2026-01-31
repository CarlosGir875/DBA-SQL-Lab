# -*- coding: utf-8 -*-
"""
========================================================================================================================
  IRONCLAD ZENITH v4.0 — ELEGANCE EDITION (GLASSMORPHISM UI)
  Authorized Personnel: SY (ARCHITECT)
  Release Date: 2026-02-01
  
  [SYSTEM MANIFEST & ARCHITECTURE]
  ----------------------------------------------------------------------------------------------------------------------
  1. CORE KERNEL      : Python 3.10+ Streamlit (Persistent State Machine v4).
  2. VISUAL ENGINE    : 'Zenith-Glass' CSS. Frosted Glass effects, Soft Gradients, Professional Dark Mode.
  3. RENDERING        : Native HTML5 Lottie Embeds (Zero-Dependency).
  4. LOGIC LAYER      : Event-Driven Quiz Controller with Buffered Inputs.
  5. GAMIFICATION     : XP System, Daily Streak Algorithms, Badge Unlockers.
  ----------------------------------------------------------------------------------------------------------------------
  
  [CHANGE LOG v4.0]
  - REMOVED: Neon colors (distraction reduction).
  - ADDED: 'Glassmorphism' Design Language.
  - FIXED: Sidebar contrast issues (White artifact removal).
  - EXPANDED: Codebase modularity for Enterprise Scalability.
  
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
import json
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple, Union
from dataclasses import dataclass, field

# --- SYSTEM INITIALIZATION ---
st.set_page_config(
    page_title="IronClad Zenith",
    page_icon="💠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ADVANCED LOGGING ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("IronCladZenith")

# ======================================================================================================================
# SECTION 1: THE ZENITH VISUAL ENGINE (CSS ARCHITECTURE)
# ======================================================================================================================

class VisualAssets:
    """
    Central Repository for Visual Assets & Animations.
    Uses Direct Embeds to ensure 100% uptime without external libraries.
    """
    # Lottie JSON Embeds (Transparent Backgrounds)
    ANIM_HOME_BOT = "https://lottie.host/embed/9863db83-4940-4ce0-8e18-60914fb499cb/pYM5sC8O3e.json"
    ANIM_BRAIN_SCAN = "https://lottie.host/embed/d3e36569-2310-444b-9759-3221c56360b6/example.json" # Placeholder for brain
    ANIM_VICTORY_ROCKET = "https://lottie.host/embed/a8c62c96-0365-4d76-805c-3e3518b26118/pQk5sH4O1e.json" 
    ANIM_SQL_SERVER = "https://lottie.host/embed/93556c4d-9659-4d9d-9c36-749340915442/asset.json" # Generic Tech
    
    # Icons
    ICON_DASHBOARD = "🏠"
    ICON_LEARN = "🎓"
    ICON_CODE = "💻"
    ICON_USER = "👤"
    ICON_TROPHY = "🏆"
    ICON_FIRE = "🔥"

class ZenithUI:
    """
    The Graphics Rendering Core. 
    Implements 'Glassmorphism': Translucency, Blur, and Soft Shadows.
    """
    # Color Palette (Professional Dark Mode)
    COLOR_BG = "#0f172a"        # Slate 900
    COLOR_SURFACE = "#1e293b"   # Slate 800 (Glass Base)
    COLOR_ACCENT = "#3b82f6"    # Royal Blue
    COLOR_TEXT_MAIN = "#f1f5f9" # Slate 100
    COLOR_TEXT_SUB = "#94a3b8"  # Slate 400
    
    @staticmethod
    def inject_css():
        """
        Injects approx 200 lines of CSS to override Streamlit defaults 
        and create the premium 'Zenith' look.
        """
        st.markdown(f"""
        <style>
        /* --- IMPORT FONTS --- */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&family=JetBrains+Mono:wght@400;700&display=swap');
        
        /* --- VARIABLES --- */
        :root {{
            --bg-color: {ZenithUI.COLOR_BG};
            --glass-color: rgba(30, 41, 59, 0.7);
            --border-color: rgba(255, 255, 255, 0.08);
            --accent-color: {ZenithUI.COLOR_ACCENT};
            --text-main: {ZenithUI.COLOR_TEXT_MAIN};
        }}

        /* --- GLOBAL APP STYLING --- */
        .stApp {{
            background-color: var(--bg-color);
            background-image: 
                radial-gradient(at 0% 0%, rgba(59, 130, 246, 0.15) 0px, transparent 50%),
                radial-gradient(at 100% 0%, rgba(139, 92, 246, 0.15) 0px, transparent 50%);
            font-family: 'Inter', sans-serif;
            color: var(--text-main);
        }}

        /* --- SIDEBAR FIXES (NO MORE WHITE ARTIFACTS) --- */
        section[data-testid="stSidebar"] {{
            background-color: #0b1120; /* Darker than BG */
            border-right: 1px solid var(--border-color);
        }}
        
        section[data-testid="stSidebar"] .block-container {{
            padding-top: 2rem;
        }}
        
        div[data-testid="stSidebarNav"] ul {{
            padding-top: 0px;
        }}

        /* --- TYPOGRAPHY --- */
        h1, h2, h3 {{
            font-weight: 800;
            letter-spacing: -0.025em;
            background: linear-gradient(to right, #fff, #94a3b8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        
        .stMarkdown p {{
            font-size: 1.05rem;
            line-height: 1.6;
            color: #cbd5e1;
        }}

        /* --- GLASS CARDS (THE CORE DESIGN) --- */
        .zenith-card {{
            background: var(--glass-color);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 24px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }}
        
        .zenith-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
            border-color: rgba(255,255,255,0.2);
        }}

        /* --- BUTTONS (ELEGANT, NOT NEON) --- */
        .stButton > button {{
            background-color: rgba(255, 255, 255, 0.03);
            color: #fff;
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 0.6rem 1.2rem;
            font-weight: 600;
            transition: all 0.2s;
            width: 100%;
        }}
        
        .stButton > button:hover {{
            background-color: var(--accent-color);
            border-color: var(--accent-color);
            color: white;
            box-shadow: 0 0 15px rgba(59, 130, 246, 0.4);
        }}

        /* --- QUIZ SPECIFIC STYLES --- */
        .quiz-option-container {{
            background: rgba(0,0,0,0.2);
            border-radius: 12px;
            padding: 20px;
            border: 1px solid var(--border-color);
        }}

        /* --- SQL TERMINAL STYLING --- */
        .stTextArea textarea {{
            background-color: #0f172a !important;
            color: #a5b4fc !important;
            font-family: 'JetBrains Mono', monospace !important;
            border: 1px solid #334155 !important;
            border-radius: 8px !important;
        }}
        
        /* --- PROGRESS BARS --- */
        .stProgress > div > div > div > div {{
            background-color: var(--accent-color);
            background-image: linear-gradient(45deg, rgba(255,255,255,.15) 25%, transparent 25%, transparent 50%, rgba(255,255,255,.15) 50%, rgba(255,255,255,.15) 75%, transparent 75%, transparent);
            background-size: 1rem 1rem;
        }}

        /* --- TOASTS --- */
        .stToast {{
            background-color: var(--surface-color) !important;
            border: 1px solid var(--border-color) !important;
            color: white !important;
        }}
        
        /* --- ANIMATIONS --- */
        @keyframes float {{
            0% {{ transform: translateY(0px); }}
            50% {{ transform: translateY(-10px); }}
            100% {{ transform: translateY(0px); }}
        }}
        
        .floating-element {{
            animation: float 6s ease-in-out infinite;
        }}

        </style>
        """, unsafe_allow_html=True)

    @staticmethod
    def render_lottie(url: str, height: int = 300, key: str = "anim"):
        """
        Renders an animation using a clean Iframe to avoid dependencies.
        """
        st.markdown(f"""
            <div style="display: flex; justify-content: center; align-items: center; margin: 20px 0;">
                <iframe src="{url}" width="100%" height="{height}px" style="border:none; background:transparent; overflow:hidden;"></iframe>
            </div>
        """, unsafe_allow_html=True)

# ======================================================================================================================
# SECTION 2: ENTERPRISE DATA MODELS
# ======================================================================================================================

@dataclass
class Badge:
    """Represents an achievement."""
    id: str
    name: str
    icon: str
    description: str
    unlocked: bool = False

@dataclass
class UserProfile:
    """
    User Entity with Gamification Stats.
    """
    username: str = "Administrator"
    role: str = "Solutions Architect"
    xp: int = 15800
    current_streak: int = 1
    max_streak: int = 5
    total_questions_answered: int = 0
    correct_answers: int = 0
    badges: List[Badge] = field(default_factory=list)

    def __post_init__(self):
        if not self.badges:
            self.badges = [
                Badge("b1", "First Step", "🌱", "Completed the first module"),
                Badge("b2", "Sniper", "🎯", "10 Correct answers in a row"),
                Badge("b3", "Iron Mind", "🧠", "Reached Level 20")
            ]

    @property
    def level(self) -> int:
        return (self.xp // 1000) + 1

    @property
    def progress_to_next_level(self) -> float:
        return (self.xp % 1000) / 1000.0

    def add_xp(self, amount: int):
        self.xp += amount
        self.total_questions_answered += 1

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
# SECTION 3: STATE MACHINE CONTROLLER
# ======================================================================================================================

class QuizPhase(enum.Enum):
    SETUP = 0
    PLAYING = 1
    COMPLETED = 2

class AppState:
    """
    Global State Manager. 
    Implements the Singleton Pattern logic via Streamlit Session State.
    """
    KEY = "ZENITH_CORE_STATE"

    @classmethod
    def _initialize(cls):
        if cls.KEY not in st.session_state:
            st.session_state[cls.KEY] = {
                # Routing
                "view": "DASHBOARD",
                
                # User Data
                "user": UserProfile(),
                
                # Quiz Engine State
                "quiz": {
                    "phase": QuizPhase.SETUP,
                    "active_topic": None,
                    "active_level": None,
                    "deck": [],
                    "current_index": 0,
                    "score": 0,
                    "user_selection": None,  # For UI binding
                    "feedback_mode": False   # True if showing answer
                },
                
                # SQL Engine State
                "sql_history": []
            }

    @classmethod
    def get(cls) -> Dict:
        cls._initialize()
        return st.session_state[cls.KEY]

    @classmethod
    def user(cls) -> UserProfile:
        return cls.get()["user"]

    @classmethod
    def quiz(cls) -> Dict:
        return cls.get()["quiz"]

    @classmethod
    def set_view(cls, view_name: str):
        cls.get()["view"] = view_name

# ======================================================================================================================
# SECTION 4: DATA REPOSITORY (ADAPTER PATTERN)
# ======================================================================================================================

class ContentRepository:
    """
    Handles data ingestion with robust error handling.
    """
    FILE = "preguntas.py"

    @staticmethod
    def fetch_data() -> Dict:
        path = os.path.join(os.getcwd(), ContentRepository.FILE)
        
        # 1. Existence Check
        if not os.path.exists(path):
            return ContentRepository._get_fallback_data("File Missing")

        # 2. Dynamic Import
        try:
            spec = importlib.util.spec_from_file_location("zenith_content", path)
            module = importlib.util.module_from_spec(spec)
            sys.modules["zenith_content"] = module
            spec.loader.exec_module(module)
            
            if not hasattr(module, 'temas'):
                return ContentRepository._get_fallback_data("Invalid Structure")
                
            return ContentRepository._clean_data(module.temas)
            
        except Exception as e:
            st.error(f"Critical Data Error: {e}")
            return ContentRepository._get_fallback_data("Corruption Detected")

    @staticmethod
    def _clean_data(raw_data: Dict) -> Dict:
        """
        Normalizes the data structure to prevent TypeErrors in the UI.
        """
        clean = {}
        for topic, content in raw_data.items():
            if isinstance(content, list):
                # Handle cases where data is wrapped in a list
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
    def _get_fallback_data(reason: str) -> Dict:
        return {
            f"SYSTEM RECOVERY ({reason})": {
                "Level 1: Diagnostics": [
                    {
                        "pregunta": "System Status Check",
                        "opciones": ["Online", "Offline", "Rebooting"],
                        "correcta": "Online",
                        "explicacion": "Fallback system engaged successfully.",
                        "traduccion": "Sistema en línea."
                    }
                ]
            }
        }

# ======================================================================================================================
# SECTION 5: LOGIC CONTROLLERS (MVC PATTERN)
# ======================================================================================================================

class QuizEngine:
    """
    Manages the logic for the Training Modules.
    """
    def __init__(self):
        self.repo = ContentRepository.fetch_data()

    def render_selector(self):
        st.markdown(f"## {VisualAssets.ICON_LEARN} Select Training Module")
        st.markdown("Choose a knowledge domain to begin synchronization.")
        
        topics = list(self.repo.keys())
        cols = st.columns(2)
        
        for i, topic in enumerate(topics):
            with cols[i % 2]:
                st.markdown(f"""
                <div class="zenith-card" style="cursor: pointer; text-align:center;">
                    <h3 style="margin-bottom: 10px;">{topic}</h3>
                    <div style="height: 4px; width: 50px; background: #3b82f6; margin: 0 auto; border-radius: 2px;"></div>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"Initialize {topic}", key=f"start_{i}", use_container_width=True):
                    q = AppState.quiz()
                    q["active_topic"] = topic
                    st.rerun()

    def render_level_selector(self):
        q = AppState.quiz()
        topic = q["active_topic"]
        
        st.markdown(f"## {VisualAssets.ICON_CODE} {topic} // Configuration")
        if st.button("← Return to Modules", type="secondary"):
            q["active_topic"] = None
            st.rerun()
            
        levels = list(self.repo[topic].keys())
        st.divider()
        
        c1, c2, c3 = st.columns(3)
        cols = [c1, c2, c3]
        
        for i, lvl in enumerate(levels):
            with cols[i % 3]:
                st.markdown(f"""
                <div class="zenith-card" style="text-align: center;">
                    <h1 style="font-size: 3rem; opacity: 0.2;">0{i+1}</h1>
                    <h3>{lvl}</h3>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"Launch {lvl}", key=f"lvl_{i}", use_container_width=True):
                    self._start_session(topic, lvl)

    def _start_session(self, topic, lvl):
        raw_list = self.repo[topic][lvl]
        deck = []
        for item in raw_list:
            opts = item.get("opciones", ["Error"])
            random.shuffle(opts)
            deck.append(Question(
                id=str(uuid.uuid4()),
                text=item.get("pregunta", "Error loading text"),
                options=opts,
                correct_option=item.get("correcta", ""),
                explanation=item.get("explicacion", "No data."),
                translation=item.get("traduccion", "No data.")
            ))
        
        random.shuffle(deck)
        q = AppState.quiz()
        q["deck"] = deck
        q["current_index"] = 0
        q["score"] = 0
        q["phase"] = QuizPhase.PLAYING
        q["feedback_mode"] = False
        q["user_selection"] = None
        st.rerun()

    def render_gameplay(self):
        q = AppState.quiz()
        deck = q["deck"]
        idx = q["current_index"]
        
        # Check Win Condition
        if idx >= len(deck):
            self._render_victory()
            return

        question = deck[idx]
        
        # --- HUD ---
        c1, c2, c3 = st.columns([1, 4, 1])
        c1.markdown(f"**Q-{idx+1}** / {len(deck)}")
        c2.progress(idx / len(deck))
        c3.markdown(f"**XP:** {AppState.user().xp}")

        # --- QUESTION CARD ---
        st.markdown(f"""
        <div class="zenith-card">
            <h2 style="font-size: 1.5rem; color: white;">{question.text}</h2>
        </div>
        """, unsafe_allow_html=True)

        # --- INTERACTION LAYER ---
        # Bug Fix: We check if we are in feedback mode. 
        # If yes, we disable inputs. If no, we enable them.
        
        if not q["feedback_mode"]:
            # --- INPUT STATE ---
            selection = st.radio(
                "Select the correct syntax:", 
                question.options, 
                index=None, 
                key=f"radio_{question.id}"
            )
            
            st.write("") # Spacing
            
            if st.button("Confirm Selection", type="primary", use_container_width=True):
                if not selection:
                    st.toast("Please make a selection first.", icon="⚠️")
                else:
                    # Transition to Feedback Mode
                    q["user_selection"] = selection
                    q["feedback_mode"] = True
                    
                    # Logic
                    if selection.strip() == question.correct_option.strip():
                        q["score"] += 1
                        AppState.user().add_xp(150)
                        AppState.user().current_streak += 1
                        st.toast("Correct! XP +150", icon="✅")
                    else:
                        AppState.user().current_streak = 0
                        st.toast("Incorrect Protocol.", icon="❌")
                    
                    st.rerun()
        
        else:
            # --- FEEDBACK STATE ---
            user_sel = q["user_selection"]
            is_correct = (user_sel.strip() == question.correct_option.strip())
            
            if is_correct:
                st.success(f"✅ Correct! The answer is **{question.correct_option}**")
            else:
                st.error(f"❌ Incorrect. You selected **{user_sel}**.")
                st.markdown(f"**Correct Answer:** `{question.correct_option}`")

            # Explanation Card
            st.markdown(f"""
            <div class="zenith-card" style="border-left: 4px solid #3b82f6;">
                <h4 style="margin-top:0;">Analysis</h4>
                <p>{question.explanation}</p>
                <hr style="border-color: rgba(255,255,255,0.1);">
                <small style="color: #94a3b8;">Translation: {question.translation}</small>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Next Question →", type="primary", use_container_width=True):
                q["current_index"] += 1
                q["feedback_mode"] = False
                q["user_selection"] = None
                st.rerun()

    def _render_victory(self):
        q = AppState.quiz()
        ZenithUI.render_lottie(VisualAssets.ANIM_VICTORY_ROCKET, 400)
        
        st.markdown(f"""
        <div class="zenith-card" style="text-align: center;">
            <h1 style="font-size: 3rem; color: #3b82f6;">Module Complete</h1>
            <h3>Score: {q['score']} / {len(q['deck'])}</h3>
            <p>Database synchronization finished.</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Return to Dashboard", use_container_width=True):
            q["active_topic"] = None
            q["phase"] = QuizPhase.SETUP
            AppState.set_view("DASHBOARD")
            st.rerun()

class SQLEngine:
    """
    Mock SQL Environment logic.
    """
    def render(self):
        st.markdown(f"## {VisualAssets.ICON_CODE} SQL Workbench")
        st.markdown("Execute T-SQL queries against the production replica.")
        
        col_main, col_sidebar = st.columns([3, 1])
        
        with col_main:
            query = st.text_area("SQL Editor", height=200, placeholder="SELECT * FROM Users WHERE...", key="sql_editor")
            
            if st.button("Execute Query", type="primary"):
                self._run_query(query)
                
        with col_sidebar:
            st.markdown("### Schema")
            st.code("""
PK ID (int)
   Username (varchar)
   Role (varchar)
   LastLogin (datetime)
            """, language="sql")
            
            st.info("ReadOnly Mode Active")

    def _run_query(self, sql):
        if not sql.strip():
            st.warning("Buffer empty.")
            return
            
        if "select" not in sql.lower():
            st.error("Access Denied: WRITE operations forbidden.")
            return
            
        # Simulate Processing
        with st.spinner("Processing..."):
            time.sleep(0.5)
            
        # Mock Data
        data = [
            {"ID": 101, "Username": "SysAdmin", "Role": "Root", "LastLogin": "2024-01-01"},
            {"ID": 102, "Username": "DevOps_01", "Role": "User", "LastLogin": "2024-01-02"},
            {"ID": 103, "Username": "Analyst_HQ", "Role": "Viewer", "LastLogin": "2024-01-03"},
        ]
        
        st.success("Query executed successfully (14ms)")
        st.dataframe(pd.DataFrame(data), use_container_width=True)

class DashboardController:
    """
    Manages the Home View.
    """
    def render(self):
        user = AppState.user()
        
        # Header
        c1, c2 = st.columns([2, 1])
        with c1:
            st.markdown(f"""
            <div style="padding: 40px 0;">
                <h1 style="font-size: 4rem; line-height: 1.1;">IRONCLAD<br><span style="color: #3b82f6;">ZENITH</span></h1>
                <p style="font-size: 1.2rem; color: #94a3b8; margin-top: 10px;">
                    Welcome, {user.username}.<br>
                    Enterprise Learning Environment v4.0
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            b1, b2 = st.columns(2)
            if b1.button("Start Training", type="primary", use_container_width=True):
                AppState.set_view("TRAINING")
                st.rerun()
            if b2.button("Open SQL Lab", use_container_width=True):
                AppState.set_view("SQL")
                st.rerun()
                
        with c2:
            ZenithUI.render_lottie(VisualAssets.ANIM_HOME_BOT, 300)

        # Stats Cards
        st.divider()
        k1, k2, k3 = st.columns(3)
        
        with k1:
            st.markdown(f"""
            <div class="zenith-card">
                <h3>{VisualAssets.ICON_FIRE} Streak</h3>
                <h2 style="color: #f59e0b;">{user.current_streak} Days</h2>
                <p>Keep it up!</p>
            </div>
            """, unsafe_allow_html=True)
            
        with k2:
            st.markdown(f"""
            <div class="zenith-card">
                <h3>{VisualAssets.ICON_TROPHY} Level</h3>
                <h2 style="color: #3b82f6;">{user.level}</h2>
                <p>{user.xp} Total XP</p>
            </div>
            """, unsafe_allow_html=True)
            
        with k3:
            st.markdown(f"""
            <div class="zenith-card">
                <h3>{VisualAssets.ICON_CODE} Completion</h3>
                <h2 style="color: #10b981;">{user.total_questions_answered} Ops</h2>
                <p>Questions Answered</p>
            </div>
            """, unsafe_allow_html=True)

# ======================================================================================================================
# SECTION 6: MAIN APPLICATION LOOP
# ======================================================================================================================

def render_sidebar():
    user = AppState.user()
    
    with st.sidebar:
        # Profile Section
        st.markdown(f"""
        <div style="text-align: center; margin-bottom: 20px;">
            <div style="width: 80px; height: 80px; background: linear-gradient(135deg, #3b82f6, #0f172a); border-radius: 50%; margin: 0 auto 10px; display: flex; align-items: center; justify-content: center; font-size: 2rem; font-weight: bold; border: 2px solid rgba(255,255,255,0.1);">
                {user.username[:2]}
            </div>
            <h3 style="margin:0;">{user.username}</h3>
            <p style="font-size: 0.8rem; color: #94a3b8;">{user.role}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # XP Bar
        st.progress(user.progress_to_next_level)
        st.caption(f"Progress to Level {user.level + 1}")
        
        st.divider()
        
        # Menu
        if st.button(f"{VisualAssets.ICON_DASHBOARD} Dashboard", use_container_width=True):
            AppState.set_view("DASHBOARD")
            st.rerun()
            
        if st.button(f"{VisualAssets.ICON_LEARN} Training", use_container_width=True):
            AppState.set_view("TRAINING")
            st.rerun()
            
        if st.button(f"{VisualAssets.ICON_CODE} SQL Lab", use_container_width=True):
            AppState.set_view("SQL")
            st.rerun()
            
        st.divider()
        
        # Footer
        st.markdown("""
        <div style="text-align: center; color: #475569; font-size: 0.7rem;">
            IRONCLAD ZENITH v4.0<br>
            Secure Connection
        </div>
        """, unsafe_allow_html=True)

def main():
    # 1. Initialize CSS
    ZenithUI.inject_css()
    
    # 2. Render Sidebar
    render_sidebar()
    
    # 3. Router
    view = AppState.get()["view"]
    
    if view == "DASHBOARD":
        DashboardController().render()
        
    elif view == "TRAINING":
        ctrl = QuizEngine()
        q = AppState.quiz()
        
        if q["active_topic"] is None:
            ctrl.render_selector()
        elif q["phase"] == QuizPhase.SETUP:
            ctrl.render_level_selector()
        elif q["phase"] == QuizPhase.PLAYING:
            ctrl.render_gameplay()
            
    elif view == "SQL":
        SQLEngine().render()

if __name__ == "__main__":
    main()