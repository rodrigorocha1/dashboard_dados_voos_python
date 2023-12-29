import streamlit as st
from depara.depara import obter_depara_empresas, obter_depara_aeroporto
from visualizacao.visualizacao import Visualizacao
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
        "Escolha o mês", min_value=1, max_value=12, key="int", value=12
    )
    nome_empresa = st.selectbox(
        "Escolha a empresa", obter_depara_empresas(opcao_codigo_voo), index=None
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
            st.warning("Não há dados de vôos realizados para a seleção")
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
            st.warning("Não há dados de vôos de cancelamento para a seleção")
        else:
            st.metric(
                label="Vôos Cancelados",
                value=int(variacao_voo_cancelados["TOTAL_SITUACAO"].values),
                delta=float(variacao_voo_cancelados["PERCENTUAL_VARIACAO"].values),
            )

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        dataframe_qt_voo = gerador_consulta.obter_situacao_voo(
            codigo_tipo_linha=opcao_codigo_voo,
            mes_partida_prevista=None,
            sigla_aeroporto=nome_aeroporto_origem,
            sigla_empresa=nome_empresa,
        )
        visualizacao_qtd_voo = Visualizacao(dataframe=dataframe_qt_voo)
        fig = visualizacao_qtd_voo.gerar_visualizacao_grafico_barra(
            barmode="group",
            color="SITUACAO_VOO",
            coluna_x="NOME_MES_PARTIDA_PREVISTA",
            coluna_y="TOTAL_SITUACAO",
        )
        st.plotly_chart(
            fig,
        )

    with col2:
        st.write("Coluna 2")
