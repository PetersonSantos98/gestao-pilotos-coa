import streamlit as st
import pandas as pd
from supabase import create_client, Client
from datetime import datetime, date

# --- CONFIGURAÇÕES DO SUPABASE ---
# Usei as chaves que estavam no seu código anterior
SUPABASE_URL = "https://wjejxlnclrdpigpratrt.supabase.co"
SUPABASE_KEY = "sb_publishable_TZrkyrcPDgaqcgTcZcmvPQ_UofXX50m"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Gestão de Pilotos COA", page_icon="🚜", layout="centered")

# Estilização para botões grandes e cores do Agro
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 10px; height: 80px; background-color: #2e7d32; color: white; font-weight: bold; margin-bottom: 10px; }
    .header { background-color: #2e7d32; padding: 15px; border-radius: 10px; color: white; text-align: center; margin-bottom: 25px; }
    div[data-testid="stExpander"] { border: 1px solid #2e7d32; border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

# Controle de Navegação
if 'pagina' not in st.session_state:
    st.session_state.pagina = 'Home'

def mudar_pagina(nome):
    st.session_state.pagina = nome

# --- HEADER ---
st.markdown('<div class="header"><h1>Aplicativo | Gestão de Pilotos</h1><p>Qualidade Agrícola - COA</p></div>', unsafe_allow_html=True)

# --- LÓGICA DE NAVEGAÇÃO ---

# 1. HOME (MENU PRINCIPAL)
if st.session_state.pagina == 'Home':
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔔\nVencimentos"): mudar_pagina('Vencimentos')
        if st.button("🚜\nFrotas"): mudar_pagina('Frotas')
    with col2:
        if st.button("🔄\nSincronização"): st.toast("Sincronizando com Banco COA...")
        if st.button("🖥️\nMonitores"): mudar_pagina('Monitores')
    with col3:
        if st.button("📝\nCadastros"): mudar_pagina('Cadastro')
        if st.button("📡\nAntenas"): mudar_pagina('Antenas')

# 2. TELA DE CADASTRO (CORRIGIDA)
elif st.session_state.pagina == 'Cadastro':
    if st.button("⬅️ Voltar para Home"): mudar_pagina('Home')
    st.subheader("📝 Novo Cadastro")
    
    with st.form("form_cadastro"):
        tipo = st.selectbox("Tipo de Equipamento", ["Monitor", "Antena"])
        m_id = st.text_input("Monitor ID / Identificador")
        n_serie = st.text_input("Número de Série")
        modelo = st.text_input("Modelo (ex: GS3, SF6000)")
        situacao = st.selectbox("Situação", ["Estoque", "Em Uso", "Manutenção", "Desativado"])
        frota = st.text_input("Frota Vinculada (ID)")
        vencimento = st.date_input("Data de Vencimento do Sinal", value=date.today())
        
        if st.form_submit_button("Salvar no Banco"):
            # NOMES DAS COLUNAS AJUSTADOS PARA BATER COM image_fc1339.png
            dados = {
                "monitor_id": m_id,
                "numero_serie": n_serie,
                "modelo": modelo,
                "situacao": situacao,
                "frota_id": frota, 
                "data_vencimento_licenca": str(vencimento),
                "tipo": tipo
            }
            try:
                supabase.table("ativos").insert(dados).execute()
                st.success("✅ Equipamento cadastrado com sucesso!")
            except Exception as e:
                st.error(f"Erro ao salvar: {e}")

# 3. TELA DE VENCIMENTOS (CORRIGIDA)
elif st.session_state.pagina == 'Vencimentos':
    if st.button("⬅️ Voltar para Home"): mudar_pagina('Home')
    st.subheader("🔔 Alertas de Vencimento de Sinal")
    
    res = supabase.table("ativos").select("*").execute()
    if res.data:
        df = pd.DataFrame(res.data)
        hoje = date.today()
        
        for _, row in df.iterrows():
            # AJUSTADO PARA USAR data_vencimento_licenca
            if row['data_vencimento_licenca']:
                dv = datetime.strptime(row['data_vencimento_licenca'], '%Y-%m-%d').date()
                cor = "red" if dv <= hoje else "orange" if (dv - hoje).days < 30 else "green"
                
                with st.container():
                    st.markdown(f"**Série:** `{row['numero_serie']}` | **Vence em:** <span style='color:{cor}; font-weight:bold;'>{dv.strftime('%d/%m/%Y')}</span>", unsafe_allow_html=True)
                    st.write(f"Frota ID: {row['frota_id']} | Modelo: {row['modelo']}")
                    st.divider()
    else:
        st.info("Nenhum dado encontrado para exibição.")

# 4. TELA DE MONITORES
elif st.session_state.pagina == 'Monitores':
    if st.button("⬅️ Voltar para Home"): mudar_pagina('Home')
    st.subheader("🖥️ Listagem de Monitores")
    
    res = supabase.table("ativos").select("*").eq("tipo", "Monitor").execute()
    if res.data:
        df = pd.DataFrame(res.data)
        # Ajustado para os nomes das colunas do banco
        st.dataframe(df[['numero_serie', 'monitor_id', 'modelo', 'situacao', 'frota_id']], use_container_width=True)
    else:
        st.info("Nenhum monitor cadastrado.")

# 5. TELA DE ANTENAS
elif st.session_state.pagina == 'Antenas':
    if st.button("⬅️ Voltar para Home"): mudar_pagina('Home')
    st.subheader("📡 Listagem de Antenas")
    
    res = supabase.table("ativos").select("*").eq("tipo", "Antena").execute()
    if res.data:
        df = pd.DataFrame(res.data)
        st.dataframe(df[['numero_serie', 'modelo', 'situacao', 'frota_id']], use_container_width=True)
    else:
        st.info("Nenhuma antena cadastrada.")

# 6. TELA DE FROTAS (CORRIGIDA)
elif st.session_state.pagina == 'Frotas':
    if st.button("⬅️ Voltar para Home"): mudar_pagina('Home')
    st.subheader("🚜 Gestão de Frotas")
    
    with st.expander("➕ Adicionar Nova Máquina à Frota"):
        c1, c2 = st.columns(2)
        cod = c1.text_input("Código da Frota")
        mod_m = c2.text_input("Modelo da Máquina")
        tipo_m = st.selectbox("Tipo de Máquina", ["Trator", "Colhedora", "Pulverizador", "Caminhão"])
        
        if st.button("Salvar Máquina"):
            # NOMES DAS COLUNAS AJUSTADOS PARA BATER COM image_fc16ba.png
            dados_frota = {
                "codigo_frota": cod, 
                "modelo": mod_m,
                "tipo_equipamento": tipo_m
            }
            try:
                supabase.table("frotas").insert(dados_frota).execute()
                st.success("✅ Máquina salva com sucesso!")
                st.rerun()
            except Exception as e:
                st.error(f"Erro ao salvar frota: {e}")

    res = supabase.table("frotas").select("*").execute()
    if res.data:
        df_frotas = pd.DataFrame(res.data)
        st.table(df_frotas[['codigo_frota', 'modelo', 'tipo_equipamento']])