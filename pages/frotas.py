import streamlit as st
import pandas as pd
from services import get_equipamentos

def render(go):
    if st.button("⬅️ Voltar"): go("home")
    
    busca = st.text_input("🔍 Pesquisar Equipamento", placeholder="Digite o código ou nome...")
    data = get_equipamentos()

    if not data:
        st.warning("Nenhum equipamento cadastrado.")
        return

    df = pd.DataFrame(data)
    
    if busca:
        # Busca insensível a maiúsculas/minúsculas e segura contra nulos
        mask = (
            df["codigo_do_equipamento"].astype(str).str.contains(busca, case=False, na=False) |
            df["nome"].astype(str).str.contains(busca, case=False, na=False)
        )
        df = df[mask]

    for _, row in df.iterrows():
        with st.container(border=True):
            c1, c2 = st.columns([4, 1])
            
            # Trata exibições para não mostrar 'None' solto
            ant = row.get('antena') or "Não vinculado"
            mon = row.get('monitor') or "Não vinculado"
            nav = row.get('nav') or "Não vinculado"

            with c1:
                st.markdown(f"**{row['codigo_do_equipamento']}** - {row.get('nome', '')}")
                st.caption(f"📡 **Antena:** {ant} | 🖥️ **Monitor:** {mon} | ⚙️ **NAV:** {nav}")
                
            with c2:
                if st.button("Editar", key=f"edit_frota_{row['id']}"):
                    st.session_state.tipo_edicao = "frotas"
                    st.session_state.edit_id = row['id']
                    st.session_state.item_para_editar = None  # Limpa resquícios de componentes
                    go("editar")
