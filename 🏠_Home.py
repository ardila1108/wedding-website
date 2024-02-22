import streamlit as st
from utils import init_state, login

st.set_page_config(page_title="CBTale", layout="wide", page_icon="👩‍❤️‍👨")

init_state()

params = st.query_params

if "group_id" in params and not st.session_state.is_logged_in:
    login(params["group_id"])

st.title("Prepárate para el gran día! :heart:")
st.write(
    """
    Si estás leyendo esto, significa que eres una de las personas más importantes de
    nuestras vidas y queremos que nos acompañes en el día más especial de todos!
    """
)
