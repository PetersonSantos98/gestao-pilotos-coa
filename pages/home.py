import streamlit as st

def render(go):
    # CSS Mínimo: Só para não deixar os botões colados e centralizar no PC
    st.markdown("""
        <style>
        .block-container {
            max-width: 500px !important;
            padding-top: 2rem !important;
        }
        div.stButton > button {
            height: 60px; /* Altura fixa confortável */
            font-size: 16px !important;
            border-radius: 8px;
        }
        </style>
    """, unsafe_allow_html=True)

    # Vamos usar colunas simples. 
    # No celular o Streamlit empilha, mas com 60px de altura fica organizado.
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🚜 Frotas", use_container_width=True): go("frotas")
        if st.button("📡 Antenas", use_container_width=True): go("antenas")
        if st.button("🧭 NAVs", use_container_width=True): go("navs")

    with col2:
        if st.button("➕ Nova Frota", use_container_width=True): go("adicionar_frota")
        if st.button("🖥️ Monitores", use_container_width=True): go("monitores")
        if st.button("🔔 Vencimentos", use_container_width=True): go("vencimentos")
    
    st.markdown("---")
    if st.button("🔄 Atualizar Dados", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
