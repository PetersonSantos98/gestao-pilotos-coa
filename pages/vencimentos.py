import streamlit as st
import services
from utils import formatar_data

def render(go):
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

    if not licencas:
        st.warning("Nenhuma licença cadastrada.")
        return

    if busca.strip():
        termo = busca.strip().lower()
        licencas = [
            l for l in licencas 
            if l.get("licenca") and termo in str(l.get("licenca")).lower()
        ]

    for item in licencas:
        num_licenca = str(item.get("licenca") or "S/N")
        data_fmt, status = formatar_data(item.get("data_vencimento"))
        
        # Procura onde está a licença na frota (compara com antena, monitor e nav)
        vinc = next(
            (e for e in equipamentos if num_licenca in [str(e.get("antena")), str(e.get("monitor")), str(e.get("nav"))]), 
            None
        )

        # Captura flexível de ID
        id_licenca = item.get("id") if item.get("id") is not None else item.get("ID")

        with st.container(border=True):
            c1, c2 = st.columns([3, 1.3])
            with c1:
                st.markdown(f"**Série:** `{num_licenca}`")
                st.caption(f"📍 {f'Frota: **{vinc.get(\"codigo_do_equipamento\")}**' if vinc else '📦 Estoque'}")
            
            with c2:
                # Definição de cores e rótulos do status
                if status == "val-expirada":
                    cor = "#FF4B4B"
                    label_status = "⚠️ Vencida"
                elif status == "val-atencao":
                    cor = "#FFA500"
                    label_status = "⏳ A Vencer"
                else:
                    cor = "#00C853"
                    label_status = "✅ Válida"

                st.markdown(
                    f"<p style='color:{cor}; font-weight:bold; text-align:right; margin-bottom:2px; font-size:14px;'>"
                    f"{label_status}<br><span style='font-size:12px;'>{data_fmt}</span></p>", 
                    unsafe_allow_html=True
                )
                
                if st.button("📝 Editar", key=f"edit_lic_{id_licenca}", use_container_width=True):
                    st.session_state.licenca_edit = item
                    go("gerir_licenca")
