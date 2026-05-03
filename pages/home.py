import streamlit as st

def render(go):
    # CSS para forçar 2 colunas no celular e estilizar os botões
    st.markdown("""
        <style>
        /* Força as colunas a ficarem lado a lado no celular */
        [data-testid="column"] {
            width: calc(50% - 1rem) !important;
            flex: 1 1 calc(50% - 1rem) !important;
            min-width: calc(50% - 1rem) !important;
        }
        
        /* Centraliza o app e limita a largura no PC */
        .block-container {
            max-width: 450px !important;
            padding-top: 2rem !important;
        }

        /* Estilo dos Botões (Cards) */
        div.stButton > button {
            height: 90px;
            border-radius: 15px;
            border: 1px solid #ddd;
            background-color: #ffffff;
            color: #333;
            font-weight: bold;
            font-size: 15px !important;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }
        
        /* Efeito ao clicar/passar o mouse */
        div.stButton > button:active, div.stButton > button:hover {
            border-color: #4CAF50 !important;
            color: #4CAF50 !important;
            background-color: #f9fff9 !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # O layout agora respeitará o 50/50 em qualquer tela
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🚜\nFrotas", use_container_width=True): go("frotas")
        if st.button("📡\nAntenas", use_container_width=True): go("antenas")
        if st.button("🧭\nNAVs", use_container_width=True): go("navs")

    with col2:
        if st.button("➕\nNova Frota", use_container_width=True): go("adicionar_frota")
        if st.button("🖥️\nMonitores", use_container_width=True): go("monitores")
        if st.button("🔔\nVencimentos", use_container_width=True): go("vencimentos")
    
    st.write("---")
    if st.button("🔄 Atualizar Dados", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
