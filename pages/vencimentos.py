import streamlit as st
from services import get_licencas
from utils import formatar_data

def render(go):
    if st.button("⬅️ Voltar"):
        go("home")

    with st.spinner("Carregando..."):
        data = get_licencas()

    for item in data:
        data_fmt, status = formatar_data(item.get("data_vencimento"))

        st.markdown(f"""
        **{item.get('licenca')}**  
        <span class="{status}">{data_fmt}</span>
        """, unsafe_allow_html=True)
