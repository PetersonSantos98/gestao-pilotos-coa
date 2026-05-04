import streamlit as st
from services import add_registro, get_client # get_client para o update específico

def render(go):
    # Recupera se estamos editando ou criando
    lic_data = st.session_state.get("licenca_edit", None)
    modo_edicao = lic_data is not None

    if st.button("⬅️ Voltar"): 
        st.session_state.licenca_edit = None
        go("vencimentos")

    st.subheader("📝 " + ("Editar Licença" if modo_edicao else "Nova Licença"))

    with st.form("form_licenca"):
        serie = st.text_input("Número de Série", value=lic_data['serie'] if modo_edicao else "")
        vencimento = st.date_input("Data de Vencimento", 
                                   value=lic_data['data_vencimento'] if modo_edicao else None)
        local = st.text_input("Localização (Frota ou Estoque)", 
                              value=lic_data['localizacao'] if modo_edicao else "")

        if st.form_submit_button("Confirmar Salvamento"):
            dados = {
                "serie": serie,
                "data_vencimento": str(vencimento),
                "localizacao": local
            }
            
            if modo_edicao:
                # Lógica de Update
                supabase = get_client()
                res = supabase.table("Licencas_Validades").update(dados).eq("id", lic_data['id']).execute()
                if res: st.success("Licença atualizada!")
            else:
                # Lógica de Insert
                if add_registro("Licencas_Validades", dados):
                    st.success("Nova licença cadastrada!")
            
            st.session_state.licenca_edit = None
            st.cache_data.clear() # Limpa cache para atualizar a lista
