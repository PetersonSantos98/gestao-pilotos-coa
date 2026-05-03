import streamlit as st

def render(go):
    # CSS para deixar os botões com cara de "App" e remover espaços extras
    st.markdown("""
        <style>
        div.stButton > button {
            height: 4em;
            border-radius: 10px;
            font-weight: bold;
            font-size: 16px !important;
            margin-bottom: -10px;
        }
        /* Remove o espaço excessivo no topo no celular */
        .block-container {
            padding-top: 1rem !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # Grid de botões 2 por linha para economizar espaço vertical
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🚜 Frotas", use_container_width=True): go("frotas")
        if st.button("📡 Antenas", use_container_width=True): go("antenas")
        if st.button("🧭 NAVs", use_container_width=True): go("navs")

    with col2:
        if st.button("➕ Nova Frota", use_container_width=True): go("adicionar_frota")
        if st.button("🖥️ Monitores", use_container_width=True): go("monitores")
        if st.button("🔔 Vencimentos", use_container_width=True): go("vencimentos")
    
    st.divider() # Linha fina separadora
    
    if st.button("🔄 Atualizar Dados", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
