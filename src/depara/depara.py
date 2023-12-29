import pickle
from typing import Tuple
import pandas as pd
import os


CAMINHO_BASE = os.getcwd()
print(os.path.join(CAMINHO_BASE, "src", "depara", "lista_companias.pkl"))


def obter_depara_empresas(codigo_tipo_linha: str) -> Tuple[str]:
    """Função para retornar depara de empresas

    Returns:
        Tuple[str]: Tupla com as companias
    """
    codigo_tipo_linha = codigo_tipo_linha.split("-")[0]
    caminho_completo = os.path.join(
        CAMINHO_BASE, "src", "depara", "lista_companias.pkl"
    )
    with open(
        caminho_completo,
        "rb",
    ) as arq:
        df_companias: pd.DataFrame = pickle.load(arq)

    df_companias = df_companias.query(f' CODIGO_TIPO_LINHA == "{codigo_tipo_linha}"')
    df_companias = df_companias.drop_duplicates()
    companias = tuple(df_companias["NOME_COMPLETO_EMPRESA"].to_list())

    return companias


if __name__ == "__main__":
    df = depara_empresas("N")
    print(df)
    print()
