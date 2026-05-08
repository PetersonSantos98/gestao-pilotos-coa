import streamlit as st
import services

def render(go):
    # Recupera o item e o tipo definidos no botão 'Editar' das outras páginas
    item = st.session_state.get("item_para_editar")
    tipo = st.session_state.get("tipo_edicao")

    if not item or not tipo:
        st.error("Nenhum item selecionado para edição.")
        if st.button("⬅️ Voltar"): go("home")
        return

    # Título dinâmico
    st.subheader(f"📝 Editando {tipo.title()}: {item.get('antena_serie') or item.get('monitor_serie') or item.get('nav_serie') or item.get('codigo_do_equipamento') or ''}")

    with st.form("form_edicao_geral"):
        novos_dados = {}
        nome_tabela = ""

        # --- FORMULÁRIO PARA ANTENAS ---
        if tipo == "antenas":
            nome_tabela = "Antenas"
            col_id = "antena_serie" # Usamos a série como referência se não houver ID numérico
            serie = st.text_input("Série da Antena", value=item.get("antena_serie", ""))
            modelo = st.text_input("Modelo", value=item.get("modelo_antena", ""))
            marca = st.text_input("Marca", value=item.get("marca_sinal", ""))
            novos_dados = {"antena_serie": serie, "modelo_antena": modelo, "marca_sinal": marca}

        # --- FORMULÁRIO PARA MONITORES ---
        elif tipo == "monitores":
            nome_tabela = "Monitores"
            col_id = "monitor_serie"
            serie = st.text_input("Série do Monitor", value=item.get("monitor_serie", ""))
            modelo = st.text_input("Modelo", value=item.get("modelo_monitor", ""))
            novos_dados = {"monitor_serie": serie, "modelo_monitor": modelo}

        # --- FORMULÁRIO PARA NAVS ---
        elif tipo == "navs":
            nome_tabela = "Navs"
            col_id = "nav_serie"
            serie = st.text_input("Série do Nav", value=item.get("nav_serie", ""))
            novos_dados = {"nav_serie": serie}

        # --- FORMULÁRIO PARA LICENÇAS ---
        elif tipo == "licencas":
            nome_tabela = "Licencas_Validades"
            col_id = "id"
            serie = st.text_input("Série do Equipamento", value=item.get("serie_equipamento", ""))
            data = st.text_input("Data de Vencimento", value=item.get("data_vencimento", ""))
            obs = st.text_area("Observações", value=item.get("observacoes", ""))
            novos_dados = {"serie_equipamento": serie, "data_vencimento": data, "observacoes": obs}

        # Botões de ação
        col_salvar, col_cancelar = st.columns(2)
        
        if col_salvar.form_submit_button("💾 Salvar Alterações"):
            # Usamos uma função genérica de update no services
            id_valor = item.get("id") # Tenta pegar o ID único do banco
            
            if services.update_registro_generico(nome_tabela, id_valor, novos_dados):
                st.success("✅ Atualizado com sucesso!")
                st.rerun()

        if col_cancelar.form_submit_button("❌ Cancelar"):
            go("home")
