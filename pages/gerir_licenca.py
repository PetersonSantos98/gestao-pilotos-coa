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
        
        # Correção da data: usamos datetime.date.today()
        data_sugerida = datetime.date.today()
        vencimento = st.date_input("Data de Vencimento", value=data_sugerida)

        # O botão de submit DEVE estar dentro do bloco 'with st.form'
        submetido = st.form_submit_button("Salvar Alterações")

        if submetido:
            if not serie:
                st.error("O número da licença é obrigatório.")
            else:
                dados = {"licenca": serie, "data_vencimento": str(vencimento)}
                
                if modo_edicao:
                    # Chamada corrigida usando o padrão 'services.funcao'
                    res = services.get_client().table("Licencas_Validades").update(dados).eq("id", lic_data['id']).execute()
                    if res: st.success("Licença atualizada!")
                else:
                    if services.add_registro("Licencas_Validades", dados):
                        st.success("Licença cadastrada!")

                st.session_state.licenca_edit = None
                st.cache_data.clear()
                # Não usamos rerun dentro do form submetido diretamente para evitar loops, 
                # mas como vamos mudar de página, o go() resolve.
                go("vencimentos")
