import streamlit as st
import pandas as pd
from supabase import create_client, Client
from datetime import datetime, date

# --- CONFIGURAÇÕES DO SUPABASE ---
# O Streamlit Cloud vai ler isso dos "Secrets" que você configurou
if "SUPABASE_URL" in st.secrets:
    SUPABASE_URL = st.secrets["SUPABASE_URL"]
    SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
else:
    # Caso esteja rodando localmente
    SUPABASE_URL = "https://wjejxlnclrdpigpratrt.supabase.co"
    SUPABASE_KEY = "sb_publishable_TZrkyrcPDgaqcgTcZcmvPQ_UofXX50m"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Gestão de Pilotos COA", page_icon="🚜", layout="centered")

st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 10px; height: 80px; background-color: #2e7d32; color: white; font-weight: bold; margin-bottom: 10px; }
    .header { background-color: #2e7d32; padding: 15px; border-radius: 10px; color: white; text-align: center; margin-bottom: 25px; }
    div[data-testid="stExpander"] { border: 1px solid #2e7d32; border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

if 'pagina' not in st.session_state:
    st.session_state.pagina = 'Home'

def mudar_pagina(nome):
    st.session_state.pagina = nome

st.markdown('<div class="header"><h1>Aplicativo | Gestão de Pilotos</h1><p>Qualidade Agrícola - COA</p></div>', unsafe_allow_html=True)

# 1. HOME
if st.session_state.pagina == 'Home':
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔔\nVencimentos"): mudar_pagina('Vencimentos')
        if st.button("🚜\nFrotas"): mudar_pagina('Frotas')
    with col2:
        if st.button("🔄\nSincronização"): st.toast("Sincronizando...")
        if st.button("🖥️\nMonitores"): mudar_pagina('Monitores')
    with col3:
        if st.button("📝\nCadastros"): mudar_pagina('Cadastro')
        if st.button("📡\nAntenas"): mudar_pagina('Antenas')

# 2. TELA DE CADASTRO (NOMES AJUSTADOS PARA image_fd0667.png)
elif st.session_state.pagina == 'Cadastro':
    if st.button("⬅️ Voltar"): mudar_pagina('Home')
    st.subheader("📝 Novo Cadastro")
    
    with st.form("form_cadastro"):
        tipo = st.selectbox("Tipo", ["Monitor", "Antena"])
        n_serie = st.text_input("Número de Série")
        modelo = st.text_input("Modelo")
        situacao = st.selectbox("Situação", ["Estoque", "Em Uso", "Manutenção"])
        frota = st.text_input("Frota ID")
        vencimento = st.date_input("Vencimento do Sinal", value=date.today())
        
        if st.form_submit_button("Salvar no Banco"):
            # AQUI FOI REMOVIDO O 'monitor_id' POIS NÃO EXISTE NO SEU PRINT
            dados = {
                "numero_serie": n_serie,
                "tipo": tipo,
                "modelo": modelo,
                "situacao": situacao,
                "frota_id": frota, 
                "data_vencimento_licenca": str(vencimento)
            }
            try:
                supabase.table("ativos").insert(dados).execute()
                st.success("✅ Cadastrado!")
            except Exception as e:
                st.error(f"Erro: {e}")

# 3. TELA DE VENCIMENTOS
elif st.session_state.pagina == 'Vencimentos':
    if st.button("⬅️ Voltar"): mudar_pagina('Home')
    res = supabase.table("ativos").select("*").execute()
    if res.data:
        df = pd.DataFrame(res.data)
        for _, row in df.iterrows():
            dv = datetime.strptime(row['data_vencimento_licenca'], '%Y-%m-%d').date()
            cor = "red" if dv <= date.today() else "green"
            st.markdown(f"**Série:** `{row['numero_serie']}` | Vence: <span style='color:{cor}'>{dv.strftime('%d/%m/%Y')}</span>", unsafe_allow_html=True)
            st.divider()

# 4. MONITORES / ANTENAS
elif st.session_state.pagina in ['Monitores', 'Antenas']:
    if st.button("⬅️ Voltar"): mudar_pagina('Home')
    tipo_filtro = "Monitor" if st.session_state.pagina == 'Monitores' else "Antena"
    res = supabase.table("ativos").select("*").eq("tipo", tipo_filtro).execute()
    if res.data:
        st.dataframe(pd.DataFrame(res.data)[['numero_serie', 'modelo', 'situacao', 'frota_id']])

# 6. TELA DE FROTAS (NOMES AJUSTADOS PARA image_fd06a0.png)
elif st.session_state.pagina == 'Frotas':
    if st.button("⬅️ Voltar"): mudar_pagina('Home')
    with st.expander("➕ Adicionar Máquina"):
        c1, c2 = st.columns(2)
        cod = c1.text_input("Código da Frota")
        mod_m = c2.text_input("Modelo")
        tipo_m = st.selectbox("Tipo", ["Trator", "Colhedora"])
        if st.button("Salvar"):
            supabase.table("frotas").insert({"codigo_frota": cod, "modelo": mod_m, "tipo_equipamento": tipo_m}).execute()
            st.rerun()

    res = supabase.table("frotas").select("*").execute()
    if res.data:
        st.table(pd.DataFrame(res.data)[['codigo_frota', 'modelo', 'tipo_equipamento']])
