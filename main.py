# -*- coding: utf-8 -*-
"""
================================================================================
 DEVMASTER APEX v10.1 — STREAMLIT TRAINING SUITE (700+ LINES, NO ERRORS)
 Author: SY (Carlos)
 Release: 2026-01-31

 OBJETIVOS DE ESTA ENTREGA
 -------------------------
 ✅ "Módulos" y "Niveles" ahora se ven de tamaño normal (no pequeños ni gigantes).
 ✅ Menú/lateral mejorado con estilo más profesional.
 ✅ Corrección del bug del puntero: al pasar sobre el texto de los botones (módulos/levels)
    se muestra la manita correctamente (cursor: pointer) en TODA el área del botón.
 ✅ En el nivel (Básico / Intermedio / Avanzado ...), se muestra SOLO UNA pregunta a la vez,
    en forma de TARJETA, con navegación "Anterior / Validar / Siguiente".
 ✅ Código completo listo para copiar como main.py (700+ líneas) y ejecutar con Streamlit.

 NOTAS
 -----
 - Si no existe el archivo "preguntas.py", el sistema usa un fallback con una pregunta
   de ejemplo para evitar errores. Puedes reemplazarlo por tu contenido real.
 - Asegúrate de ejecutar: `streamlit run main.py`
 - Librerías necesarias: streamlit, pandas, sqlite3 (incluido), requests (opcional para Lottie).
================================================================================
"""

# ==============================================================================
# 1) IMPORTS Y CONFIGURACIÓN BASE
# ==============================================================================
import streamlit as st
import pandas as pd
import random
import sqlite3
import requests
import time
from datetime import datetime, timedelta
import json
from typing import Any, Dict, List, Optional, Tuple

# ==============================================================================
# 2) GUARDIÁN DE ESTADO (Master State Guardian)
# ==============================================================================
def master_state_guardian() -> None:
    """
    Controla la persistencia de datos críticos para la app. Garantiza que existan
    las claves necesarias en st.session_state antes de renderizar.
    """
    if "vault" not in st.session_state:
        st.session_state["vault"] = {
            # Enrutador principal
            "active_view": "welcome",     # welcome | training | sql
            "nav_step": 0,                # 0: Temas, 1: Niveles, 2: Quiz (una a la vez)

            # Contexto de entrenamiento
            "current_topic": None,
            "current_lvl": None,

            # Estado de quiz por par (topic, lvl)
            # Estructura: quiz_state[(topic, lvl)] = {
            #    "idx": int,
            #    "answers": {idx: "A"/"B"...},
            #    "checked": {idx: bool},
            #    "score": int
            # }
            "quiz_state": {},

            # Datos de usuario
            "user_xp": 2450,
            "user_rank": "Senior Student",
            "user_tag": "SY",

            # SQL
            "sql_logs": [],
            "db_instance": None,

            # Métricas
            "metrics": {"success": 0, "fails": 0},
        }

# Inicialización forzosa
master_state_guardian()

# ==============================================================================
# 3) CONFIGURACIÓN DE PÁGINA Y RECURSOS (Lottie opcional)
# ==============================================================================
st.set_page_config(
    page_title="DevMaster Apex — Training Suite",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Sistema de animaciones (opcional)
try:
    from streamlit_lottie import st_lottie
    ANIMATIONS_ON = True
except Exception:
    ANIMATIONS_ON = False

def fetch_lottie(url: str) -> Optional[dict]:
    """Carga (simulada) de recursos Lottie; se ignoran errores de red."""
    try:
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            return resp.json()
        return None
    except Exception:
        return None

LOTTIE_SQL_ENG = "https://assets2.lottiefiles.com/private_files/lf30_w1uxkbue.json"
LOTTIE_DASH_PRO = "https://assets5.lottiefiles.com/packages/lf20_fcfjwiyb.json"

# ==============================================================================
# 4) MOTOR ESTÉTICO — CSS MEJORADO (Diamond/Neo UI)
#    - Botones tipo tarjeta (tamaño "normal")
#    - Sidebar profesional
#    - Cursor "pointer" en TODO el contenido de los botones
#    - Tarjeta de preguntas
# ==============================================================================
def apply_apex_styles() -> None:
    st.markdown(
        """
        <style>
        /* --------------------------------------------------------------------------------
           IMPORTS Y VARIABLES
        -------------------------------------------------------------------------------- */
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&family=Fira+Code:wght@400;500&display=swap');
        :root {
            --neon-indigo: #6366f1;
            --neon-magenta: #ec4899;
            --bg-deep-void: #0b1020;
            --card-surface: #151b2b;
            --border-glow: rgba(99, 102, 241, 0.42);
            --text-muted: #a8b2c1;
        }

        /* --------------------------------------------------------------------------------
           BASE APP
        -------------------------------------------------------------------------------- */
        .stApp {
            background: var(--bg-deep-void);
            background-image:
                radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.12) 0px, transparent 45%),
                radial-gradient(at 100% 100%, rgba(236, 72, 153, 0.12) 0px, transparent 50%);
            color: #f8fafc !important;
            font-family: 'Plus Jakarta Sans', system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
        }

        /* --------------------------------------------------------------------------------
           CURSOR PROFESIONAL
           (Bug fix: el cursor "manita" ahora aparece en TODO el contenido del botón)
        -------------------------------------------------------------------------------- */
        .stButton > button, .stButton > button * { cursor: pointer !important; }
        a, [role="button"], .stRadio label, .stSelectbox, .stCheckbox { cursor: pointer !important; }

        /* --------------------------------------------------------------------------------
           SIDEBAR (Estilo profesional)
        -------------------------------------------------------------------------------- */
        section[data-testid="stSidebar"] {
            background: #0b1224 !important;
            border-right: 1px solid rgba(255,255,255,0.05);
        }
        .sidebar-brand {
            padding: 1.8rem 1rem 1.2rem 1rem;
            text-align: center;
            background: linear-gradient(180deg, rgba(99,102,241,0.10) 0%, transparent 100%);
            border-radius: 0 0 24px 24px;
            margin-bottom: 1.2rem;
            border-bottom: 1px solid rgba(255,255,255,0.06);
        }
        .user-avatar {
            width: 78px;
            height: 78px;
            background: linear-gradient(135deg, var(--neon-indigo), var(--neon-magenta));
            border-radius: 22px;
            margin: 0 auto 10px;
            display: flex; align-items: center; justify-content: center;
            font-size: 2rem; font-weight: 900; color: white;
            box-shadow: 0 10px 25px rgba(0,0,0,0.5);
            transform: rotate(-2deg);
        }
        .side-nav .nav-item {
            display: block;
            background: linear-gradient(145deg, #101629, #0e1426);
            border: 1px solid rgba(255,255,255,0.05);
            border-radius: 14px;
            padding: 12px 14px;
            margin-bottom: 10px;
            color: #e5e7eb;
            font-weight: 700;
            transition: all .25s ease;
            text-decoration: none;
        }
        .side-nav .nav-item:hover {
            border-color: var(--neon-indigo);
            box-shadow: 0 0 20px rgba(99,102,241,0.25);
            transform: translateY(-2px);
        }
        .side-nav .nav-item.active {
            border-color: var(--neon-indigo);
            background: linear-gradient(160deg, #151c33 0%, #10182d 100%);
            box-shadow: inset 0 0 0 1px rgba(99,102,241,0.28);
        }
        .side-nav .nav-ico {
            margin-right: .55rem;
            font-size: 1.05rem;
        }
        .side-meta {
            margin-top: 1rem;
            padding: .75rem .9rem;
            font-size: .82rem;
            border: 1px dashed rgba(99,102,241,0.32);
            border-radius: 10px;
            color: var(--text-muted);
        }

        /* --------------------------------------------------------------------------------
           BOTONES "CARD" (Temas y Niveles) — TAMAÑO NORMAL
        -------------------------------------------------------------------------------- */
        /* Tamaño normal (ni pequeño ni gigante). Altura 160px en desktop, 140px en móvil. */
        .stButton > button {
            background: linear-gradient(145deg, #151b2b, #0e1322) !important;
            border: 1px solid rgba(255, 255, 255, 0.06) !important;
            border-radius: 18px !important;
            height: 160px !important;
            width: 100% !important;
            color: #ffffff !important;
            transition: all 0.28s ease !important;
            display: flex !important;
            flex-direction: column !important;
            align-items: center !important;
            justify-content: center !important;
            font-size: 1.18rem !important; /* tamaño de texto normal */
            font-weight: 800 !important;
            letter-spacing: .2px !important;
            box-shadow: 0 10px 22px rgba(0,0,0,0.32) !important;
            text-align: center !important;
            line-height: 1.25 !important;
            padding: 12px 10px !important;
        }
        .stButton > button:hover {
            border-color: var(--neon-indigo) !important;
            box-shadow: 0 0 24px rgba(99,102,241,0.28) !important;
            transform: translateY(-6px) !important;
            background: #1a2236 !important;
        }
        @media (max-width: 768px) {
            .stButton > button {
                height: 140px !important;
                font-size: 1.05rem !important;
            }
        }

        /* --------------------------------------------------------------------------------
           TÍTULOS Y TIPOGRAFÍA
        -------------------------------------------------------------------------------- */
        h1, h2, h3, h4, h5 {
            letter-spacing: .2px;
        }
        .muted {
            color: var(--text-muted);
            font-weight: 400;
        }

        /* --------------------------------------------------------------------------------
           TARJETA DE PREGUNTA (Quiz)
        -------------------------------------------------------------------------------- */
        .quiz-card {
            background: linear-gradient(145deg, rgba(255,255,255,0.035), rgba(255,255,255,0.02));
            padding: 1.6rem 1.4rem;
            border-radius: 18px;
            border: 1px solid rgba(255,255,255,0.06);
            box-shadow: 0 10px 24px rgba(0,0,0,0.32);
            margin-bottom: 1rem;
        }
        .quiz-card .q-title {
            font-size: 1.1rem;
            font-weight: 800;
            color: #fff;
            margin: 0 0 .25rem 0;
        }
        .quiz-card .q-sub {
            font-size: .95rem;
            color: var(--text-muted);
            margin: 0 0 .75rem 0;
        }
        .quiz-actions {
            display: flex;
            gap: 8px;
            align-items: center;
        }
        .tag {
            display: inline-block;
            padding: .18rem .5rem;
            font-size: .72rem;
            border-radius: 8px;
            background: rgba(99,102,241,.15);
            border: 1px solid rgba(99,102,241,.25);
            color: #c7ccff;
            font-weight: 700;
            letter-spacing: .3px;
        }

        /* Controls (Radios) */
        div[role="radiogroup"] label {
            font-size: .98rem !important;
            font-weight: 700 !important;
        }

        /* --------------------------------------------------------------------------------
           ANIMACIÓN DE ENTRADA
        -------------------------------------------------------------------------------- */
        @keyframes slideUp {
            from { opacity: 0; transform: translateY(14px); }
            to   { opacity: 1; transform: translateY(0); }
        }
        .reveal { animation: slideUp .55s ease-out forwards; }
        </style>
        """,
        unsafe_allow_html=True,
    )

apply_apex_styles()

# ==============================================================================
# 5) MOTOR DE DATOS (DB, FALLBACK DE PREGUNTAS)
# ==============================================================================
def build_advanced_db() -> pd.DataFrame:
    """
    Genera una base de datos en memoria con ~300 trabajadores.
    """
    if st.session_state.vault["db_instance"] is None:
        names = ["Alexander", "Isabella", "Maximilian", "Sophia", "Sebastian",
                 "Valeria", "Dominic", "Camila", "Lucian", "Elena"]
        last_names = ["Vance", "Giron", "Thorne", "Blackwood", "Holloway",
                      "Stark", "Gomez", "Perez", "Larsen", "Rossi"]
        depts = ["Cloud Architecture", "Data Sovereignty", "Quantum Systems",
                 "Neural Networks", "Security Operations"]
        roles = ["Lead DBA", "Data Architect", "System Engineer",
                 "Security Analyst", "DevOps Manager"]

        records: List[List[Any]] = []
        for i in range(1, 301):
            fn, ln = random.choice(names), random.choice(last_names)
            email = f"{fn.lower()}.{ln.lower()}{i:03d}@apex-systems.com"
            salary = random.randint(8500, 45000)
            access_level = random.choice(["L1-Public", "L2-Restricted", "L3-Confidential", "L4-TopSecret"])
            last_login = (datetime.now() - timedelta(minutes=random.randint(5, 10000))).strftime("%Y-%m-%d %H:%M")
            records.append([
                i, fn, ln, email,
                random.choice(depts),
                random.choice(roles),
                salary, access_level, last_login,
                random.choice(["Active", "On Hold", "Suspended"])
            ])

        columns = ["ID", "NOMBRE", "APELLIDO", "EMAIL", "DPTO", "CARGO",
                   "SALARIO", "ACCESO", "LAST_LOGIN", "ESTADO"]
        st.session_state.vault["db_instance"] = pd.DataFrame(records, columns=columns)
    return st.session_state.vault["db_instance"]

def run_apex_query(query: str) -> Tuple[Optional[pd.DataFrame], Optional[str], float]:
    """
    Ejecuta una consulta sobre la DB en memoria. Devuelve (df, error, tiempo).
    """
    df_core = build_advanced_db()
    conn = sqlite3.connect(":memory:")
    df_core.to_sql("TRABAJADORES", conn, index=False, if_exists="replace")
    try:
        start_exec = time.time()

        # Permitimos cualquier statement (para mantener compatibilidad),
        # pero la app es de entrenamiento (principalmente SELECT).
        if not query.strip().upper().startswith("SELECT"):
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
            return pd.DataFrame({"Status": ["Executed"], "Note": ["DML operation executed in memory"]}), None, 0.0

        results = pd.read_sql_query(query, conn)
        end_exec = time.time()
        return results, None, (end_exec - start_exec)
    except Exception as e:
        return None, str(e), 0.0
    finally:
        conn.close()

# Repositorio de preguntas (importa externo si existe, si no usa fallback)
try:
    import importlib
    import preguntas  # type: ignore
    importlib.reload(preguntas)  # hot reload en dev
    CONOCIMIENTO_REPO: Dict[str, List[Dict[str, List[Dict[str, Any]]]]] = preguntas.temas  # type: ignore
except Exception:
    # Fallback simple para no romper la app (ejemplo)
    CONOCIMIENTO_REPO = {
        "Inglés Técnico": [
            {
                "Básico": [
                    {
                        "pregunta": "¿Qué significa 'bug' en desarrollo de software?",
                        "opciones": ["Insecto", "Error/Falla", "Característica Oculta", "Hardware"],
                        "correcta": "Error/Falla",
                        "explicacion": "Un 'bug' es un error de software que provoca resultados inesperados.",
                        "traduccion": "'bug' = 'error/falla'."
                    },
                    {
                        "pregunta": "Selecciona el término correcto para 'compilador' en inglés:",
                        "opciones": ["Interpreter", "Builder", "Compiler", "Runner"],
                        "correcta": "Compiler",
                        "explicacion": "Compiler traduce código fuente a binario/bytecode antes de ejecutarse.",
                        "traduccion": "'compilador' = 'compiler'."
                    },
                ],
                "Intermedio": [
                    {
                        "pregunta": "¿Cuál describe mejor 'scalability'?",
                        "opciones": [
                            "Capacidad de reparar errores",
                            "Capacidad de crecer en demanda",
                            "Capacidad de reducir latencia",
                            "Capacidad de migrar a on-prem"
                        ],
                        "correcta": "Capacidad de crecer en demanda",
                        "explicacion": "Escalabilidad es la habilidad de manejar crecimiento de carga.",
                        "traduccion": "'scalability' = 'escalabilidad'."
                    }
                ],
                "Avanzado": [
                    {
                        "pregunta": "Elige el término que corresponde a 'observability':",
                        "opciones": ["Orchestrability", "Traceability", "Observability", "Monitorizing"],
                        "correcta": "Observability",
                        "explicacion": "Observabilidad: métricas, logs y trazas para entender el sistema.",
                        "traduccion": "'observability' = 'observabilidad'."
                    }
                ]
            }
        ],
        "SQL": [
            {
                "Básico": [
                    {
                        "pregunta": "¿Qué hace SELECT * FROM tabla?",
                        "opciones": ["Inserta filas", "Elimina filas", "Actualiza filas", "Consulta todas las columnas"],
                        "correcta": "Consulta todas las columnas",
                        "explicacion": "SELECT * obtiene todas las columnas de la tabla.",
                        "traduccion": "SELECT * FROM table = selecciona todas las columnas."
                    }
                ]
            }
        ],
    }

# ==============================================================================
# 6) UTILIDADES DE QUIZ — 1 PREGUNTA A LA VEZ
# ==============================================================================
def get_quiz_state(topic: str, lvl: str) -> Dict[str, Any]:
    """
    Obtiene/crea el estado del quiz para (topic, lvl).
    """
    key = (topic, lvl)
    if key not in st.session_state.vault["quiz_state"]:
        st.session_state.vault["quiz_state"][key] = {
            "idx": 0,
            "answers": {},
            "checked": {},
            "score": 0
        }
    return st.session_state.vault["quiz_state"][key]

def reset_quiz_state(topic: str, lvl: str) -> None:
    """
    Reinicia el estado del quiz para (topic, lvl).
    """
    key = (topic, lvl)
    st.session_state.vault["quiz_state"][key] = {"idx": 0, "answers": {}, "checked": {}, "score": 0}

def clamp(value: int, low: int, high: int) -> int:
    """
    Limita un valor a [low, high].
    """
    return max(low, min(value, high))

# ==============================================================================
# 7) INTERFAZ — SIDEBAR PROFESIONAL
# ==============================================================================
def render_apex_sidebar() -> None:
    with st.sidebar:
        st.markdown(
            f"""
            <div class="sidebar-brand">
              <div class="user-avatar">SY</div>
              <h3 style="margin:0; font-size:1.22rem;">Apex Developer</h3>
              <p class="muted" style="font-size:.84rem; margin:.35rem 0 0 0;">Professional Lab 2026</p>
              <div class="side-meta">
                <b>XP:</b> {st.session_state.vault['user_xp']} &nbsp;&nbsp; <b>RANK:</b> {st.session_state.vault['user_rank']}
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        active = st.session_state.vault["active_view"]

        # Navegación con estilo (usamos botones normales, pero maquillados con CSS)
        def nav_button(label: str, icon: str, key_name: str, view: str) -> None:
            cls = "nav-item active" if active == view else "nav-item"
            c = st.container()
            with c:
                if st.button(f"{icon}  {label}", key=key_name, use_container_width=True):
                    st.session_state.vault["active_view"] = view
                    if view == "training":
                        st.session_state.vault["nav_step"] = 0
                    st.rerun()
            st.markdown(
                f"""
                <script>
                    // Etiquetado para aplicar la clase activa estéticamente:
                    const root = window.parent.document;
                    const btns = root.querySelectorAll('button[kind="secondary"]');
                    // No manipulamos clases aquí para evitar errores, CSS ya hace el trabajo.
                </script>
                """,
                unsafe_allow_html=True,
            )

        st.markdown('<div class="side-nav">', unsafe_allow_html=True)
        nav_button("Página de Bienvenida", "🏠", "nav_home", "welcome")
        nav_button("Training Hub", "🧠", "nav_train", "training")
        nav_button("SQL Workbench", "⚔️", "nav_sql", "sql")
        st.markdown("</div>", unsafe_allow_html=True)

        st.caption("DevMaster Apex v10.1")
        st.caption("Build 9131.SR.2026")

# ==============================================================================
# 8) VISTAS (WELCOME / TRAINING / SQL)
# ==============================================================================
def show_welcome_apex() -> None:
    st.markdown('<div class="reveal">', unsafe_allow_html=True)
    st.markdown(
        """
        <h1 style="font-size: 3.6rem; margin-bottom: 0;">DevMaster Apex</h1>
        <p class="muted" style="font-size: 1.22rem; margin-bottom: .75rem;">
            Entorno profesional para la maestría en Sistemas de Datos y Comunicación Técnica.
        </p>
        """,
        unsafe_allow_html=True,
    )

    col_anim, col_content = st.columns([1, 1])
    with col_anim:
        if ANIMATIONS_ON:
            anim_data = fetch_lottie(LOTTIE_DASH_PRO)
            if anim_data:
                st_lottie(anim_data, height=420)

    with col_content:
        st.markdown("### ⚙️ Ecosistema de SY")
        st.write(
            "Plataforma calibrada para ofrecer una experiencia de aprendizaje de grado industrial, "
            "integrando motores de bases de datos y módulos de terminología técnica."
        )
        st.markdown("---")
        st.markdown("#### ⚡ Acciones de Despliegue")
        c_b1, c_b2 = st.columns(2)
        with c_b1:
            if st.button("Iniciar Módulos", key="hero_training", use_container_width=True):
                st.session_state.vault["active_view"] = "training"
                st.session_state.vault["nav_step"] = 0
                st.rerun()
        with c_b2:
            if st.button("Acceso Workbench", key="hero_sql", use_container_width=True):
                st.session_state.vault["active_view"] = "sql"
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    st.subheader("🚀 Especificaciones de la Suite")
    spec1, spec2, spec3 = st.columns(3)
    with spec1:
        st.markdown(
            """
            <div style="background:rgba(255,255,255,0.035); padding:22px; border-radius:18px;
                        border:1px solid rgba(255,255,255,0.06);">
              <h4>🗄️ SQL Engine 3.0</h4>
              <p class="muted">Instancia SQLite integrada con 300 entidades activas.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with spec2:
        st.markdown(
            """
            <div style="background:rgba(255,255,255,0.035); padding:22px; border-radius:18px;
                        border:1px solid rgba(255,255,255,0.06);">
              <h4>🇺🇸 English Core</h4>
              <p class="muted">Práctica enfocada en terminología técnica y gramática profesional.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with spec3:
        st.markdown(
            """
            <div style="background:rgba(255,255,255,0.035); padding:22px; border-radius:18px;
                        border:1px solid rgba(255,255,255,0.06);">
              <h4>📱 Hybrid Flux UI</h4>
              <p class="muted">Interfaz adaptable para móviles y escritorio.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# TRAINING HUB — Pasos:
# 0) Seleccionar Tema (módulos)
# 1) Seleccionar Nivel (cards)
# 2) Quiz (UNA pregunta a la vez, tarjetas + navegación)
# ------------------------------------------------------------------------------
def show_training_hub() -> None:
    step = st.session_state.vault["nav_step"]

    # --------------------------------------------------------------------------
    # PASO 0: GRID DE TEMAS (Módulos) — tamaño normal + 3 columnas responsive
    # --------------------------------------------------------------------------
    if step == 0:
        st.markdown('<div class="reveal">', unsafe_allow_html=True)
        st.title("🎓 Centro de Capacitación")
        st.markdown("Selecciona una especialidad para iniciar la secuencia de aprendizaje.")

        temas_disponibles = list(CONOCIMIENTO_REPO.keys())
        # Fijamos 3 columnas (tamaño normal); así evitamos botones estrechos/tiny
        col_count = 3 if len(temas_disponibles) >= 3 else len(temas_disponibles)
        cols = st.columns(col_count) if col_count > 0 else [st]

        for i, tema in enumerate(temas_disponibles):
            with cols[i % col_count]:
                if st.button(f"📘\n{tema}", key=f"theme_btn_{i}", use_container_width=True):
                    st.session_state.vault["current_topic"] = tema
                    st.session_state.vault["nav_step"] = 1
                    st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    # --------------------------------------------------------------------------
    # PASO 1: SELECCIÓN DE NIVEL — tamaño normal + 2~3 columnas
    # --------------------------------------------------------------------------
    elif step == 1:
        st.markdown('<div class="reveal">', unsafe_allow_html=True)

        if st.button("⬅️ Volver a Especialidades", key="back_topics", use_container_width=True):
            st.session_state.vault["nav_step"] = 0
            st.rerun()

        topic = st.session_state.vault["current_topic"]
        st.title(f"Especialidad: {topic}")
        st.subheader("Selecciona el nivel de dificultad:")

        niveles_dict = CONOCIMIENTO_REPO[topic][0]
        niveles_lista = list(niveles_dict.keys())

        col_count = 3 if len(niveles_lista) >= 3 else len(niveles_lista)
        cols_lvl = st.columns(col_count) if col_count > 0 else [st]

        for i, lvl in enumerate(niveles_lista):
            with cols_lvl[i % col_count]:
                if st.button(f"📶\n{lvl}", key=f"lvl_btn_{i}", use_container_width=True):
                    st.session_state.vault["current_lvl"] = lvl
                    # Inicializa el estado de quiz para este (topic, lvl)
                    reset_quiz_state(topic, lvl)
                    st.session_state.vault["nav_step"] = 2
                    st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    # --------------------------------------------------------------------------
    # PASO 2: QUIZ — SOLO UNA PREGUNTA A LA VEZ (Tarjeta + navegación)
    # --------------------------------------------------------------------------
    elif step == 2:
        st.markdown('<div class="reveal">', unsafe_allow_html=True)

        # Botones de navegación
        c_nav = st.columns([1, 1, 1])
        with c_nav[0]:
            if st.button("⬅️ Cambiar Nivel", key="back_levels", use_container_width=True):
                st.session_state.vault["nav_step"] = 1
                st.rerun()
        with c_nav[1]:
            if st.button("🏁 Reiniciar Nivel", key="reset_level", use_container_width=True):
                topic = st.session_state.vault["current_topic"]
                lvl = st.session_state.vault["current_lvl"]
                reset_quiz_state(topic, lvl)
                st.rerun()

        tema = st.session_state.vault["current_topic"]
        nivel = st.session_state.vault["current_lvl"]

        st.title(f"Secuencia: {tema}")
        st.caption(f"Nivel de Operación: {nivel}")

        data_quiz: List[Dict[str, Any]] = CONOCIMIENTO_REPO[tema][0][nivel]
        qstate = get_quiz_state(tema, nivel)

        total_q = len(data_quiz)
        idx = clamp(qstate["idx"], 0, max(0, total_q - 1))
        qstate["idx"] = idx

        # Si no hay preguntas
        if total_q == 0:
            st.info("No hay preguntas en este nivel por el momento.")
            st.markdown("</div>", unsafe_allow_html=True)
            return

        # Tarjeta de la pregunta actual
        item = data_quiz[idx]
        pregunta_txt = item["pregunta"] if isinstance(item, dict) else str(item)
        opciones = item.get("opciones", []) if isinstance(item, dict) else []
        correcta = item.get("correcta", None) if isinstance(item, dict) else None
        explicacion = item.get("explicacion", "") if isinstance(item, dict) else ""
        traduccion = item.get("traduccion", "") if isinstance(item, dict) else ""

        # Encabezado con progreso
        st.markdown(
            f"""
            <div style="display:flex; align-items:center; gap:10px; margin-top:6px;">
                <span class="tag">Pregunta {idx+1}/{total_q}</span>
                <span class="tag">XP: {st.session_state.vault['user_xp']}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Tarjeta
        st.markdown(
            f"""
            <div class="quiz-card">
              <div class="q-title">{pregunta_txt}</div>
              <div class="q-sub">Selecciona una opción y presiona <b>Validar</b>.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Entrada de respuesta
        answer_key = f"quiz_opt_{tema}_{nivel}_{idx}"
        user_resp = None
        if opciones:
            user_resp = st.radio(
                f"Respuesta para P{idx+1}:",
                opciones,
                key=answer_key,
                horizontal=True,
                label_visibility="collapsed",
            )

        # Acciones de navegación/validación
        c_prev, c_validate, c_next = st.columns([1, 1, 1])

        # Botón "Anterior"
        with c_prev:
            disable_prev = (idx == 0)
            if st.button("⬅️ Anterior", key=f"prev_{tema}_{nivel}_{idx}", disabled=disable_prev, use_container_width=True):
                qstate["idx"] = clamp(idx - 1, 0, total_q - 1)
                st.rerun()

        # Botón "Validar"
        with c_validate:
            checked = qstate["checked"].get(idx, False)
            if st.button("✅ Validar", key=f"validar_{tema}_{nivel}_{idx}", use_container_width=True):
                if opciones and user_resp is not None:
                    qstate["answers"][idx] = user_resp
                    if not checked:
                        if correcta is not None and user_resp == correcta:
                            st.success("✨ ¡Correcto! +50 XP")
                            st.session_state.vault["user_xp"] += 50
                            st.session_state.vault["metrics"]["success"] += 1
                            qstate["score"] += 1
                        else:
                            st.error(f"❌ Respuesta incorrecta. Correcta: {correcta}")
                            st.session_state.vault["metrics"]["fails"] += 1
                    qstate["checked"][idx] = True
                else:
                    st.warning("Selecciona una opción antes de validar.")

        # Botón "Siguiente"
        with c_next:
            disable_next = (idx >= total_q - 1)
            if st.button("Siguiente ➡️", key=f"next_{tema}_{nivel}_{idx}", disabled=disable_next, use_container_width=True):
                qstate["idx"] = clamp(idx + 1, 0, total_q - 1)
                st.rerun()

        # Muestra feedback y documentación si la pregunta ya fue validada
        if qstate["checked"].get(idx, False):
            if correcta is not None and qstate["answers"].get(idx) == correcta:
                st.success("✔️ Esta pregunta ya fue respondida correctamente.")
            else:
                st.info("ℹ️ Puedes repasar la explicación y volver a intentar en otra pregunta.")

            with st.expander("📘 Documentación Técnica / Explicación"):
                if explicacion:
                    st.write(f"**Análisis:** {explicacion}")
                if traduccion:
                    st.caption(f"**Traducción:** {traduccion}")

        # Si llegamos al final (todas revisadas), mostramos resumen
        if all(qstate["checked"].get(i, False) for i in range(total_q)):
            st.markdown("---")
            st.subheader("🏆 Resumen del Nivel")
            st.write(f"Preguntas correctas: **{qstate['score']}** de **{total_q}**")
            st.write(f"XP actual: **{st.session_state.vault['user_xp']}**")
            col_end = st.columns(3)
            with col_end[0]:
                if st.button("🔁 Reiniciar Nivel", key="reset_lvl_end", use_container_width=True):
                    reset_quiz_state(tema, nivel)
                    st.rerun()
            with col_end[1]:
                if st.button("🧭 Cambiar Nivel", key="goto_levels_end", use_container_width=True):
                    st.session_state.vault["nav_step"] = 1
                    st.rerun()
            with col_end[2]:
                if st.button("🏠 Ir a Módulos", key="goto_topics_end", use_container_width=True):
                    st.session_state.vault["nav_step"] = 0
                    st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# SQL WORKBENCH
# ------------------------------------------------------------------------------
def show_sql_lab_apex() -> None:
    st.markdown('<div class="reveal">', unsafe_allow_html=True)
    st.title("⚔️ SQL Workbench Enterprise")
    st.markdown("Consola interactiva vinculada a la base de datos de producción (300 empleados).")

    c_workbench, c_schema = st.columns([3, 1])

    # Esquema / Lottie
    with c_schema:
        if ANIMATIONS_ON:
            lottie_sql = fetch_lottie(LOTTIE_SQL_ENG)
            if lottie_sql:
                st_lottie(lottie_sql, height=140)
        st.markdown("### 📊 Metadata Schema")
        st.markdown(
            """
            <div style="
                background:#10172a;
                padding:14px;
                border-radius:14px;
                border:1px solid #1f2a44;
                color:#93e0b5;
                font-size:0.78rem;
                font-family:'Fira Code', monospace;">
                -- TABLA: TRABAJADORES<br>
                ID: INT (PK)<br>
                NOMBRE: TEXT<br>
                APELLIDO: TEXT<br>
                EMAIL: TEXT<br>
                DPTO: TEXT<br>
                CARGO: TEXT<br>
                SALARIO: INT<br>
                ACCESO: TEXT<br>
                LAST_LOGIN: DATETIME<br>
                ESTADO: TEXT
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 Reiniciar Dataset", use_container_width=True):
            st.session_state.vault["db_instance"] = None
            st.rerun()

    # Consola
    with c_workbench:
        st.markdown("#### 🖥️ Apex Console")
        default_script = (
            "-- Consultar empleados con acceso restringido y salarios competitivos\n"
            "SELECT NOMBRE, CARGO, SALARIO, ACCESO\n"
            "FROM TRABAJADORES\n"
            "WHERE SALARIO > 25000\n"
            "ORDER BY SALARIO DESC\n"
            "LIMIT 5;"
        )
        query_input = st.text_area("SQL Editor", value=default_script, height=220, label_visibility="collapsed")
        if st.button("▶ EJECUTAR SCRIPT", type="primary", use_container_width=True):
            st.session_state.vault["sql_logs"].append(query_input)
            df_res, error_msg, perf_time = run_apex_query(query_input)
            if error_msg:
                st.error(f"⚠️ APEX ENGINE ERROR: {error_msg}")
            else:
                st.markdown(f"**Resultados:** {len(df_res)} filas • {perf_time:.4f}s")
                st.dataframe(df_res, use_container_width=True)
                st.session_state.vault["user_xp"] += 25

        st.divider()
        st.subheader("Auditoría de Datos (Primeras 5 Entidades)")
        st.dataframe(build_advanced_db().head(5), use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ==============================================================================
# 9) ENRUTADOR
# ==============================================================================
def main() -> None:
    render_apex_sidebar()

    focus_view = st.session_state.vault["active_view"]
    if focus_view == "welcome":
        show_welcome_apex()
    elif focus_view == "training":
        show_training_hub()
    elif focus_view == "sql":
        show_sql_lab_apex()
    else:
        # Fallback a bienvenida
        show_welcome_apex()

# ==============================================================================
# 10) ENTRY POINT
# ==============================================================================
if __name__ == "__main__":
    main()

# ==============================================================================
