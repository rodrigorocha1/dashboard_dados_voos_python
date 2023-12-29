import pickle
import os
from typing import Tuple

CAMINHO_BASE = os.getcwd()


def depara_empresas() -> Tuple[str]:
    """Função para retornar depara de empresas

    Returns:
        Tuple[str]: Tupla com as companias
    """
    with open(
        os.path.join(CAMINHO_BASE, "src", "depara", "lista_companias.pkl"), "rb"
    ) as arq:
        lista_companias = pickle.load(arq)
    return lista_companias
