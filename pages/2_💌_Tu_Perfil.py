import time
import streamlit as st
from utils import login, change_button_color, update_profile, init_state
from components.invitee import Profile

st.set_page_config(page_title="CBTale", layout="wide", page_icon="👩‍❤️‍👨")

init_state()

if not st.session_state.is_logged_in:
    st.title("Tu perfil")

    group_id = st.text_input("Ingresa el código que aparece en tu invitación")
    login_button = st.button("Login")
    if login_button:
        with st.spinner("Buscando tu código"):
            login(group_id)
            st.session_state.is_logged_in = True
        st.success("Usuario encontrado!")
        time.sleep(1)
        st.rerun()
else:
    st.title(f"Hola {st.session_state.group_profile.name}!")
    profile_list = [Profile(inv) for inv in st.session_state.group_profile.invitee_list if "-" not in inv.user_id]
    for invitee in profile_list:
        invitee.render()

    if st.button("Enviar Cambios"):
        with st.spinner("Actualizando cambios..."):
            for profile in profile_list:
                st.write(profile.update_dict)
                profile.invitee_object.update(profile.update_dict)
            update_profile()
            st.success("Información actualizada")
            time.sleep(1)
            st.rerun()

    change_button_color("Enviar Cambios", "white", "green")
