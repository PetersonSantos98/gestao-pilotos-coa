import streamlit as st
import pandas as pd
from supabase import create_client, Client
from datetime import datetime, date

# --- CONEXÃO ---
SUPABASE_URL = "https://wjejxlnclrdpigpratrt.supabase.co"
SUPABASE_KEY = "sb_publishable_TZrkyrcPDgaqcgTcZcmvPQ_UofXX50m"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Gestão de Pilotos COA", page_icon="🚜", layout="centered")

# Estilização para simular o App do Vídeo
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button { 
        width: 100%; border-radius: 15px; height: 110px; 
        background-color: #4CAF50; color: white; font-weight: bold; 
        font-size: 18px; border: none; box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
        display: flex; flex-direction: column; align-items: center; justify-content: center;
    }
    .stButton>button:hover { background-color: #45a049; border: none; color: white; }
    .header-app { 
        background-color: #2e7d32; padding: 15px; border-radius: 10px; 
        color: white; text-align: center; margin-bottom: 20px;
        font-family: sans-serif;
    }
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

# --- HEADER ---
st.markdown(f'<div class="header-app"><h2>Aplicativo | Gestão de Pilotos</h2><p>Elaborado por: Peterson Santos - COA</p></div>', unsafe_allow_html=True)

# --- LÓGICA DE BUSCA DE VALIDADE ---
def buscar_validade_inteligente(id_equip, serie_antena, serie_monitor):
    # 1. Tenta buscar na tabela de licencas_validades
    vencimento = None
    for serie in [serie_antena, serie_monitor]:
        if serie and str(serie) != 'nan':
            res = supabase.table("licencas_validades").select("data_vencimento").eq("licenca", str(serie)).execute()
            if res.data:
                return res.data[0]['data_vencimento']
    return "Sem Validade"

# --- TELAS ---

# 1. HOME (MENU COM BLOCOS VERDES)
if st.session_state.pagina == 'Home':
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔔\nVencimentos"): mudar_pagina('Vencimentos')
        if st.button("🚜\nFrotas"): mudar_pagina('Frotas')
    with col2:
        if st.button("🔄\nSincronizar"): st.toast("Sincronizando dados...")
        if st.button("🖥️\nMonitores"): mudar_pagina('Monitores')
    with col3:
        if st.button("📝\nCadastros"): mudar_pagina('Cadastro')
        if st.button("📡\nAntenas"): mudar_pagina('Antenas')

# 2. TELA DE FROTAS (LAYOUT DE LISTA)
elif st.session_state.pagina == 'Frotas':
    if st.button("⬅️ Voltar para o Início"): mudar_pagina('Home')
    busca = st.text_input("🔍 Pesquisar Frota...", placeholder="Digite o número da frota")
    
    # Busca na tabela minúscula 'equipamentos'
    res = supabase.table("equipamentos").select("*").execute()
    if res.data:
        df = pd.DataFrame(res.data)
        if busca:
            df = df[df['codigo_do_equipamento'].astype(str).str.contains(busca)]
        
        for _, row in df.iterrows():
            with st.container():
                st.markdown(f"""
                <div class="card-equip">
                    <b>🚜 Frota: {row['codigo_do_equipamento']}</b> - {row['nome']}<br>
                    <small>📡 Antena: {row['antena']} | 🖥️ Monitor: {row['monitor']}</small>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"Gerenciar Frota {row['codigo_do_equipamento']}", key=row['id']):
                    st.session_state.edit_id = row
                    mudar_pagina('Editar')

# 3. TELA DE VENCIMENTOS (BUSCA NAS DUAS TABELAS)
elif st.session_state.pagina == 'Vencimentos':
    if st.button("⬅️ Voltar para o Início"): mudar_pagina('Home')
    st.subheader("Vencimento de Sinais")
    
    res = supabase.table("equipamentos").select("*").execute()
    if res.data:
        for row in res.data:
            validade = buscar_validade_inteligente(row['id'], row['antena'], row['monitor'])
            if validade != "Sem Validade":
                cor = "red" if datetime.strptime(validade, "%Y-%m-%d").date() < date.today() else "green"
                st.markdown(f"**Frota {row['codigo_do_equipamento']}** - Vence em: <span style='color:{cor}'>{validade}</span>", unsafe_allow_html=True)
                st.divider()

# 4. TELA DE EDIÇÃO (ONDE O USUÁRIO ALTERA TUDO)
elif st.session_state.pagina == 'Editar':
    item = st.session_state.edit_id
    if st.button("⬅️ Cancelar"): mudar_pagina('Frotas')
    
    st.subheader(f"Configurar Equipamento: {item['codigo_do_equipamento']}")
    
    with st.form("edit_form"):
        novo_nome = st.text_input("Nome/Modelo Máquina", value=item['nome'])
        nova_antena = st.text_input("Série da Antena", value=item['antena'])
        novo_monitor = st.text_input("Série do Monitor", value=item['monitor'])
        novo_nav = st.text_input("Série do NAV", value=item['nav'])
        
        if st.form_submit_button("✅ Salvar Alterações"):
            dados_up = {
                "nome": novo_nome,
                "antena": nova_antena,
                "monitor": novo_monitor,
                "nav": novo_nav
            }
            supabase.table("equipamentos").update(dados_up).eq("id", item['id']).execute()
            st.success("Dados atualizados com sucesso!")
            mudar_pagina('Frotas')
            st.rerun()
