import streamlit as st
from services import get_tabela_simples

def render(go, tipo):
    st.button("⬅️ Voltar", on_click=lambda: go("home"))
    st.subheader(f"Lista de {tipo.capitalize()}")
    
    tabela = tipo.capitalize() # Antenas, Monitores ou Navs
    dados = get_tabela_simples(tabela)
    
    if not dados:
        st.info(f"Nenhum registro em {tabela}")
        return

    for item in dados:
        with st.container(border=True):
            if tipo == "antenas":
                st.write(f"Série: {item['antena_serie']}")
                st.caption(f"Modelo: {item['modelo_antena']} | Sinal: {item['marca_sinal']}")
            elif tipo == "monitores":
                st.write(f"Série: {item['monitor_serie']}")
                st.caption(f"Modelo: {item['modelo_monitor']}")
            else:
                st.write(f"Série: {item['nav_serie']}")
