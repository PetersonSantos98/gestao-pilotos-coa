import streamlit as st
from services import get_licencas_simples, get_equipamentos
from utils import formatar_data

def render(go):
    if st.button("⬅️ Voltar"): 
        go("home")
    
    st.subheader("🔔 Controle de Vencimentos")
    
    # Carrega os dados separadamente para cruzar no código
    licencas = get_licencas_simples()
    equipamentos = get_equipamentos()

    if not licencas:
        st.info("Nenhuma licença encontrada.")
        return

    for item in licencas:
        num_licenca = str(item.get("licenca"))
        data_fmt, status = formatar_data(item.get("data_vencimento"))
        
        # Procura qual equipamento tem esse número de licença em qualquer componente
        # Varre as colunas 'antena', 'monitor' e 'nav' da tabela Equipamentos
        equip_vinc = next((e for e in equipamentos if 
                           str(e.get("antena")) == num_licenca or 
                           str(e.get("monitor")) == num_licenca or 
                           str(e.get("nav")) == num_licenca), None)

        if equip_vinc:
            nome_exibicao = f"{equip_vinc['codigo_do_equipamento']} - {equip_vinc['nome']}"
        else:
            nome_exibicao = "Componente em Estoque (Sem Equipamento)"

        with st.container(border=True):
            col_info, col_status = st.columns([3, 1])
            with col_info:
                st.markdown(f"**Licença/Série:** `{num_licenca}`")
                st.caption(f"🚜 Vinculado a: {nome_exibicao}")
                if item.get("modelo"):
                    st.caption(f"📦 Modelo: {item.get('modelo')}")
            
            with col_status:
                cor = "red" if status == "val-expirada" else "green"
                st.markdown(f"<p style='color:{cor}; font-weight:bold; text-align:right;'>{data_fmt}</p>", unsafe_allow_html=True)
