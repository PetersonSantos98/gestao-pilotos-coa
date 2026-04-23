import streamlit as st
import pandas as pd
from supabase import create_client, Client
from datetime import datetime, date

# --- CONFIGURAÇÕES DO SUPABASE ---
# O Streamlit Cloud lê dos "Secrets" configurados no site.
if "SUPABASE_URL" in st.secrets:
    SUPABASE_URL = st.secrets["SUPABASE_URL"]
    SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
else:
    # Backup para rodar localmente no seu computador
    SUPABASE_URL = "https://wjejxlnclrdpigpratrt.supabase.co"
    SUPABASE_KEY = "sb_publishable_TZrkyrcPDgaqcgTcZcmvPQ_UofXX50m"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Gestão de Pilotos COA", page_icon="🚜", layout="centered")

# Estilos Visuais
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 10px; height: 60px; background-color: #2e7d32; color: white; font-weight: bold; margin-bottom: 10px; }
    .header { background-color: #2e7d32; padding: 15px; border-radius: 10px; color: white; text-align: center; margin-bottom: 25px; }
    div[data-testid="stExpander"] { border: 1px solid #2e7d32; border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

# Controle de Navegação
if 'pagina' not in st.session_state:
    st.session_state.pagina = 'Home'

def mudar_pagina(nome):
    st.session_state.pagina = nome

# Header fixo
st.markdown('<div class="header"><h1>🚜 Gestão de Pilotos COA</h1><p>Qualidade Agrícola</p></div>', unsafe_allow_html=True)

# --- 1. HOME (MENU) ---
if st.session_state.pagina == 'Home':
    c1, c2 = st.columns(2)
    with c1:
        if st.button("📝 Novo Cadastro"): mudar_pagina('Cadastro')
        if st.button("🚜 Frotas"): mudar_pagina('Frotas')
    with c2:
        if st.button("🖥️ Monitores"): mudar_pagina('Monitores')
        if st.button("📡 Antenas"): mudar_pagina('Antenas')
    
    if st.button("🔔 Vencimentos de Sinal"): mudar_pagina('Vencimentos')

# --- 2. TELA DE CADASTRO (Ajustada para image_fd0667.png) ---
elif st.session_state.pagina == 'Cadastro':
    if st.button("⬅️ Voltar para o Menu"): mudar_pagina('Home')
    st.subheader("📝 Novo Cadastro de Equipamento")
    
    with st.form("form_cadastro"):
        tipo = st.selectbox("Tipo de Equipamento", ["Monitor", "Antena"])
        n_serie = st.text_input("Número de Série")
        modelo = st.text_input("Modelo (Ex: GS3, SF6000)")
        situacao = st.selectbox("Situação", ["Estoque", "Em Uso", "Manutenção"])
        frota_input = st.text_input("Frota ID (Apenas números ou deixe vazio)")
        vencimento = st.date_input("Data de Vencimento do Sinal", value=date.today())
        
        if st.form_submit_button("Salvar no Banco"):
            # Trata o Frota ID para não dar erro 22P02 no Supabase
            frota_final = int(frota_input) if frota_input.strip().isdigit() else None
            
            # Nomes das chaves batendo 100% com o print do Supabase
            dados = {
                "numero_serie": n_serie,
                "tipo": tipo,
                "modelo": modelo,
                "situacao": situacao,
                "frota_id": frota_final, 
                "data_vencimento_licenca": str(vencimento)
            }
            try:
                supabase.table("ativos").insert(dados).execute()
                st.success("✅ Equipamento cadastrado com sucesso!")
            except Exception as e:
                st.error(f"Erro ao salvar: {e}")

# --- 3. TELA DE FROTAS (Ajustada para image_fd06a0.png) ---
elif st.session_state.pagina == 'Frotas':
    if st.button("⬅️ Voltar para o Menu"): mudar_pagina('Home')
    st.subheader("🚜 Gestão de Máquinas")
    
    with st.expander("➕ Adicionar Nova Máquina"):
        c1, c2 = st.columns(2)
        cod = c1.text_input("Código da Frota")
        mod_m = c2.text_input("Modelo da Máquina")
        tipo_m = st.selectbox("Tipo", ["Trator", "Colhedora", "Pulverizador"])
        
        if st.button("Salvar Máquina"):
            dados_frota = {
                "codigo_frota": cod, 
                "modelo": mod_m,
                "tipo_equipamento": tipo_m
            }
            try:
                supabase.table("frotas").insert(dados_frota).execute()
                st.success("✅ Máquina salva!")
                st.rerun()
            except Exception as e:
                st.error(f"Erro: {e}")

    # Exibição da Tabela de Frotas
    res = supabase.table("frotas").select("*").execute()
    if res.data:
        st.table(pd.DataFrame(res.data)[['codigo_frota', 'modelo', 'tipo_equipamento']])

# --- 4. LISTAGENS (MONITORES E ANTENAS) ---
elif st.session_state.pagina in ['Monitores', 'Antenas']:
    if st.button("⬅️ Voltar para o Menu"): mudar_pagina('Home')
    tipo_filtro = "Monitor" if st.session_state.pagina == 'Monitores' else "Antena"
    st.subheader(f"📋 Lista de {st.session_state.pagina}")
    
    res = supabase.table("ativos").select("*").eq("tipo", tipo_filtro).execute()
    if res.data:
        df = pd.DataFrame(res.data)
        st.dataframe(df[['numero_serie', 'modelo', 'situacao', 'frota_id']], use_container_width=True)
    else:
        st.info("Nenhum registro encontrado.")

# --- 5. TELA DE VENCIMENTOS ---
elif st.session_state.pagina == 'Vencimentos':
    if st.button("⬅️ Voltar para o Menu"): mudar_pagina('Home')
    st.subheader("🔔 Vencimentos de Licença")
    
    res = supabase.table("ativos").select("*").execute()
    if res.data:
        df = pd.DataFrame(res.data)
        hoje = date.today()
        for _, row in df.iterrows():
            if row['data_vencimento_licenca']:
                dv = datetime.strptime(row['data_vencimento_licenca'], '%Y-%m-%d').date()
                cor = "red" if dv <= hoje else "orange" if (dv - hoje).days < 30 else "green"
                st.markdown(f"**Série:** `{row['numero_serie']}` | Vence: <span style='color:{cor}; font-weight:bold;'>{dv.strftime('%d/%m/%Y')}</span>", unsafe_allow_html=True)
                st.divider()
