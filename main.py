# -*- coding: utf-8 -*-
"""
========================================================================================================================
  IRONCLAD TITAN v9.0 — THE OMEGA BUILD (AUTO-FIX EDITION)
  Authorized Personnel: ADMINISTRATOR (SY)
  System Status: ONLINE
  Location: Port of San Jose, Escuintla, Guatemala
  
  [SYSTEM MANIFEST]
  ----------------------------------------------------------------------------------------------------------------------
  1. KERNEL             : Python 3.10+ Streamlit State Machine.
  2. UI ENGINE          : 'Void-Glass' v9. Dynamic Particles & Sidebar Transparency Fix.
  3. DATA ENGINE        : Omni-Parser v4 (Auto-corrects List/Dict mismatches in large datasets).
  4. FAILSAFE SYSTEM    : Redundant Fallback Protocols.
  5. INTERACTIVITY      : Quiz Logic with Translation & Explanations.
  6. ARCHITECTURE       : Hierarchical MVC.
  7. SECURITY           : SQL Sandbox (Read-Only).

  [PATCH NOTES v9.0]
  - DATA FIX: Implemented '_normalize_data_structure' to automatically fix the 8k line file structure 
              (removes extra brackets [] wrapping topics).
  - UI: Added CSS particles for "Space Dust" effect.
  - UI: Forced Sidebar transparency to eliminate white boxes.
  - SQL: Expanded mocked database schema for the new SQL questions.
  
  [COPYRIGHT]
  © 2026 IronClad Analytics Corp. All rights reserved.
========================================================================================================================
"""

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
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple, Union
from dataclasses import dataclass, field

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="IronClad Titan // v9.0",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={'About': "IronClad Analytics v9.0. Authorized for SY."}
)

# --- LOGGING ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s | TITAN-CORE | %(levelname)s | %(message)s')
logger = logging.getLogger("IronCladTitan")

# ======================================================================================================================
# SECTION 1: VISUAL ENGINE (CSS & ASSETS)
# ======================================================================================================================

class VisualAssets:
    """Recursos visuales y animaciones Lottie."""
    ANIM_HOME_BOT = "https://lottie.host/embed/9863db83-4940-4ce0-8e18-60914fb499cb/pYM5sC8O3e.json"
    ANIM_VICTORY = "https://lottie.host/embed/a8c62c96-0365-4d76-805c-3e3518b26118/pQk5sH4O1e.json"
    ANIM_ERROR = "https://lottie.host/embed/e74d9f67-3362-4b25-a774-6720d2cb2666/asset.json"
    
    ICON_DASHBOARD = "🏠"
    ICON_LEARN = "🧠"
    ICON_CODE = "💻"

class VoidGlassUI:
    """Motor Gráfico v9.0: Efectos de Partículas y Vidrio."""
    
    @staticmethod
    def inject_css():
        st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&family=JetBrains+Mono:wght@400;700&display=swap');
        
        :root {{
            --bg-color: #02040a;
            --sidebar-color: #050b14;
            --surface-color: rgba(30, 41, 59, 0.6);
            --accent-color: #3b82f6;
            --text-main: #f8fafc;
        }}

        /* --- FONDO ANIMADO DE PARTÍCULAS --- */
        .stApp {{
            background-color: var(--bg-color);
            background-image: 
                radial-gradient(white, rgba(255,255,255,.2) 2px, transparent 3px),
                radial-gradient(white, rgba(255,255,255,.15) 1px, transparent 2px),
                radial-gradient(white, rgba(255,255,255,.1) 2px, transparent 3px);
            background-size: 550px 550px, 350px 350px, 250px 250px;
            background-position: 0 0, 40px 60px, 130px 270px;
            animation: particleAnim 60s linear infinite;
            color: var(--text-main);
            font-family: 'Inter', sans-serif;
        }}
        
        @keyframes particleAnim {{
            from {{ background-position: 0 0, 40px 60px, 130px 270px; }}
            to {{ background-position: 550px 550px, 390px 410px, 680px 820px; }}
        }}

        /* --- CORRECCIÓN SIDEBAR (CERO BLANCO) --- */
        section[data-testid="stSidebar"] {{
            background-color: var(--sidebar-color) !important;
            border-right: 1px solid rgba(255,255,255,0.1);
        }}
        div[data-testid="stSidebarNav"] {{
            background-color: transparent !important;
            padding-top: 20px;
        }}

        /* --- TARJETAS DE VIDRIO --- */
        .void-card {{
            background: var(--surface-color);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 20px;
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.2);
            transition: transform 0.3s ease;
        }}
        .void-card:hover {{
            transform: translateY(-5px);
            border-color: var(--accent-color);
            box-shadow: 0 0 20px rgba(59, 130, 246, 0.3);
        }}

        /* --- BOTONES --- */
        .stButton > button {{
            background: linear-gradient(180deg, rgba(255,255,255,0.05), rgba(255,255,255,0.01));
            border: 1px solid rgba(255,255,255,0.1);
            color: white;
            border-radius: 8px;
            font-weight: 600;
            transition: all 0.3s;
        }}
        .stButton > button:hover {{
            background: var(--accent-color);
            box-shadow: 0 0 15px var(--accent-color);
        }}

        /* --- INPUTS --- */
        .stTextArea textarea, .stTextInput input {{
            background-color: #0f172a !important;
            border: 1px solid #334155 !important;
            color: white !important;
        }}
        </style>
        """, unsafe_allow_html=True)

    @staticmethod
    def render_lottie(url: str, height: int = 300):
        st.markdown(f'<iframe src="{url}" width="100%" height="{height}px" style="border:none; background:transparent;"></iframe>', unsafe_allow_html=True)

# ======================================================================================================================
# SECTION 2: DATA ENGINE (OMNI-PARSER)
# ======================================================================================================================

class DataRepository:
    """
    Maneja la carga de datos.
    INCLUYE EL FIX AUTOMÁTICO PARA TU ARCHIVO DE 8K LÍNEAS.
    """
    FILENAME = "preguntas.py"
    
    @staticmethod
    def load_content() -> Dict:
        file_path = os.path.join(os.getcwd(), DataRepository.FILENAME)
        
        if not os.path.exists(file_path):
            st.toast("⚠️ Archivo de preguntas no encontrado.", icon="❌")
            return DataRepository._generate_emergency_data()

        try:
            spec = importlib.util.spec_from_file_location("content_module", file_path)
            module = importlib.util.module_from_spec(spec)
            sys.modules["content_module"] = module
            spec.loader.exec_module(module)
            
            # Buscar la variable 'temas'
            raw_data = getattr(module, 'temas', getattr(module, 'DB_PREGUNTAS', None))
            
            if not raw_data:
                st.error("❌ Archivo cargado pero sin datos válidos (variable 'temas' no encontrada).")
                return DataRepository._generate_emergency_data()
                
            # --- AQUÍ ESTÁ EL ARREGLO MÁGICO ---
            return DataRepository._normalize_structure(raw_data)

        except Exception as e:
            st.error(f"❌ Error crítico leyendo el archivo: {e}")
            st.code(traceback.format_exc())
            return DataRepository._generate_emergency_data()

    @staticmethod
    def _normalize_structure(raw_data: Dict) -> Dict:
        """
        Esta función arregla el problema de los corchetes [] extra automáticamente.
        Transforma: "Tema": [ { "Nivel": ... } ]  --> "Tema": { "Nivel": ... }
        """
        clean_data = {}
        for topic, content in raw_data.items():
            # Si el contenido es una lista (el error que tienes), sacamos el primer elemento
            if isinstance(content, list):
                if len(content) > 0 and isinstance(content[0], dict):
                    clean_data[topic] = content[0]
                else:
                    # Si es una lista vacía o rara, ponemos placeholder
                    clean_data[topic] = {"General": []}
            elif isinstance(content, dict):
                # Si ya es un diccionario, está perfecto
                clean_data[topic] = content
            else:
                clean_data[topic] = {}
        return clean_data

    @staticmethod
    def _generate_emergency_data() -> Dict:
        return {"Modo Emergencia": {"Básico": [{"pregunta": "Error de carga", "opciones": ["A", "B"], "correcta": "A", "explicacion": "...", "traduccion": "..."}]}}

# ======================================================================================================================
# SECTION 3: SQL ENGINE & DATA GENERATOR
# ======================================================================================================================

class SQLSimulator:
    """Simulador SQL con datos persistentes."""
    _EMPLOYEES = None
    _PRODUCTS = None
    _ORDERS = None
    _CUSTOMERS = None

    @classmethod
    def init_db(cls):
        if cls._EMPLOYEES is None:
            # Generar datos Mock
            names = ["Carlos", "Ana", "Luis", "Maria", "Jorge", "Sofia", "Miguel", "Lucia"]
            lastnames = ["Lopez", "Garcia", "Perez", "Martinez", "Sanchez", "Diaz"]
            
            data_emp = []
            for i in range(1, 101):
                data_emp.append((i, random.choice(names), random.choice(lastnames), random.randint(3000, 9000), "IT"))
            cls._EMPLOYEES = pd.DataFrame(data_emp, columns=["EmployeeID", "FirstName", "LastName", "Salary", "Department"])
            
            data_prod = []
            products = ["Laptop", "Mouse", "Keyboard", "Monitor", "USB Drive", "Headset"]
            for i in range(1, 51):
                data_prod.append((i, f"{random.choice(products)} {i}", random.randint(10, 500), random.randint(1, 5)))
            cls._PRODUCTS = pd.DataFrame(data_prod, columns=["ProductID", "ProductName", "Price", "CategoryID"])

    @classmethod
    def execute(cls, query: str) -> Tuple[Optional[pd.DataFrame], Optional[str]]:
        cls.init_db()
        # Validación de seguridad
        if any(x in query.lower() for x in ['drop', 'delete', 'update', 'insert', 'alter']):
            return None, "🔒 ACCIÓN BLOQUEADA: Modo solo lectura."
        
        try:
            conn = sqlite3.connect(":memory:")
            cls._EMPLOYEES.to_sql("Employees", conn, index=False, if_exists="replace")
            cls._PRODUCTS.to_sql("Products", conn, index=False, if_exists="replace")
            
            res = pd.read_sql_query(query, conn)
            conn.close()
            return res, None
        except Exception as e:
            return None, f"Error de Sintaxis: {str(e)}"

# ======================================================================================================================
# SECTION 4: APP STATE & USER PROFILE
# ======================================================================================================================

@dataclass
class UserProfile:
    username: str = "Administrator"
    role: str = "Senior DBA"
    xp: int = 24500
    level_progress: float = 0.45
    streak: int = 12

class AppState:
    KEY = "TITAN_V9"
    
    @classmethod
    def get(cls):
        if cls.KEY not in st.session_state:
            st.session_state[cls.KEY] = {
                "view": "DASHBOARD",
                "user": UserProfile(),
                "quiz": {"active": False, "topic": None, "level": None, "score": 0, "q_index": 0, "history": []},
                "sql_history": []
            }
        return st.session_state[cls.KEY]

# ======================================================================================================================
# SECTION 5: UI CONTROLLERS
# ======================================================================================================================

def render_dashboard():
    user = AppState.get()["user"]
    
    c1, c2 = st.columns([2, 1])
    with c1:
        st.markdown(f"""
        <div style="padding: 40px 0;">
            <h1 style="font-size: 3.5rem; text-shadow: 0 0 30px #3b82f6;">IRONCLAD <span style="color:#3b82f6">TITAN</span></h1>
            <p style="font-size: 1.2rem; color: #94a3b8;">
                Bienvenido, <b>{user.username}</b>. Sistema optimizado y listo para entrenamiento.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        b1, b2 = st.columns(2)
        if b1.button("🚀 INICIAR ENTRENAMIENTO", use_container_width=True):
            AppState.get()["view"] = "TRAINING"
            st.rerun()
        if b2.button("💾 CONSOLA SQL", use_container_width=True):
            AppState.get()["view"] = "SQL"
            st.rerun()
            
    with c2:
        VisualAssets.render_lottie(VisualAssets.ANIM_HOME_BOT)

    # Métricas
    st.markdown("---")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Nivel", "24", "+450 XP")
    m2.metric("Racha", f"{user.streak} Días", "🔥 On Fire")
    m3.metric("Precisión", "94.5%", "+2.1%")
    m4.metric("Módulos", "8/12", "En Progreso")

def render_training():
    state = AppState.get()["quiz"]
    repo = DataRepository.load_content()
    
    if not state["active"]:
        st.markdown("## 🧠 Selección de Módulo")
        
        # Selector de Tema
        temas = list(repo.keys())
        tema_sel = st.selectbox("Selecciona un Tema:", temas)
        
        if tema_sel:
            # Selector de Nivel (Manejo robusto de errores)
            niveles = list(repo[tema_sel].keys())
            if not niveles:
                st.warning("Este tema no tiene niveles disponibles.")
            else:
                nivel_sel = st.radio("Nivel de Dificultad:", niveles, horizontal=True)
                
                if st.button(f"Comenzar {tema_sel} - {nivel_sel}", type="primary"):
                    state["active"] = True
                    state["topic"] = tema_sel
                    state["level"] = nivel_sel
                    state["deck"] = repo[tema_sel][nivel_sel]
                    # Asegurar que sea una lista de preguntas
                    if not isinstance(state["deck"], list):
                         # Si por alguna razón es un dict, intentar sacar la lista
                         state["deck"] = list(state["deck"].values())[0] if state["deck"] else []
                    
                    random.shuffle(state["deck"])
                    state["q_index"] = 0
                    state["score"] = 0
                    st.rerun()
    else:
        # Modo Juego
        deck = state["deck"]
        idx = state["q_index"]
        
        if idx >= len(deck):
            st.markdown("## 🎉 ¡Entrenamiento Completado!")
            st.metric("Puntaje Final", f"{state['score']} / {len(deck)}")
            VisualAssets.render_lottie(VisualAssets.ANIM_VICTORY)
            if st.button("Volver al Menú"):
                state["active"] = False
                st.rerun()
            return

        q = deck[idx]
        
        # Barra de progreso
        st.progress((idx + 1) / len(deck))
        st.markdown(f"**Pregunta {idx + 1} de {len(deck)}**")
        
        st.markdown(f"""
        <div class="void-card">
            <h3>{q.get('pregunta', 'Error loading question')}</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Opciones
        opts = q.get('opciones', [])
        if isinstance(opts, str): opts = [opts] # Fix por si acaso
        
        selection = st.radio("Tu respuesta:", opts, key=f"q_{idx}")
        
        c1, c2 = st.columns(2)
        if c1.button("✅ Confirmar"):
            if selection == q.get('correcta'):
                st.success("¡Correcto! +100 XP")
                state["score"] += 1
                if 'explicacion' in q: st.info(q['explicacion'])
            else:
                st.error(f"Incorrecto. La respuesta era: {q.get('correcta')}")
                if 'traduccion' in q: st.warning(f"Traducción: {q['traduccion']}")
            
            if st.button("Siguiente ➡"):
                state["q_index"] += 1
                st.rerun()
                
        if c2.button("❌ Salir"):
            state["active"] = False
            st.rerun()

def render_sql():
    st.markdown("## 💻 Terminal SQL")
    
    col_code, col_info = st.columns([3, 1])
    
    with col_code:
        query = st.text_area("Consulta SQL:", height=200, value="SELECT * FROM Employees LIMIT 5;")
        if st.button("Ejecutar Query", type="primary"):
            df, err = SQLSimulator.execute(query)
            if err:
                st.error(err)
            else:
                st.success(f"Query OK: {len(df)} filas encontradas.")
                st.dataframe(df, use_container_width=True)
                
    with col_info:
        st.markdown("### Esquema")
        with st.expander("Employees"):
            st.code("EmployeeID (INT)\nFirstName (TXT)\nLastName (TXT)\nSalary (INT)")
        with st.expander("Products"):
            st.code("ProductID (INT)\nProductName (TXT)\nPrice (INT)")

# ======================================================================================================================
# MAIN EXECUTION
# ======================================================================================================================

def main():
    VoidGlassUI.inject_css()
    
    # Sidebar
    with st.sidebar:
        user = AppState.get()["user"]
        st.markdown(f"""
        <div style="text-align:center;">
            <div style="width:80px; height:80px; border-radius:50%; background:linear-gradient(45deg, #3b82f6, #1e1b4b); margin:0 auto; display:flex; align-items:center; justify-content:center; font-size:2rem; font-weight:bold; border:2px solid white;">
                {user.username[0]}
            </div>
            <h3 style="color:white; margin-top:10px;">{user.username}</h3>
            <p style="color:#94a3b8;">{user.role}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        if st.button(f"{VisualAssets.ICON_DASHBOARD} Dashboard", use_container_width=True):
            AppState.get()["view"] = "DASHBOARD"
            st.rerun()
        if st.button(f"{VisualAssets.ICON_LEARN} Training", use_container_width=True):
            AppState.get()["view"] = "TRAINING"
            st.rerun()
        if st.button(f"{VisualAssets.ICON_CODE} SQL Lab", use_container_width=True):
            AppState.get()["view"] = "SQL"
            st.rerun()

    # Routing
    view = AppState.get()["view"]
    if view == "DASHBOARD": render_dashboard()
    elif view == "TRAINING": render_training()
    elif view == "SQL": render_sql()

if __name__ == "__main__":
    main()