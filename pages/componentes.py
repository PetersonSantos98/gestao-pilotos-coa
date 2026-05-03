import streamlit as st
from services import get_tabela_simples, add_registro

def render(go, tipo):
    if st.button("⬅️ Voltar"): go("home")
    
    tabelas = {"antenas": "Antenas", "monitores": "Monitores", "navs": "Navs"}
    nome_tabela = tabelas.get(tipo)
    st.subheader(f"📋 Gestão de {nome_tabela}")

    # --- FORMULÁRIO DE CADASTRO COM LOGICA DE COLUNAS REAIS ---
    with st.expander(f"➕ Novo Cadastro de {nome_tabela[:-1]}"):
        with st.form(f"form_add_{tipo}"):
            dados_para_salvar = {}
            
            if tipo == "antenas":
                # Colunas: antena_serie, modelo_antena, marca_sinal
                serie = st.text_input("Número de Série (Antena)")
                modelo = st.text_input("Modelo da Antena")
                marca = st.text_input("Marca do Sinal")
                dados_para_salvar = {
                    "antena_serie": serie, 
                    "modelo_antena": modelo, 
                    "marca_sinal": marca
                }
            
            elif tipo == "monitores":
                # Colunas: monitor_serie, modelo_monitor
                serie = st.text_input("Número de Série (Monitor)")
                modelo = st.text_input("Modelo do Monitor")
                dados_para_salvar = {
                    "monitor_serie": serie, 
                    "modelo_monitor": modelo
                }
            
            elif tipo == "navs":
                # Coluna: nav_serie
                serie = st.text_input("Número de Série (NAV)")
                dados_para_salvar = {"nav_serie": serie}

            if st.form_submit_button("Salvar no Banco"):
                # Validação simples: precisa ter ao menos a série
                valor_serie = dados_para_salvar.get(f"{tipo[:-1]}_serie")
                if valor_serie:
                    if add_registro(nome_tabela, dados_para_salvar):
                        st.success(f"{nome_tabela[:-1]} cadastrado com sucesso!")
                        st.rerun()
                else:
                    st.error("O campo Número de Série é obrigatório.")

    # --- LISTAGEM E PESQUISA ---
    busca = st.text_input(f"🔍 Pesquisar em {nome_tabela}...")
    dados = get_tabela_simples(nome_tabela)
    
    if busca:
        dados = [d for d in dados if any(busca.lower() in str(v).lower() for v in d.values())]

    for item in dados:
        with st.container(border=True):
            # Lógica para exibir a série correta na lista
            serie = item.get("antena_serie") or item.get("monitor_serie") or item.get("nav_serie")
            # Lógica para exibir o modelo correto na lista
            modelo = item.get("modelo_antena") or item.get("modelo_monitor")
            
            st.markdown(f"**Série:** `{serie}`")
            if modelo: st.caption(f"📦 Modelo: {modelo}")
            if item.get("marca_sinal"): st.caption(f"📡 Sinal: {item.get('marca_sinal')}")
            
            frota = item.get("codigo_do_equipamento")
            st.caption(f"🚜 {'Frota: ' + str(frota) if frota else '✅ Disponível no Estoque'}")
