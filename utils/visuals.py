import streamlit as st
import os

SVG_PATH = "assets/athlete_silhouette.svg"

def get_color_for_damage(level):
    if level == 0:
        return "#8fbc8f"  # Green
    elif level == 1:
        return "#ffd700"  # Yellow
    elif level == 2:
        return "#ff8c00"  # Orange
    else:
        return "#ff0000"  # Red

def render_svg_avatar(body_state):
    try:
        with open(SVG_PATH, "r") as f:
            svg_data = f.read()
    except FileNotFoundError:
        st.error("SVG file not found.")
        return None

    # Replace fill colours dynamically
    for part_id, damage in body_state.items():
        color = get_color_for_damage(damage)
        svg_data = svg_data.replace(
            f'id="{part_id}"',
            f'id="{part_id}" fill="{color}"'
        )

    # Display SVG
    st.components.v1.html(f"""
        <div style="text-align: center;">
            <svg width="300" height="600" viewBox="0 0 300 600" xmlns="http://www.w3.org/2000/svg">
                {svg_data}
            </svg>
        </div>
    """, height=600)

    # Simulate clicking parts (placeholder logic — to be improved with JavaScript integration)
    clicked_part = st.selectbox("Simulate manual damage to:", options=list(body_state.keys()) + ["None"])
    return None if clicked_part == "None" else clicked_part
