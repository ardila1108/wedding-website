import time
import streamlit as st

if not st.session_state.is_logged_in:
    st.title("Tu perfil")

    user_code = st.text_input("Ingresa el código que aparece en tu invitación")
    login_button = st.button("Login")
    if login_button:
        st.session_state.name = "charlie"
        st.session_state.is_logged_in = True
        st.success("Usuario encontrado!")
        time.sleep(2)
        st.experimental_rerun()
else:
    st.title(f"Hola {st.session_state.name.title()}!")