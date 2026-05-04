import streamlit as st
from supabase import create_client

def get_config():
    try:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
    except:
        # Fallback para chaves manuais (Development)
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
        # Alterado de "usuario" para "usuarios" para bater com seu banco
        res = supabase.table("usuarios").select("*").eq("usuarios", usuario).eq("senha", senha).execute()
        return len(res.data) > 0
    except Exception as e:
        st.error(f"Erro na autenticação: {e}")
        return False

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
        
        # Define qual coluna olhar na tabela Equipamentos com base na tabela de origem
        vinc_map = {"Antenas": "antena", "Monitores": "monitor", "NAVs": "nav"}
        col_vinc = vinc_map.get(tabela)
        
        if not col_vinc:
            return todos

        em_uso = supabase.table("Equipamentos").select(col_vinc).execute().data
        series_em_uso = [str(x[col_vinc]) for x in em_uso if x[col_vinc]]

        return [item for item in todos if str(item[coluna_serie]) not in series_em_uso or str(item[coluna_serie]) == str(valor_atual)]
    except Exception as e:
        st.error(f"Erro na disponibilidade: {e}")
        return []

# --- CRUD (Inserção e Atualização) ---

def add_registro(tabela, dados):
    """Insere dados respeitando as colunas do banco."""
    try:
        supabase = get_client()
        supabase.table(tabela).insert(dados).execute()
        st.cache_data.clear() # Limpa o cache para refletir a mudança
        return True
    except Exception as e:
        st.error(f"Erro ao inserir no banco: {e}")
        return False

def update_equipamento(equip_id, dados):
    """Atualiza os dados da frota."""
    try:
        supabase = get_client()
        supabase.table("Equipamentos").update(dados).eq("id", equip_id).execute()
        st.cache_data.clear() # Limpa o cache para refletir a mudança
        return True
    except Exception as e:
        st.error(f"Erro ao atualizar: {e}")
        return False
