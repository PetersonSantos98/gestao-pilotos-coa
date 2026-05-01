import streamlit as st
from pages import home, frotas, editar, vencimentos

st.set_page_config(page_title="Gestão COA", layout="centered")

if "page" not in st.session_state:
    st.session_state.page = "home"

def go(page):
    st.session_state.page = page
    st.rerun()

# HEADER
st.markdown("## 🚜 Gestão de Pilotos")

# ROUTER
if st.session_state.page == "home":
    home.render(go)

elif st.session_state.page == "frotas":
    frotas.render(go)

elif st.session_state.page == "editar":
    editar.render(go)

elif st.session_state.page == "vencimentos":
    vencimentos.render(go)
