import streamlit as st
import pandas as pd
from supabase import create_client, Client
from datetime import datetime, date

# --- CONEXÃO ---
SUPABASE_URL = "https://wjejxlnclrdpigpratrt.supabase.co"
SUPABASE_KEY = "sb_publishable_TZrkyrcPDgaqcgTcZcmvPQ_UofXX50m"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Gestão de Pilotos", page_icon="🚜", layout="centered")

# Estilização Ajustada
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    /* Estilo dos Botões do Menu Principal */
    .stButton>button { 
        width: 100%; border-radius: 15px; height: 100px; 
        background-color: #4CAF50; color: white; font-weight: bold; 
        font-size: 16px; border: none; box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    /* Estilo do NOVO CABEÇALHO (Mais limpo) */
    .header-container {
        text-align: center;
        padding-bottom: 20px;
        border-bottom: 2px solid #4CAF50;
        margin-bottom: 25px;
    }
    .header-title { color: #2e7d32; margin-bottom: 0; font-weight: bold; }
    .header-subtitle { color: #666; font-size: 14px; }
    
    .card-equip {
        background-color: white; padding: 15px; border-radius: 10px;
        border-left: 5px solid #2e7d32; margin-bottom: 10px;
        box-shadow: 1px 1px 3px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

# --- NAVEGAÇÃO ---
if 'pagina' not in st.session_state: st.session_state.pagina = 'Home'
def mudar_pagina(nome): st.session_state.pagina = nome

# --- NOVO CABEÇALHO (Ajustado para ser menos "bloco" e mais elegante) ---
st.markdown("""
    <div class="header-container">
        <h1 class="header-title">🚜 Gestão de Pilotos</h1>
        <div class="header-subtitle">Aplicativo de Monitoramento | Peterson Santos </div>
    </div>
""", unsafe_allow_html=True)

# --- LÓGICA DE BUSCA DE VALIDADE ---
def buscar_validade_inteligente(serie_antena, serie_monitor):
    # ATENÇÃO: Nome da tabela com Letra Maiúscula conforme seu print
    for serie in [serie_antena, serie_monitor]:
        if serie and str(serie) != 'nan' and str(serie) != 'NULO':
            res = supabase.table("Licencias_Validades").select("data_vencimento").eq("licenca", str(serie)).execute()
            if res.data:
                return res.data[0]['data_vencimento']
    return "Sem Validade"

# --- TELAS ---

if st.session_state.pagina == 'Home':
    # Grid de botões 2x3 para caber melhor no celular
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔔 Vencimentos"): mudar_pagina('Vencimentos')
        if st.button("🚜 Frotas"): mudar_pagina('Frotas')
        if st.button("🖥️ Monitores"): mudar_pagina('Monitores')
    with col2:
        if st.button("🔄 Sincronizar"): st.toast("Dados atualizados!")
        if st.button("📝 Cadastros"): mudar_pagina('Cadastro')
        if st.button("📡 Antenas"): mudar_pagina('Antenas')

elif st.session_state.pagina == 'Frotas':
    if st.button("⬅️ Voltar"): mudar_pagina('Home')
    busca = st.text_input("🔍 Pesquisar Frota...", placeholder="Ex: 1218")
    
    # CORREÇÃO: Nome da tabela "Equipamentos" (E Maiúsculo)
    res = supabase.table("Equipamentos").select("*").execute()
    if res.data:
        df = pd.DataFrame(res.data)
        if busca:
            df = df[df['codigo_do_equipamento'].astype(str).str.contains(busca)]
        
        for _, row in df.iterrows():
            with st.container():
                st.markdown(f"""
                <div class="card-equip">
                    <b>🚜 Frota: {row['codigo_do_equipamento']}</b> - {row['nome']}<br>
                    <small>📡 Antena: {row['antena']} | 🖥️ Monitor: {row['monitor_serie'] if 'monitor_serie' in row else 'N/A'}</small>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"Gerenciar {row['codigo_do_equipamento']}", key=f"btn_{row['codigo_do_equipamento']}"):
                    st.session_state.edit_id = row
                    mudar_pagina('Editar')
