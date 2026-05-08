import streamlit as st
from services import get_itens_com_status, add_registro

def render(go, tipo):
    if st.button("⬅️ Voltar"): go("home")
    
    # Configurações de mapeamento
    tabelas = {"antenas": "Antenas", "monitores": "Monitores", "navs": "Navs"}
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
                dados_final = {"antena_serie": serie, "modelo_antena": modelo, "marca_sinal": marca}
            
            elif tipo == "monitores":
                st.info("Campos da Tabela: Monitores")
                serie = st.text_input("Monitor Série", placeholder="Ex: PCG5...")
                modelo = st.text_input("Modelo Monitor", placeholder="Ex: G5 PLUS")
                dados_final = {"monitor_serie": serie, "modelo_monitor": modelo}
                
            elif tipo == "navs":
                st.info("Campos da Tabela: Navs")
                serie = st.text_input("Nav Série")
                dados_final = {"nav_serie": serie}

            if st.form_submit_button("Salvar no Banco"):
                valor_serie = dados_final.get(coluna_id)
                if valor_serie:
                    if add_registro(nome_tabela, dados_final):
                        st.success("✅ Gravado com sucesso no Supabase!")
                        st.rerun()
                else:
                    st.error("O campo de Série é obrigatório.")

    # --- LISTAGEM COM RASTREAMENTO E EDIÇÃO ---
    st.write("---")
    busca = st.text_input(f"🔍 Filtrar {nome_tabela}...")
    
    # Busca dados processados (com o campo 'vinculo' injetado via Python)
    dados = get_itens_com_status(nome_tabela, coluna_id)
    
    if busca:
        dados = [d for d in dados if any(busca.lower() in str(v).lower() for v in d.values())]

    if not dados:
        st.info(f"Nenhum registro encontrado em {nome_tabela}.")

    for item in dados:
        with st.container(border=True):
            # Criamos duas colunas: uma para os dados e outra para o botão editar
            col_dados, col_acao = st.columns([0.85, 0.15])
            
            with col_dados:
                # 1. Exibição dos dados técnicos
                if tipo == "antenas":
                    st.markdown(f"**Série:** `{item.get('antena_serie')}`")
                    st.caption(f"📦 **Modelo:** {item.get('modelo_antena')} | 📡 **Marca:** {item.get('marca_sinal')}")
                
                elif tipo == "monitores":
                    st.markdown(f"**Série:** `{item.get('monitor_serie')}`")
                    st.caption(f"📦 **Modelo:** {item.get('modelo_monitor')}")
                
                elif tipo == "navs":
                    st.markdown(f"**Série:** `{item.get('nav_serie')}`")
                
                # 2. Exibição do Status de Vínculo
                trator_dono = item.get("vinculo")
                if trator_dono:
                    st.markdown(
                        f"""
                        <div style="background-color: #31333F; padding: 10px; border-radius: 5px; border-left: 5px solid #FF4B4B; margin-top: 5px;">
                            📍 <b>Frota: {trator_dono}</b>
                        </div>
                        """, 
                        unsafe_allow_html=True
                    )
                else:
                    st.success("✅ Disponível em Estoque")
            
            with col_acao:
                # Botão de Editar
                # Usamos o ID ou Série como chave única para o botão
                if st.button("📝 Editar", key=f"edit_{item.get(coluna_id)}"):
                    st.session_state.item_para_editar = item
                    st.session_state.tipo_edicao = tipo
                    go("editar")
