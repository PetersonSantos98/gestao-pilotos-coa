import streamlit as st

def render(go):
    st.write("### Painel de Controle")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🚜 Frotas", use_container_width=True): go("frotas")
        if st.button("➕ Nova Frota", use_container_width=True): go("adicionar_frota")
        if st.button("🧭 NAVs", use_container_width=True): go("navs")

    with col2:
        if st.button("🔔 Vencimentos", use_container_width=True): go("vencimentos")
        if st.button("📡 Antenas", use_container_width=True): go("antenas")
        if st.button("🖥️ Monitores", use_container_width=True): go("monitores")
        
    if st.button("🔄 Atualizar Dados", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
