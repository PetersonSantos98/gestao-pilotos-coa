import streamlit as st
from supabase import create_client
import httpx

# ================================
# 🔐 CONFIG AUTOMÁTICA
# ================================
def get_config():
    try:
        # tenta pegar do secrets (produção)
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
    except:
        # fallback TEMPORÁRIO (prototipo)
        url = "https://wjejxlnclrdpigpratrt.supabase.co"
        key = "sb_publishable_TZrkyrcPDgaqcgTcZcmvPQ_UofXX50m"

    return url, key


# ================================
# 🔌 CLIENTE
# ================================
@st.cache_resource
def get_client():
    url, key = get_config()

    try:
        return create_client(
            url,
            key,
            options={"http_client": httpx.Client(timeout=10.0)}
        )
    except Exception as e:
        st.error(f"Erro ao conectar no Supabase: {e}")
        st.stop()


# ================================
# 🚜 EQUIPAMENTOS
# ================================
@st.cache_data(ttl=60)
def get_equipamentos():
    try:
        supabase = get_client()
        res = supabase.table("Equipamentos") \
            .select("id, codigo_do_equipamento, nome, antena, monitor") \
            .order("codigo_do_equipamento") \
            .execute()

        return res.data or []
    except Exception as e:
        st.error(f"Erro ao buscar equipamentos: {e}")
        return []


def update_equipamento(equip_id, dados):
    try:
        supabase = get_client()
        res = supabase.table("Equipamentos") \
            .update(dados) \
            .eq("id", equip_id) \
            .execute()

        st.cache_data.clear()
        return res.data
    except Exception as e:
        st.error(f"Erro ao atualizar: {e}")
        return None


# ================================
# 📡 LICENÇAS
# ================================
@st.cache_data(ttl=60)
def get_licencas():
    try:
        supabase = get_client()
        res = supabase.table("Licencias_Validades") \
            .select("id, licenca, data_vencimento") \
            .order("data_vencimento") \
            .execute()

        return res.data or []
    except Exception as e:
        st.error(f"Erro ao buscar licenças: {e}")
        return []
