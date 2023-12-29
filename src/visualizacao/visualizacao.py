import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import List


class Visualizacao:
    def __init__(self, dataframe: pd.DataFrame) -> None:
        self.__dataframe = dataframe

    def gerar_visualizacao_grafico_barra(
        self,
        coluna_x: str,
        coluna_y: str,
        cor_sequencia_legenda: List[str],
        titulo_grafico: str = "Teste",
        color: str = None,
        barmode: str = None,
    ):
        """Método para gerar gráfio de barra

        Args:
            coluna_x (str): eixo x do gráfico
            coluna_y (str): eixo y do gráfico
            cor_sequencia_legenda (List[str]): cor das legendas
            titulo_grafico (str, optional): título do grafico. Defaults to "Teste".
            color (str, optional): cor para separação no gráfico. Defaults to None.
            barmode (str, optional): coluna de agrupamento. Defaults to None.

        Returns:
            _type_: figura
        """
        fig = px.bar(
            self.__dataframe,
            x=coluna_x,
            y=coluna_y,
            color=color,
            barmode=barmode,
            text_auto="0",
            color_discrete_sequence=cor_sequencia_legenda,
        )
        fig.update_layout(
            title_text=titulo_grafico,
            showlegend=True,
            title=dict(x=0.1, font=dict(color="white", size=12)),
            # plotly_bgcolor=None,
            xaxis=dict(title="", tickfont=dict(color="white")),
            legend=dict(font=dict(color="white")),
        )

        fig.update_traces(textfont_color="white", textposition="outside")
        return fig
