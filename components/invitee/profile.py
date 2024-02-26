import streamlit as st
from src.entities import InviteeProfile


class Profile:
    def __init__(
            self,
            invitee_object: InviteeProfile
    ):
        self.invitee_object = invitee_object
        self.update_dict = {}

    def render(self):
        with st.expander(r"$\textsf{\Large %s}$" % self.invitee_object.name):
            self.update_dict["attending"] = st.checkbox(
                "Confirmo mi asistencia",
                self.invitee_object.attending,
                key=f"attending_{self.invitee_object.user_id}"
            )
            if self.update_dict["attending"]:
                self.update_dict["restrictions"] = st.text_area(
                    "Restricciones alimenticias",
                    self.invitee_object.restrictions,
                    key=f"rest_{self.invitee_object.user_id}"
                )
                if self.invitee_object.can_bring_plus_one:
                    plus_one = st.checkbox(
                        "Voy con una persona adicional",
                        bool(self.invitee_object.plus_one),
                        key=f"plus_one_{self.invitee_object.user_id}"
                    )
                    if plus_one:
                        self._render_plus_one_info(self.invitee_object.plus_one)

        emoji_col, plus_one_col = st.columns([0.03, 0.97])
        with emoji_col:
            st.markdown("<h3 style='text-align: center; color: grey;'>✅</h3>", unsafe_allow_html=True)
        with plus_one_col:
            with st.expander(r"$\textsf{\Large %s}$" % ("" + self.invitee_object.plus_one.name)):
                self._render_plus_one_profile(self.invitee_object.plus_one)

    def _render_plus_one_info(self, plus_one_object):
        self.update_dict["plus_one"] = {}
        _, col = st.columns([0.05, 0.95])
        with col:
            self.update_dict["plus_one"]["name"] = st.text_input(
                "Nombre",
                plus_one_object.name
            )
            self.update_dict["plus_one"]["restrictions"] = st.text_area(
                "Restricciones alimenticias",
                plus_one_object.restrictions
            )
            self.update_dict["plus_one"]["attending"] = True

    @staticmethod
    def _render_plus_one_profile(plus_one_object):
        st.text_area(
            "Restricciones alimenticias",
            plus_one_object.restrictions,
            disabled=True,
            key="Mock_" + plus_one_object.user_id
        )
