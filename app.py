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
    st.metric("Cognition", f"{cognition:.2f}")
    st.metric("Performance", f"{performance:.2f}")

    if fatigue >= 90 or cognition <= 40:
        st.error("🔴 Replace Athlete! Threshold passed.")
        st.session_state.sim_state["running"] = False
    elif fatigue >= 70 or cognition <= 60:
        st.warning("🟠 5-minute rest needed (Break threshold).")

# --- Graphs and Logs ---
with col3:
    st.subheader("Fatigue and Cognition Over Time")
    df = pd.DataFrame({
        "Time": st.session_state.sim_state["time_log"],
        "Fatigue": st.session_state.sim_state["fatigue_log"],
        "Cognition": st.session_state.sim_state["cognition_log"],
    })

    line_chart = alt.Chart(df).transform_fold(
        ["Fatigue", "Cognition"],
        as_=["Measure", "Value"]
    ).mark_line().encode(
        x="Time:Q",
        y="Value:Q",
        color="Measure:N"
    ).properties(height=300)

    st.altair_chart(line_chart, use_container_width=True)

    st.subheader("📝 Damage Log")
    st.dataframe(st.session_state.sim_state["damage_log"], use_container_width=True)
