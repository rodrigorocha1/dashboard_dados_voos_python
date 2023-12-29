import streamlit as st

st.set_page_config(layout="wide", page_title="Dashboard dados vôos")
st.title("Análise de dados dos Vôos do Ano de 2022")

col1, col2, col3, col4 = st.columns(4)

with col1:
    opcao = st.radio("Opção", [1, 2, 3], horizontal=True, captions="Teste")

with col2:
    st.metric(label="Temperatura", value="70 F", delta="1.2F")
    st.metric(label="Temperatura", value="70 F", delta="1.2F")
    st.metric(label="Temperatura", value="70 F", delta="1.2F")


with col3:
    st.metric(label="Temperatura", value="70 F", delta="1.2F")
    st.metric(label="Temperatura", value="70 F", delta="1.2F")
    st.metric(label="Temperatura", value="70 F", delta="1.2F")
with col4:
    st.metric(label="Temperatura", value="70 F", delta="1.2F")
    st.metric(label="Temperatura", value="70 F", delta="1.2F")
    st.metric(label="Temperatura", value="70 F", delta="1.2F")
