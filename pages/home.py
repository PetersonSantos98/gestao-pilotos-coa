import streamlit as st

def render(go):
    col1, col2 = st.columns(2)

    with col1:
        if st.button("🔔 Vencimentos"):
            go("vencimentos")
        if st.button("🚜 Frotas"):
            go("frotas")

    with col2:
        if st.button("🔄 Atualizar"):
            st.cache_data.clear()
