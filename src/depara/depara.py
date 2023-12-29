import pickle
from typing import List


def depara_empresas() -> List[str]:
    """Método para abir o depara de empresas

    Returns:
        List[str]: Uma lista de empresa unido ao código
    """
    with open("lista_companias.pkl", "rb") as arq:
        lista_companias = pickle.load(arq)
    return lista_companias
