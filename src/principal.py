import streamlit as st

st.set_page_config(layout="wide", page_title="Dashboard dados vôos")
st.title("Análise de dados dos Vôos do Ano de 2022")


with st.sidebar:
    opcao_codigo_voo = st.radio(
        "Selecione o código do vôo",
        [
            "N-Doméstica Mista",
            "C-Doméstica Cargueira",
            "G-Internacional Cargueira",
        ],
        index=0,
    )
    numero_mes = st.number_input("Escolha o mês", min_value=1, max_value=12, key="int")


with st.container(border=True):
    col1, col2 = st.columns([3, 2])
    with col1:
        st.metric(label="Vôos Realizados", value="70 F", delta="1.2F")
    with col2:
        st.metric(label="Vôos Cancelados", value="70 F", delta="1.2F")
