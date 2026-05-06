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

# --- BUSCAS ---

@st.cache_data(ttl=10) # TTL baixo para você ver as mudanças rápido
def get_equipamentos():
    """Busca a frota e os modelos das peças separadamente para evitar erro PGRST200."""
    try:
        supabase = get_client()
        # Buscamos apenas os dados que existem com certeza
        query = "id, codigo_do_equipamento, nome, antena, monitor, nav"
        res = supabase.table("Equipamentos").select(query).order("codigo_do_equipamento").execute()
        
        # Agora buscamos os modelos para cruzar no código
        antenas = {a['antena_serie']: a for a in supabase.table("Antenas").select("*").execute().data}
        monitores = {m['monitor_serie']: m for m in supabase.table("Monitores").select("*").execute().data}
        
        dados_completos = []
        for eq in res.data:
            # Anexamos os modelos manualmente
            eq['info_antena'] = antenas.get(eq['antena'], {})
            eq['info_monitor'] = monitores.get(eq['monitor'], {})
            dados_completos.append(eq)
            
        return dados_completos
    except Exception as e:
        st.error(f"Erro ao buscar frota: {e}")
        return []

@st.cache_data(ttl=10)
def get_licencas_simples():
    """Resolve o AttributeError da sua imagem image_5d06f2.png"""
    try:
        supabase = get_client()
        res = supabase.table("Licencas_Validades").select("*").order("data_vencimento").execute()
        return res.data or []
    except Exception as e:
        st.error(f"Erro ao buscar licenças: {e}")
        return []

# --- AUXILIARES ---

def get_itens_disponiveis(tabela, coluna_serie, valor_atual=None):
    try:
        supabase = get_client()
        todos = supabase.table(tabela).select("*").execute().data or []
        ocupados = supabase.table("Equipamentos").select("antena, monitor, nav").execute().data
        
        series_em_uso = set()
        for o in ocupados:
            for k in o: 
                if o[k]: series_em_uso.add(str(o[k]))
        
        return [i for i in todos if str(i[coluna_serie]) not in series_em_uso or str(i[coluna_serie]) == str(valor_atual)]
    except:
        return []

def update_equipamento(equip_id, dados):
    try:
        supabase = get_client()
        # Filtro de segurança: só envia o que a tabela Equipamentos realmente tem
        colunas_reais = ["nome", "antena", "monitor", "nav"]
        payload = {k: v for k, v in dados.items() if k in colunas_reais}
        supabase.table("Equipamentos").update(payload).eq("id", equip_id).execute()
        st.cache_data.clear()
        return True
    except Exception as e:
        st.error(f"Erro no banco: {e}")
        return False
