import streamlit as st
from supabase import create_client

# ================================
# 🔐 CONFIG AUTOMÁTICA (SECRETS + FALLBACK)
# ================================
def get_config():
    try:
        # Produção (Streamlit Secrets)
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
    except:
        # 🔥 Fallback TEMPORÁRIO (protótipo)
        url = "https://wjejxlnclrdpigpratrt.supabase.co"
        key = "sb_publishable_TZrkyrcPDgaqcgTcZcmvPQ_UofXX50m"

    return url, key


# ================================
# 🔌 CLIENTE SUPABASE
# ================================
@st.cache_resource
def get_client():
    url, key = get_config()

    try:
        # ✅ SEM options (corrige seu erro)
        return create_client(url, key)
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

        # limpa cache pra atualizar tela
        st.cache_data.clear()

        return res.data

    except Exception as e:
        st.error(f"Erro ao atualizar equipamento: {e}")
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


def update_licenca(licenca_id, dados):
    try:
        supabase = get_client()

        res = supabase.table("Licencias_Validades") \
            .update(dados) \
            .eq("id", licenca_id) \
            .execute()

        st.cache_data.clear()

        return res.data

    except Exception as e:
        st.error(f"Erro ao atualizar licença: {e}")
        return None
