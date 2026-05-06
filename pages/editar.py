import streamlit as st
import services

def render(go):
    if st.button("⬅️ Cancelar"): go("frotas")

    id_edit = st.session_state.get("edit_id")
    data = services.get_equipamentos()
    item = next((x for x in data if x["id"] == id_edit), None)

    if not item:
        st.error("Equipamento não localizado.")
        return

    st.subheader(f"Editando {item['codigo_do_equipamento']}")

    # 1. Buscamos as opções disponíveis
    antenas_opt = services.get_itens_disponiveis("Antenas", "antena_serie", item["antena"])
    monitores_opt = services.get_itens_disponiveis("Monitores", "monitor_serie", item["monitor"])
    navs_opt = services.get_itens_disponiveis("Navs", "nav_serie", item["nav"])

    # 2. Criamos um item padrão "Vazio" simplificado
    VAZIO = {"antena_serie": None, "modelo_antena": None, "marca_sinal": None, 
             "monitor_serie": None, "modelo_monitor": None, "nav_serie": None}

    with st.form("form_edit"):
        nome = st.text_input("Nome", value=item["nome"])
        
        # --- SELEÇÃO DE ANTENA ---
        lista_antenas = [VAZIO] + antenas_opt
        idx_antena = next((i for i, x in enumerate(lista_antenas) if x["antena_serie"] == item["antena"]), 0)
        
        antena = st.selectbox(
            "Antena", 
            options=lista_antenas,
            format_func=lambda x: f"{x['antena_serie']} ({x['modelo_antena']})" if x["antena_serie"] else "❌ Nenhum / Remover",
            index=idx_antena
        )

        # --- SELEÇÃO DE MONITOR ---
        lista_monitores = [VAZIO] + monitores_opt
        idx_monitor = next((i for i, x in enumerate(lista_monitores) if x["monitor_serie"] == item["monitor"]), 0)
        
        monitor = st.selectbox(
            "Monitor", 
            options=lista_monitores,
            format_func=lambda x: f"{x['monitor_serie']} ({x['modelo_monitor']})" if x["monitor_serie"] else "❌ Nenhum / Remover",
            index=idx_monitor
        )

        # --- SELEÇÃO DE NAV ---
        lista_navs = [VAZIO] + navs_opt
        idx_nav = next((i for i, x in enumerate(lista_navs) if x["nav_serie"] == item["nav"]), 0)
        
        nav = st.selectbox(
            "NAV", 
            options=lista_navs,
            format_func=lambda x: f"{x['nav_serie']}" if x["nav_serie"] else "❌ Nenhum / Remover",
            index=idx_nav
        )

        if st.form_submit_button("💾 Salvar Alterações"):
            # --- CORREÇÃO AQUI ---
            # Enviamos apenas as colunas que REALMENTE existem na tabela Equipamentos
            payload = {
                "nome": nome,
                "antena": antena["antena_serie"],
                "monitor": monitor["monitor_serie"],
                "nav": nav["nav_serie"]
            }
            
            if services.update_equipamento(id_edit, payload):
                st.success("Equipamento atualizado com sucesso!")
                st.rerun() # Use rerun para atualizar a tela e limpar o cache visual
