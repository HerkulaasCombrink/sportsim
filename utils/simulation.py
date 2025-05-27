import random
import pandas as pd

# Define body parts and their impact multipliers
BODY_PART_IMPACTS = {
    "head": {"fatigue": 10, "cognition": 20},
    "chest": {"fatigue": 8, "cognition": 10},
    "left_arm": {"fatigue": 5, "cognition": 3},
    "right_arm": {"fatigue": 5, "cognition": 3},
    "left_leg": {"fatigue": 5, "cognition": 3},
    "right_leg": {"fatigue": 5, "cognition": 3},
    "abdomen": {"fatigue": 3, "cognition": 1},
}

def initialize_simulation_state():
    st = {
        "current_time": 0,
        "running": False,
        "fatigue": 0.0,
        "cognition": 100.0,
        "body_state": {part: 0 for part in BODY_PART_IMPACTS},
        "fatigue_log": [],
        "cognition_log": [],
        "time_log": [],
        "damage_log": pd.DataFrame(columns=["Time", "Body Part", "Damage Type", "Fatigue Δ", "Cognition Δ"]),
    }
    import streamlit as st_module
    st_module.session_state.sim_state = st

def reset_simulation_state():
    initialize_simulation_state()

def update_simulation_state():
    import streamlit as st
    state = st.session_state.sim_state

    # Passive changes
    state["current_time"] += 1
    state["fatigue"] += 0.02
    state["cognition"] -= 0.015

    # Random damage event
    if random.random() < 0.1:  # 10% chance per second
        part = random.choice(list(BODY_PART_IMPACTS.keys()))
        apply_damage_to_body(part, damage_type="Random")

    # Log values
    state["fatigue_log"].append(state["fatigue"])
    state["cognition_log"].append(state["cognition"])
    state["time_log"].append(state["current_time"])

def apply_manual_damage(part):
    apply_damage_to_body(part, damage_type="Manual")

def apply_damage_to_body(part, damage_type="Manual"):
    import streamlit as st
    state = st.session_state.sim_state
    impact = BODY_PART_IMPACTS.get(part, {"fatigue": 0, "cognition": 0})

    state["body_state"][part] +_]()
