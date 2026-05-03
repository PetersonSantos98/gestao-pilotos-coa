import streamlit as st
from services import get_tabela_simples, add_registro

def render(go, tipo):
    if st.button("⬅️ Voltar"): go("home")
    
    tabelas = {"antenas": "Antenas", "monitores": "Monitores", "navs": "Navs"}
    nome_tabela = tabelas.get(tipo)
    st.subheader(f"📋 Gestão de {nome_tabela}")

    # Formulário de Cadastro
    with st.expander(f"➕ Novo Cadastro de {nome_tabela[:-1]}"):
        with st.form(f"form_add_{tipo}"):
            col_serie = "antena_serie" if tipo == "antenas" else ("monitor_serie" if tipo == "monitores" else "nav_serie")
            nova_serie = st.text_input("Número de Série")
            modelo = st.text_input("Modelo/Marca")
            if st.form_submit_button("Salvar"):
                if nova_serie:
                    add_registro(nome_tabela, {col_serie: nova_serie, "modelo": modelo})
                    st.success("Cadastrado!"); st.rerun()

    # Filtro de Busca
    busca = st.text_input(f"🔍 Pesquisar em {nome_tabela}...")
    
    dados = get_tabela_simples(nome_tabela)
    if busca:
        dados = [d for d in dados if any(busca.lower() in str(v).lower() for v in d.values())]

    for item in dados:
        with st.container(border=True):
            serie = item.get("antena_serie") or item.get("monitor_serie") or item.get("nav_serie")
            st.markdown(f"**Série:** `{serie}`")
            if item.get("modelo"): st.caption(f"📦 {item.get('modelo')}")
            
            frota = item.get("codigo_do_equipamento")
            st.caption(f"🚜 {'Frota: ' + str(frota) if frota else '✅ Disponível'}")
