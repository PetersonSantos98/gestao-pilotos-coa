import streamlit as st
import pandas as pd
from services import get_equipamentos

def render(go):
    if st.button("⬅️ Voltar"):
        go("home")

    busca = st.text_input("Pesquisar")

    with st.spinner("Carregando..."):
        data = get_equipamentos()

    if not data:
        st.warning("Sem dados")
        return

    df = pd.DataFrame(data)

    if busca:
        df = df[df["codigo_do_equipamento"].astype(str).str.contains(busca)]

    for _, row in df.iterrows():
        col1, col2 = st.columns([4,1])

        with col1:
            st.write(f"**{row['codigo_do_equipamento']}** - {row['nome']}")

        with col2:
            if st.button("Editar", key=row["id"]):
                st.session_state.edit_id = row["id"]
                go("editar")
