import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
from typing import List

def obter_variacao_flag_atraso(
        sigla_aeroporto: str,
        flag_atraso: str,
        flag_partida_chegada: str,
        sigla_empresa: str = None,
        
    ):

    colunas = [
        'NOME_AEROPORTO_ORIGEM',
        'SIGLA_ICAO_AEROPORTO_ORIGEM',
        'NOME_EMPRESA',
        f'MES_{flag_partida_chegada}_PREVISTA',
        f'NOME_MES_{flag_partida_chegada}_PREVISTA',
        f'DIA_DA_SEMANA_{flag_partida_chegada}_PREVISTA',
        'INDICE_SEMANA_PARTIDA_PREVISTA',
        f'FLAG_ATRASO_{flag_partida_chegada}',
        'FLAG_FIM_SEMANA_PARTIDA_PREVISTA'
    ]
    print(colunas)
    query = (
        f'SIGLA_ICAO_AEROPORTO_ORIGEM == "{sigla_aeroporto}" ' 
        f' and FLAG_ATRASO_PARTIDA == "{flag_atraso}" '
    )
  
    if sigla_empresa is not None:
        query += f' SIGLA_ICAO_EMPRESA_AEREA == "{sigla_empresa}"'
        colunas.append('SIGLA_ICAO_EMPRESA_AEREA')

    dataframe = pd.read_parquet(r'E:\projetos\nova_pasta\dashboard_dados_voos_python\data\processed\df_processed_v2.parquet', columns=colunas)
    dataframe = dataframe.query(query)
   
    dataframe[f'NOME_MES_{flag_partida_chegada}_PREVISTA'] = dataframe[f'NOME_MES_{flag_partida_chegada}_PREVISTA'].astype('string')
    
    dataframe = dataframe.groupby(
        [
            f'FLAG_ATRASO_{flag_partida_chegada}', 
            f'NOME_MES_{flag_partida_chegada}_PREVISTA', 
            f'MES_{flag_partida_chegada}_PREVISTA'
        ]
    ).agg(
        TOTAL_ATRASO=(f'FLAG_ATRASO_{flag_partida_chegada}', 'count')
    ).reset_index().sort_values(by=[f'MES_{flag_partida_chegada}_PREVISTA'])
    dataframe['TOTAL_ATRASO_DESLOCADO'] = dataframe.groupby(f'FLAG_ATRASO_{flag_partida_chegada}')['TOTAL_ATRASO'].shift(1)
    dataframe.fillna(0, axis=1, inplace=True)
    dataframe[
        [f'FLAG_ATRASO_{flag_partida_chegada}', f'NOME_MES_{flag_partida_chegada}_PREVISTA']
    ] = dataframe[
        [f'FLAG_ATRASO_{flag_partida_chegada}', f'NOME_MES_{flag_partida_chegada}_PREVISTA']
    ].astype('string')
    dataframe[
        [f'MES_{flag_partida_chegada}_PREVISTA', 'TOTAL_ATRASO', 'TOTAL_ATRASO_DESLOCADO']
    ] = dataframe[
        [f'MES_{flag_partida_chegada}_PREVISTA', 'TOTAL_ATRASO', 'TOTAL_ATRASO_DESLOCADO']
    ].astype('int32')
    return dataframe

dataframe = obter_variacao_flag_atraso(
    flag_partida_chegada='CHEGADA',
    flag_atraso='Vôo Atrasado',
    sigla_aeroporto='SBRP'
)
dataframe