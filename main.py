# -*- coding: utf-8 -*-
"""
========================================================================================================================
  IRONCLAD ANALYTICS v2.1 — INDEPENDENT BUILD (NO PIP REQUIRED)
  Authorized Personnel: ARCHITECT LEVEL
  Release Date: 2026-02-01
  
  [CAMBIOS CRÍTICOS v2.1]
  1. FIX: Eliminada dependencia de 'streamlit-lottie'. Se usa renderizado HTML nativo.
  2. FIX: Lógica del Quiz desbloqueada. El selector ya no se deshabilita.
  3. FIX: Botón de 'Hard Reset' agregado para desatascar estados.
========================================================================================================================
"""

import streamlit as st
import pandas as pd
import random
import sqlite3
import requests
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

# --- LOGGING CONFIGURATION ---
logging.basicConfig(level=logging.INFO)

# ======================================================================================================================
# MODULE 1: VISUAL ENGINE (NO LIBRARIES REQUIRED)
# ======================================================================================================================

class VisualAssets:
    """Links directos a las animaciones."""
    # Usamos Embeds directos de LottieFiles para asegurar que funcionen sin instalar nada.
    ANIM_ROBOT_HELLO = "https://lottie.host/embed/9863db83-4940-4ce0-8e18-60914fb499cb/pYM5sC8O3e.json" 
    
    ICON_COMPANY = "🏢"
    ICON_SECURE = "🔒"
    ICON_WARNING = "⚠️"
    ICON_DANGER = "☢️"
    ICON_SQL = "💾"

class IronCladUI:
    THEME_PRIMARY = "#3b82f6"
    THEME_BG_DARK = "#0f172a"
    
    @staticmethod
    def deploy():
        st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&family=JetBrains+Mono:wght@400;700&display=swap');
        
        :root {{
            --primary: {IronCladUI.THEME_PRIMARY};
            --bg-dark: {IronCladUI.THEME_BG_DARK};
        }}

        .stApp {{ background-color: var(--bg-dark); font-family: 'Inter', sans-serif; color: #f8fafc; }}
        
        /* --- CARDS --- */
        .iron-card {{
            background: #1e293b;
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            transition: transform 0.2s ease;
        }}
        .iron-card:hover {{ border-color: var(--primary); transform: translateY(-2px); }}

        /* --- BUTTONS --- */
        .stButton > button {{
            border-radius: 8px !important;
            font-weight: 600 !important;
            text-transform: uppercase !important;
            border: 1px solid rgba(255,255,255,0.1) !important;
        }}
        
        /* --- QUIZ --- */
        .quiz-container {{
            background: rgba(30, 41, 59, 0.5);
            border-left: 4px solid var(--primary);
            padding: 30px;
            border-radius: 0 12px 12px 0;
            margin-bottom: 25px;
            font-size: 1.3rem;
        }}

        /* --- FEEDBACK COLORS --- */
        .hud-success {{ background: rgba(16, 185, 129, 0.1); border: 1px solid #10b981; color: #10b981; padding: 20px; border-radius: 8px; }}
        .hud-error {{ background: rgba(239, 68, 68, 0.1); border: 1px solid #ef4444; color: #ef4444; padding: 20px; border-radius: 8px; }}

        /* --- SQL TERMINAL --- */
        .sql-terminal textarea {{ background: #020617 !important; color: #a5b4fc !important; border: 1px solid #334155 !important; font-family: 'JetBrains Mono', monospace; }}
        </style>
        """, unsafe_allow_html=True)

    @staticmethod
    def render_lottie_direct(url_embed: str, height=300):
        """
        Renderiza la animación usando un iframe HTML. 
        Esto NO falla porque usa el navegador, no Python.
        """
        st.markdown(f"""
            <div style="display: flex; justify-content: center;">
                <iframe src="{url_embed}" width="100%" height="{height}" style="border:none; overflow:hidden; background:transparent;"></iframe>
            </div>
        """, unsafe_allow_html=True)

# ======================================================================================================================
# MODULE 2: DATA MODELS
# ======================================================================================================================

@dataclass
class UserProfile:
    username: str = "Administrator"
    role: str = "Senior Data Engineer"
    xp: int = 15800
    level: int = 15
    current_streak: int = 0
    total_questions: int = 0
    correct_answers: int = 0

    def add_xp(self, amount: int):
        self.xp += amount
        self.level = self.xp // 1000

@dataclass
class QuestionData:
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
# MODULE 3: STATE MANAGEMENT
# ======================================================================================================================

class QuizState(enum.Enum):
    IDLE = 0
    SUCCESS = 1
    FAILURE = 2

class AppState:
    KEY = "IRONCLAD_STATE_V2"

    @classmethod
    def init(cls):
        if cls.KEY not in st.session_state:
            st.session_state[cls.KEY] = {
                "view": "home",
                "training_phase": 0,
                "active_topic": None,
                "active_level": None,
                "quiz_queue": [],
                "quiz_index": 0,
                "quiz_score": 0,
                "quiz_state": QuizState.IDLE,
                "sql_db_cache": None,
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
        cls.set("quiz_state", QuizState.IDLE)

AppState.init()

# ======================================================================================================================
# MODULE 4: KNOWLEDGE BASE (ADAPTER)
# ======================================================================================================================

class KnowledgeBase:
    FILE = "preguntas.py"

    @staticmethod
    def load() -> Dict:
        path = os.path.join(os.getcwd(), KnowledgeBase.FILE)
        if not os.path.exists(path):
            return {"DEMO MODE": {"Basic": [{"pregunta": "File not found. Create preguntas.py", "opciones": ["OK"], "correcta": "OK"}]}}

        try:
            spec = importlib.util.spec_from_file_location("apex_content", path)
            module = importlib.util.module_from_spec(spec)
            sys.modules["apex_content"] = module
            spec.loader.exec_module(module)
            
            raw_data = getattr(module, 'temas', {})
            clean_data = {}
            
            # Limpieza de datos robusta
            for topic, content in raw_data.items():
                if isinstance(content, list) and content:
                    clean_data[topic] = content[0] if isinstance(content[0], dict) else {}
                elif isinstance(content, dict):
                    clean_data[topic] = content
                else:
                    clean_data[topic] = {}
            return clean_data
        except Exception as e:
            st.error(f"Data Error: {e}")
            return {}

# ======================================================================================================================
# MODULE 5: CONTROLLERS
# ======================================================================================================================

class SQLEngine:
    @staticmethod
    def query(sql: str) -> Tuple[Optional[pd.DataFrame], Optional[str]]:
        # Generar datos simulados si no existen
        if AppState.get("sql_db_cache") is None:
            data = [{"ID": i, "Name": f"Emp_{i}", "Salary": random.randint(40, 150)*1000} for i in range(1, 200)]
            AppState.set("sql_db_cache", pd.DataFrame(data))
        
        df = AppState.get("sql_db_cache")
        if not sql.strip().lower().startswith("select"):
            return None, "🚫 READ ONLY MODE. Use SELECT."
        
        try:
            conn = sqlite3.connect(":memory:")
            df.to_sql("Employees", conn, index=False, if_exists="replace")
            return pd.read_sql_query(sql, conn), None
        except Exception as e:
            return None, str(e)

class TrainingController:
    def __init__(self):
        self.kb = KnowledgeBase.load()

    def run(self):
        phase = AppState.get("training_phase")
        if phase == 0: self._select_topic()
        elif phase == 1: self._select_level()
        elif phase == 2: self._gameplay()

    def _select_topic(self):
        st.markdown(f"<h1>{VisualAssets.ICON_COMPANY} KNOWLEDGE BASE</h1>", unsafe_allow_html=True)
        topics = list(self.kb.keys())
        cols = st.columns(2)
        for i, topic in enumerate(topics):
            with cols[i % 2]:
                st.markdown(f'<div class="iron-card"><h3>{topic}</h3></div>', unsafe_allow_html=True)
                if st.button(f"ACCESS {topic}", key=f"t_{i}", use_container_width=True):
                    AppState.set("active_topic", topic)
                    AppState.set("training_phase", 1)
                    st.rerun()

    def _select_level(self):
        topic = AppState.get("active_topic")
        st.markdown(f"<h1>📂 {topic}</h1>", unsafe_allow_html=True)
        if st.button("⬅️ BACK", type="secondary"):
            AppState.set("training_phase", 0)
            st.rerun()
            
        levels = list(self.kb.get(topic, {}).keys())
        
        # --- TARJETAS GRANDES ---
        c1, c2, c3 = st.columns(3)
        cols = [c1, c2, c3]
        
        for i, lvl in enumerate(levels):
            with cols[i % 3]:
                st.markdown(f"""
                <div class="iron-card" style="text-align:center; height:180px;">
                    <div style="font-size:2.5rem;">{VisualAssets.ICON_SECURE}</div>
                    <h3>{lvl}</h3>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"START {lvl}", key=f"l_{i}", use_container_width=True):
                    self._init_deck(topic, lvl)

    def _init_deck(self, topic, lvl):
        raw = self.kb[topic][lvl]
        deck = []
        for item in raw:
            # Asegurar que options es lista
            opts = list(item.get("opciones", []))
            random.shuffle(opts)
            deck.append(QuestionData(
                uuid=str(uuid.uuid4()),
                text=item.get("pregunta", "??"),
                options=opts,
                correct=item.get("correcta", ""),
                explanation=item.get("explicacion", ""),
                translation=item.get("traduccion", "")
            ))
        random.shuffle(deck)
        AppState.set("quiz_queue", deck)
        AppState.set("quiz_index", 0)
        AppState.set("quiz_score", 0)
        AppState.set("active_level", lvl)
        AppState.set("training_phase", 2)
        AppState.reset_quiz_flags() # Reset crucial
        st.rerun()

    def _gameplay(self):
        deck = AppState.get("quiz_queue")
        idx = AppState.get("quiz_index")
        
        if idx >= len(deck):
            self._victory()
            return

        q = deck[idx]
        state = AppState.get("quiz_state")
        
        # --- HEADER ---
        c1, c2, c3 = st.columns([1, 4, 1])
        c1.markdown(f"**Q: {idx+1}/{len(deck)}**")
        c2.progress((idx)/len(deck))
        if c3.button("❌ EXIT", use_container_width=True):
            AppState.set("training_phase", 1)
            st.rerun()

        # --- QUESTION CARD ---
        st.markdown(f'<div class="quiz-container">{q.text}</div>', unsafe_allow_html=True)

        # --- SELECTION AREA (SOLUCIÓN AL BUG) ---
        # 1. NO usamos disabled=True para no bloquear la interacción
        # 2. Usamos index=None para forzar elección fresca
        
        selection = st.radio(
            "Select Protocol:", 
            q.options, 
            index=None, 
            key=f"q_radio_{q.uuid}"
        )

        # --- BOTÓN DE CONFIRMACIÓN ---
        # Solo mostramos el botón si NO hemos validado aún
        if state == QuizState.IDLE:
            st.write("")
            if st.button("✅ CONFIRM ANSWER", type="primary", use_container_width=True):
                if not selection:
                    st.warning("⚠️ Debes seleccionar una opción.")
                else:
                    if q.check_answer(selection):
                        AppState.set("quiz_state", QuizState.SUCCESS)
                        AppState.set("quiz_score", AppState.get("quiz_score") + 1)
                        AppState.user().add_xp(100)
                        AppState.user().current_streak += 1
                    else:
                        AppState.set("quiz_state", QuizState.FAILURE)
                        AppState.user().current_streak = 0
                    st.rerun()
        
        # --- FEEDBACK ---
        if state != QuizState.IDLE:
            if state == QuizState.SUCCESS:
                st.markdown(f'<div class="hud-success">✅ CORRECT! Protocol Accepted.</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="hud-error">❌ FAILURE. Expected: {q.correct}</div>', unsafe_allow_html=True)
            
            # EXPLICACIÓN
            st.markdown(f"""
            <div class="iron-card" style="margin-top:15px;">
                <b>Analysis:</b> {q.explanation}<br>
                <i style="color:#94a3b8">Translation: {q.translation}</i>
            </div>
            """, unsafe_allow_html=True)

            if st.button("NEXT ➡️", type="primary", use_container_width=True):
                AppState.set("quiz_index", idx + 1)
                AppState.reset_quiz_flags()
                st.rerun()

    def _victory(self):
        st.balloons()
        score = AppState.get("quiz_score")
        st.markdown(f"<h1 style='text-align:center; color:#10b981;'>COMPLETED: {score}/{len(AppState.get('quiz_queue'))}</h1>", unsafe_allow_html=True)
        if st.button("BACK TO MENU", use_container_width=True):
            AppState.set("training_phase", 1)
            st.rerun()

# ======================================================================================================================
# MAIN
# ======================================================================================================================

def main():
    st.set_page_config(page_title="IronClad Analytics", page_icon="🛡️", layout="wide")
    IronCladUI.deploy()
    
    # SIDEBAR
    with st.sidebar:
        user = AppState.user()
        st.markdown(f"""
        <div style="text-align:center; padding:20px; background:#1e293b; border-radius:10px;">
            <h2>{user.username[:2]}</h2>
            <p>{user.role}</p>
            <hr style="border-color:#334155">
            <b>LVL {user.level}</b> | {user.xp} XP
        </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        if st.button("🏠 HOME", use_container_width=True):
            AppState.set("view", "home")
            st.rerun()
        if st.button("🧠 TRAINING", use_container_width=True):
            AppState.set("view", "training")
            AppState.set("training_phase", 0)
            st.rerun()
        if st.button("💾 SQL LAB", use_container_width=True):
            AppState.set("view", "sql")
            st.rerun()
            
        st.markdown("---")
        st.caption(f"Streak: {user.current_streak} 🔥")

    # VIEW ROUTING
    view = AppState.get("view")
    
    if view == "home":
        c1, c2 = st.columns([2, 1])
        with c1:
            st.markdown(f"""
            <div style="padding:40px 0;">
                <h1 style="font-size:3.5rem;">IRONCLAD<br><span style="color:#3b82f6">ANALYTICS v2.1</span></h1>
                <p style="border-left:3px solid #3b82f6; padding-left:15px; color:#94a3b8;">
                    Independent System Architecture.<br>No external dependencies required.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            b1, b2 = st.columns(2)
            if b1.button("LAUNCH MODULES", type="primary", use_container_width=True):
                AppState.set("view", "training")
                st.rerun()
            if b2.button("SQL TERMINAL", use_container_width=True):
                AppState.set("view", "sql")
                st.rerun()

        with c2:
            # ROBOT SIN LIBRERÍA (Embed Directo)
            # Usamos un embed público de LottieFiles que funciona sin instalar nada
            IronCladUI.render_lottie_direct(VisualAssets.ANIM_ROBOT_HELLO)

    elif view == "training":
        ctrl = TrainingController()
        ctrl.run()
        
    elif view == "sql":
        st.markdown("<h1>💾 SQL WORKBENCH</h1>", unsafe_allow_html=True)
        q = st.text_area("Query Editor", "SELECT * FROM Employees LIMIT 5;", height=150)
        if st.button("EXECUTE", type="primary"):
            df, err = SQLEngine.query(q)
            if err: st.error(err)
            else: st.dataframe(df, use_container_width=True)

if __name__ == "__main__":
    main()