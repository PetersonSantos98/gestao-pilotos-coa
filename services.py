import streamlit as st
from supabase import create_client

def get_config():
    try:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
    except:
        url = "https://wjejxlnclrdpigpratrt.supabase.co"
        key = "sb_publishable_TZrkyrcPDgaqcgTcZcmvPQ_UofXX50m"
    return url, key

@st.cache_resource
def get_client():
    url, key = get_config()
    return create_client(url, key)

# --- BUSCA EQUIPAMENTOS ---
@st.cache_data(ttl=60)
def get_equipamentos():
    supabase = get_client()
    # Busca dados da tabela principal
    res = supabase.table("Equipamentos").select("*").order("codigo_do_equipamento").execute()
    return res.data or []

# --- BUSCA LICENÇAS COM RELAÇÃO (ITEM 3) ---
@st.cache_data(ttl=60)
def get_licencas_com_equipamento():
    supabase = get_client()
    # Cruzamento de Licencas_Validades com Equipamentos
    res = supabase.table("Licencas_Validades").select("*, Equipamentos(codigo_do_equipamento, nome)").execute()
    return res.data or []

# --- BUSCA ITENS DISPONÍVEIS (ITEM 1) ---
def get_itens_disponiveis(tabela, coluna_serie, valor_atual=None):
    supabase = get_client()
    # Busca todos os itens da tabela mestre (ex: Antenas)
    todos = supabase.table(tabela).select("*").execute().data or []
    
    # Busca o que já está em uso na tabela Equipamentos (na coluna correspondente)
    col_vinc = "antena" if tabela == "Antenas" else ("monitor" if tabela == "Monitores" else "nav")
    em_uso = supabase.table("Equipamentos").select(col_vinc).execute().data
    series_em_uso = [x[col_vinc] for x in em_uso if x[col_vinc]]

    # Filtra: Mantém se não estiver em uso OU se for o valor que já está no equipamento atual
    disponiveis = [item for item in todos if item[coluna_serie] not in series_em_uso or item[coluna_serie] == valor_atual]
    return disponiveis

def update_equipamento(equip_id, dados):
    supabase = get_client()
    supabase.table("Equipamentos").update(dados).eq("id", equip_id).execute()
    st.cache_data.clear()

def get_tabela_simples(tabela):
    supabase = get_client()
    return supabase.table(tabela).select("*").execute().data or []
