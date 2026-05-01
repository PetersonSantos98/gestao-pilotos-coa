import streamlit as st
import pandas as pd
from supabase import create_client, Client
from datetime import datetime, date

# --- CONEXÃO ---
SUPABASE_URL = "https://wjejxlnclrdpigpratrt.supabase.co"
SUPABASE_KEY = "sb_publishable_TZrkyrcPDgaqcgTcZcmvPQ_UofXX50m"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Gestão GPS COA", page_icon="🚜", layout="wide")

# Estilização Profissional
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 8px; height: 50px; font-weight: bold; }
    .card { background-color: white; padding: 20px; border-radius: 15px; border: 1px solid #e6e9ef; box-shadow: 2px 2px 10px rgba(0,0,0,0.05); }
    .status-ok { color: #2e7d32; font-weight: bold; }
    .status-alerta { color: #f57c00; font-weight: bold; }
    .header { background: linear-gradient(90deg, #1b5e20 0%, #2e7d32 100%); padding: 20px; border-radius: 10px; color: white; text-align: center; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

# --- SISTEMA DE NAVEGAÇÃO ---
if 'pagina' not in st.session_state: st.session_state.pagina = 'Home'
def mudar_pagina(nome): st.session_state.pagina = nome

# --- FUNÇÕES DE LÓGICA ---
def buscar_validade(serie_antena, serie_monitor):
    """Lógica Inteligente: Busca validade na Antena, se não achar, busca no Monitor"""
    # 1. Tenta na tabela de Licenças pelo número de série
    for serie in [serie_antena, serie_monitor]:
        if serie:
            res = supabase.table("licencas_validades").select("data_vencimento").eq("licenca", str(serie)).execute()
            if res.data:
                return res.data[0]['data_vencimento']
    return "Não encontrada"

# --- UI - HEADER ---
st.markdown('<div class="header"><h1>🚜 Qualidade Agrícola - Gestão de Pilotos</h1></div>', unsafe_allow_html=True)

# --- PÁGINA HOME ---
if st.session_state.pagina == 'Home':
    col_nav, col_busca = st.columns([1, 3])
    with col_nav:
        if st.button("➕ Novo Equipamento"): mudar_pagina('Cadastro')
        if st.button("🔔 Ver Vencimentos"): mudar_pagina('Vencimentos')
    
    with col_busca:
        busca = st.text_input("🔍 Buscar por Frota ou Nome...", placeholder="Ex: 1218")

    # Listagem de Equipamentos em Cards
    res = supabase.table("equipamentos").select("*").order("codigo_do_equipamento").execute()
    if res.data:
        df = pd.DataFrame(res.data)
        if busca:
            df = df[df['codigo_do_equipamento'].astype(str).str.contains(busca) | df['nome'].str.contains(busca, case=False)]

        cols = st.columns(3)
        for idx, row in df.iterrows():
            with cols[idx % 3]:
                st.markdown(f"""
                <div class="card">
                    <h3>🚜 Frota: {row['codigo_do_equipamento']}</h3>
                    <p><b>Modelo:</b> {row['nome']}</p>
                    <hr>
                    <p>🖥️ <b>Monitor:</b> {row['monitor'] or '---'}</p>
                    <p>📡 <b>Antena:</b> {row['antena'] or '---'}</p>
                    <p>🧭 <b>NAV:</b> {row['nav'] or '---'}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Botão de edição para cada card
                if st.button(f"Editar Frota {row['codigo_do_equipamento']}", key=f"ed_{row['id']}"):
                    st.session_state.equip_edit = row
                    mudar_pagina('Editar')
                st.write("")

# --- PÁGINA DE EDIÇÃO/ALTERAÇÃO ---
elif st.session_state.pagina == 'Editar':
    equip = st.session_state.equip_edit
    st.subheader(f"📝 Alterar Equipamentos - Frota {equip['codigo_do_equipamento']}")
    
    with st.form("form_edit"):
        col1, col2 = st.columns(2)
        novo_monitor = col1.text_input("Série Monitor", value=equip['monitor'])
        nova_antena = col2.text_input("Série Antena", value=equip['antena'])
        novo_nav = col1.text_input("Série NAV", value=equip['nav'])
        
        # Busca validade em tempo real
        validade = buscar_validade(nova_antena, novo_monitor)
        st.info(f"📅 Validade de Sinal detectada: {validade}")

        if st.form_submit_button("Salvar Alterações"):
            update_data = {
                "monitor": novo_monitor,
                "antena": nova_antena,
                "nav": novo_nav,
                "data_vencimento": validade if validade != "Não encontrada" else None
            }
            supabase.table("equipamentos").update(update_data).eq("id", equip['id']).execute()
            st.success("Dados atualizados com sucesso!")
            mudar_pagina('Home')
            st.rerun()
    
    if st.button("Cancelar"): mudar_pagina('Home')

# --- PÁGINA DE CADASTRO ---
elif st.session_state.pagina == 'Cadastro':
    st.subheader("➕ Inserir Novo Equipamento na Frota")
    with st.form("form_cadastro"):
        c1, c2 = st.columns(2)
        tipo = c1.selectbox("Tipo", ["[TR] GRUNNER", "[TR] CASE", "[TR] JOHN DEERE"])
        codigo = c2.text_input("Código da Frota (Ex: 1500)")
        nome = st.text_input("Nome/Descrição do Equipamento")
        
        if st.form_submit_button("Cadastrar"):
            if codigo and nome:
                supabase.table("equipamentos").insert({
                    "tipo_de_equipamento": tipo,
                    "codigo_do_equipamento": codigo,
                    "nome": nome
                }).execute()
                st.success("Equipamento adicionado!")
                mudar_pagina('Home')
                st.rerun()
            else:
                st.error("Preencha Código e Nome.")
    if st.button("Voltar"): mudar_pagina('Home')

# --- PÁGINA DE VENCIMENTOS ---
elif st.session_state.pagina == 'Vencimentos':
    st.subheader("🔔 Relatório de Validades")
    if st.button("⬅️ Voltar"): mudar_pagina('Home')
    
    res = supabase.table("equipamentos").select("codigo_do_equipamento, nome, data_vencimento, antena, monitor").execute()
    if res.data:
        df_v = pd.DataFrame(res.data)
        df_v = df_v.dropna(subset=['data_vencimento'])
        df_v['data_vencimento'] = pd.to_datetime(df_v['data_vencimento'])
        
        hoje = datetime.now()
        df_v['Status'] = df_v['data_vencimento'].apply(lambda x: "🔴 VENCIDO" if x < hoje else "🟢 OK")
        
        st.dataframe(df_v.sort_values("data_vencimento"), use_container_width=True)
