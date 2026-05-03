import streamlit as st
from services import get_itens_disponiveis, add_registro

def render(go):
    if st.button("⬅️ Voltar"): go("frotas")
    
    st.subheader("🚜 Cadastrar Nova Frota")
    st.info("Selecione os componentes disponíveis para montar o equipamento.")

    # 1. Busca o que está no estoque (disponível) direto do banco
    antenas_dispo = get_itens_disponiveis("Antenas", "antena_serie")
    monitores_dispo = get_itens_disponiveis("Monitores", "monitor_serie")
    navs_dispo = get_itens_disponiveis("Navs", "nav_serie")

    with st.form("form_nova_frota"):
        # Dados da Máquina
        codigo = st.text_input("Prefixo do Equipamento (Ex: 1118)")
        tipo_maquina = st.selectbox("Tipo", ["Harvester", "Trator", "Caminhão", "Outros"])
        
        st.divider()
        
        # Seleção de Componentes (Apenas os que não estão em uso)
        antena = st.selectbox(
            "Vincular Antena", 
            options=[None] + [a['antena_serie'] for a in antenas_dispo],
            format_func=lambda x: "📦 " + x if x else "Nenhuma"
        )
        
        monitor = st.selectbox(
            "Vincular Monitor", 
            options=[None] + [m['monitor_serie'] for m in monitores_dispo],
            format_func=lambda x: "🖥️ " + x if x else "Nenhum"
        )
        
        nav = st.selectbox(
            "Vincular NAV", 
            options=[None] + [n['nav_serie'] for n in navs_dispo],
            format_func=lambda x: "🛰️ " + x if x else "Nenhum"
        )

        if st.form_submit_button("Finalizar Cadastro e Enviar ao Banco"):
            if not codigo:
                st.error("O código do equipamento é obrigatório.")
            else:
                # Monta o dicionário exatamente com as colunas da sua tabela Equipamentos
                nova_frota = {
                    "codigo_do_equipamento": codigo,
                    "tipo": tipo_maquina,
                    "antena": antena,
                    "monitor": monitor,
                    "nav": nav
                }
                
                if add_registro("Equipamentos", nova_frota):
                    st.success(f"Frota {codigo} cadastrada com sucesso!")
                    st.balloons()
                    # Opcional: go("frotas") para voltar automaticamente
