# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import random
import sqlite3
import requests
import time
from datetime import datetime, timedelta
import json
from typing import Any, Dict, List, Optional, Tuple
import os
import sys
import importlib
import importlib.util
import ast

def master_state_guardian() -> None:
    if "vault" not in st.session_state:
        st.session_state["vault"] = {
            "active_view": "welcome",
            "nav_step": 0,
            "current_topic": None,
            "current_lvl": None,
            "quiz_state": {},
            "user_xp": 2450,
            "user_rank": "Senior Student",
            "user_tag": "SY",
            "sql_logs": [],
            "db_instance": None,
            "metrics": {"success": 0, "fails": 0},
        }
master_state_guardian()

st.set_page_config(
    page_title="DevMaster Apex — Training Suite",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded",
)

try:
    from streamlit_lottie import st_lottie
    ANIMATIONS_ON = True
except Exception:
    ANIMATIONS_ON = False

def fetch_lottie(url: str) -> Optional[dict]:
    try:
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            return resp.json()
        return None
    except Exception:
        return None

LOTTIE_SQL_ENG = "https://assets2.lottiefiles.com/private_files/lf30_w1uxkbue.json"
LOTTIE_DASH_PRO = "https://assets5.lottiefiles.com/packages/lf20_fcfjwiyb.json"

def apply_apex_styles() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&family=Fira+Code:wght@400;500&display=swap');
        :root {
            --neon-indigo: #6366f1;
            --neon-magenta: #ec4899;
            --bg-deep-void: #0b1020;
            --card-surface: #151b2b;
            --border-glow: rgba(99, 102, 241, 0.42);
            --text-muted: #a8b2c1;
        }
        .stApp {
            background: var(--bg-deep-void);
            background-image:
                radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.12) 0px, transparent 45%),
                radial-gradient(at 100% 100%, rgba(236, 72, 153, 0.12) 0px, transparent 50%);
            color: #f8fafc !important;
            font-family: 'Plus Jakarta Sans', system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
        }
        .stButton > button, .stButton > button * { cursor: pointer !important; }
        a, [role="button"], .stRadio label, .stSelectbox, .stCheckbox { cursor: pointer !important; }

        section[data-testid="stSidebar"] {
            background: #0b1224 !important;
            border-right: 1px solid rgba(255,255,255,0.05);
            position: relative;
            overflow: hidden;
        }
        .menu-anim{
            position:absolute;
            inset:-25%;
            background:
                radial-gradient(40% 40% at 20% 20%, rgba(99,102,241,.25), transparent 60%),
                radial-gradient(35% 35% at 80% 30%, rgba(236,72,153,.25), transparent 60%),
                radial-gradient(45% 45% at 50% 80%, rgba(34,197,94,.22), transparent 60%);
            filter: blur(28px);
            opacity:.7;
            animation: sideFloat 12s ease-in-out infinite alternate;
            z-index:0;
        }
        @keyframes sideFloat{
            0%{ transform: translate3d(-10px,-8px,0) scale(1.0); }
            50%{ transform: translate3d(8px,10px,0) scale(1.05); }
            100%{ transform: translate3d(-6px,6px,0) scale(1.02); }
        }
        .sidebar-brand,
        .side-nav,
        .side-meta,
        .stButton,
        .stMarkdown,
        .stCaption,
        .stDivider { position: relative; z-index: 1; }

        .sidebar-brand {
            padding: 1.8rem 1rem 1.2rem 1rem;
            text-align: center;
            background: linear-gradient(180deg, rgba(99,102,241,0.10) 0%, transparent 100%);
            border-radius: 0 0 24px 24px;
            margin-bottom: 1.2rem;
            border-bottom: 1px solid rgba(255,255,255,0.06);
        }
        .user-avatar {
            width: 78px; height: 78px;
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
        .side-nav .nav-ico { margin-right: .55rem; font-size: 1.05rem; }

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
            font-size: 1.18rem !important;
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
            .stButton > button { height: 140px !important; font-size: 1.05rem !important; }
        }

        h1, h2, h3, h4, h5 { letter-spacing: .2px; }
        .muted { color: var(--text-muted); font-weight: 400; }

        .quiz-card {
            background: linear-gradient(145deg, rgba(255,255,255,0.035), rgba(255,255,255,0.02));
            padding: 1.6rem 1.4rem;
            border-radius: 18px;
            border: 1px solid rgba(255,255,255,0.06);
            box-shadow: 0 10px 24px rgba(0,0,0,0.32);
            margin-bottom: 1rem;
        }
        .quiz-card .q-title { font-size: 1.1rem; font-weight: 800; color: #fff; margin: 0 0 .25rem 0; }
        .quiz-card .q-sub { font-size: .95rem; color: var(--text-muted); margin: 0 0 .75rem 0; }
        .quiz-actions { display: flex; gap: 8px; align-items: center; }
        .tag {
            display: inline-block; padding: .18rem .5rem; font-size: .72rem; border-radius: 8px;
            background: rgba(99,102,241,.15); border: 1px solid rgba(99,102,241,.25);
            color: #c7ccff; font-weight: 700; letter-spacing: .3px;
        }
        div[role="radiogroup"] label { font-size: .98rem !important; font-weight: 700 !important; }

        @keyframes slideUp { from { opacity: 0; transform: translateY(14px); } to { opacity: 1; transform: translateY(0); } }
        .reveal { animation: slideUp .55s ease-out forwards; }
        </style>
        """,
        unsafe_allow_html=True,
    )
apply_apex_styles()

def build_advanced_db() -> pd.DataFrame:
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
    df_core = build_advanced_db()
    conn = sqlite3.connect(":memory:")
    df_core.to_sql("TRABAJADORES", conn, index=False, if_exists="replace")
    try:
        start_exec = time.time()
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

def _extract_temas_from_text(raw_text: str) -> Optional[Dict[str, Any]]:
    try:
        idx = raw_text.find("temas")
        if idx == -1:
            return None
        eq_idx = raw_text.find("=", idx)
        if eq_idx == -1:
            return None
        brace_start = raw_text.find("{", eq_idx)
        if brace_start == -1:
            return None
        # bracket matching across { } and [ ]
        i = brace_start
        depth_curly = 0
        depth_square = 0
        while i < len(raw_text):
            ch = raw_text[i]
            if ch == "{":
                depth_curly += 1
            elif ch == "}":
                depth_curly -= 1
                if depth_curly == 0 and depth_square == 0:
                    dict_str = raw_text[brace_start:i+1]
                    break
            elif ch == "[":
                depth_square += 1
            elif ch == "]":
                depth_square -= 1
            i += 1
        else:
            return None
        # Normalizar escapes comunes provenientes de serializaciones
        cleaned = dict_str.encode("utf-8", "ignore").decode("unicode_escape")
        # A veces vienen con secuencias \\' y \\"
        cleaned = cleaned.replace("\\'", "'").replace('\\"', '"')
        # literal_eval para seguridad
        parsed = ast.literal_eval(cleaned)
        if isinstance(parsed, dict):
            return parsed
        return None
    except Exception:
        return None

def _load_preguntas_module() -> Optional[Dict[str, Any]]:
    module_name = "preguntas"
    module_path = os.path.join(os.path.dirname(__file__), "preguntas.py")
    try:
        # 1) Intento estándar de import
        if module_name in sys.modules:
            mod = sys.modules[module_name]
            importlib.reload(mod)
        else:
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            if spec is not None and spec.loader is not None:
                mod = importlib.util.module_from_spec(spec)
                sys.modules[module_name] = mod
                spec.loader.exec_module(mod)  # type: ignore[attr-defined]
            else:
                mod = None
        if mod is not None:
            temas_obj = getattr(mod, "temas", None)
            if isinstance(temas_obj, dict) and temas_obj:
                return temas_obj
        # 2) Si no se pudo importar como módulo Python válido, lo intentamos como JSON envolviendo texto rico.
        if os.path.exists(module_path):
            with open(module_path, "r", encoding="utf-8", errors="ignore") as fh:
                raw = fh.read().strip()
            # Caso JSON (exportado de editor): buscar campo 'text' con el script dentro
            temas_from_text = None
            if raw.startswith("{") and ("\"value\"" in raw or "\"content\"" in raw):
                try:
                    data = json.loads(raw)
                    # Buscar la primera entrada que tenga 'value'->'text'
                    if isinstance(data, dict):
                        for v in data.values():
                            if isinstance(v, dict):
                                inner = v.get("value") or {}
                                if isinstance(inner, dict) and "text" in inner:
                                    txt = inner.get("text") or ""
                                    temas_from_text = _extract_temas_from_text(txt)
                                    if temas_from_text:
                                        break
                    if temas_from_text:
                        return temas_from_text
                except Exception:
                    pass
            # 3) Último intento: extraer directamente de texto plano del archivo .py aunque esté escapado
            temas_plain = _extract_temas_from_text(raw)
            if temas_plain:
                return temas_plain
        return None
    except Exception:
        return None

CONOCIMIENTO_REPO = _load_preguntas_module()
if not CONOCIMIENTO_REPO:
    CONOCIMIENTO_REPO = {
        "Inglés Técnico": [
            {
                "Básico": [
                    {
                        "pregunta": "Fallback: ¿Qué significa 'bug'?",
                        "opciones": ["Insecto", "Error/Falla"],
                        "correcta": "Error/Falla",
                        "explicacion": "Un 'bug' es un error de software.",
                        "traduccion": "'bug' = 'error/falla'."
                    }
                ]
            }
        ]
    }

def get_quiz_state(topic: str, lvl: str) -> Dict[str, Any]:
    key = (topic, lvl)
    if key not in st.session_state.vault["quiz_state"]:
        st.session_state.vault["quiz_state"][key] = {"idx": 0, "answers": {}, "checked": {}, "score": 0}
    return st.session_state.vault["quiz_state"][key]

def reset_quiz_state(topic: str, lvl: str) -> None:
    key = (topic, lvl)
    st.session_state.vault["quiz_state"][key] = {"idx": 0, "answers": {}, "checked": {}, "score": 0}

def clamp(value: int, low: int, high: int) -> int:
    return max(low, min(value, high))

def render_apex_sidebar() -> None:
    with st.sidebar:
        st.markdown('<div class="menu-anim"></div>', unsafe_allow_html=True)
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
        def nav_button(label: str, icon: str, key_name: str, view: str) -> None:
            c = st.container()
            with c:
                if st.button(f"{icon}  {label}", key=key_name, use_container_width=True):
                    st.session_state.vault["active_view"] = view
                    if view == "training":
                        st.session_state.vault["nav_step"] = 0
                    st.rerun()
        st.markdown('<div class="side-nav">', unsafe_allow_html=True)
        nav_button("Página de Bienvenida", "🏠", "nav_home", "welcome")
        nav_button("Training Hub", "🧠", "nav_train", "training")
        nav_button("SQL Workbench", "⚔️", "nav_sql", "sql")
        st.markdown("</div>", unsafe_allow_html=True)
        st.caption("DevMaster Apex v10.1")
        st.caption("Build 9131.SR.2026")

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

def show_training_hub() -> None:
    step = st.session_state.vault["nav_step"]
    if step == 0:
        st.markdown('<div class="reveal">', unsafe_allow_html=True)
        st.title("🎓 Centro de Capacitación")
        st.markdown("Selecciona una especialidad para iniciar la secuencia de aprendizaje.")
        temas_disponibles = list(CONOCIMIENTO_REPO.keys())
        col_count = 3 if len(temas_disponibles) >= 3 else len(temas_disponibles)
        cols = st.columns(col_count) if col_count > 0 else [st]
        for i, tema in enumerate(temas_disponibles):
            with cols[i % col_count]:
                if st.button(f"📘\n{tema}", key=f"theme_btn_{i}", use_container_width=True):
                    st.session_state.vault["current_topic"] = tema
                    st.session_state.vault["nav_step"] = 1
                    st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
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
                    reset_quiz_state(topic, lvl)
                    st.session_state.vault["nav_step"] = 2
                    st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    elif step == 2:
        st.markdown('<div class="reveal">', unsafe_allow_html=True)
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
        if total_q == 0:
            st.info("No hay preguntas en este nivel por el momento.")
            st.markdown("</div>", unsafe_allow_html=True)
            return
        item = data_quiz[idx]
        pregunta_txt = item["pregunta"] if isinstance(item, dict) else str(item)
        opciones = item.get("opciones", []) if isinstance(item, dict) else []
        correcta = item.get("correcta", None) if isinstance(item, dict) else None
        explicacion = item.get("explicacion", "") if isinstance(item, dict) else ""
        traduccion = item.get("traduccion", "") if isinstance(item, dict) else ""
        st.markdown(
            f"""
            <div style="display:flex; align-items:center; gap:10px; margin-top:6px;">
                <span class="tag">Pregunta {idx+1}/{total_q}</span>
                <span class="tag">XP: {st.session_state.vault['user_xp']}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            f"""
            <div class="quiz-card">
              <div class="q-title">{pregunta_txt}</div>
              <div class="q-sub">Selecciona una opción y presiona <b>Validar</b>.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
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
        c_prev, c_validate, c_next = st.columns([1, 1, 1])
        with c_prev:
            disable_prev = (idx == 0)
            if st.button("⬅️ Anterior", key=f"prev_{tema}_{nivel}_{idx}", disabled=disable_prev, use_container_width=True):
                qstate["idx"] = clamp(idx - 1, 0, total_q - 1)
                st.rerun()
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
        with c_next:
            disable_next = (idx >= total_q - 1)
            if st.button("Siguiente ➡️", key=f"next_{tema}_{nivel}_{idx}", disabled=disable_next, use_container_width=True):
                qstate["idx"] = clamp(idx + 1, 0, total_q - 1)
                st.rerun()
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

def show_sql_lab_apex() -> None:
    st.markdown('<div class="reveal">', unsafe_allow_html=True)
    st.title("⚔️ SQL Workbench Enterprise")
    st.markdown("Consola interactiva vinculada a la base de datos de producción (300 empleados).")
    c_workbench, c_schema = st.columns([3, 1])
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
        show_welcome_apex()

if __name__ == "__main__":
    main()