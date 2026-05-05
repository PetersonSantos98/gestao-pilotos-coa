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
                # Tenta converter a string do banco para objeto date
                # Ajustado para garantir que o Streamlit receba o tipo correto
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
        submetido = st.form_submit_button("Salvar Alterações")

        if submetido:
            if not serie:
                st.error("O número da licença é obrigatório.")
            else:
                # Salvamos a data como string para o banco de dados
                dados = {"licenca": serie, "data_vencimento": str(vencimento)}
                
                if modo_edicao:
                    # Atualização no Supabase/Banco usando o ID existente
                    res = services.get_client().table("Licencas_Validades").update(dados).eq("id", lic_data['id']).execute()
                    if res: st.success("Licença atualizada!")
                else:
                    # Cadastro de nova licença
                    if services.add_registro("Licencas_Validades", dados):
                        st.success("Licença cadastrada!")

                # Limpeza de estado e retorno
                st.session_state.licenca_edit = None
                st.cache_data.clear()
                go("vencimentos")
