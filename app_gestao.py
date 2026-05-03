import streamlit as st
from pages import home, frotas, editar, vencimentos, componentes

# Configuração da página (Deve ser a primeira linha de comando Streamlit)
st.set_page_config(page_title="Gestão COA", layout="centered")

# Inicialização do estado da página
if "page" not in st.session_state:
    st.session_state.page = "home"

# Função de Navegação
def go(page):
    st.session_state.page = page
    st.rerun()

# Cabeçalho Fixo
st.markdown("## 🚜 Gestão de Pilotos - COA")

# --- ROTEADOR (ROUTER) ---
p = st.session_state.page

if p == "home":
    home.render(go)

elif p == "frotas":
    frotas.render(go)

elif p == "editar":
    editar.render(go)

elif p == "vencimentos":
    vencimentos.render(go)

# Aqui é onde os botões de componentes são processados
elif p in ["antenas", "monitores", "navs"]:
    componentes.render(go, p)
