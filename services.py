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
        res = supabase.table("usuarios").select("*").eq("usuarios", usuario).eq("senha", senha).execute()
        return len(res.data) > 0
    except Exception as e:
        st.error(f"Erro na autenticação: {e}")
        return False

# --- BUSCAS GERAIS E RELACIONAIS ---

@st.cache_data(ttl=60)
def get_equipamentos():
    """
    Busca a frota trazendo AUTOMATICAMENTE os modelos das tabelas vinculadas.
    Nota: A data de vencimento é cruzada via código para evitar erros de FK.
    """
    try:
        supabase = get_client()
        # Query limpa: Trator + Modelo da Antena + Modelo do Monitor
        query = """
            id,
            codigo_do_equipamento,
            nome,
            antena,
            Antenas (
                modelo_antena,
                marca_sinal
            ),
            monitor,
            Monitores (
                modelo_monitor
            ),
            nav
        """
        res = supabase.table("Equipamentos").select(query).order("codigo_do_equipamento").execute()
        return res.data or []
    except Exception as e:
        st.error(f"Erro ao buscar frota sincronizada: {e}")
        return []

@st.cache_data(ttl=60)
def get_licencas_simples():
    """Busca todas as licenças para a página de vencimentos e cruzamento de dados."""
    try:
        supabase = get_client()
        res = supabase.table("Licencas_Validades").select("*").order("data_vencimento").execute()
        return res.data or []
    except Exception as e:
        st.error(f"Erro ao buscar licenças: {e}")
        return []

def get_tabela_simples(tabela):
    """Busca todos os dados de uma tabela específica (Antenas, Monitores, Navs)."""
    try:
        supabase = get_client()
        return supabase.table(tabela).select("*").execute().data or []
    except Exception as e:
        st.error(f"Erro na tabela {tabela}: {e}")
        return []

# --- LÓGICA DE DISPONIBILIDADE ---

def get_itens_disponiveis(tabela, coluna_serie, valor_atual=None):
    """
    Retorna itens que NÃO estão vinculados a nenhuma frota.
    Permite que o item atual do trator apareça na lista de edição.
    """
    try:
        supabase = get_client()
        todos_itens = get_tabela_simples(tabela)
        
        # Busca o que já está em uso
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
        st.error(f"Erro ao filtrar disponibilidade: {e}")
        return []

# --- CRUD (Inserção e Atualização) ---

def add_registro(tabela, dados):
    """Insere um novo registro em qualquer tabela."""
    try:
        supabase = get_client()
        supabase.table(tabela).insert(dados).execute()
        st.cache_data.clear()
        return True
    except Exception as e:
        st.error(f"Erro ao inserir no banco: {e}")
        return False

def update_equipamento(equip_id, dados):
    """
    Atualiza os dados de um trator.
    Envia apenas as colunas que restaram na tabela Equipamentos (nome e séries).
    """
    try:
        supabase = get_client()
        # Garante que não estamos enviando colunas que foram deletadas do banco
        colunas_permitidas = ["nome", "antena", "monitor", "nav"]
        payload = {k: v for k, v in dados.items() if k in colunas_permitidas}
        
        supabase.table("Equipamentos").update(payload).eq("id", equip_id).execute()
        st.cache_data.clear() 
        return True
    except Exception as e:
        st.error(f"Erro ao atualizar equipamento: {e}")
        return False
