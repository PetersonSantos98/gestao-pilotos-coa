import streamlit as st

def render(go):
    # ================================
    # 🎨 CSS PARA CENTRALIZAR E AJUSTAR
    # ================================
    st.markdown("""
    <style>
    /* Remove o espaço excessivo no topo */
    .block-container {
        max-width: 500px !important;
        padding-top: 2rem !important;
        margin: auto;
    }

    /* Estilização do Título Centralizado */
    .main-title {
        font-size: 24px !important;
        font-weight: 700;
        text-align: center;
        color: #FFFFFF;
        margin-bottom: 20px;
        line-height: 1.2;
    }

    /* BOTÕES: Fonte ajustada e sem quebra */
    div.stButton > button {
        height: 55px;
        border-radius: 12px;
        font-size: 14px !important;
        font-weight: 600;
        white-space: nowrap !important;
    }

    /* SECTION TITLE */
    .section-title {
        font-size: 12px;
        font-weight: 700;
        color: #888;
        text-transform: uppercase;
        margin: 15px 0 5px 5px;
        text-align: left;
    }
    </style>
""", unsafe_allow_html=True)

    # Título Centralizado e com fonte menor que o padrão H1
    st.markdown('<div class="main-title">Gestão de Componentes</div>', unsafe_allow_html=True)

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
