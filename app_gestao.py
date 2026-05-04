import streamlit as st
from pages import home, frotas, editar, vencimentos, componentes, adicionar_frota, gerir_licenca
import services  # Importação robusta para evitar erro de cache

# Configuração de Layout
st.set_page_config(page_title="Gestão de Componentes", layout="centered")

# Inicialização de variáveis de estado
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if "page" not in st.session_state:
    st.session_state.page = "home"

def go(page):
    st.session_state.page = page
    st.rerun()

# --- TELA DE LOGIN ---
if not st.session_state.autenticado:
    st.markdown("""
        <style>
        .block-container { max-width: 400px !important; padding-top: 5rem !important; margin: auto; }
        div.stButton > button { width: 100%; border-radius: 12px; height: 3.5em; font-weight: bold; background-color: #1E1E1E; color: white; }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown("<h2 style='text-align: center;'>🔐 Acesso Restrito</h2>", unsafe_allow_html=True)
    
    with st.container(border=True):
        user = st.text_input("Usuário")
        password = st.text_input("Senha", type="password")
        
        if st.button("Entrar"):
            # Chamada usando o prefixo do módulo
            if services.verificar_login(user, password):
                st.session_state.autenticado = True
                st.rerun()
            else:
                st.error("Credenciais inválidas. Tente novamente.")
    st.stop()  # Impede que o restante do código seja lido sem login

# --- ÁREA AUTENTICADA ---

# Barra lateral para Logoff
if st.sidebar.button("Sair / Logoff"):
    st.session_state.autenticado = False
    st.rerun()

st.markdown("## ")

p = st.session_state.page

# Roteador de Páginas
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
elif p == "gerir_licenca":
    gerir_licenca.render(go)
elif p in ["antenas", "monitores", "navs"]:
    componentes.render(go, p)
