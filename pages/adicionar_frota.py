import streamlit as st
from services import get_itens_disponiveis, add_registro

def render(go):
    if st.button("⬅️ Voltar"): go("home")
    
    st.write("### 🚜 Cadastrar Nova Frota")
    
    # Busca itens que NÃO estão vinculados a nenhuma frota
    antenas = get_itens_disponiveis("Antenas", "antena_serie")
    monitores = get_itens_disponiveis("Monitores", "monitor_serie")
    navs = get_itens_disponiveis("Navs", "nav_serie")

    with st.form("form_nova_frota"):
        codigo = st.text_input("Código do Equipamento (Prefixo)", placeholder="Ex: 1118")
        nome = st.text_input("Nome/Descrição", placeholder="Ex: Colhedora John Deere")
        
        st.divider()
        
        # Selectbox que mostra apenas o que está livre no estoque
        antena = st.selectbox("Selecionar Antena Disponível", 
                              options=[None] + [a['antena_serie'] for a in antenas])
        
        monitor = st.selectbox("Selecionar Monitor Disponível", 
                               options=[None] + [m['monitor_serie'] for m in monitores])
        
        nav = st.selectbox("Selecionar NAV Disponível", 
                           options=[None] + [n['nav_serie'] for n in navs])

        if st.form_submit_button("Salvar Frota"):
            if not codigo:
                st.error("O código do equipamento é obrigatório.")
            else:
                dados = {
                    "codigo_do_equipamento": codigo,
                    "nome": nome,
                    "antena": antena,
                    "monitor": monitor,
                    "nav": nav
                }
                # Insere na tabela Equipamentos do Supabase
                if add_registro("Equipamentos", dados):
                    st.success(f"Equipamento {codigo} cadastrado!")
                    st.balloons()
