import pickle
from typing import Tuple


def depara_empresas() -> Tuple[str]:
    """Função para retornar depara de empresas

    Returns:
        Tuple[str]: Tupla com as companias
    """
    with open("lista_companias.pkl", "rb") as arq:
        lista_companias = pickle.load(arq)
    return lista_companias
