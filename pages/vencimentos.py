import streamlit as st
from services import get_licencas_simples, get_equipamentos
from utils import formatar_data

def render(go):
    if st.button("⬅️ Voltar"): go("home")
    st.subheader("🔔 Controle de Vencimentos")
    
    busca = st.text_input("🔍 Pesquisar Licença...")
    licencas = get_licencas_simples()
    equipamentos = get_equipamentos()

    if busca:
        licencas = [l for l in licencas if busca.lower() in str(l.get("licenca")).lower()]

    for item in licencas:
        num_licenca = str(item.get("licenca"))
        data_fmt, status = formatar_data(item.get("data_vencimento"))
        
        # Procura onde está a licença
        vinc = next((e for e in equipamentos if num_licenca in [str(e.get("antena")), str(e.get("monitor")), str(e.get("nav"))]), None)

        with st.container(border=True):
            c1, c2 = st.columns([3, 1])
            with c1:
                st.markdown(f"**Série:** `{num_licenca}`")
                st.caption(f"📍 {f'Frota: {vinc.get('codigo_do_equipamento')}' if vinc else 'Estoque'}")
            with c2:
                cor = "red" if status == "val-expirada" else "orange" if status == "val-atencao" else "green"
                st.markdown(f"<p style='color:{cor}; font-weight:bold; text-align:right;'>{data_fmt}</p>", unsafe_allow_html=True)
