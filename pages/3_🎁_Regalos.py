import streamlit as st
import streamlit.components.v1 as components
from utils import init_state

from src.entities import Gift
from src.connectors.database.experiences import SheetsGiftDatabaseConnector

st.set_page_config(page_title="CBTale", layout="wide", page_icon="👩‍❤️‍👨")

init_state()

st.title("🎁 Regalos")


if not st.session_state["gift_list"]:
    with st.spinner("Cargando los regalos! Espera un momento"):
        db = SheetsGiftDatabaseConnector()
        gift_list = db.get_gift_list()
        st.session_state.gift_list = [Gift.read(gift_id) for gift_id in gift_list]

imageCarouselComponent = components.declare_component(
    "image-carousel-component",
    path="components/carousel/public"
)

imageUrls = [g.img for g in st.session_state.gift_list]
selectedImageUrl = imageCarouselComponent(imageUrls=imageUrls, height=200)

if selectedImageUrl is not None:
    st.write(selectedImageUrl)
    st.image(selectedImageUrl, width=300)
