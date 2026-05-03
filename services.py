import streamlit as st
from supabase import create_client

# ================================
# 🔐 CONFIGURAÇÃO DE CONEXÃO
# ================================
def get_config():
    try:
        # Tenta buscar das Secrets do Streamlit (Produção)
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
    except:
        # Fallback para o seu projeto atual (Desenvolvimento)
        url = "https://wjejxlnclrdpigpratrt.supabase.co"
        key = "sb_publishable_TZrkyrcPDgaqcgTcZcmvPQ_UofXX50m"
    return url, key

@st.cache_resource
def get_client():
    """Retorna o cliente autenticado do Supabase."""
    url, key = get_config()
    return create_client(url, key)

# ================================
# 🚜 GESTÃO DE EQUIPAMENTOS
# ================================
@st.cache_data(ttl=60)
def get_equipamentos():
    """Busca todos os equipamentos da frota."""
    try:
        supabase = get_client()
        res = supabase.table("Equipamentos").select("*").order("codigo_do_equipamento").execute()
        return res.data or []
    except Exception as e:
        st.error(f"Erro ao buscar equipamentos: {e}")
        return []

def update_equipamento(equip_id, dados):
    """Atualiza os dados de um equipamento e limpa o cache."""
    try:
        supabase = get_client()
        supabase.table("Equipamentos").update(dados).eq("id", equip_id).execute()
        st.cache_data.clear()
        return True
    except Exception as e:
        st.error(f"Erro ao atualizar: {e}")
        return False

# ================================
# 🔔 GESTÃO DE LICENÇAS (CORRIGIDO)
# ================================
@st.cache_data(ttl=60)
def get_licencas_simples():
    """Busca licenças sem Join para evitar erro de APIError."""
    try:
        supabase = get_client()
        res = supabase.table("Licencas_Validades").select("*").execute()
        return res.data or []
    except Exception as e:
        st.error(f"Erro ao buscar licenças: {e}")
        return []

# ================================
# 📡 COMPONENTES E DISPONIBILIDADE
# ================================
def get_tabela_simples(tabela):
    """Busca todos os registros de Antenas, Monitores ou Navs."""
    try:
        supabase = get_client()
        return supabase.table(tabela).select("*").execute().data or []
    except Exception as e:
        st.error(f"Erro na tabela {tabela}: {e}")
        return []

def get_itens_disponiveis(tabela, coluna_serie, valor_atual=None):
    """
    Retorna apenas itens que não estão vinculados a nenhum equipamento.
    Garante que um componente não seja usado em dois lugares ao mesmo tempo.
    """
    try:
        supabase = get_client()
        todos = get_tabela_simples(tabela)
        
        # Define qual coluna da tabela Equipamentos checar baseado no componente
        # Mapeia: Antenas -> coluna 'antena', Monitores -> coluna 'monitor', etc.
        col_vinc = "antena" if tabela == "Antenas" else ("monitor" if tabela == "Monitores" else "nav")
        
        # Busca o que já está em uso na frota
        em_uso = supabase.table("Equipamentos").select(col_vinc).execute().data
        series_em_uso = [x[col_vinc] for x in em_uso if x[col_vinc]]

        # Filtra: Mantém se (não estiver em uso) OU (for o valor que já está no equipamento que estamos editando)
        disponiveis = [
            item for item in todos 
            if item[coluna_serie] not in series_em_uso or item[coluna_serie] == valor_atual
        ]
        return disponiveis
    except Exception as e:
        st.error(f"Erro ao validar disponibilidade: {e}")
        return []
