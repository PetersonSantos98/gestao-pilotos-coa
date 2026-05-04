import streamlit as st
from services import get_tabela_simples, add_registro

def render(go, tipo):
    if st.button("⬅️ Voltar"): go("home")
    
    # Mapeamento para garantir que usamos os nomes das tabelas do banco
    tabelas = {"antenas": "Antenas", "monitores": "Monitores", "navs": "Navs"}
    nome_tabela = tabelas.get(tipo)
    st.subheader(f"📋 Gestão de {nome_tabela}")

    # --- FORMULÁRIO DE CADASTRO ESPECÍFICO ---
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
                # Validação: Não deixa salvar se a série estiver vazia
                valor_serie = list(dados_final.values())[0] 
                if valor_serie:
                    if add_registro(nome_tabela, dados_final):
                        st.success("✅ Gravado com sucesso no Supabase!")
                        st.rerun()
                else:
                    st.error("O campo de Série é obrigatório para o cadastro.")

    # --- LISTAGEM COM OS NOMES DE COLUNA CORRETOS ---
    st.write("---")
    busca = st.text_input(f"🔍 Filtrar {nome_tabela}...")
    dados = get_tabela_simples(nome_tabela)
    
    if busca:
        dados = [d for d in dados if any(busca.lower() in str(v).lower() for v in d.values())]

    for item in dados:
        with st.container(border=True):
            # Lógica para mostrar os dados conforme a tabela
            if tipo == "antenas":
                st.markdown(f"**Série:** `{item.get('antena_serie')}`")
                st.caption(f"📦 **Modelo:** {item.get('modelo_antena')} | 📡 **Marca:** {item.get('marca_sinal')}")
            
            elif tipo == "monitores":
                st.markdown(f"**Série:** `{item.get('monitor_serie')}`")
                st.caption(f"📦 **Modelo:** {item.get('modelo_monitor')}")
            
            elif tipo == "navs":
                st.markdown(f"**Série:** `{item.get('nav_serie')}`")
            
            # Status de uso (se está em algum equipamento)
            frota = item.get("codigo_do_equipamento")
            if frota:
                st.warning(f"🚜 Vinculado à Frota: {frota}")
            else:
                st.success("✅ Disponível em Estoque")
