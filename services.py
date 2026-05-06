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
    """Cria o cliente de conexão."""
    url, key = get_config()
    return create_client(url, key)

# --- BUSCAS DE DADOS ---

@st.cache_data(ttl=10)
def get_equipamentos():
    """Busca a frota e anexa modelos manualmente para evitar erros de relacionamento no banco."""
    try:
        supabase = get_client()
        # Busca básica na tabela de frotas
        res = supabase.table("Equipamentos").select("id, codigo_do_equipamento, nome, antena, monitor, nav").order("codigo_do_equipamento").execute()
        
        # Busca dados auxiliares para fazer o 'join' no Python
        antenas = {a['antena_serie']: a for a in supabase.table("Antenas").select("*").execute().data}
        monitores = {m['monitor_serie']: m for m in supabase.table("Monitores").select("*").execute().data}
        
        dados_completos = []
        for eq in res.data:
            # Anexa as informações das outras tabelas se o número de série existir
            eq['Antenas'] = antenas.get(eq['antena'], {})
            eq['Monitores'] = monitores.get(eq['monitor'], {})
            dados_completos.append(eq)
            
        return dados_completos
    except Exception as e:
        st.error(f"Erro ao buscar frota: {e}")
        return []

@st.cache_data(ttl=10)
def get_licencas_simples():
    """Recupera as licenças para a página de vencimentos."""
    try:
        supabase = get_client()
        res = supabase.table("Licencas_Validades").select("*").order("data_vencimento").execute()
        return res.data or []
    except Exception as e:
        st.error(f"Erro ao buscar licenças: {e}")
        return []

@st.cache_data(ttl=10)
def get_tabela_simples(tabela):
    """Busca todos os dados de uma tabela. Necessário para a página de componentes."""
    try:
        supabase = get_client()
        return supabase.table(tabela).select("*").execute().data or []
    except Exception as e:
        st.error(f"Erro na tabela {tabela}: {e}")
        return []

# --- LÓGICA DE NEGÓCIO E CRUD ---

def get_itens_disponiveis(tabela, coluna_serie, valor_atual=None):
    """Filtra itens que não estão em uso em nenhum equipamento."""
    try:
        todos = get_tabela_simples(tabela)
        supabase = get_client()
        ocupados = supabase.table("Equipamentos").select("antena, monitor, nav").execute().data
        
        series_em_uso = set()
        for o in ocupados:
            for k in o: 
                if o[k]: series_em_uso.add(str(o[k]))
        
        return [i for i in todos if str(i[coluna_serie]) not in series_em_uso or str(i[coluna_serie]) == str(valor_atual)]
    except:
        return []

def add_registro(tabela, dados):
    """Adiciona um novo registro (Antena, Monitor, NAV ou Licença)."""
    try:
        supabase = get_client()
        supabase.table(tabela).insert(dados).execute()
        st.cache_data.clear()
        return True
    except Exception as e:
        st.error(f"Erro ao inserir: {e}")
        return False

def update_equipamento(equip_id, dados):
    """Atualiza o equipamento enviando apenas colunas existentes para evitar erros de cache."""
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
    """Autenticação simples."""
    try:
        supabase = get_client()
        res = supabase.table("usuarios").select("*").eq("usuarios", usuario).eq("senha", senha).execute()
        return len(res.data) > 0
    except:
        return False
