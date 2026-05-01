import streamlit as st
from services import get_equipamentos, update_equipamento

def render(go):
    if st.button("⬅️ Voltar"):
        go("frotas")

    id = st.session_state.get("edit_id")

    data = get_equipamentos()
    item = next((x for x in data if x["id"] == id), None)

    if not item:
        st.error("Item não encontrado")
        return

    with st.form("form"):
        nome = st.text_input("Nome", value=item["nome"])
        antena = st.text_input("Antena", value=item["antena"])
        monitor = st.text_input("Monitor", value=item["monitor"])

        if st.form_submit_button("Salvar"):
            with st.spinner("Salvando..."):
                update_equipamento(id, {
                    "nome": nome,
                    "antena": antena,
                    "monitor": monitor
                })

            st.success("Salvo!")
            go("frotas")
