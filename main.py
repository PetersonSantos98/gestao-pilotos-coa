import streamlit as st
from pages import home, frotas, editar, vencimentos, componentes

st.set_page_config(page_title="Gestão de Componentes", layout="centered")

if "page" not in st.session_state:
    st.session_state.page = "home"

def go(page):
    st.session_state.page = page
    st.rerun()

st.markdown("## 🚜Gestão de Componentes")

# ROTEAMENTO
p = st.session_state.page
if p == "home": home.render(go)
elif p == "frotas": frotas.render(go)
elif p == "editar": editar.render(go)
elif p == "vencimentos": vencimentos.render(go)
# Para as páginas de Antenas, Monitores e NAVs, criamos um renderizador genérico
elif p in ["antenas", "monitores", "navs"]: 
    import pages.componentes as componentes
    componentes.render(go, p)
