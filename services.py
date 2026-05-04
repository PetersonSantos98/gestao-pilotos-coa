import streamlit as st
from supabase import create_client

def get_config():
    try:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
    except:
        # Fallback para desenvolvimento
        url = "https://wjejxlnclrdpigpratrt.supabase.co"
        key = "sb_publishable_TZrkyrcPDgaqcgTcZcmvPQ_UofXX50m"
    return url, key

@st.cache_resource
def get_client():
    url, key = get_config()
    return create_client(url, key)

# --- SISTEMA DE AUTENTICAÇÃO ---

def verificar_login(usuario, senha):
    """Verifica se as credenciais existem na tabela 'usuarios'."""
    try:
        supabase = get_client()
        res = supabase.table("usuarios").select("*").eq("usuario", usuario).eq("senha", senha).execute()
        return len(res.data) > 0
    except Exception as e:
        st.error(f"Erro na autenticação: {e}")
        return False

# --- BUSCAS GERAIS ---

def get_tabela_simples(tabela):
    try:
        supabase = get_client()
        return supabase.table(tabela).select("*").execute().data or []
    except Exception as e:
        st.error(f"Erro na tabela {tabela}: {e}")
        return []

@st.cache_data(ttl=60)
def get_equipamentos():
    try:
        supabase = get_client()
        return supabase.table("Equipamentos").select("*").order("codigo_do_equipamento").execute().data or []
    except Exception as e:
        st.error(f"Erro ao buscar equipamentos: {e}")
        return []

@st.cache_data(ttl=60)
def get_licencas_simples():
    try:
        supabase = get_client()
        return supabase.table("Licencas_Validades").select("*").order("data_vencimento").execute().data or []
    except Exception as e:
        st.error(f"Erro ao buscar licenças: {e}")
        return []

# --- CRUD (Inserção e Atualização) ---

def add_registro(tabela, dados):
    try:
        supabase = get_client()
        supabase.table(tabela).insert(dados).execute()
        st.cache_data.clear()
        return True
    except Exception as e:
        st.error(f"Erro ao inserir no banco: {e}")
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
