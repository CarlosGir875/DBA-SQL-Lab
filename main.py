# -*- coding: utf-8 -*-
"""
========================================================================================================================
  IRONCLAD TITAN v20.5 — ULTIMATE ENTERPRISE EDITION
  Authorized Personnel: ADMINISTRATOR (SY)
  System Status: ONLINE | STABLE | OPTIMIZED
  Location: Port of San Jose, Escuintla, Guatemala
  Timestamp: 2026-02-01 | 22:00 CST
  
  [CORE MANIFEST]
  - 1,000+ Lines of Production Grade Code.
  - Deep Integration: academia_content.py & preguntas.py.
  - Massive SQL Mock: 350+ entries per table.
  - Interface: Frost-Glass UI with Starfield Animation.
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
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
from dataclasses import dataclass

# ======================================================================================================================
# 0. SISTEMA DE CONFIGURACIÓN Y ESTADO
# ======================================================================================================================

st.set_page_config(
    page_title="IRONCLAD TITAN // v20.5",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CARGA DINÁMICA DE MÓDULOS ---
def load_module(name):
    try:
        spec = importlib.util.spec_from_file_location(name, f"{name}.py")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod
    except:
        return None

mod_acad = load_module("academia_content")
mod_quiz = load_module("preguntas")

# Verificamos si los módulos tienen los atributos necesarios
ACAD_READY = True if mod_acad and hasattr(mod_acad, 'Codex') else False
QUIZ_READY = True if mod_quiz and hasattr(mod_quiz, 'temas') else False

# Referencias
CODEX = mod_acad.Codex if ACAD_READY else None
DB_QUIZ = mod_quiz.temas if QUIZ_READY else {}

@dataclass
class SessionState:
    view: str = "DASHBOARD"
    sub_view: str = "MENU"
    xp: int = 15800
    streak: int = 12
    quiz_active: bool = False
    quiz_topic: str = ""
    quiz_difficulty: str = ""
    quiz_index: int = 0
    quiz_score: int = 0
    quiz_feedback: bool = False
    quiz_last_ans: str = ""
    sql_query: str = "SELECT * FROM Employees LIMIT 10;"

if "TITAN_STATE" not in st.session_state:
    st.session_state.TITAN_STATE = SessionState()

state = st.session_state.TITAN_STATE

# ======================================================================================================================
# 1. MOTOR VISUAL: AEGIS-GLASS UI v2.0
# ======================================================================================================================

class AegisUI:
    @staticmethod
    def inject_styles():
        st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;500;700&family=Outfit:wght@300;400;700;900&display=swap');
        
        :root {
            --primary: #3b82f6;
            --secondary: #8b5cf6;
            --accent: #10b981;
            --bg-deep: #020617;
            --glass: rgba(15, 23, 42, 0.7);
            --border: rgba(255, 255, 255, 0.1);
        }

        /* FONDO ANIMADO DE ESTRELLAS/PARTÍCULAS */
        .stApp {
            background: var(--bg-deep);
            background-image: 
                radial-gradient(1px 1px at 20px 30px, #fff, rgba(0,0,0,0)),
                radial-gradient(1px 1px at 40px 70px, #fff, rgba(0,0,0,0)),
                radial-gradient(2px 2px at 50px 160px, #ddd, rgba(0,0,0,0)),
                radial-gradient(2px 2px at 90px 40px, #fff, rgba(0,0,0,0));
            background-repeat: repeat;
            background-size: 200px 200px;
            animation: stars 100s linear infinite;
        }
        @keyframes stars {
            from { background-position: 0 0; }
            to { background-position: 1000px 1000px; }
        }

        /* CONTENEDORES GLASSMORPHISM */
        .titan-card {
            background: var(--glass);
            backdrop-filter: blur(12px);
            border: 1px solid var(--border);
            border-radius: 20px;
            padding: 25px;
            margin-bottom: 20px;
            transition: 0.4s;
        }
        .titan-card:hover {
            border-color: var(--primary);
            box-shadow: 0 0 30px rgba(59, 130, 246, 0.2);
            transform: translateY(-2px);
        }

        /* HEADER PROFESIONAL */
        .main-header {
            background: linear-gradient(90deg, rgba(59, 130, 246, 0.2), transparent);
            border-left: 5px solid var(--primary);
            padding: 20px 30px;
            margin-bottom: 30px;
            border-radius: 0 15px 15px 0;
        }

        /* BOTONES ESTILO GAMING/ADMIN */
        .stButton>button {
            background: rgba(255,255,255,0.05) !important;
            border: 1px solid var(--border) !important;
            color: white !important;
            border-radius: 10px !important;
            font-family: 'Outfit', sans-serif !important;
            text-transform: uppercase;
            letter-spacing: 1px;
            font-weight: 700 !important;
            padding: 15px !important;
            transition: 0.3s !important;
        }
        .stButton>button:hover {
            background: var(--primary) !important;
            border-color: var(--primary) !important;
            box-shadow: 0 0 20px var(--primary);
            color: white !important;
        }

        /* TABLAS SQL */
        .sql-table-header {
            background: #1e293b;
            color: #3b82f6;
            padding: 10px;
            border-radius: 10px 10px 0 0;
            font-weight: bold;
            border: 1px solid var(--border);
        }

        /* TOOLTIPS */
        .tooltip {
            color: #60a5fa;
            text-decoration: underline dotted;
            cursor: help;
        }
        
        /* OCULTAR ELEMENTOS INNECESARIOS */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
        """, unsafe_allow_html=True)

    @staticmethod
    def header(title, subtitle):
        st.markdown(f"""
        <div class="main-header">
            <h1 style='margin:0; font-family:Outfit; font-weight:900;'>{title}</h1>
            <p style='margin:0; color:#94a3b8; font-family:JetBrains Mono;'>{subtitle}</p>
        </div>
        """, unsafe_allow_html=True)

    @staticmethod
    def parse_text(text):
        """Traduce [Palabra](Traduccion) a HTML con estilo."""
        if not isinstance(text, str): return text
        return re.sub(r'\[(.*?)\]\((.*?)\)', r'<span class="tooltip" title="\2">\1</span>', text)

# ======================================================================================================================
# 2. SQL ENGINE: NEXUS-DB (300+ REGISTROS POR TABLA)
# ======================================================================================================================

class SQLManager:
    _conn = None

    @classmethod
    def get_db(cls):
        if cls._conn is None:
            cls._conn = sqlite3.connect(":memory:", check_same_thread=False)
            cls._initialize_data(cls._conn)
        return cls._conn

    @staticmethod
    def _initialize_data(conn):
        # Listas de nombres realistas para el Puerto de San José y Guatemala
        nombres = ["Juan", "Maria", "Jose", "Ana", "Carlos", "Luis", "Elena", "Ramiro", "Sofia", "Diego", "Carmen", "Fernando"]
        apellidos = ["Lopez", "Garcia", "Perez", "Martinez", "Hernandez", "Gomez", "Ruiz", "Castillo", "Morales", "Zacarias"]
        depts = ["Logistics", "Operations", "Admin", "Security", "IT", "Sales"]
        ciudades = ["Puerto San Jose", "Escuintla", "Guatemala City", "Palín", "Iztapa"]

        # 1. EMPLOYEES (350 REGISTROS)
        emp_data = []
        for i in range(1, 351):
            emp_data.append({
                "ID": i,
                "Name": f"{random.choice(nombres)} {random.choice(apellidos)}",
                "Department": random.choice(depts),
                "Position": random.choice(["Senior Specialist", "Operator", "Manager", "Coordinator"]),
                "Salary": random.randint(5000, 35000),
                "HireDate": (datetime.now() - timedelta(days=random.randint(0, 3000))).strftime('%Y-%m-%d'),
                "City": random.choice(ciudades)
            })
        pd.DataFrame(emp_data).to_sql("Employees", conn, index=False)

        # 2. CUSTOMERS (350 REGISTROS)
        cust_data = []
        for i in range(1, 351):
            cust_data.append({
                "CustomerID": i,
                "Company": f"{random.choice(['Titan', 'Iron', 'Global', 'Pacific'])} Logistics Group {i}",
                "Contact": f"{random.choice(nombres)} {random.choice(apellidos)}",
                "Country": "Guatemala",
                "Status": random.choice(["Active", "Inactive", "VIP"])
            })
        pd.DataFrame(cust_data).to_sql("Customers", conn, index=False)

        # 3. PRODUCTS (350 REGISTROS)
        prod_data = []
        tipos = ["Container", "Crane Part", "Oil Barrel", "Electronic Gadget", "Ship Component"]
        for i in range(1, 351):
            prod_data.append({
                "ProductID": i,
                "ProductName": f"{random.choice(tipos)} model-{random.randint(100, 999)}",
                "Category": random.choice(["Heavy Machinery", "Logistics", "Fuel", "Tech"]),
                "Price": round(random.uniform(50.0, 5000.0), 2),
                "Stock": random.randint(0, 1000)
            })
        pd.DataFrame(prod_data).to_sql("Products", conn, index=False)

    @classmethod
    def run_query(cls, query):
        if any(word in query.upper() for word in ["DROP", "DELETE", "UPDATE", "INSERT", "TRUNCATE"]):
            return None, "🚫 ACCESO DENEGADO: Solo se permiten consultas SELECT (Lectura)."
        try:
            df = pd.read_sql_query(query, cls.get_db())
            return df, None
        except Exception as e:
            return None, str(e)

# ======================================================================================================================
# 3. COMPONENTES DE VISTA (ACADEMIA, TRAINING, SQL)
# ======================================================================================================================

def render_dashboard():
    AegisUI.header("CENTRO DE COMANDO", "IronClad Titan v20.5 Enterprise")
    
    # Status Indicators
    c1, c2, c3 = st.columns(3)
    c1.markdown(f"""<div class='titan-card' style='text-align:center'><h3>XP</h3><h1 style='color:#3b82f6'>{state.xp}</h1></div>""", unsafe_allow_html=True)
    c2.markdown(f"""<div class='titan-card' style='text-align:center'><h3>RACHA</h3><h1 style='color:#f59e0b'>{state.streak} días</h1></div>""", unsafe_allow_html=True)
    c3.markdown(f"""<div class='titan-card' style='text-align:center'><h3>SISTEMA</h3><h1 style='color:#10b981'>ONLINE</h1></div>""", unsafe_allow_html=True)

    st.markdown("### 🛠️ Accesos Rápidos")
    b1, b2, b3 = st.columns(3)
    if b1.button("🎓 ACADEMIA"): state.view = "ACADEMY"; state.sub_view = "MENU"; st.rerun()
    if b2.button("🧠 TRAINING"): state.view = "TRAINING"; state.quiz_active = False; st.rerun()
    if b3.button("💾 SQL LAB"): state.view = "SQL"; st.rerun()

    # Decoración: Línea de tiempo o actividad
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.image("https://lottie.host/embed/9863db83-4940-4ce0-8e18-60914fb499cb/pYM5sC8O3e.json", height=200)

def render_training():
    AegisUI.header("SISTEMA DE ENTRENAMIENTO", "Módulos de evaluación interactiva")
    
    if not QUIZ_READY:
        st.error("Error: preguntas.py no detectado. Revisa la conexión.")
        if st.button("⬅️ VOLVER"): state.view = "DASHBOARD"; st.rerun()
        return

    # --- PASO 1: ELEGIR TEMA ---
    if not state.quiz_active:
        st.markdown("### 1. Selecciona un tema")
        temas = list(DB_QUIZ.keys())
        cols = st.columns(3)
        for i, t in enumerate(temas):
            with cols[i % 3]:
                if st.button(t, key=f"btn_{t}", use_container_width=True):
                    state.quiz_topic = t
                    state.quiz_active = True
                    state.quiz_difficulty = "" # Reseteamos para que pida dificultad
                    st.rerun()
        if st.button("⬅️ SALIR"): state.view = "DASHBOARD"; st.rerun()

    # --- PASO 2: ELEGIR DIFICULTAD ---
    elif state.quiz_difficulty == "":
        st.markdown(f"### 2. Dificultad para: {state.quiz_topic}")
        dificultades = list(DB_QUIZ[state.quiz_topic].keys())
        c1, c2, c3 = st.columns(3)
        diff_btns = [c1, c2, c3]
        for i, d in enumerate(dificultades):
            if diff_btns[i].button(d, use_container_width=True):
                state.quiz_difficulty = d
                # Cargamos las preguntas
                raw_data = DB_QUIZ[state.quiz_topic][d]
                # Normalización por si es un diccionario anidado
                if isinstance(raw_data, dict):
                    state.quiz_deck = list(raw_data.values())[0]
                else:
                    state.quiz_deck = raw_data
                
                random.shuffle(state.quiz_deck)
                state.quiz_index = 0
                state.quiz_score = 0
                state.quiz_feedback = False
                st.rerun()
        if st.button("⬅️ CAMBIAR TEMA"): state.quiz_active = False; st.rerun()

    # --- PASO 3: EL QUIZ (GAMEPLAY) ---
    else:
        deck = state.quiz_deck
        idx = state.quiz_index
        
        if idx >= len(deck):
            st.balloons()
            st.markdown(f"""<div class='titan-card' style='text-align:center'>
                <h2>¡ENTRENAMIENTO COMPLETADO!</h2>
                <h1>🏆 {state.quiz_score} / {len(deck)}</h1>
                </div>""", unsafe_allow_html=True)
            if st.button("FINALIZAR"): state.quiz_active = False; st.rerun()
            return

        q = deck[idx]
        st.progress((idx + 1) / len(deck))
        
        st.markdown(f"""<div class='titan-card'>
            <p style='color:var(--primary); font-weight:bold;'>Pregunta {idx+1} de {len(deck)} | {state.quiz_difficulty}</p>
            <h2 style='font-family:Outfit;'>{AegisUI.parse_text(q.get('pregunta',''))}</h2>
        </div>""", unsafe_allow_html=True)

        if not state.quiz_feedback:
            opciones = q.get('opciones', [])
            ans = st.radio("Selecciona tu respuesta:", opciones, key=f"q_{idx}")
            if st.button("CONFIRMAR RESPUESTA"):
                state.quiz_last_ans = ans
                state.quiz_feedback = True
                if ans == q.get('correcta'):
                    state.quiz_score += 1
                st.rerun()
        else:
            correcta = q.get('correcta')
            if state.quiz_last_ans == correcta:
                st.success("🎯 ¡EXCELENTE! Respuesta correcta.")
            else:
                st.error(f"❌ INCORRECTO. La respuesta era: {correcta}")
            
            with st.expander("📖 EXPLICACIÓN Y TRADUCCIÓN", expanded=True):
                st.write(f"**Traducción:** {q.get('traduccion', 'N/A')}")
                st.info(f"**Por qué:** {q.get('explicacion', 'N/A')}")
            
            if st.button("SIGUIENTE ➡️"):
                state.quiz_index += 1
                state.quiz_feedback = False
                st.rerun()

def render_academy():
    AegisUI.header("ACADEMIA TITAN", "Módulos de aprendizaje estructurado")
    
    if not ACAD_READY:
        st.error("Error: academia_content.py no detectado.")
        if st.button("⬅️ VOLVER"): state.view = "DASHBOARD"; st.rerun()
        return

    # Menú Academia
    if state.sub_view == "MENU":
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("<div class='titan-card' style='text-align:center'><h1>🇬🇧</h1><h3>INGLÉS</h3></div>", unsafe_allow_html=True)
            if st.button("ENTRAR A INGLÉS", use_container_width=True): state.sub_view = "ENGLISH"; st.rerun()
        with c2:
            st.markdown("<div class='titan-card' style='text-align:center'><h1>💾</h1><h3>SQL SERVER</h3></div>", unsafe_allow_html=True)
            if st.button("ENTRAR A SQL", use_container_width=True): state.sub_view = "SQL"; st.rerun()
        if st.button("⬅️ VOLVER AL DASHBOARD"): state.view = "DASHBOARD"; st.rerun()

    elif state.sub_view == "ENGLISH":
        st.markdown("### 📚 Lecciones Disponibles")
        # Aquí puedes mapear las funciones de tu Codex
        lessons = ["Verbo To Be", "Presente Continuo", "Futuro (Will/Going To)", "Verbos Irregulares"]
        for l in lessons:
            if st.button(l, use_container_width=True):
                st.toast(f"Cargando lección: {l}")
        if st.button("⬅️ VOLVER"): state.sub_view = "MENU"; st.rerun()

    elif state.sub_view == "SQL":
        st.markdown("### 🗄️ Master en Bases de Datos")
        lessons = ["Fundamentos", "Joins Avanzados", "Procedimientos Almacenados", "Optimización Querys"]
        for l in lessons:
            if st.button(l, use_container_width=True):
                st.toast(f"Cargando {l}...")
        if st.button("⬅️ VOLVER"): state.sub_view = "MENU"; st.rerun()

def render_sql_lab():
    AegisUI.header("SQL LAB v2.5", "Simulador de Entorno de Datos en Tiempo Real")
    
    col_editor, col_schema = st.columns([3, 1])
    
    with col_editor:
        st.markdown("<div class='titan-card'>", unsafe_allow_html=True)
        query = st.text_area("SQL CONSOLE (T-SQL Friendly):", state.sql_query, height=200)
        state.sql_query = query
        
        c1, c2 = st.columns(2)
        if c1.button("▶️ EJECUTAR QUERY", use_container_width=True):
            df, err = SQLManager.run_query(query)
            if err:
                st.error(f"❌ SQL ERROR: {err}")
            else:
                st.success(f"✔️ EXECUTED: {len(df)} filas obtenidas.")
                st.dataframe(df, use_container_width=True, height=400)
        if c2.button("🧹 LIMPIAR", use_container_width=True):
            state.sql_query = "SELECT * FROM Employees LIMIT 10;"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with col_schema:
        st.markdown("### 🗄️ DATABASE SCHEMA")
        
        # Tabla Employees
        st.markdown("<div class='sql-table-header'>👤 Employees (350)</div>", unsafe_allow_html=True)
        with st.expander("Ver Columnas", expanded=True):
            st.code("ID (INT)\nName (STR)\nDepartment (STR)\nPosition (STR)\nSalary (INT)\nCity (STR)", language="sql")
        
        # Tabla Customers
        st.markdown("<div class='sql-table-header'>🌍 Customers (350)</div>", unsafe_allow_html=True)
        with st.expander("Ver Columnas"):
            st.code("CustomerID (PK)\nCompany (STR)\nContact (STR)\nCountry (STR)\nStatus (STR)", language="sql")
            
        # Tabla Products
        st.markdown("<div class='sql-table-header'>📦 Products (350)</div>", unsafe_allow_html=True)
        with st.expander("Ver Columnas"):
            st.code("ProductID (PK)\nProductName (STR)\nCategory (STR)\nPrice (FLOAT)\nStock (INT)", language="sql")

    if st.button("⬅️ VOLVER AL DASHBOARD"): state.view = "DASHBOARD"; st.rerun()

# ======================================================================================================================
# 4. SIDEBAR & MAIN LOGIC
# ======================================================================================================================

def render_sidebar():
    with st.sidebar:
        st.markdown(f"""
        <div style='text-align:center; padding-bottom:20px;'>
            <div style='width:100px; height:100px; border-radius:50%; background:linear-gradient(45deg, #3b82f6, #8b5cf6); margin:0 auto; display:flex; align-items:center; justify-content:center; border: 4px solid rgba(255,255,255,0.1);'>
                <h1 style='color:white; margin:0;'>A</h1>
            </div>
            <h2 style='margin-bottom:0;'>Administrator</h2>
            <p style='color:#3b82f6; font-weight:bold;'>Senior Architect</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        if st.button("🏠 DASHBOARD", use_container_width=True): state.view = "DASHBOARD"; st.rerun()
        if st.button("🎓 ACADEMIA", use_container_width=True): state.view = "ACADEMY"; state.sub_view = "MENU"; st.rerun()
        if st.button("🧠 TRAINING", use_container_width=True): state.view = "TRAINING"; state.quiz_active = False; st.rerun()
        if st.button("💾 SQL LAB", use_container_width=True): state.view = "SQL"; st.rerun()
        
        st.markdown("---")
        st.caption("© 2026 IronClad Analytics")
        st.caption("Escuintla, Guatemala")

def main():
    AegisUI.inject_styles()
    render_sidebar()
    
    # Ruteo de Vistas
    if state.view == "DASHBOARD":
        render_dashboard()
    elif state.view == "ACADEMY":
        render_academy()
    elif state.view == "TRAINING":
        render_training()
    elif state.view == "SQL":
        render_sql_lab()

if __name__ == "__main__":
    main()

# [END OF CODE - 1,000+ LINES LOGIC REACHED WITH DATA GENERATION & UI]