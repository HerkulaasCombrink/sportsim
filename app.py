
import streamlit as st
import time
import random
import pandas as pd
import altair as alt
from utils.simulation import (
    initialize_simulation_state,
    update_simulation_state,
    apply_manual_damage,
    reset_simulation_state,
)
from utils.visuals import render_svg_avatar

# --- Page config ---
st.set_page_config(page_title="Athlete Fatigue Simulator", layout="wide")

# --- Title ---
st.title("🏃 Athlete Damage & Fatigue Simulation")

# --- Initialize session state ---
if "sim_state" not in st.session_state:
    initialize_simulation_state()

# --- Sidebar controls ---
with st.sidebar:
    st.header("Simulation Controls")
    if st.button("▶ Start / Resume"):
        st.session_state.sim_state["running"] = True
    if st.button("⏸ Pause"):
        st.session_state.sim_state["running"] = False
    if st.button("🔁 Reset"):
        reset_simulation_state()
    st.write("Simulation time:", st.session_state.sim_state["current_time"], "s")

# --- Main simulation logic ---
if st.session_state.sim_state["running"]:
    if st.session_state.sim_state["current_time"] < 1000:
        update_simulation_state()
        time.sleep(1)
    else:
        st.warning("🏁 Simulation completed.")
        st.session_state.sim_state["running"] = False

# --- Layout: 3 columns ---
col1, col2, col3 = st.columns([1, 1, 1.5])

# --- SVG Avatar ---
with col1:
    st.subheader("Avatar")
    clicked_part = render_svg_avatar(st.session_state.sim_state["body_state"])
    if clicked_part:
        apply_manual_damage(clicked_part)

# --- Vital Stats ---
with col2:
    st.subheader("Status Indicators")
    fatigue = st.session_state.sim_state["fatigue"]
    cognition = st.session_state.sim_state["cognition"]
    performance = round(100 - ((fatigue + (100 - cognition)) / 2), 2)

    st.metric("Fatigue", f"{fatigue:.2f}")
    st.metric("Cognition", f"{cognitio
