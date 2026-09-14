import streamlit as st
import services
import datetime
import pandas as pd

def render(go):
    lic_data = st.session_state.get("licenca_edit", None)
    modo_edicao = lic_data is not None

    if st.button("⬅️ Voltar"): 
        st.session_state.licenca_edit = None
        go("vencimentos")

    st.subheader("📝 " + ("Editar Licença" if modo_edicao else "Cadastrar Licença"))

    # Início do formulário
    with st.form("form_licenca"):
        val_licenca = lic_data.get('licenca') if (modo_edicao and lic_data.get('licenca')) else ""
        serie = st.text_input("Número de Série (Licença)", value=str(val_licenca))
        
        # Lógica para definir a data inicial do seletor
        if modo_edicao and lic_data.get('data_vencimento'):
            try:
                # pd.to_datetime trata tanto YYYY-MM-DD quanto formatos ISO com timestamp
                dt_parsed = pd.to_datetime(lic_data['data_vencimento']).date()
                data_sugerida = dt_parsed
            except Exception:
                data_sugerida = datetime.date.today()
        else:
            data_sugerida = datetime.date.today()

        # Widget de data com o valor recuperado e formato BR
        vencimento = st.date_input("Data de Vencimento", value=data_sugerida, format="DD/MM/YYYY")

        submetido = st.form_submit_button("💾 Salvar Alterações")

        if submetido:
            if not serie.strip():
                st.error("O número da licença é obrigatório.")
            else:
                dados = {"licenca": serie.strip(), "data_vencimento": str(vencimento)}
                
                if modo_edicao:
                    id_registro = lic_data.get('id') if lic_data.get('id') is not None else lic_data.get('ID')
                    if services.update_registro_generico("Licencas_Validades", id_registro, dados):
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
        with st.expander("⚠️ Zona de Perigo - Excluir Registro"):
            st.warning("Tem certeza de que deseja deletar esta licença? Essa ação não pode ser desfeita.")
            
            id_para_excluir = lic_data.get('id') if lic_data.get('id') is not None else lic_data.get('ID')
            
            if st.button("🗑️ Confirmar Exclusão Definitiva", type="primary", use_container_width=True):
                if services.delete_registro("Licencas_Validades", id_para_excluir):
                    st.success("Licença excluída com sucesso!")
                    st.session_state.licenca_edit = None
                    st.cache_data.clear()
                    go("vencimentos")
