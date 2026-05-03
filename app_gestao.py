import streamlit as st
from pages import home, frotas, editar, vencimentos, componentes, adicionar_frota

st.set_page_config(page_title="Gestão de Componentes", layout="centered")

if "page" not in st.session_state:
    st.session_state.page = "home"

def go(page):
    st.session_state.page = page
    st.rerun()

st.markdown("## ")

p = st.session_state.page

if p == "home":
    home.render(go)
elif p == "frotas":
    frotas.render(go)
elif p == "editar":
    editar.render(go)
elif p == "vencimentos":
    vencimentos.render(go)
elif p == "adicionar_frota":
    adicionar_frota.render(go)
elif p in ["antenas", "monitores", "navs"]:
    componentes.render(go, p)
