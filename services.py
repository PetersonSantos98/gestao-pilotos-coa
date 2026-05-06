import streamlit as st
from supabase import create_client

def get_config():
    """Recupera as credenciais do Supabase."""
    try:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
    except:
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
    try:
        supabase = get_client()
        res = supabase.table("usuarios").select("*").eq("usuarios", usuario).eq("senha", senha).execute()
        return len(res.data) > 0
    except Exception as e:
        st.error(f"Erro na autenticação: {e}")
        return False

# --- BUSCA INTELIGENTE (COM RELACIONAMENTOS) ---

@st.cache_data(ttl=60)
def get_equipamentos():
    """
    Busca a frota completa trazendo AUTOMATICAMENTE os modelos e vencimentos
    através das Foreign Keys configuradas no banco.
    """
    try:
        supabase = get_client()
        # Esta query pede os dados do trator + dados das tabelas vinculadas
        query = """
            id,
            codigo_do_equipamento,
            nome,
            antena,
            Antenas (
                modelo_antena,
                marca_sinal,
                Licencas_Validades (data_vencimento)
            ),
            monitor,
            Monitores (
                modelo_monitor,
                Licencas_Validades (data_vencimento)
            ),
            nav
        """
        res = supabase.table("Equipamentos").select(query).order("codigo_do_equipamento").execute()
        return res.data or []
    except Exception as e:
        st.error(f"Erro ao buscar frota sincronizada: {e}")
        return []

# --- DISPONIBILIDADE E AUXILIARES ---

def get_tabela_simples(tabela):
    try:
        supabase = get_client()
        return supabase.table(tabela).select("*").execute().data or []
    except Exception as e:
        st.error(f"Erro na tabela {tabela}: {e}")
        return []

def get_itens_disponiveis(tabela, coluna_serie, valor_atual=None):
    """Filtra itens que não estão em uso em nenhum trator."""
    try:
        supabase = get_client()
        todos_itens = get_tabela_simples(tabela)
        
        # Verifica quem já está ocupado na frota
        res_vinculados = supabase.table("Equipamentos").select("antena, monitor, nav").execute()
        
        series_ocupadas = set()
        for eq in res_vinculados.data:
            if eq.get('antena'): series_ocupadas.add(str(eq['antena']))
            if eq.get('monitor'): series_ocupadas.add(str(eq['monitor']))
            if eq.get('nav'): series_ocupadas.add(str(eq['nav']))

        return [
            item for item in todos_itens 
            if str(item[coluna_serie]) not in series_ocupadas 
            or str(item[coluna_serie]) == str(valor_atual)
        ]
    except Exception as e:
        st.error(f"Erro na disponibilidade: {e}")
        return []

# --- CRUD ATUALIZADO ---

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
    """
    Atualiza o trator. Como o banco é relacional, enviamos apenas 
    os números de série. O Supabase cuida do resto.
    """
    try:
        supabase = get_client()
        # Removemos chaves vazias para não sobrescrever com NULL por erro
        dados_limpos = {k: v for k, v in dados.items() if v is not None}
        
        supabase.table("Equipamentos").update(dados_limpos).eq("id", equip_id).execute()
        st.cache_data.clear() 
        return True
    except Exception as e:
        st.error(f"Erro ao atualizar trator: {e}")
        return False
