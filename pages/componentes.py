import streamlit as st
from services import get_tabela_simples

def render(go, tipo):
    if st.button("⬅️ Voltar"):
        go("home")
    
    # Define o nome da tabela no Supabase baseado na página clicada
    tabelas = {
        "antenas": "Antenas",
        "monitores": "Monitores",
        "navs": "Navs"
    }
    
    nome_tabela = tabelas.get(tipo)
    st.subheader(f"📋 Cadastro de {nome_tabela}")
    
    with st.spinner(f"Carregando {tipo}..."):
        dados = get_tabela_simples(nome_tabela)
    
    if not dados:
        st.info(f"Nenhum registro encontrado em {nome_tabela}.")
        return

    # Exibição dos cards de acordo com as colunas reais do seu banco
    for item in dados:
        with st.container(border=True):
            if tipo == "antenas":
                st.markdown(f"**Série:** `{item.get('antena_serie')}`")
                st.caption(f"Modelo: {item.get('modelo_antena')} | Sinal: {item.get('marca_sinal')}")
                st.caption(f"Equipamento Atual: {item.get('codigo_do_equipamento')}")
            
            elif tipo == "monitores":
                st.markdown(f"**Série:** `{item.get('monitor_serie')}`")
                st.caption(f"Modelo: {item.get('modelo_monitor')}")
                st.caption(f"Equipamento Atual: {item.get('codigo_do_equipamento')}")
            
            elif tipo == "navs":
                st.markdown(f"**Série:** `{item.get('nav_serie')}`")
                st.caption(f"Equipamento Atual: {item.get('codigo_do_equipamento')}")
