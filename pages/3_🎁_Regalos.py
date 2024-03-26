import streamlit as st
from utils import init_state

st.set_page_config(page_title="CBTale", layout="wide", page_icon="👩‍❤️‍👨")

init_state()

st.title("🎁 Regalos")

from src.entities import Gift

if not st.session_state["gift_list"]:
    with st.spinner("Cargando los regalos! Espera un momento"):
        st.session_state.gift_list = [Gift.read("X001") for _ in range(5)]

from streamlit_carousel import carousel

test_items = [
    dict(
        title="Slide 1",
        text="A tree in the savannah",
        interval=None,
        img="https://i.ibb.co/QcqVrXL/Game-Boy-Advance-Crash-Bandicoot-2-N-Tranced-Diamonds-and-Power-Crystals.png",
    ),
    dict(
        title="Slide 2",
        text="A wooden bridge in a forest in Autumn",
        img="https://i.ibb.co/QcqVrXL/Game-Boy-Advance-Crash-Bandicoot-2-N-Tranced-Diamonds-and-Power-Crystals.png",
    ),
    dict(
        title="Slide 3",
        text="A distant mountain chain preceded by a sea",
        img="https://i.ibb.co/QcqVrXL/Game-Boy-Advance-Crash-Bandicoot-2-N-Tranced-Diamonds-and-Power-Crystals.png",
    ),
]

carousel(items=test_items, width=1)