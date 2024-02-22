import streamlit as st
from src.entities import InvitationGroup


def login(group_id: str):
    st.session_state.group_id = group_id
    st.session_state.group_profile = InvitationGroup.read(group_id)
    st.session_state.is_logged_in = True
