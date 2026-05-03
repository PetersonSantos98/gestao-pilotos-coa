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

# --- BUSCAS COM ORDENAÇÃO ---
@st.cache_data(ttl=60)
def get_equipamentos():
    try:
        supabase = get_client()
        res = supabase.table("Equipamentos").select("*").order("codigo_do_equipamento").execute()
        return res.data or []
    except Exception as e:
        st.error(f"Erro ao buscar equipamentos: {e}")
        return []

@st.cache_data(ttl=60)
def get_licencas_simples():
    try:
        supabase = get_client()
        # Ordenado por data: vencidos há mais tempo aparecem primeiro
        res = supabase.table("Licencas_Validades").select("*").order("data_vencimento").execute()
        return res.data or []
    except Exception as e:
        st.error(f"Erro ao buscar licenças: {e}")
        return []

def get_tabela_simples(tabela):
    try:
        supabase = get_client()
        return supabase.table(tabela).select("*").execute().data or []
    except Exception as e:
        st.error(f"Erro na tabela {tabela}: {e}")
        return []

# --- LÓGICA DE DISPONIBILIDADE (O QUE FAVA FALTA) ---
def get_itens_disponiveis(tabela, coluna_serie, valor_atual=None):
    try:
        supabase = get_client()
        todos = get_tabela_simples(tabela)
        col_vinc = "antena" if tabela == "Antenas" else ("monitor" if tabela == "Monitores" else "nav")
        
        em_uso = supabase.table("Equipamentos").select(col_vinc).execute().data
        series_em_uso = [x[col_vinc] for x in em_uso if x[col_vinc]]

        disponiveis = [
            item for item in todos 
            if item[coluna_serie] not in series_em_uso or item[coluna_serie] == valor_atual
        ]
        return disponiveis
    except Exception as e:
        st.error(f"Erro ao validar disponibilidade: {e}")
        return []

# --- CRUD (CREATE, UPDATE) ---
def add_registro(tabela, dados):
    try:
        supabase = get_client()
        supabase.table(tabela).insert(dados).execute()
        st.cache_data.clear()
        return True
    except Exception as e:
        st.error(f"Erro ao inserir: {e}")
        return False

def update_equipamento(equip_id, dados):
    try:
        supabase = get_client()
        supabase.table("Equipamentos").update(dados).eq("id", equip_id).execute()
        st.cache_data.clear()
        return True
    except Exception as e:
        st.error(f"Erro ao atualizar: {e}")
        return False
