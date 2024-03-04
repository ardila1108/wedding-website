import time
import streamlit as st
from utils import login, change_button_color, update_profile, init_state
from components import Profile

st.set_page_config(page_title="CBTale", layout="wide", page_icon="👩‍❤️‍👨")

init_state()

if not st.session_state.is_logged_in:
    st.title("💌 Tu perfil")

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
    st.write("""
    Estamos muy emocionados de que hayas llegado hasta acá 😊.
    \n
    Es tu momento de confirmar (o no) tu asistencia dando click en los nombres a continuación, donde te pediremos información relevante para el evento.
    Completa toda la info dando click en el nombre de cada uno de los invitados que aparecen en pantalla!
    \n
    Si en algún momento requieres actualizarla, sólo debes repetir el proceso.
    """)
    st.info("💡 No olvides enviar todos los cambios (Click en el botón de ¨Enviar Cambios¨ al final de la página)!")
    profile_list = [Profile(inv) for inv in st.session_state.group_profile.invitee_list if "-" not in inv.user_id]
    for invitee in profile_list:
        invitee.render()

    if st.button("Enviar Cambios"):
        with st.spinner("Actualizando cambios..."):
            for profile in profile_list:
                profile.invitee_object.update(profile.update_dict)
            update_profile()
            st.success("Información actualizada")
            time.sleep(1)
            st.rerun()

    change_button_color("Enviar Cambios", "white", "green")

