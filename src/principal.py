import streamlit as st
from depara.depara import obter_depara_empresas, obter_depara_aeroporto
from consulta.gerador_consulta import GeradorConsulta

st.set_page_config(layout="wide", page_title="Dashboard dados vôos")
st.title("Análise de dados dos Vôos do Ano de 2022")


with st.sidebar:
    opcao_codigo_voo = st.radio(
        "Selecione o código do vôo",
        [
            "N-Doméstica Mista",
            "C-Doméstica Cargueira",
            "G-Internacional Cargueira",
            "X-Não informado",
        ],
        index=0,
    )
    numero_mes = st.number_input(
        "Escolha o mês", min_value=1, max_value=12, key="int", value=2
    )
    nome_empresa = st.selectbox(
        "Escolha a empresa", obter_depara_empresas(opcao_codigo_voo)
    )
    nome_aeroporto_origem = st.selectbox(
        "Escolha o aeroporto de origem",
        obter_depara_aeroporto(codigo_tipo_linha=opcao_codigo_voo),
    )
    situacao = st.radio(
        "Escolha a situação do vôo",
        [
            "REALIZADO",
            "CANCELADO",
        ],
        index=0,
    )

with st.container(border=True):
    col1, col2 = st.columns([3, 2])
    gerador_consulta = GeradorConsulta()
    with col1:
        variacao_voo_realizado = gerador_consulta.obter_variacao_percentual(
            sigla_aeroporto=nome_aeroporto_origem,
            mes_partida=numero_mes,
            codigo_tipo_linha=opcao_codigo_voo,
            sigla_empresa=nome_empresa,
            situacao_voo="Realizado",
        )
        if variacao_voo_realizado.empty:
            st.metric("Não há Registro de Vôos")
        else:
            st.metric(
                label="Vôos Realizados",
                value=variacao_voo_realizado["TOTAL_SITUACAO"].values,
                delta=float(variacao_voo_realizado["PERCENTUAL_VARIACAO"].values),
            )

    with col2:
        variacao_voo_cancelados = gerador_consulta.obter_variacao_percentual(
            sigla_aeroporto=nome_aeroporto_origem,
            mes_partida=numero_mes,
            codigo_tipo_linha=opcao_codigo_voo,
            sigla_empresa=nome_empresa,
            situacao_voo="Cancelado",
        )

        if variacao_voo_cancelados.empty:
            st.metric("Não há Cancelamento Registrado")
        else:
            st.metric(
                label="Vôos Cancelados",
                value=float(variacao_voo_cancelados["TOTAL_SITUACAO"].values),
                delta=float(variacao_voo_cancelados["PERCENTUAL_VARIACAO"].values),
            )
