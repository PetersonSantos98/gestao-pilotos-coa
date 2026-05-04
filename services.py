import streamlit as st
from supabase import create_client

def get_config():
    """Recupera as credenciais do Supabase."""
    try:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
    except:
        # Fallback para ambiente de desenvolvimento local
        url = "https://wjejxlnclrdpigpratrt.supabase.co"
        key = "sb_publishable_TZrkyrcPDgaqcgTcZcmvPQ_UofXX50m"
    return url, key

@st.cache_resource
def get_client():
    """Cria e armazena o cliente de conexão com o banco."""
    url, key = get_config()
    return create_client(url, key)

# --- SISTEMA DE AUTENTICAÇÃO ---

def verificar_login(usuario, senha):
    """Verifica se as credenciais existem na tabela 'usuarios'."""
    try:
        supabase = get_client()
        # Ajustado para a coluna 'usuarios' (plural) conforme seu banco de dados
        res = supabase.table("usuarios").select("*").eq("usuarios", usuario).eq("senha", senha).execute()
        return len(res.data) > 0
    except Exception as e:
        st.error(f"Erro na autenticação: {e}")
        return False

# --- BUSCAS GERAIS ---

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

# --- LÓGICA DE DISPONIBILIDADE (CORRIGIDA) ---

def get_itens_disponiveis(tabela, coluna_serie, valor_atual=None):
    """
    Retorna apenas itens que NÃO estão vinculados a nenhuma frota.
    Garante exclusividade: se o item está em um trator, não aparece para outro.
    """
    try:
        supabase = get_client()
        
        # 1. Busca todos os componentes cadastrados (Antenas, Monitores ou Navs)
        todos_itens = get_tabela_simples(tabela)
        
        # 2. Busca todos os registros da frota para identificar o que já está em uso
        res_vinculados = supabase.table("Equipamentos").select("antena, monitor, nav").execute()
        
        # Criamos um conjunto de séries ocupadas para busca rápida
        series_ocupadas = set()
        for eq in res_vinculados.data:
            if eq.get('antena'): series_ocupadas.add(str(eq['antena']))
            if eq.get('monitor'): series_ocupadas.add(str(eq['monitor']))
            if eq.get('nav'): series_ocupadas.add(str(eq['nav']))

        # 3. Filtra a lista: mantém se não estiver ocupado OU se for o item que já pertence ao trator atual
        disponiveis = [
            item for item in todos_itens 
            if str(item[coluna_serie]) not in series_ocupadas 
            or str(item[coluna_serie]) == str(valor_atual)
        ]
        
        return disponiveis
    except Exception as e:
        st.error(f"Erro ao filtrar disponibilidade: {e}")
        return []

# --- CRUD (Inserção e Atualização) ---

def add_registro(tabela, dados):
    """Insere um novo registro em qualquer tabela."""
    try:
        supabase = get_client()
        supabase.table(tabela).insert(dados).execute()
        st.cache_data.clear() # Limpa o cache para atualizar as listas
        return True
    except Exception as e:
        st.error(f"Erro ao inserir no banco: {e}")
        return False

def update_equipamento(equip_id, dados):
    """Atualiza os dados de um trator da frota."""
    try:
        supabase = get_client()
        supabase.table("Equipamentos").update(dados).eq("id", equip_id).execute()
        st.cache_data.clear() # Limpa o cache para atualizar as listas
        return True
    except Exception as e:
        st.error(f"Erro ao atualizar equipamento: {e}")
        return False
