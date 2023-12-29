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
    situacao_voo = st.radio(
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
            st.warning("Não há dados de vôos cancelados para a seleção")
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
        titulo = (
            f"Comparação da Situação dos Vôos do aeroporto {nome_aeroporto_origem.split('-')[1]} para a empresa {nome_empresa.split('-')[1]}"
            if nome_empresa is not None
            else f"Comparação da Situação dos Vôos do aeroporto {nome_aeroporto_origem.split('-')[1]} "
        )
        visualizacao_qtd_voo = Visualizacao(dataframe=dataframe_qt_voo)
        fig = visualizacao_qtd_voo.gerar_visualizacao_grafico_barra(
            barmode="group",
            color="SITUACAO_VOO",
            coluna_x="NOME_MES_PARTIDA_PREVISTA",
            coluna_y="TOTAL_SITUACAO",
            titulo_grafico=titulo,
            cor_sequencia_legenda=["#1F3BB3", "#DC3545"],
        )
        st.plotly_chart(
            fig,
        )

    with col2:
        df_variacao_voo = gerador_consulta.obter_variacao_situacao_voo(
            sigla_aeroporto=nome_aeroporto_origem.split("-")[0],
            codigo_tipo_linha=opcao_codigo_voo.split("-")[0],
            sigla_empresa=nome_empresa,
            situacao_voo=situacao_voo,
        )
        visualizacao_variacao_voo = Visualizacao(dataframe=df_variacao_voo)
        fig = visualizacao_variacao_voo.gerar_grafico_variacao_voo(
            coluna_x="NOME_MES_PARTIDA_PREVISTA",
            coluna_y_atual="TOTAL_SITUACAO",
            coluna_y_anterior="TOTAL_SITUACAO_MES_ANTERIOR",
            legenda_valor_atual="Valor Mês atual",
            legenda_valor_anterior="Valor Mês anterior",
        )
        st.plotly_chart(
            fig,
        )
