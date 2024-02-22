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
