import streamlit as st
import services  # Importação robusta para evitar ImportError
from utils import formatar_data

def render(go):
    # Cabeçalho com botões de ação
    col_v, col_n = st.columns([3, 1])
    with col_v:
        if st.button("⬅️ Voltar"): go("home")
    with col_n:
        if st.button("➕ Nova", use_container_width=True):
            st.session_state.licenca_edit = None
            go("gerir_licenca")

    st.subheader("🔔 Controle de Vencimentos")
    
    busca = st.text_input("🔍 Pesquisar Licença...")
    
    # Chamadas via módulo services
    licencas = services.get_licencas_simples()
    equipamentos = services.get_equipamentos()

    if busca:
        licencas = [l for l in licencas if busca.lower() in str(l.get("licenca")).lower()]

    for item in licencas:
        num_licenca = str(item.get("licenca"))
        data_fmt, status = formatar_data(item.get("data_vencimento"))
        
        # Procura onde está a licença na frota
        vinc = next((e for e in equipamentos if num_licenca in [str(e.get("antena")), str(e.get("monitor")), str(e.get("nav"))]), None)

        with st.container(border=True):
            c1, c2 = st.columns([3, 1.2])
            with c1:
                st.markdown(f"**Série:** `{num_licenca}`")
                st.caption(f"📍 {f'Frota: {vinc.get('codigo_do_equipamento')}' if vinc else 'Estoque'}")
            with c2:
                cor = "red" if status == "val-expirada" else "orange" if status == "val-atencao" else "green"
                st.markdown(f"<p style='color:{cor}; font-weight:bold; text-align:right; margin-bottom: 5px;'>{data_fmt}</p>", unsafe_allow_html=True)
                
                if st.button("📝 Editar", key=f"edit_lic_{item.get('id')}", use_container_width=True):
                    st.session_state.licenca_edit = item
                    go("gerir_licenca")
