import streamlit as st
from supabase import create_client
import httpx

# ================================
# 🔐 CONFIG (USAR SECRETS)
# ================================
SUPABASE_URL = st.secrets["https://wjejxlnclrdpigpratrt.supabase.com"]
SUPABASE_KEY = st.secrets["sb_publishable_TZrkyrcPDgaqcgTcZcmvPQ_UofXX50m"]


# ================================
# 🔌 CLIENTE COM TIMEOUT
# ================================
@st.cache_resource
def get_client():
    try:
        return create_client(
            SUPABASE_URL,
            SUPABASE_KEY,
            options={
                "http_client": httpx.Client(timeout=10.0)
            }
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


def get_equipamento_por_id(equip_id):
    try:
        supabase = get_client()
        res = supabase.table("Equipamentos") \
            .select("*") \
            .eq("id", equip_id) \
            .single() \
            .execute()

        return res.data

    except Exception as e:
        st.error(f"Erro ao buscar equipamento: {e}")
        return None


def update_equipamento(equip_id, dados):
    try:
        supabase = get_client()

        res = supabase.table("Equipamentos") \
            .update(dados) \
            .eq("id", equip_id) \
            .execute()

        # 🔄 limpa cache após alteração
        st.cache_data.clear()

        return res.data

    except Exception as e:
        st.error(f"Erro ao atualizar equipamento: {e}")
        return None


# ================================
# 📡 LICENÇAS / VENCIMENTOS
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


def update_licenca(licenca_id, dados):
    try:
        supabase = get_client()

        res = supabase.table("Licencias_Validades") \
            .update(dados) \
            .eq("id", licenca_id) \
            .execute()

        # 🔄 limpa cache
        st.cache_data.clear()

        return res.data

    except Exception as e:
        st.error(f"Erro ao atualizar licença: {e}")
        return None
