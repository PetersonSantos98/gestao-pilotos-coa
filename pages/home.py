import streamlit as st

def render(go):
    # ================================
    # 🎨 CSS PROFISSIONAL
    # ================================
    st.markdown("""
    <style>
    .block-container {
        max-width: 700px;
        padding-top: 1rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }

    /* REMOVE qualquer corte de texto */
    * {
        word-wrap: break-word !important;
        white-space: normal !important;
    }

    /* BOTÕES */
    div.stButton > button {
        height: 65px;
        border-radius: 12px;
        font-size: 15px;
        font-weight: 600;
        white-space: normal !important;
        line-height: 1.2;
    }

    /* SECTION */
    .section-title {
        font-size: 14px;
        font-weight: 600;
        color: #6c757d;
        margin: 15px 0 8px 5px;
    }
    </style>
""", unsafe_allow_html=True)
    # ================================
    # 🧠 HEADER
    # ================================
    st.markdown("""
        <div class="header">
            <div class="header-title">🚜 Gestão de Pilotos</div>
            <div class="header-sub">Controle de frotas e dispositivos</div>
        </div>
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
