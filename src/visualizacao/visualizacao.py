import pandas as pd
import plotly.express as px


class Visualizacao:
    def __init__(self, dataframe: pd.DataFrame) -> None:
        self.__dataframe = dataframe

    def gerar_visualizacao_grafico_barra(
        self, coluna_x: str, coluna_y: str, color: str = None, barmode: str = None
    ):
        """Método para gerar o gráfico de barras agrupado

        Args:
            coluna_x (str): coluna X do df
            coluna_y (str): coluna y
            color (str, optional): atributo para cor. Defaults to None.
            barmode (str, optional): agrupamento do gráfico. Defaults to None.

        Returns:
            _type_: _description_
        """
        fig = px.bar(
            self.__dataframe,
            x=coluna_x,
            y=coluna_y,
            color=color,
            barmode=barmode,
            text_auto="0",
        )
        return fig
