import streamlit as st
import pandas as pd
from supabase import create_client, Client
from datetime import datetime, date

# --- 1. CONEXÃO COM O BANCO ---
# Certifique-se de que estas credenciais estão corretas
SUPABASE_URL = "https://wjejxlnclrdpigpratrt.supabase.co"
SUPABASE_KEY = "sb_publishable_TZrkyrcPDgaqcgTcZcmvPQ_UofXX50m"

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    st.error(f"Erro Crítico de Conexão: {e}")

# --- 2. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Gestão COA", page_icon="🚜", layout="centered")

# CSS para Layout Mobile (Botões Grandes e Cards Limpos)
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { 
        width: 100%; border-radius: 12px; height: 75px; 
        background-color: #2e7d32; color: white; font-weight: bold; 
        font-size: 16px; border: none; box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
        margin-bottom: 5px;
    }
    .header-container {
        text-align: center; padding: 15px;
        background-color: #ffffff; border-radius: 12px;
        border-bottom: 4px solid #2e7d32; margin-bottom: 20px;
    }
    .card-equip {
        background-color: #ffffff; padding: 12px; border-radius: 10px;
        border-left: 6px solid #2e7d32; margin-bottom: 5px;
        box-shadow: 0px 2px 4px rgba(0,0,0,0.05);
    }
    .val-expirada { color: #d32f2f; font-weight: bold; }
    .val-ok { color: #388e3c; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- 3. LOGICA DE NAVEGAÇÃO ---
if 'pagina' not in st.session_state:
    st.session_state.pagina = 'Home'

def mudar_pagina(nome):
    st.session_state.pagina = nome
    st.rerun()

# --- 4. CABEÇALHO FIXO ---
st.markdown("""
    <div class="header-container">
        <h2 style="margin:0;">🚜 Gestão de Pilotos</h2>
        <small style="color:#666;">COA - Peterson Santos</small>
    </div>
""", unsafe_allow_html=True)

# --- 5. TELAS DO APLICATIVO ---

# --- TELA: HOME ---
if st.session_state.pagina == 'Home':
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔔\nVencimentos"): mudar_pagina('Vencimentos')
        if st.button("🚜\nFrotas"): mudar_pagina('Frotas')
    with col2:
        if st.button("📝\nCadastros"): mudar_pagina('Cadastro')
        if st.button("🔄\nAtualizar"): st.rerun()

# --- TELA: FROTAS ---
elif st.session_state.pagina == 'Frotas':
    if st.button("⬅️ Voltar"): mudar_pagina('Home')
    
    busca = st.text_input("🔍 Pesquisar Frota...", placeholder="Ex: 1218")
    
    try:
        # Busca na tabela Equipamentos (E maiúsculo conforme print)
        res = supabase.table("Equipamentos").select("*").order("codigo_do_equipamento").execute()
        
        if res.data:
            df = pd.DataFrame(res.data)
            if busca:
                df = df[df['codigo_do_equipamento'].astype(str).str.contains(busca)]
            
            for _, row in df.iterrows():
                c1, c2 = st.columns([4, 1])
                with c1:
                    st.markdown(f"""
                    <div class="card-equip">
                        <b>Frota: {row.get('codigo_do_equipamento', '---')}</b><br>
                        <span style="font-size:12px; color:#555;">{row.get('nome', 'N/A')}</span><br>
                        <span style="font-size:11px; color:#888;">📡 {row.get('antena', 'N/A')} | 🖥️ {row.get('monitor', 'N/A')}</span>
                    </div>
                    """, unsafe_allow_html=True)
                with c2:
                    # Botão pequeno de engrenagem para editar
                    if st.button("⚙️", key=f"edit_{row.get('id')}"):
                        st.session_state.edit_id = row
                        mudar_pagina('Editar')
        else:
            st.info("Nenhum dado encontrado na tabela 'Equipamentos'.")
    except Exception as e:
        st.error(f"Erro ao carregar Equipamentos: {e}")

# --- TELA: VENCIMENTOS ---
elif st.session_state.pagina == 'Vencimentos':
    if st.button("⬅️ Voltar"): mudar_pagina('Home')
    st.subheader("Prazos de Sinais")
    
    try:
        res = supabase.table("Licencias_Validades").select("*").execute()
        if res.data:
            for item in res.data:
                data_str = item.get('data_vencimento')
                try:
                    dt_venc = datetime.strptime(data_str, "%Y-%m-%d").date()
                    status_classe = "val-expirada" if dt_venc < date.today() else "val-ok"
                    venc_formatado = dt_venc.strftime('%d/%m/%Y')
                except:
                    status_classe = ""
                    venc_formatado = "Data Inválida"

                st.markdown(f"""
                <div style="padding:10px; border-bottom:1px solid #eee;">
                    <small>📡 Licença:</small> <b>{item.get('licenca', '---')}</b><br>
                    <small>📅 Vencimento:</small> <span class="{status_classe}">{venc_formatado}</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Sem licenças cadastradas.")
    except Exception as e:
        st.error(f"Erro ao carregar Licenças: {e}")

# --- TELA: EDIÇÃO ---
elif st.session_state.pagina == 'Editar':
    item = st.session_state.edit_id
    if st.button("⬅️ Cancelar"): mudar_pagina('Frotas')
    
    st.subheader(f"Editar Frota {item.get('codigo_do_equipamento')}")
    
    with st.form("form_update"):
        novo_nome = st.text_input("Modelo/Nome", value=item.get('nome', ''))
        nova_antena = st.text_input("Série Antena", value=item.get('antena', ''))
        novo_monitor = st.text_input("Série Monitor", value=item.get('monitor', ''))
        
        if st.form_submit_button("✅ Salvar Alterações"):
            try:
                supabase.table("Equipamentos").update({
                    "nome": novo_nome,
                    "antena": nova_antena,
                    "monitor": novo_monitor
                }).eq("id", item['id']).execute()
                
                st.success("Dados salvos com sucesso!")
                mudar_pagina('Frotas')
            except Exception as e:
                st.error(f"Erro ao salvar: {e}")
