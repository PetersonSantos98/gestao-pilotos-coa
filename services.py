import streamlit as st
from supabase import create_client

def get_config():
    """Recupera as credenciais do Supabase."""
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
    """Cria o cliente de conexão com o Supabase."""
    url, key = get_config()
    return create_client(url, key)

# --- BUSCAS DE DADOS (COM INTELIGÊNCIA DE STATUS) ---

@st.cache_data(ttl=10)
def get_equipamentos():
    """Busca a frota e anexa os modelos das peças via Python para evitar erros de relacionamento."""
    try:
        supabase = get_client()
        # Busca básica na tabela de Equipamentos
        res = supabase.table("Equipamentos").select("id, codigo_do_equipamento, nome, antena, monitor, nav").order("codigo_do_equipamento").execute()
        
        # Busca dados auxiliares das peças
        antenas = {a['antena_serie']: a for a in supabase.table("Antenas").select("*").execute().data}
        monitores = {m['monitor_serie']: m for m in supabase.table("Monitores").select("*").execute().data}
        
        dados_completos = []
        for eq in res.data:
            # Vincula os dados das peças ao trator
            eq['Antenas'] = antenas.get(eq['antena'], {})
            eq['Monitores'] = monitores.get(eq['monitor'], {})
            dados_completos.append(eq)
            
        return dados_completos
    except Exception as e:
        st.error(f"Erro ao buscar frota: {e}")
        return []

@st.cache_data(ttl=10)
def get_itens_com_status(tabela, coluna_serie):
    """
    Busca todas as peças e identifica quais estão em uso na frota.
    Resolve o problema das peças aparecerem todas como 'disponíveis'.
    """
    try:
        supabase = get_client()
        # 1. Busca todas as peças da tabela (Antenas, Monitores ou Navs)
        pecas = supabase.table(tabela).select("*").execute().data or []
        
        # 2. Busca o que está registrado na frota atual
        frota = supabase.table("Equipamentos").select("antena, monitor, nav").execute().data
        
        # Criamos um conjunto de séries ocupadas para comparação rápida
        series_ocupadas = set()
        for trator in frota:
            if trator.get('antena'): series_ocupadas.add(str(trator['antena']))
            if trator.get('monitor'): series_ocupadas.add(str(trator['monitor']))
            if trator.get('nav'): series_ocupadas.add(str(trator['nav']))

        # 3. Define o status de disponibilidade
        for p in pecas:
            p['disponivel'] = str(p.get(coluna_serie)) not in series_ocupadas
            
        return pecas
    except Exception as e:
        st.error(f"Erro ao processar status: {e}")
        return []

@st.cache_data(ttl=10)
def get_licencas_simples():
    """Busca as licenças para a página de vencimentos."""
    try:
        supabase = get_client()
        res = supabase.table("Licencas_Validades").select("*").order("data_vencimento").execute()
        return res.data or []
    except Exception as e:
        st.error(f"Erro ao buscar licenças: {e}")
        return []

@st.cache_data(ttl=10)
def get_tabela_simples(tabela):
    """Busca dados brutos de qualquer tabela auxiliar."""
    try:
        supabase = get_client()
        return supabase.table(tabela).select("*").execute().data or []
    except Exception as e:
        st.error(f"Erro na tabela {tabela}: {e}")
        return []

# --- OPERAÇÕES DE BANCO (CRUD) ---

def get_itens_disponiveis(tabela, coluna_serie, valor_atual=None):
    """Filtra itens para o SELECT de edição, permitindo a peça atual do trator."""
    try:
        todos = get_itens_com_status(tabela, coluna_serie)
        return [i for i in todos if i['disponivel'] or str(i[coluna_serie]) == str(valor_atual)]
    except:
        return []

def add_registro(tabela, dados):
    """Insere novos registros (Antenas, Monitores, etc)."""
    try:
        supabase = get_client()
        supabase.table(tabela).insert(dados).execute()
        st.cache_data.clear()
        return True
    except Exception as e:
        st.error(f"Erro ao inserir: {e}")
        return False

def update_equipamento(equip_id, dados):
    """Atualiza o equipamento filtrando apenas colunas que existem na tabela."""
    try:
        supabase = get_client()
        colunas_validas = ["nome", "antena", "monitor", "nav"]
        payload = {k: v for k, v in dados.items() if k in colunas_validas}
        
        supabase.table("Equipamentos").update(payload).eq("id", equip_id).execute()
        st.cache_data.clear()
        return True
    except Exception as e:
        st.error(f"Erro ao atualizar: {e}")
        return False

def verificar_login(usuario, senha):
    """Validação de acesso."""
    try:
        supabase = get_client()
        res = supabase.table("usuarios").select("*").eq("usuarios", usuario).eq("senha", senha).execute()
        return len(res.data) > 0
    except:
        return False
