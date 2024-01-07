import streamlit as st

with open("teste.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
st.button("Botão de teste")

coluna1, coluna2 = st.columns(2)

with coluna1:
    st.metric("teste de métrica", value=1)

with coluna2:
    st.metric("teste de métrica", value=1)
