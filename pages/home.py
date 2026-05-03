import streamlit as st

def render(go):
    # ================================
    # 🎨 CSS PROFISSIONAL
    # ================================
    st.markdown("""
        <style>
        .block-container {
            max-width: 620px;
            padding-top: 1.5rem;
        }

        /* HEADER */
        .header {
            text-align: center;
            margin-bottom: 20px;
        }

        .header-title {
            font-size: 22px;
            font-weight: 700;
        }

        .header-sub {
            font-size: 13px;
            color: #6c757d;
        }

        /* SECTION */
        .section-title {
            font-size: 14px;
            font-weight: 600;
            color: #6c757d;
            margin: 15px 0 5px 5px;
        }

        /* CARD */
        .card {
            background: white;
            padding: 16px;
            border-radius: 14px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
            margin-bottom: 10px;
        }

        /* BOTÕES */
        div.stButton > button {
            height: 65px;
            border-radius: 12px;
            font-size: 16px;
            font-weight: 600;
        }

        /* BOTÃO PRINCIPAL */
        .primary button {
            background-color: #2e7d32 !important;
            color: white !important;
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
