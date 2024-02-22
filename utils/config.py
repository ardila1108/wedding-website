import streamlit as st
from src.entities import InvitationGroup


def init_state():
    if 'is_logged_in' not in st.session_state:
        st.session_state.is_logged_in = False

    if 'group_profile' not in st.session_state:
        st.session_state.group_profile = {}

    if 'group_id' not in st.session_state:
        st.session_state.group_id = ""


def update_profile():
    st.session_state.group_profile = InvitationGroup.read(st.session_state.group_id)
