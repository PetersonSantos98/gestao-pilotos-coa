import streamlit as st
import services

def render(go):
    # Recuperamos as variáveis de controlo do session_state
    item = st.session_state.get("item_para_editar")
    tipo = st.session_state.get("tipo_edicao")
    id_edit = st.session_state.get("edit_id")

    # Botão de voltar dinâmico
    if st.button("⬅️ Cancelar"): 
        go("frotas" if tipo == "frotas" else "home")

    if not tipo:
        st.error("Erro: Tipo de edição não definido.")
        return

    # --- CENÁRIO A: EDIÇÃO DE FROTAS (VÍNCULOS DE ANTENA, MONITOR E NAV) ---
    if tipo == "frotas":
        data = services.get_equipamentos()
        item_frota = next((x for x in data if x["id"] == id_edit), None)

        if not item_frota:
            st.error("Equipamento de frota não localizado.")
            return

        st.subheader(f"Editando Frota: {item_frota['codigo_do_equipamento']}")

        # Buscamos as opções disponíveis no banco para cada categoria
        antenas_opt = services.get_itens_disponiveis("Antenas", "antena_serie", item_frota["antena"])
        monitores_opt = services.get_itens_disponiveis("Monitores", "monitor_serie", item_frota["monitor"])
        navs_opt = services.get_itens_disponiveis("Navs", "nav_serie", item_frota["nav"])

        # Item padrão para desvincular uma peça
        VAZIO = {"antena_serie": None, "modelo_antena": None, "monitor_serie": None, "modelo_monitor": None, "nav_serie": None}

        with st.form("form_edit_frota"):
            nome = st.text_input("Nome do Equipamento", value=item_frota["nome"])
            
            # --- SELECÇÃO DE ANTENA ---
            lista_antenas = [VAZIO] + antenas_opt
            idx_antena = next((i for i, x in enumerate(lista_antenas) if x["antena_serie"] == item_frota["antena"]), 0)
            antena = st.selectbox("Antena", options=lista_antenas, 
                                 format_func=lambda x: f"{x['antena_serie']} ({x['modelo_antena']})" if x["antena_serie"] else "❌ Remover", 
                                 index=idx_antena)

            # --- SELECÇÃO DE MONITOR ---
            lista_monitores = [VAZIO] + monitores_opt
            idx_monitor = next((i for i, x in enumerate(lista_monitores) if x["monitor_serie"] == item_frota["monitor"]), 0)
            monitor = st.selectbox("Monitor", options=lista_monitores, 
                                  format_func=lambda x: f"{x['monitor_serie']} ({x['modelo_monitor']})" if x["monitor_serie"] else "❌ Remover", 
                                  index=idx_monitor)

            # --- SELECÇÃO DE NAV (READICIONADO) ---
            lista_navs = [VAZIO] + navs_opt
            idx_nav = next((i for i, x in enumerate(lista_navs) if x["nav_serie"] == item_frota["nav"]), 0)
            nav = st.selectbox("NAV", options=lista_navs, 
                              format_func=lambda x: f"{x['nav_serie']}" if x["nav_serie"] else "❌ Remover", 
                              index=idx_nav)

            if st.form_submit_button("💾 Salvar Vínculos da Frota"):
                payload = {
                    "nome": nome,
                    "antena": antena["antena_serie"],
                    "monitor": monitor["monitor_serie"],
                    "nav": nav["nav_serie"]  # Agora o NAV é enviado corretamente
                }
                if services.update_equipamento(id_edit, payload):
                    st.success("Frota e vínculos atualizados com sucesso!")
                    st.rerun()

    # --- CENÁRIO B: EDIÇÃO DE COMPONENTES (DADOS TÉCNICOS) ---
    else:
        if not item:
            st.error("Item para editar não encontrado.")
            return

        st.subheader(f"Editando {tipo.title()}: {item.get('antena_serie') or item.get('monitor_serie') or item.get('nav_serie')}")

        with st.form("form_edit_componente"):
            novos_dados = {}
            tabela = ""
            
            if tipo == "antenas":
                tabela = "Antenas"
                serie = st.text_input("Série", value=item.get("antena_serie"))
                mod = st.text_input("Modelo", value=item.get("modelo_antena"))
                novos_dados = {"antena_serie": serie, "modelo_antena": mod}
            
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
                    st.success("Dados atualizados!")
                    st.rerun()
