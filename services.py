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

# --- BUSCAS DE DADOS (COM RASTREAMENTO DE VÍNCULOS) ---

@st.cache_data(ttl=10)
def get_equipamentos():
    """Busca a frota e anexa os modelos das peças via Python para evitar erros de relacionamento."""
    try:
        supabase = get_client()
        # Busca básica na tabela de Equipamentos
        res = supabase.table("Equipamentos").select("id, codigo_do_equipamento, nome, antena, monitor, nav").order("codigo_do_equipamento").execute()
        
        # Busca dados auxiliares das peças para o 'join' manual
        antenas = {a['antena_serie']: a for a in supabase.table("Antenas").select("*").execute().data}
        monitores = {m['monitor_serie']: m for m in supabase.table("Monitores").select("*").execute().data}
        
        dados_completos = []
        for eq in res.data:
            # Vincula os dados técnicos das peças ao trator para exibição na frota
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
    RASTREAMENTO TIPO VENCIMENTO: Identifica se a peça está em uso e por QUAL trator.
    """
    try:
        supabase = get_client()
        # 1. Busca todas as peças cadastradas (Antenas, Monitores ou Navs)
        pecas = supabase.table(tabela).select("*").execute().data or []
        
        # 2. Busca a frota para criar o mapa de quem está usando o quê
        frota = supabase.table("Equipamentos").select("codigo_do_equipamento, antena, monitor, nav").execute().data
        
        # Criamos um dicionário: { 'NÚMERO_DE_SÉRIE': 'CÓDIGO_DO_TRATOR' }
        mapa_vinculos = {}
        for trator in frota:
            cod = trator['codigo_do_equipamento']
            if trator.get('antena'): mapa_vinculos[str(trator['antena'])] = cod
            if trator.get('monitor'): mapa_vinculos[str(trator['monitor'])] = cod
            if trator.get('nav'): mapa_vinculos[str(trator['nav'])] = cod

        # 3. Injeta a informação do trator dentro do objeto da peça
        for p in pecas:
            serie_atual = str(p.get(coluna_serie))
            # Se a série estiver no mapa, 'vinculo' recebe o código do trator, senão None
            p['vinculo'] = mapa_vinculos.get(serie_atual) 
            p['disponivel'] = p['vinculo'] is None
            
        return pecas
    except Exception as e:
        st.error(f"Erro ao processar status e vínculos: {e}")
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
    """Filtra itens para o SELECT de edição, permitindo a peça que já está no trator."""
    try:
        # Reutiliza a lógica de status para saber o que está livre
        todos = get_itens_com_status(tabela, coluna_serie)
        return [i for i in todos if i['disponivel'] or str(i[coluna_serie]) == str(valor_atual)]
    except:
        return []

def add_registro(tabela, dados):
    """Insere novos registros no banco."""
    try:
        supabase = get_client()
        supabase.table(tabela).insert(dados).execute()
        st.cache_data.clear() # Limpa o cache para atualizar as listas
        return True
    except Exception as e:
        st.error(f"Erro ao inserir: {e}")
        return False

def update_equipamento(equip_id, dados):
    """Atualiza o equipamento filtrando apenas colunas reais da tabela Equipamentos."""
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
    """Validação de acesso simples."""
    try:
        supabase = get_client()
        res = supabase.table("usuarios").select("*").eq("usuarios", usuario).eq("senha", senha).execute()
        return len(res.data) > 0
    except:
        return False
