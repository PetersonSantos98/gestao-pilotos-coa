import streamlit as st
from services import get_licencas_com_equipamento
from utils import formatar_data

def render(go):
    if st.button("⬅️ Voltar"): go("home")
    
    st.subheader("🔔 Controle de Vencimentos")
    licencas = get_licencas_com_equipamento()

    for item in licencas:
        data_fmt, status = formatar_data(item.get("data_vencimento"))
        equip = item.get("Equipamentos")
        nome_equip = f"{equip['codigo_do_equipamento']} - {equip['nome']}" if equip else "Sem vínculo"

        with st.container(border=True):
            c1, c2 = st.columns([3, 1])
            with c1:
                st.write(f"**Licença:** {item['licenca']}")
                st.caption(f"🚜 Equipamento: {nome_equip}")
            with c2:
                # Usa o status da utils.py para cor (val-expirada = Vermelho / val-ok = Verde)
                cor = "red" if status == "val-expirada" else "green"
                st.markdown(f"<p style='color:{cor}; font-weight:bold;'>{data_fmt}</p>", unsafe_allow_html=True)
