import streamlit as st
import services
import datetime

def render(go):
    lic_data = st.session_state.get("licenca_edit", None)
    modo_edicao = lic_data is not None

    if st.button("⬅️ Voltar"): 
        st.session_state.licenca_edit = None
        go("vencimentos")

    st.subheader("📝 " + ("Editar Licença" if modo_edicao else "Cadastrar Licença"))

    # Início do formulário
    with st.form("form_licenca"):
        serie = st.text_input("Número de Série (Licença)", value=str(lic_data.get('licenca', '')) if modo_edicao else "")
        
        # Lógica para definir a data inicial do seletor
        if modo_edicao and lic_data.get('data_vencimento'):
            try:
                if isinstance(lic_data['data_vencimento'], str):
                    data_sugerida = datetime.datetime.strptime(lic_data['data_vencimento'], '%Y-%m-%d').date()
                else:
                    data_sugerida = lic_data['data_vencimento']
            except Exception:
                data_sugerida = datetime.date.today()
        else:
            data_sugerida = datetime.date.today()

        # Widget de data com o valor recuperado e formato BR
        vencimento = st.date_input("Data de Vencimento", value=data_sugerida, format="DD/MM/YYYY")

        # O botão de submit DEVE estar dentro do bloco 'with st.form'
        submetido = st.form_submit_button("💾 Salvar Alterações")

        if submetido:
            if not serie:
                st.error("O número da licença é obrigatório.")
            else:
                dados = {"licenca": serie, "data_vencimento": str(vencimento)}
                
                if modo_edicao:
                    if services.update_registro_generico("Licencas_Validades", lic_data['id'], dados):
                        st.success("Licença atualizada!")
                else:
                    if services.add_registro("Licencas_Validades", dados):
                        st.success("Licença cadastrada!")

                st.session_state.licenca_edit = None
                st.cache_data.clear()
                go("vencimentos")

    # --- BOTÃO DE EXCLUIR (Apenas visível se estiver editando um item existente) ---
    if modo_edicao:
        st.write("---")
        # Criamos um expander ou caixinha de aviso para evitar exclusão acidental
        with st.expander("⚠️ Zona de Perigo - Excluir Registro"):
            st.warning("Tem certeza de que deseja deletar esta licença? Essa ação não pode ser desfeita.")
            if st.button("🗑️ Confirmar Exclusão Definitiva", type="primary", use_container_width=True):
                if services.delete_registro("Licencas_Validades", lic_data['id']):
                    st.success("Licença excluída com sucesso!")
                    st.session_state.licenca_edit = None
                    st.cache_data.clear()
                    go("vencimentos")
