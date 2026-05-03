import streamlit as st

def render(go):
    # 1. EMPURRANDO O CONTEÚDO PARA BAIXO (O "Pulo do Gato")
    # Isso garante que o título comece abaixo da área de corte do sistema
    st.write("#") 
    st.write("") 

    # 2. CSS PARA CORRIGIR O ESTILO
    st.markdown("""
    <style>
    /* Remove o espaço fixo que o Streamlit reserva no topo */
    .stAppHeader {
        display: none;
    }
    
    .block-container {
        max-width: 500px !important;
        padding-top: 2rem !important; /* Aumentamos aqui para garantir */
        margin: auto;
    }

    /* BOTÕES: Fonte menor e sem quebra */
    div.stButton > button {
        height: 55px;
        border-radius: 10px;
        font-size: 13px !important; 
        font-weight: 600;
        white-space: nowrap !important;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    /* TÍTULOS DE SEÇÃO */
    .section-title {
        font-size: 12px;
        font-weight: 700;
        color: #888;
        text-transform: uppercase;
        margin: 15px 0 5px 5px;
    }
    </style>
""", unsafe_allow_html=True)

    # ================================
    # 🚜 OPERAÇÃO
    # ================================
    st.markdown('<div class="section-title">Operação</div>', unsafe_allow_html=True)

    if st.button("🚜 Frotas", use_container_width=True):
        go("frotas")

    if st.button("➕ Nova Frota", use_container_width=True):
        go("adicionar_frota")

    # ================================
    # 📡 DISPOSITIVOS
    # ================================
    st.markdown('<div class="section-title">Dispositivos</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("📡 Antenas", use_container_width=True):
            go("antenas")

        if st.button("🧭 NAVs", use_container_width=True):
            go("navs")

    with col2:
        if st.button("🖥️ Monitores", use_container_width=True):
            go("monitores")

        if st.button("🔔 Vencimentos", use_container_width=True):
            go("vencimentos")

    # ================================
    # ⚙️ SISTEMA
    # ================================
    st.markdown('<div class="section-title">Sistema</div>', unsafe_allow_html=True)

    if st.button("🔄 Atualizar Dados", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
