import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from utils.config import init_state

st.set_page_config(page_title="CBTale", layout="wide", page_icon="👩‍❤️‍👨")

init_state()

params = st.query_params

if "group_id" in params and not st.session_state.is_logged_in:
    st.session_state.is_logged_in = True
    st.session_state.name = "test"
    switch_page("tu perfil")

st.title("Prepárate para el gran dia! :heart:")
st.write(
    """
    Si estás leyendo esto, significa que eres una de las personas más importantes de
    nuestras vidas y queremos que nos acompañes en el día más especial de todos!
    """
)
