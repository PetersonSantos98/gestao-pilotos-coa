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

# --- BUSCAS GERAIS (Para listagens e filtros) ---

def get_tabela_simples(tabela):
    """Busca todos os dados de uma tabela específica."""
    try:
        supabase = get_client()
        return supabase.table(tabela).select("*").execute().data or []
    except Exception as e:
        st.error(f"Erro na tabela {tabela}: {e}")
        return []

@st.cache_data(ttl=60)
def get_equipamentos():
    """Busca a frota completa ordenada pelo prefixo."""
    try:
        supabase = get_client()
        return supabase.table("Equipamentos").select("*").order("codigo_do_equipamento").execute().data or []
    except Exception as e:
        st.error(f"Erro ao buscar equipamentos: {e}")
        return []

@st.cache_data(ttl=60)
def get_licencas_simples():
    """Busca licenças para a página de vencimentos."""
    try:
        supabase = get_client()
        return supabase.table("Licencas_Validades").select("*").order("data_vencimento").execute().data or []
    except Exception as e:
        st.error(f"Erro ao buscar licenças: {e}")
        return []

# --- LÓGICA DE DISPONIBILIDADE ---

def get_itens_disponiveis(tabela, coluna_serie, valor_atual=None):
    """Retorna itens que não estão em uso em nenhum equipamento."""
    try:
        supabase = get_client()
        todos = get_tabela_simples(tabela)
        col_vinc = "antena" if tabela == "Antenas" else ("monitor" if tabela == "Monitores" else "nav")
        
        em_uso = supabase.table("Equipamentos").select(col_vinc).execute().data
        series_em_uso = [x[col_vinc] for x in em_uso if x[col_vinc]]

        return [item for item in todos if item[coluna_serie] not in series_em_uso or item[coluna_serie] == valor_atual]
    except Exception as e:
        st.error(f"Erro na disponibilidade: {e}")
        return []

# --- CRUD (Inserção e Atualização) ---

def add_registro(tabela, dados):
    """Insere dados respeitando as colunas do banco (usado em Componentes)."""
    try:
        supabase = get_client()
        supabase.table(tabela).insert(dados).execute()
        st.cache_data.clear()
        return True
    except Exception as e:
        st.error(f"Erro ao inserir no banco: {e}")
        return False

def update_equipamento(equip_id, dados):
    """Atualiza os dados da frota (usado em Editar)."""
    try:
        supabase = get_client()
        supabase.table("Equipamentos").update(dados).eq("id", equip_id).execute()
        st.cache_data.clear()
        return True
    except Exception as e:
        st.error(f"Erro ao atualizar: {e}")
        return False
