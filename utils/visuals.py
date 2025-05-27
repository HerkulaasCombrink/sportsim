import streamlit as st

IMAGE_PATH = "assets/athlete_silhouette.jpg"

def render_static_avatar():
    st.image(IMAGE_PATH, caption="Athlete Silhouette", use_column_width=True)

def select_body_part_for_damage():
    parts = [
        "None", "head", "chest", "abdomen",
        "left_arm", "right_arm", "left_leg", "right_leg"
    ]
    return st.selectbox("Simulate manual damage to:", options=parts)
