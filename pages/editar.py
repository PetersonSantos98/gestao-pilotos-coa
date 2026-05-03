import streamlit as st
from services import get_equipamentos, get_itens_disponiveis, update_equipamento

def render(go):
    if st.button("⬅️ Cancelar"): go("frotas")

    id_edit = st.session_state.get("edit_id")
    data = get_equipamentos()
    item = next((x for x in data if x["id"] == id_edit), None)

    if not item:
        st.error("Equipamento não localizado.")
        return

    st.subheader(f"Editando {item['codigo_do_equipamento']}")

    # Busca apenas componentes disponíveis ou o que já está nele
    antenas_opt = get_itens_disponiveis("Antenas", "antena_serie", item["antena"])
    monitores_opt = get_itens_disponiveis("Monitores", "monitor_serie", item["monitor"])
    navs_opt = get_itens_disponiveis("Navs", "nav_serie", item["nav"])

    with st.form("form_edit"):
        nome = st.text_input("Nome", value=item["nome"])
        
        # Selectboxes baseadas nas tabelas mestras
        antena = st.selectbox("Antena Disponível", options=antenas_opt, 
                             format_func=lambda x: f"{x['antena_serie']} ({x['modelo_antena']})",
                             index=next((i for i, x in enumerate(antenas_opt) if x["antena_serie"] == item["antena"]), 0))
        
        monitor = st.selectbox("Monitor Disponível", options=monitores_opt, 
                              format_func=lambda x: f"{x['monitor_serie']} ({x['modelo_monitor']})",
                              index=next((i for i, x in enumerate(monitores_opt) if x["monitor_serie"] == item["monitor"]), 0))
        
        nav = st.selectbox("NAV Disponível", options=navs_opt, 
                          format_func=lambda x: f"{x['nav_serie']}",
                          index=next((i for i, x in enumerate(navs_opt) if x["nav_serie"] == item["nav"]), 0))

        if st.form_submit_button("💾 Salvar Alterações"):
            update_equipamento(id_edit, {
                "nome": nome,
                "antena": antena["antena_serie"],
                "modelo_antena": antena["modelo_antena"],
                "marca_do_sinal": antena["marca_sinal"],
                "monitor": monitor["monitor_serie"],
                "modelo_monitor": monitor["modelo_monitor"],
                "nav": nav["nav_serie"]
            })
            st.success("Dados atualizados!")
            go("frotas")
