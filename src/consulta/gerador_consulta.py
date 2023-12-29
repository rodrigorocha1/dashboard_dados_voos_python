import os
from typing import List
import pandas as pd


class GeradorConsulta:
    def __init__(self) -> None:
        """Classe para fazer a consulta"""
        self.__caminho_base = os.path.join(
            os.getcwd(), "data", "processed", "df_processed_v2.parquet"
        )

    def __abrir_dataframe(self, colunas: List[str]) -> pd.DataFrame:
        """Método para carregar o dataframe

        Args:
            colunas (List[str]): colunas selecionadas para abrir o dataframe

        Returns:
            pd.DataFrame: dataframe do pandas
        """
        dataframe = pd.read_parquet(self.__caminho_base, columns=colunas)
        return dataframe

    def obter_situacao_voo(
        self,
        sigla_aeroporto: str,
        mes_partida_prevista: List[int],
        codigo_tipo_linha: str,
        sigla_empresa: str = None,
    ) -> pd.DataFrame:
        """Método para quantificar a situação do vôo por aeroporto origem

        Args:
            sigla_aeroporto (str): sigla do aeroporo
            mes_partida_prevista (List[int]): mês de partida do aeroporto de origem
            codigo_tipo_linha (str): código do tipo de linha
            sigla_empresa (str, optional): sigla da empresa (não obrigatório). Defaults to None.

        Returns:
            pd.DataFrame: Dataframe
        """
        query = (
            f' SIGLA_ICAO_AEROPORTO_ORIGEM == "{sigla_aeroporto}" '
            f" and MES_PARTIDA_PREVISTA in {mes_partida_prevista}"
            f' and CODIGO_TIPO_LINHA == "{codigo_tipo_linha}"'
        )
        colunas = [
            "SITUACAO_VOO",
            "MES_PARTIDA_PREVISTA",
            "NOME_MES_PARTIDA_PREVISTA",
            "SIGLA_ICAO_AEROPORTO_ORIGEM",
            "CODIGO_TIPO_LINHA",
        ]

        if sigla_empresa is not None:
            query += f' and SIGLA_ICAO_EMPRESA_AEREA == "{sigla_empresa}" '
            colunas.append("SIGLA_ICAO_EMPRESA_AEREA")

        dataframe = self.__abrir_dataframe(colunas=colunas)
        total = dataframe.query(query)[colunas].value_counts()
        percentual = (
            dataframe.query(query)[colunas].value_counts(
                normalize=True,
            )
            * 100
        )
        dataframe = pd.concat([total, percentual], axis=1).reset_index()
        dataframe["TOTAL_SITUACAO"] = dataframe["count"].astype("int32")
        dataframe["PROPORCAO"] = dataframe["proportion"].astype("float32")
        dataframe = dataframe.sort_values(by=["SITUACAO_VOO", "MES_PARTIDA_PREVISTA"])
        dataframe.drop(
            ["proportion", "count", "CODIGO_TIPO_LINHA"],
            axis=1,
            inplace=True,
        )
        dataframe["SITUACAO_VOO"] = dataframe["SITUACAO_VOO"].astype("string")
        if sigla_empresa is not None:
            dataframe = dataframe.sort_values(by="MES_PARTIDA_PREVISTA")
        return dataframe

    @staticmethod
    def calcular_variacao(linha) -> float:
        """Calcula a variação do mês atual ao mês antrior

        Args:
            linha (_type_): linha do dataframe

        Returns:
            float: variação em porcentagem
        """

        try:
            total_atual = linha["TOTAL_SITUACAO"]
            total_mes_anterior = linha["TOTAL_SITUACAO_MES_ANTERIOR"]
            variacao = ((total_atual - total_mes_anterior) / total_mes_anterior) * 100
        except ZeroDivisionError:
            variacao = 0
        return round(variacao, 2)

    def obter_variacao_percentual(
        self,
        sigla_aeroporto: str,
        situacao_voo: str,
        mes_partida: int,
        codigo_tipo_linha: str,
        sigla_empresa: str = None,
    ) -> pd.DataFrame:
        """Método para obter a variação percentual em relação ao mês anterior

        Args:
            sigla_aeroporto (str): sigla do aeroporto
            situacao_voo (str): situação do vôo
            mes_partida (int): mês de partida 1: jan 2: fev
            codigo_tipo_linha (str): código tipo linha
            sigla_empresa (str, optional): código da empresa. Defaults to None.

        Returns:
            pd.DataFrame: dataframe
        """
        codigo_tipo_linha = codigo_tipo_linha.split("-")[0]
        sigla_aeroporto = sigla_aeroporto.split("-")[0]
        sigla_empresa = sigla_empresa.split("-")[0]
        colunas = [
            "SITUACAO_VOO",
            "MES_PARTIDA_PREVISTA",
            "NOME_MES_PARTIDA_PREVISTA",
            "SIGLA_ICAO_AEROPORTO_ORIGEM",
            "NOME_AEROPORTO_ORIGEM",
            "NOME_EMPRESA",
            "CODIGO_TIPO_LINHA",
        ]
        query = (
            f' SIGLA_ICAO_AEROPORTO_ORIGEM == "{sigla_aeroporto}" '
            f' and  CODIGO_TIPO_LINHA == "{codigo_tipo_linha}" '
        )
        if sigla_empresa is not None:
            query += f' and SIGLA_ICAO_EMPRESA_AEREA == "{sigla_empresa}"  '
            colunas.append("SIGLA_ICAO_EMPRESA_AEREA")

        dataframe = self.__abrir_dataframe(colunas=colunas)

        dataframe = dataframe.query(query)

        dataframe[["SITUACAO_VOO", "NOME_MES_PARTIDA_PREVISTA"]] = dataframe[
            ["SITUACAO_VOO", "NOME_MES_PARTIDA_PREVISTA"]
        ].astype("string")
        dataframe = (
            dataframe.groupby(
                ["SITUACAO_VOO", "NOME_MES_PARTIDA_PREVISTA", "MES_PARTIDA_PREVISTA"]
            )
            .agg(TOTAL_SITUACAO=("SITUACAO_VOO", "count"))
            .sort_values(by=["SITUACAO_VOO", "MES_PARTIDA_PREVISTA"])
            .reset_index()
        )
        dataframe["TOTAL_SITUACAO_MES_ANTERIOR"] = dataframe.groupby("SITUACAO_VOO")[
            "TOTAL_SITUACAO"
        ].shift(1)
        dataframe.fillna(0, axis=1, inplace=True)

        dataframe["PERCENTUAL_VARIACAO"] = dataframe.apply(
            self.calcular_variacao, axis=1
        )

        query = f'SITUACAO_VOO == "{situacao_voo.upper()}" and MES_PARTIDA_PREVISTA == {mes_partida}'
        dataframe["MES_PARTIDA_PREVISTA"] = dataframe["MES_PARTIDA_PREVISTA"].astype(
            "int32"
        )

        dataframe = dataframe.query(query)[
            ["TOTAL_SITUACAO", "TOTAL_SITUACAO_MES_ANTERIOR", "PERCENTUAL_VARIACAO"]
        ]

        return dataframe
