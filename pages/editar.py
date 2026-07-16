import streamlit as st
import services

def render(go):
    item = st.session_state.get("item_para_editar")
    tipo = st.session_state.get("tipo_edicao")
    id_edit = st.session_state.get("edit_id")

    if st.button("⬅️ Voltar"): 
        go("frotas" if tipo == "frotas" else "home")

    if not tipo:
        st.error("Erro: Tipo de edição não definido.")
        return

    # --- BLOCO 1: EDIÇÃO DE FROTAS (VÍNCULOS) ---
    if tipo == "frotas":
        data = services.get_equipamentos()
        item_frota = next((x for x in data if x["id"] == id_edit), None)

        if not item_frota:
            st.error("Equipamento não localizado.")
            return

        st.subheader(f"Edição de Vínculos - Frota: {item_frota['codigo_do_equipamento']}")

        antenas_opt = services.get_itens_disponiveis("Antenas", "antena_serie", item_frota["antena"])
        monitores_opt = services.get_itens_disponiveis("Monitores", "monitor_serie", item_frota["monitor"])
        navs_opt = services.get_itens_disponiveis("Navs", "nav_serie", item_frota["nav"])

        VAZIO = {"antena_serie": None, "modelo_antena": None, "monitor_serie": None, "modelo_monitor": None, "nav_serie": None}

        with st.form("form_edit_frota"):
            nome = st.text_input("Nome do Equipamento", value=item_frota["nome"])
            
            # Antena
            l_antenas = [VAZIO] + antenas_opt
            idx_ant = next((i for i, x in enumerate(l_antenas) if x["antena_serie"] == item_frota["antena"]), 0)
            antena = st.selectbox("Antena", options=l_antenas, index=idx_ant,
                                  format_func=lambda x: f"{x['antena_serie']} ({x['modelo_antena']})" if x["antena_serie"] else "❌ Remover")

            # Monitor
            l_monitores = [VAZIO] + monitores_opt
            idx_mon = next((i for i, x in enumerate(l_monitores) if x["monitor_serie"] == item_frota["monitor"]), 0)
            monitor = st.selectbox("Monitor", options=l_monitores, index=idx_mon,
                                   format_func=lambda x: f"{x['monitor_serie']} ({x['modelo_monitor']})" if x["monitor_serie"] else "❌ Remover")

            # NAV
            l_navs = [VAZIO] + navs_opt
            idx_nav = next((i for i, x in enumerate(l_navs) if x["nav_serie"] == item_frota["nav"]), 0)
            nav = st.selectbox("NAV", options=l_navs, index=idx_nav,
                               format_func=lambda x: f"{x['nav_serie']}" if x["nav_serie"] else "❌ Remover")

            if st.form_submit_button("💾 Salvar Alterações"):
                payload = {
                    "nome": nome,
                    "antena": antena["antena_serie"],
                    "monitor": monitor["monitor_serie"],
                    "nav": nav["nav_serie"]
                }
                if services.update_equipamento(id_edit, payload):
                    st.success("Frota atualizada!")
                    go("frotas")

        # Excluir Frota
        st.write("---")
        with st.expander("⚠️ Zona de Perigo - Excluir Equipamento"):
            st.warning("Deletar a frota liberará todos os componentes (Antena, Monitor e Nav) para uso em outros tratores.")
            if st.button("🗑️ Confirmar Exclusão da Frota", type="primary", use_container_width=True):
                if services.delete_registro("Equipamentos", id_edit):
                    st.success("Frota excluída!")
                    go("frotas")

    # --- BLOCO 2: EDIÇÃO DE COMPONENTES (CADASTRO) ---
    else:
        if not item:
            st.error("Dados do componente não carregados.")
            return

        st.subheader(f"Editar Cadastro: {tipo.title()}")
        
        with st.form("form_edit_peca"):
            novos_dados = {}
            tabela = ""

            if tipo == "antenas":
                tabela = "Antenas"
                serie = st.text_input("Série", value=item.get("antena_serie"))
                mod = st.text_input("Modelo", value=item.get("modelo_antena"))
                mar = st.text_input("Marca Sinal", value=item.get("marca_sinal"))
                novos_dados = {"antena_serie": serie, "modelo_antena": mod, "marca_sinal": mar}

            elif tipo == "monitores":
                tabela = "Monitores"
                serie = st.text_input("Série", value=item.get("monitor_serie"))
                mod = st.text_input("Modelo", value=item.get("modelo_monitor"))
                novos_dados = {"monitor_serie": serie, "modelo_monitor": mod}

            elif tipo == "navs":
                tabela = "Navs"
                serie = st.text_input("Série", value=item.get("nav_serie"))
                novos_dados = {"nav_serie": serie}

            if st.form_submit_button("💾 Salvar Alterações"):
                if services.update_registro_generico(tabela, item['id'], novos_dados):
                    st.success("Cadastro atualizado!")
                    go("home")

        # Excluir Componente
        st.write("---")
        with st.expander("⚠️ Zona de Perigo - Excluir Componente"):
            st.warning("Verifique se o componente não está associado a nenhuma frota ativa antes de excluí-lo.")
            if st.button(f"🗑️ Confirmar Exclusão de {tipo.title()}", type="primary", use_container_width=True):
                if services.delete_registro(tabela, item['id']):
                    st.success("Componente excluído!")
                    go("home")
