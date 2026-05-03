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

# --- BUSCAS INTELIGENTES (INTEGRAÇÃO DE TABELAS) ---

def get_info_antena(serie):
    """Busca modelo_antena e marca_sinal na tabela Antenas."""
    try:
        supabase = get_client()
        res = supabase.table("Antenas").select("modelo_antena, marca_sinal").eq("antena_serie", serie).maybe_single().execute()
        return res.data
    except:
        return None

def get_vencimento_licenca(serie):
    """Busca data_vencimento na tabela Licencas_Validades."""
    try:
        supabase = get_client()
        res = supabase.table("Licencas_Validades").select("data_vencimento").eq("licenca", serie).maybe_single().execute()
        return res.data.get("data_vencimento") if res.data else None
    except:
        return None

def get_info_monitor(serie):
    """Busca modelo_monitor na tabela Monitores."""
    try:
        supabase = get_client()
        res = supabase.table("Monitores").select("modelo_monitor").eq("monitor_serie", serie).maybe_single().execute()
        return res.data
    except:
        return None

# --- BUSCAS GERAIS ---

@st.cache_data(ttl=60)
def get_equipamentos():
    try:
        supabase = get_client()
        return supabase.table("Equipamentos").select("*").order("codigo_do_equipamento").execute().data or []
    except Exception as e:
        st.error(f"Erro: {e}")
        return []

def get_itens_disponiveis(tabela, coluna_serie, valor_atual=None):
    """Mantém a lógica de disponibilidade para não duplicar itens na frota."""
    try:
        supabase = get_client()
        todos = supabase.table(tabela).select("*").execute().data or []
        col_vinc = "antena" if tabela == "Antenas" else ("monitor" if tabela == "Monitores" else "nav")
        
        em_uso = supabase.table("Equipamentos").select(col_vinc).execute().data
        series_em_uso = [x[col_vinc] for x in em_uso if x[col_vinc]]

        return [item for item in todos if item[coluna_serie] not in series_em_uso or item[coluna_serie] == valor_atual]
    except Exception as e:
        st.error(f"Erro na disponibilidade: {e}")
        return []

# --- CRUD (CREATE, UPDATE) ---

def add_registro(tabela, dados):
    """Garante que os nomes das colunas nos 'dados' batam com o banco."""
    try:
        supabase = get_client()
        supabase.table(tabela).insert(dados).execute()
        st.cache_data.clear()
        return True
    except Exception as e:
        st.error(f"Erro ao salvar no banco: {e}")
        return False

def update_equipamento(equip_id, dados):
    """Atualiza a tabela Equipamentos com as infos amarradas."""
    try:
        supabase = get_client()
        supabase.table("Equipamentos").update(dados).eq("id", equip_id).execute()
        st.cache_data.clear()
        return True
    except Exception as e:
        st.error(f"Erro ao atualizar frota: {e}")
        return False
@st.cache_data(ttl=60)
def get_licencas_simples():
    """Busca todas as licenças da tabela Licencas_Validades ordenadas por vencimento."""
    try:
        supabase = get_client()
        # Ordenado por data para que os que vencem antes apareçam primeiro
        res = supabase.table("Licencas_Validades").select("*").order("data_vencimento").execute()
        return res.data or []
    except Exception as e:
        st.error(f"Erro ao buscar licenças: {e}")
        return []
