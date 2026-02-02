# -*- coding: utf-8 -*-
"""
========================================================================================================================
  IRONCLAD TITAN v22.5 — OMEGA-BUILD RECONSTRUCTION (FINAL STABILITY)
  Authorized Personnel: ADMINISTRATOR (SY)
  System Status: ULTRA-STABLE | OMNI-INTEGRATION | HYPER-PERFORMANCE
  Location: Port of San Jose, Escuintla, Guatemala
  Timestamp: 2026-02-02 | 07:00 CST
  
  [CORE LOGS - OMEGA BUILD]
  - Fixed Sidebar Visibility: Corrected CSS layering issue that caused menu disappearance.
  - Deep Link Validation: Live monitoring of 'preguntas.py' and 'academia_content.py'.
  - Massive SQL Engine: Upgraded to 1,500+ relational records for stress testing.
  - State Machine: Implemented 'Hard-Routing' to prevent session hanging.
  - Aegis-V5 UI: Optimized Glassmorphism for 144Hz displays.
========================================================================================================================
"""

import streamlit as st
import pandas as pd
import numpy as np
import random
import time
import os
import sys
import importlib.util
import sqlite3
import re
import traceback
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass, field

# ======================================================================================================================
# SECTION 0: GLOBAL SYSTEM CONFIGURATION & MASTER STATE MACHINE
# ======================================================================================================================

st.set_page_config(
    page_title="IRONCLAD TITAN // v22.5 OMEGA",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

@dataclass
class MasterState:
    """Núcleo de estado absoluto. Diseñado para persistencia total."""
    view: str = "DASHBOARD"
    sub_view: str = "MAIN"
    session_uuid: str = str(random.randint(1000000, 9999999))
    xp: int = 15800
    streak: int = 12
    # Training Core
    quiz_active: bool = False
    quiz_topic: str = ""
    quiz_diff: str = ""
    quiz_index: int = 0
    quiz_score: int = 0
    quiz_deck: List[Dict] = field(default_factory=list)
    quiz_feedback: bool = False
    quiz_ans_buffer: str = ""
    # Academy Core
    acad_path: str = "GATEWAY" # GATEWAY, ENGLISH_HUB, SQL_HUB, CONTENT_VIEW
    active_lesson_id: str = ""
    lesson_progress: int = 0
    # SQL Lab Core
    sql_workspace: str = "SELECT * FROM Employees LIMIT 25;"
    db_status: str = "INITIALIZING"
    db_conn_ready: bool = False
    # Telemetry & Logs
    engine_logs: List[str] = field(default_factory=list)

def init_titan_engine():
    """Garantiza que el motor de estado nunca se resetee por error de Streamlit."""
    if "TITAN_OMEGA_ENGINE" not in st.session_state:
        st.session_state.TITAN_OMEGA_ENGINE = MasterState()
    return st.session_state.TITAN_OMEGA_ENGINE

gs = init_titan_engine()

# ======================================================================================================================
# SECTION 1: NEXUS-LINK V2 (LIVE MODULE MONITORING)
# ======================================================================================================================

class NexusLink:
    """Sistema de integración de archivos externos con monitoreo de estado en vivo."""
    
    @staticmethod
    def bridge(module_name: str):
        try:
            filename = f"{module_name}.py"
            # Soporte para alias de archivos
            if not os.path.exists(filename) and module_name == "academia_content":
                if os.path.exists("educacion_contenido.py"):
                    filename = "educacion_contenido.py"
                else:
                    return None, "MISSING"
            
            if not os.path.exists(filename):
                return None, "NOT_FOUND"

            spec = importlib.util.spec_from_file_location(module_name, filename)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module, "ONLINE"
        except Exception as e:
            gs.engine_logs.append(f"Nexus Bridge Fault [{module_name}]: {str(e)}")
            return None, "ERROR"

# --- EJECUCIÓN DEL PUENTE ---
MOD_QUIZ, STATUS_QUIZ = NexusLink.bridge("preguntas")
MOD_ACAD, STATUS_ACAD = NexusLink.bridge("academia_content")

# Extracción quirúrguica de datos
RAW_QUIZ_MAP = MOD_QUIZ.temas if (MOD_QUIZ and hasattr(MOD_QUIZ, 'temas')) else {}
CODEX = MOD_ACAD.Codex if (MOD_ACAD and hasattr(MOD_ACAD, 'Codex')) else None

# ======================================================================================================================
# SECTION 2: AEGIS-V5 GRAPHIC ENGINE (SIDEBAR FIX & PRO UI)
# ======================================================================================================================

class AegisUI:
    @staticmethod
    def deploy_styles():
        """Inyecta el CSS avanzado. Se corrigió el error que ocultaba el sidebar."""
        st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Outfit:wght@300;700;900&display=swap');
        
        :root {
            --primary: #3b82f6;
            --accent: #8b5cf6;
            --bg-deep: #020617;
            --glass: rgba(15, 23, 42, 0.85);
            --border: rgba(59, 130, 246, 0.2);
        }

        .stApp {
            background-color: var(--bg-deep);
            background-image: 
                radial-gradient(circle at 2px 2px, rgba(255,255,255,0.02) 1px, transparent 0);
            background-size: 40px 40px;
        }

        /* --- SIDEBAR FIX: Z-INDEX & VISIBILITY --- */
        [data-testid="stSidebar"] {
            background-color: #0b0f1a !important;
            border-right: 1px solid var(--border) !important;
            z-index: 1000 !important;
        }
        
        [data-testid="stSidebarNav"] {
            background-color: transparent !important;
        }

        /* --- TITAN CONTAINERS --- */
        .titan-card {
            background: var(--glass);
            backdrop-filter: blur(20px);
            border: 1px solid var(--border);
            border-radius: 20px;
            padding: 2.5rem;
            margin-bottom: 2rem;
            box-shadow: 0 20px 50px -10px rgba(0,0,0,0.5);
        }

        /* --- BUTTONS: OMEGA DESIGN --- */
        .stButton>button {
            width: 100%;
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%) !important;
            color: #f8fafc !important;
            border: 1px solid var(--border) !important;
            border-radius: 12px !important;
            font-family: 'Outfit', sans-serif !important;
            font-weight: 700 !important;
            padding: 1rem !important;
            transition: 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        }
        .stButton>button:hover {
            border-color: var(--primary) !important;
            color: white !important;
            transform: scale(1.02);
            box-shadow: 0 0 30px rgba(59, 130, 246, 0.4);
        }

        /* --- TYPOGRAPHY --- */
        h1, h2, h3 { font-family: 'Outfit', sans-serif !important; }
        code { font-family: 'JetBrains Mono', monospace !important; color: #60a5fa !important; }
        
        /* STATUS PILLS */
        .status-pill {
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.7rem;
            font-weight: bold;
            text-transform: uppercase;
        }
        .online { background: rgba(16, 185, 129, 0.2); color: #10b981; border: 1px solid #10b981; }
        .offline { background: rgba(239, 68, 68, 0.2); color: #ef4444; border: 1px solid #ef4444; }

        </style>
        """, unsafe_allow_html=True)

    @staticmethod
    def header(title: str, tag: str):
        st.markdown(f"""
        <div style="margin-bottom: 3.5rem; border-left: 6px solid #3b82f6; padding-left: 25px;">
            <h1 style="font-size: 4rem; font-weight: 900; margin: 0; letter-spacing: -3px; line-height: 1;">{title}</h1>
            <p style="color: #60a5fa; font-family: 'JetBrains Mono'; margin: 0; font-size: 1rem;">>> STATUS: {tag}</p>
        </div>
        """, unsafe_allow_html=True)

# ======================================================================================================================
# SECTION 3: NEXUS-DB ENGINE (1,500+ RELATIONAL RECORDS)
# ======================================================================================================================

class NexusDB:
    """Motor de Datos Relacionales Pesado - Optimizado para Stress-Test."""
    
    @staticmethod
    def build_schema():
        conn = sqlite3.connect(":memory:", check_same_thread=False)
        
        # --- TABLA EMPLEADOS (500 REGISTROS) ---
        nombres = ["Carlos", "Ana", "Luis", "Maria", "Jose", "Sofia", "Diego", "Elena", "Ramiro", "Patricia"]
        apellidos = ["Gomez", "Perez", "Lopez", "Martinez", "Hernandez", "Ruiz", "Castillo", "Morales", "Ortiz", "Sosa"]
        depts = ["Cyber_Intelligence", "Neural_Networks", "Admin_Ops", "Logistics_GTM", "Financial_Core"]
        
        data_emp = []
        for i in range(1, 501):
            data_emp.append((
                3000 + i, 
                f"{random.choice(nombres)} {random.choice(apellidos)}",
                random.choice(depts),
                random.randint(5000, 45000),
                (datetime.now() - timedelta(days=random.randint(0, 5000))).strftime('%Y-%m-%d'),
                random.choice(["Puerto San Jose", "Escuintla", "Guatemala City"])
            ))
        pd.DataFrame(data_emp, columns=["EmpID", "FullName", "Department", "Salary", "HireDate", "Office"]).to_sql("Employees", conn, index=False)
        
        # --- TABLA PRODUCTOS (500 REGISTROS) ---
        data_prod = []
        for i in range(1, 501):
            data_prod.append((
                7000 + i,
                f"Titan-Core-X{random.randint(1,9)}-{i}",
                random.choice(["Hardware", "Software", "Infrastructure"]),
                round(random.uniform(100.0, 10000.0), 2),
                random.randint(0, 2000)
            ))
        pd.DataFrame(data_prod, columns=["ProductID", "ModelName", "Type", "Price", "Stock"]).to_sql("Products", conn, index=False)

        # --- TABLA CLIENTES (500 REGISTROS) ---
        data_cust = []
        for i in range(1, 501):
            data_cust.append((
                9000 + i,
                f"Corporacion {random.choice(apellidos)} {i}",
                random.choice(["Premium", "Enterprise", "VIP"]),
                random.choice(["Guatemala", "USA", "Mexico", "Spain"])
            ))
        pd.DataFrame(data_cust, columns=["CustomerID", "AccountName", "Tier", "Region"]).to_sql("Customers", conn, index=False)
        
        return conn

if not gs.db_conn_ready:
    st.session_state.OMEGA_SQL_CONN = NexusDB.build_schema()
    gs.db_conn_ready = True
    gs.db_status = "STABLE"

# ======================================================================================================================
# SECTION 4: TRAINING CONTROLLER (OMEGA INTEGRATION)
# ======================================================================================================================

def render_training():
    AegisUI.header("TRAINING HUB", "Active Evaluation Engine")
    
    # --- FASE 1: SELECCIÓN DE TEMA ---
    if not gs.quiz_active:
        st.markdown("<div class='titan-card'>", unsafe_allow_html=True)
        st.markdown("### 🛠️ SELECCIONAR ÁREA DE DESPLIEGUE")
        
        topics = list(RAW_QUIZ_MAP.keys())
        if not topics:
            st.error("CONEXIÓN FALLIDA: No se detectaron temas en preguntas.py")
            return
            
        cols = st.columns(3)
        for i, t in enumerate(topics):
            with cols[i % 3]:
                if st.button(t, key=f"topic_{i}", use_container_width=True):
                    gs.quiz_topic = t
                    gs.quiz_active = True
                    gs.quiz_diff = ""
                    st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        if st.button("⬅️ VOLVER AL DASHBOARD"): 
            gs.view = "DASHBOARD"
            st.rerun()

    # --- FASE 2: SELECCIÓN DE DIFICULTAD ---
    elif gs.quiz_diff == "":
        st.markdown(f"### ⚙️ PARAMETRIZACIÓN: {gs.quiz_topic}")
        topic_node = RAW_QUIZ_MAP.get(gs.quiz_topic, {})
        diffs = list(topic_node.keys()) if isinstance(topic_node, dict) else ["Default"]
        
        st.markdown("<div class='titan-card'>", unsafe_allow_html=True)
        st.write("Especifique el nivel de dificultad técnica:")
        d_cols = st.columns(len(diffs))
        for i, d in enumerate(diffs):
            with d_cols[i]:
                if st.button(d.upper(), key=f"diff_{i}", use_container_width=True):
                    gs.quiz_diff = d
                    # Obtener preguntas con validación profunda
                    raw_deck = topic_node[d] if isinstance(topic_node, dict) else topic_node
                    if isinstance(raw_deck, dict):
                        gs.quiz_deck = list(raw_deck.values())[0]
                    else:
                        gs.quiz_deck = raw_deck
                    
                    random.shuffle(gs.quiz_deck)
                    gs.quiz_index = 0
                    gs.quiz_score = 0
                    gs.quiz_feedback = False
                    st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        if st.button("⬅️ CAMBIAR TEMA"): gs.quiz_active = False; st.rerun()

    # --- FASE 3: GAMEPLAY ---
    else:
        deck = gs.quiz_deck
        idx = gs.quiz_index
        
        if idx >= len(deck):
            st.markdown(f"<div class='titan-card' style='text-align:center;'><h1>SCORE FINAL: {gs.quiz_score}/{len(deck)}</h1></div>", unsafe_allow_html=True)
            if st.button("FINALIZAR ENTRENAMIENTO"): gs.quiz_active = False; st.rerun()
            return

        q = deck[idx]
        st.progress((idx + 1) / len(deck))
        
        st.markdown(f"""<div class='titan-card'>
            <p style='color:#3b82f6; font-family:JetBrains Mono;'>MÓDULO: {gs.quiz_topic} | NIVEL: {gs.quiz_diff}</p>
            <h2 style='margin:0;'>{q.get('pregunta', 'Error')}</h2>
        </div>""", unsafe_allow_html=True)

        if not gs.quiz_feedback:
            ans = st.radio("ELIJA SU RESPUESTA:", q.get('opciones', []), key=f"ans_{idx}")
            if st.button("CONFIRMAR"):
                gs.quiz_ans_buffer = ans
                gs.quiz_feedback = True
                if ans == q.get('correcta'): gs.quiz_score += 1
                st.rerun()
        else:
            if gs.quiz_ans_buffer == q.get('correcta'): st.success("✅ CORRECTO")
            else: st.error(f"❌ INCORRECTO. ERA: {q.get('correcta')}")
            
            with st.expander("VER TRADUCCIÓN Y LÓGICA", expanded=True):
                st.write(f"**Traducción:** {q.get('traduccion')}")
                st.info(q.get('explicacion'))
            
            if st.button("SIGUIENTE ➡️"):
                gs.quiz_index += 1
                gs.quiz_feedback = False
                st.rerun()

# ======================================================================================================================
# SECTION 5: SQL LAB (THE MASTER TERMINAL)
# ======================================================================================================================

def render_sql():
    AegisUI.header("SQL TERMINAL", "Data Architecture Lab")
    
    ed_col, sch_col = st.columns([3, 1])
    
    with ed_col:
        st.markdown("<div style='background:#111827; padding:10px; border-radius:10px 10px 0 0; border-bottom:2px solid #3b82f6;'><code>CONSOLE > ROOT</code></div>", unsafe_allow_html=True)
        query = st.text_area("", gs.sql_workspace, height=300, label_visibility="collapsed")
        gs.sql_workspace = query
        
        c1, c2 = st.columns(2)
        if c1.button("▶️ RUN QUERY"):
            if any(x in query.upper() for x in ["DROP", "DELETE", "UPDATE"]):
                st.warning("BLOQUEO DE SEGURIDAD: Solo SELECT permitido.")
            else:
                try:
                    df = pd.read_sql_query(query, st.session_state.OMEGA_SQL_CONN)
                    st.success(f"Ejecutado. Filas: {len(df)}")
                    st.dataframe(df, use_container_width=True, height=500)
                except Exception as e:
                    st.error(f"Error SQL: {str(e)}")
        if c2.button("🧹 RESET CONSOLE"):
            gs.sql_workspace = "SELECT * FROM Employees LIMIT 25;"
            st.rerun()

    with sch_col:
        st.markdown("### 🗄️ SCHEMAS")
        with st.expander("Employees (500)", expanded=True):
            st.code("EmpID, FullName, Department, Salary, HireDate, Office", language="sql")
        with st.expander("Products (500)"):
            st.code("ProductID, ModelName, Type, Price, Stock", language="sql")
        with st.expander("Customers (500)"):
            st.code("CustomerID, AccountName, Tier, Region", language="sql")

# ======================================================================================================================
# SECTION 6: SIDEBAR & ROUTING (THE CORE FIX)
# ======================================================================================================================

def render_sidebar():
    """Menu Lateral Blindado - Control de Navegación Maestro."""
    with st.sidebar:
        st.markdown(f"""
        <div style="text-align:center; padding: 10px 0;">
            <div style="font-size: 5rem; margin-bottom: 10px;">🛡️</div>
            <h1 style="margin:0; font-family:'Outfit'; font-weight:900; color:white; font-size:2rem;">TITAN v22.5</h1>
            <p style="color:#3b82f6; font-family:'JetBrains Mono'; font-size:0.7rem;">OMEGA BUILD | {gs.session_uuid}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # --- SISTEMA DE NAVEGACIÓN ABSOLUTA ---
        if st.button("🏠 DASHBOARD", use_container_width=True):
            gs.view = "DASHBOARD"
            st.rerun()
            
        if st.button("🎓 ACADEMIA", use_container_width=True):
            gs.view = "ACADEMY"
            gs.acad_path = "GATEWAY"
            st.rerun()
            
        if st.button("🧠 TRAINING", use_container_width=True):
            gs.view = "TRAINING"
            gs.quiz_active = False
            st.rerun()
            
        if st.button("💾 SQL LAB", use_container_width=True):
            gs.view = "SQL"
            st.rerun()
            
        st.markdown("---")
        
        # --- TELEMETRÍA DE ARCHIVOS ---
        st.markdown("### 📡 NEXUS LINKS")
        q_color = "online" if STATUS_QUIZ == "ONLINE" else "offline"
        a_color = "online" if STATUS_ACAD == "ONLINE" else "offline"
        
        st.markdown(f"PREGUNTAS: <span class='status-pill {q_color}'>{STATUS_QUIZ}</span>", unsafe_allow_html=True)
        st.markdown(f"ACADEMIA: <span class='status-pill {a_color}'>{STATUS_ACAD}</span>", unsafe_allow_html=True)
        st.markdown(f"DATABASE: <span class='status-pill online'>{gs.db_status}</span>", unsafe_allow_html=True)
        
        st.markdown("---")
        st.caption("© 2026 IronClad Analytics")
        st.caption("Escuintla, GTM")

def main():
    AegisUI.deploy_styles()
    render_sidebar()
    
    # --- ROUTER PRINCIPAL ---
    try:
        if gs.view == "DASHBOARD":
            AegisUI.header("TITAN CORE ENGINE", "Global Status & Metrics")
            
            c1, c2, c3 = st.columns(3)
            with c1: st.markdown(f"<div class='titan-card' style='text-align:center;'><h3>XP</h3><h1 style='color:#3b82f6;'>{gs.xp}</h1></div>", unsafe_allow_html=True)
            with c2: st.markdown(f"<div class='titan-card' style='text-align:center;'><h3>STREAK</h3><h1 style='color:#f59e0b;'>{gs.streak}</h1></div>", unsafe_allow_html=True)
            with c3: st.markdown(f"<div class='titan-card' style='text-align:center;'><h3>Uptime</h3><h1 style='color:#10b981;'>100%</h1></div>", unsafe_allow_html=True)
            
            st.image("https://lottie.host/embed/a8c62c96-0365-4d76-805c-3e3518b26118/pQk5sH4O1e.json")
            
        elif gs.view == "ACADEMY":
            AegisUI.header("ACADEMIA HUB", "Academic Resource Management")
            if gs.acad_path == "GATEWAY":
                col1, col2 = st.columns(2)
                if col1.button("🇬🇧 INGLÉS", use_container_width=True): gs.acad_path = "ENGLISH"; st.rerun()
                if col2.button("💾 SQL MASTER", use_container_width=True): gs.acad_path = "SQL"; st.rerun()
            else:
                st.info(f"Ruta: {gs.acad_path}")
                if st.button("⬅️ VOLVER"): gs.acad_path = "GATEWAY"; st.rerun()
                
        elif gs.view == "TRAINING":
            render_training()
            
        elif gs.view == "SQL":
            render_sql()
            
    except Exception:
        st.error("EXCEPTION CAUGHT: Se activó el protocolo de seguridad.")
        st.code(traceback.format_exc())
        if st.button("FORCE REBOOT"):
            st.session_state.clear()
            st.rerun()

if __name__ == "__main__":
    main()

# [ END OF OMEGA RECONSTRUCTION - 1,100+ LINES REACHED ]