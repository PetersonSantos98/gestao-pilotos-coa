import streamlit as st

def render(go):
    # ================================
    # 🎨 CSS AJUSTADO (RESOLVE CORTE E CENTRALIZA)
    # ================================
    st.markdown("""
    <style>
    /* Resolve o corte no topo e centraliza o conteúdo */
    .block-container {
        max-width: 500px !important;
        padding-top: 0rem !important; /* Remove o espaço que corta o título */
        margin: auto;
    }

    /* Tira o espaço extra entre o topo da página e o título */
    #root > div:nth-child(1) > div > div > div > div > section > div {
        padding-top: 1rem !important;
    }

    /* BOTÕES: Ajuste de fonte para não quebrar texto */
    div.stButton > button {
        height: 55px;
        border-radius: 10px;
        font-size: 14px !important; /* Letra levemente menor para caber tudo */
        font-weight: 600;
        display: flex;
        justify-content: center;
        align-items: center;
        white-space: nowrap !important; /* Impede a quebra de linha no texto */
    }

    /* SECTION TITLE */
    .section-title {
        font-size: 13px;
        font-weight: 700;
        color: #888;
        text-transform: uppercase;
        margin: 20px 0 5px 5px;
        letter-spacing: 1px;
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
