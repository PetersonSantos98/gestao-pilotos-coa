import streamlit as st
from services import get_itens_com_status, add_registro

def render(go, tipo):
    if st.button("⬅️ Voltar"): go("home")
    
    # Mapeamento para garantir que usamos os nomes das tabelas do banco
    tabelas = {"antenas": "Antenas", "monitores": "Monitores", "navs": "Navs"}
    # Identifica qual a coluna de série correta para cada tabela
    colunas_serie = {"antenas": "antena_serie", "monitores": "monitor_serie", "navs": "nav_serie"}
    
    nome_tabela = tabelas.get(tipo)
    coluna_id = colunas_serie.get(tipo)
    
    st.subheader(f"📋 Gestão de {nome_tabela}")

    # --- FORMULÁRIO DE CADASTRO ---
    with st.expander(f"➕ Novo Cadastro de {nome_tabela[:-1]}"):
        with st.form(f"form_add_{tipo}"):
            dados_final = {}
            
            if tipo == "antenas":
                st.info("Campos da Tabela: Antenas")
                serie = st.text_input("Antena Série", placeholder="Ex: PCS75UA...")
                modelo = st.text_input("Modelo Antena", placeholder="Ex: Star Fire 7500")
                marca = st.text_input("Marca Sinal", placeholder="Ex: John Deere")
                
                dados_final = {
                    "antena_serie": serie,
                    "modelo_antena": modelo,
                    "marca_sinal": marca
                }
            
            elif tipo == "monitores":
                st.info("Campos da Tabela: Monitores")
                serie = st.text_input("Monitor Série", placeholder="Ex: PCG5...")
                modelo = st.text_input("Modelo Monitor", placeholder="Ex: G5 PLUS")
                
                dados_final = {
                    "monitor_serie": serie,
                    "modelo_monitor": modelo
                }
                
            elif tipo == "navs":
                st.info("Campos da Tabela: Navs")
                serie = st.text_input("Nav Série")
                
                dados_final = {
                    "nav_serie": serie
                }

            if st.form_submit_button("Salvar no Banco"):
                valor_serie = dados_final.get(coluna_id)
                if valor_serie:
                    if add_registro(nome_tabela, dados_final):
                        st.success("✅ Gravado com sucesso no Supabase!")
                        st.rerun()
                else:
                    st.error("O campo de Série é obrigatório.")

    # --- LISTAGEM COM RASTREAMENTO DE VÍNCULO ---
    st.write("---")
    busca = st.text_input(f"🔍 Filtrar {nome_tabela}...")
    
    # AQUI ESTÁ A MÁGICA: busca os dados já cruzados com a frota
    dados = get_itens_com_status(nome_tabela, coluna_id)
    
    if busca:
        dados = [d for d in dados if any(busca.lower() in str(v).lower() for v in d.values())]

    if not dados:
        st.info(f"Nenhum registro encontrado em {nome_tabela}.")

    for item in dados:
        with st.container(border=True):
            # 1. Exibição dos dados técnicos
            if tipo == "antenas":
                st.markdown(f"**Série:** `{item.get('antena_serie')}`")
                st.caption(f"📦 **Modelo:** {item.get('modelo_antena')} | 📡 **Marca:** {item.get('marca_sinal')}")
            
            elif tipo == "monitores":
                st.markdown(f"**Série:** `{item.get('monitor_serie')}`")
                st.caption(f"📦 **Modelo:** {item.get('modelo_monitor')}")
            
            elif tipo == "navs":
                st.markdown(f"**Série:** `{item.get('nav_serie')}`")
            
            # 2. Exibição do Status de Vínculo (Lógica igual ao Vencimento)
            # O campo 'vinculo' é injetado pela função get_itens_com_status no services.py
            trator_dono = item.get("vinculo")
            
            if trator_dono:
                st.error(f"🚜 Ocupado em Frota: **{trator_dono}**")
            else:
                st.success("✅ Disponível em Estoque")
