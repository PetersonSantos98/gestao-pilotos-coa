import streamlit as st
import pandas as pd
from services import get_equipamentos

def render(go):
    if st.button("⬅️ Voltar"): go("home")
    
    busca = st.text_input("🔍 Pesquisar Equipamento", placeholder="Digite o código...")
    data = get_equipamentos()

    if not data:
        st.warning("Nenhum equipamento cadastrado.")
        return

    df = pd.DataFrame(data)
    if busca:
        df = df[df["codigo_do_equipamento"].astype(str).str.contains(busca)]

    for _, row in df.iterrows():
        with st.container(border=True):
            c1, c2 = st.columns([4, 1])
            with c1:
                st.markdown(f"**{row['codigo_do_equipamento']}** - {row['nome']}")
                st.caption(f"Antena: {row['antena']} | Monitor: {row['monitor']} | NAV: {row['nav']}")
            with c2:
                # CORREÇÃO: Define tipo_edicao para frotas e limpa item_para_editar
                if st.button("Editar", key=f"edit_frota_{row['id']}"):
                    st.session_state.tipo_edicao = "frotas"
                    st.session_state.edit_id = row['id']
                    st.session_state.item_para_editar = None # Limpa resquícios de componentes
                    go("editar")
