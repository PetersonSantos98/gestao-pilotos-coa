import streamlit as st
from supabase import create_client

SUPABASE_URL = "SUA_URL"
SUPABASE_KEY = "SUA_KEY"

@st.cache_resource
def get_client():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

@st.cache_data(ttl=60)
def get_equipamentos():
    supabase = get_client()
    return supabase.table("Equipamentos").select("*").execute().data

@st.cache_data(ttl=60)
def get_licencas():
    supabase = get_client()
    return supabase.table("Licencias_Validades").select("*").execute().data

def update_equipamento(id, dados):
    supabase = get_client()
    return supabase.table("Equipamentos").update(dados).eq("id", id).execute()
