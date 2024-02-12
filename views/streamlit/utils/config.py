import streamlit as st


def init_state():
    if 'is_logged_in' not in st.session_state:
        st.session_state.is_logged_in = False

    if 'name' not in st.session_state:
        st.session_state.name = ""
