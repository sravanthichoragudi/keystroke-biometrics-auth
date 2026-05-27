# app.py
import streamlit as st
from src.engine import BiometricSecurityEngine
from src.interfaces import render_enrollment_view, render_security_gate_view
import src.security_audit as audit  # Imported for the interviewer simulation mode

# Page layout styling setup
st.set_page_config(page_title="Zero-Trust Terminal Console", page_icon="🛡️", layout="wide")

# Theme style override injections to create an authentic security console appearance
st.markdown("""
    <style>
    .stApp { background-color: #0F172A; color: #F1F5F9; }
    h1, h2, h3, h4 { color: #38BDF8 !important; font-family: 'Courier New', monospace; }
    div.stButton > button { 
        background-color: #0284C7 !important; 
        color: white !important; 
        font-weight: bold; 
        border-radius: 6px;
        width: 100%;
        height: 3em;
    }
    /* Sidebar custom styling overrides */
    section[data-testid="stSidebar"] {
        background-color: #0F172A !important;
        border-right: 1px solid #1E293B;
    }
    /* Clean Console Status Box Override */
    .status-panel {
        background-color: #1E293B;
        border-radius: 6px;
        padding: 12px;
        border-left: 4px solid #EF4444;
        margin-bottom: 10px;
    }
    .status-panel.active {
        border-left: 4px solid #10B981;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🛡️ Zero-Trust Biometric Behavioral Terminal")
st.markdown("---")

# Setup state storage blocks across app execution updates
if 'engine' not in st.session_state:
    st.session_state.engine = BiometricSecurityEngine()
if 'profile_data_buffer' not in st.session_state:
    st.session_state.profile_data_buffer = []
if 'compiled_brain' not in st.session_state:
    st.session_state.compiled_brain = None

# --- DECOUPLED CONTROL SIDEBAR FOR INTERVIEWS ---
st.sidebar.markdown("### 🎮 CONTROL PANEL")
app_mode = st.sidebar.selectbox(
    "OPERATION MODE:", 
    ["User Gateway Terminal", "Adversarial Penetration Test Suite"],
    label_visibility="collapsed"
)
st.sidebar.markdown("---")

# --- HIGHLY PROFESSIONAL TELEMETRY TRACKER ---
st.sidebar.markdown("### 🖥️ SYSTEM MONITOR")

samples_count = len(st.session_state.profile_data_buffer)
has_blueprint = st.session_state.compiled_brain is not None

if not has_blueprint:
    # Uninitialized state block formatted cleanly as an embedded terminal block
    st.sidebar.markdown(f"""
    <div class="status-panel">
        <span style="color: #94A3B8; font-size: 11px; font-weight: bold; font-family: monospace;">SECURITY SYSTEM STATE:</span><br>
        <span style="color: #EF4444; font-weight: bold; font-family: monospace; font-size: 14px;">● UNINITIALIZED</span>
        <br><br>
        <span style="color: #94A3B8; font-size: 11px; font-weight: bold; font-family: monospace;">BUFFER PIPELINE:</span><br>
        <span style="color: #38BDF8; font-family: monospace; font-size: 13px;">{samples_count} / 3 Vectors Loaded</span>
    </div>
    """, unsafe_allow_html=True)
else:
    # Armed state block showing active metrics smoothly
    baseline_speed = st.session_state.get('baseline_avg_speed', 0.000)
    st.sidebar.markdown(f"""
    <div class="status-panel active">
        <span style="color: #94A3B8; font-size: 11px; font-weight: bold; font-family: monospace;">SECURITY SYSTEM STATE:</span><br>
        <span style="color: #10B981; font-weight: bold; font-family: monospace; font-size: 14px;">● ACTIVE & ARMED</span>
        <br><br>
        <span style="color: #94A3B8; font-size: 11px; font-weight: bold; font-family: monospace;">TARGET PROFILE SPEED:</span><br>
        <span style="color: #38BDF8; font-family: monospace; font-size: 14px; font-weight: bold;">{baseline_speed:.3f} s/key</span>
    </div>
    """, unsafe_allow_html=True)

st.sidebar.markdown("---")

# INTERACTIVE INTERFACE ROUTING PIPELINE
if app_mode == "User Gateway Terminal":
    # Automatic deployment routing matching original system rules
    if st.session_state.compiled_brain is None:
        render_enrollment_view(st.session_state.engine)
    else:
        render_security_gate_view()

elif app_mode == "Adversarial Penetration Test Suite":
    # Triggers independent audit screen without touching validation states
    audit.run_adversarial_simulations()