import streamlit as st
from services import add_registro, get_client

def render(go):
    lic_data = st.session_state.get("licenca_edit", None)
    modo_edicao = lic_data is not None

    if st.button("⬅️ Voltar"): 
        st.session_state.licenca_edit = None
        go("vencimentos")

    st.subheader("📝 " + ("Editar Licença" if modo_edicao else "Cadastrar Licença"))

    with st.form("form_licenca"):
        # Se sua tabela no banco usar 'licenca' para o número de série:
        serie = st.text_input("Número de Série (Licença)", value=str(lic_data.get('licenca', '')) if modo_edicao else "")
        vencimento = st.date_input("Nova Data de Vencimento", 
                                   value=st.date_today() if not modo_edicao else None) # Ajuste o valor inicial conforme necessário

        if st.form_submit_button("Salvar no Banco de Dados"):
            if not serie:
                st.error("O número da licença é obrigatório.")
            else:
                dados = {
                    "licenca": serie,
                    "data_vencimento": str(vencimento)
                }
                
                if modo_edicao:
                    supabase = get_client()
                    # Atualiza pelo ID único da linha
                    res = supabase.table("Licencas_Validades").update(dados).eq("id", lic_data['id']).execute()
                    if res: st.success("Licença atualizada!")
                else:
                    if add_registro("Licencas_Validades", dados):
                        st.success("Licença cadastrada!")

                st.session_state.licenca_edit = None
                st.cache_data.clear()
                st.rerun()
