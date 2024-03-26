import streamlit as st
from src.entities import InvitationGroup
from src.entities import Gift


def init_state():
    if 'is_logged_in' not in st.session_state:
        st.session_state.is_logged_in = False

    if 'group_profile' not in st.session_state:
        st.session_state.group_profile = {}

    if 'group_id' not in st.session_state:
        st.session_state.group_id = ""

    if 'gift_list' not in st.session_state:
        st.session_state.gift_list = []


def update_profile():
    st.session_state.group_profile = InvitationGroup.read(st.session_state.group_id)
