CREATE DATABASE DADOS_VOO;
SELECT current_date;

SELECT data_extracao,  turno_extracao,  total_visualizacoes_turno  FROM youtube.TOTAL_VISUALIZACOES_POR_SEMANA  where assunto = "assunto_cities_skylines"  AND ID_CANAL="UC1mk6EtfMjxR4eEZ7C43zTQ"  AND  data_extracao in ("2023-10-22" , "2023-10-21")

SELECT data_extracao,  turno_extracao,  total_visualizacoes_turno  FROM youtube.TOTAL_VISUALIZACOES_POR_SEMANA  where assunto = "assunto_cities_skylines"  AND ID_CANAL="UCMqGy4xIIGs01ZVcBv0B8Cw"  AND  data_extracao in ("2023-10-22" , "2023-10-21")
CREATE EXTERNAL TABLE EXPLORACAO_FAIXA_ATRASO_PARTIDA (
    NUMERO_VOO INT,
    NOME_AEROPORTO_ORIGEM STRING,
    CIDADE_AEROPORTO_ORIGEM STRING,
    NOME_EMPRESA STRING,
    NOME_MES_PARTIDA_REAL STRING,
    MINUTOS_ATRASADO_PARTIDA FLOAT,
    DIA_DA_SEMANA_PARTIDA_PREVISTA STRING
    
)
PARTITIONED BY (
    CODIGO_TIPO_LINHA VARCHAR(1),
    MES_PARTIDA_REAL TINYINT,
    INDICE_SEMANA_PARTIDA_REAL TINYINT,
    FIM_DE_SEMANA_PARTIDA_REAL BOOLEAN,
    UF_AEROPORTO_ORIGEM VARCHAR(2),
    SIGLA_ICAO_AEROPORTO_ORIGEM VARCHAR(15),
    SIGLA_ICAO_EMPRESA_AEREA VARCHAR(25),
    FAIXA_ATRASO_PARTIDA STRING
)

 ROW FORMAT DELIMITED
FIELDS TERMINATED BY '|'
STORED AS TEXTFILE;


CREATE EXTERNAL TABLE EXPLORACAO_FAIXA_ATRASO_CHEGADA(
    NUMERO_VOO INT,
    NOME_AEROPORTO_DESTINO STRING,
    CIDADE_AEROPORTO_DESTINO STRING,
    NOME_EMPRESA STRING,
    NOME_MES_CHEGADA_REAL STRING,
    MINUTOS_ATRASADO_CHEGADA FLOAT,
    DIA_DA_SEMANA_CHEGADA_REAL STRING,
    FIM_DE_SEMANA_CHEGADA_REAL BOOLEAN
    
)
PARTITIONED BY (
    CODIGO_TIPO_LINHA VARCHAR(1),
    MES_CHEGADA_REAL TINYINT,
    INDICE_SEMANA_CHEGADA_REAL TINYINT,
    UF_AEROPORTO_DESTINO VARCHAR(2),
    SIGLA_ICAO_AEROPORTO_DESTINO VARCHAR(15),
    SIGLA_ICAO_EMPRESA_AEREA VARCHAR(25),
    FAIXA_ATRASO_CHEGADA STRING
)

 ROW FORMAT DELIMITED
FIELDS TERMINATED BY '|'
STORED AS TEXTFILE;



CREATE EXTERNAL TABLE IF NOT EXISTS SITUACAO_ROTA_VOO (
    NOME_AEROPORTO_ORIGEM STRING,
    CIDADE_AEROPORTO_ORIGEM STRING,
    NOME_AEROPORTO_DESTINO STRING,
    CIDADE_AEROPORTO_DESTINO STRING,
    NOME_EMPRESA STRING,
    NOME_MES_PARTIDA_PREVISTA STRING,
    NOME_MES_CHEGADA_PREVISTA STRING,
    MINUTOS_ATRASADO_PARTIDA STRING,
    MINUTOS_ATRASADO_CHEGADA STRING,
    DIA_DA_SEMANA_PARTIDA_PREVISTA STRING,
    DIA_DA_SEMANA_CHEGADA_PREVISTA STRING,
    MES_CHEGADA_REAL STRING,
    ROTA STRING
  
  
)
PARTITIONED BY (
	CODIGO_TIPO_LINHA VARCHAR(1),
	UF_AEROPORTO_ORIGEM VARCHAR(2),
	UF_AEROPORTO_DESTINO VARCHAR(2),
	MES_PARTIDA_PREVISTA TINYINT,
	MES_CHEGADA_PREVISTA TINYINT,
	INDICE_SEMANA_PARTIDA_PREVISTA TINYINT,
	INDICE_SEMANA_CHEGADA_PREVISTA TINYINT,
	SIGLA_ICAO_AEROPORTO_ORIGEM  VARCHAR(30),
    SIGLA_ICAO_AEROPORTO_DESTINO VARCHAR(30),
    SIGLA_ICAO_EMPRESA_AEREA VARCHAR(10),
    SITUACAO_VOO STRING
    
	
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '|'
STORED AS TEXTFILE;









SELECT *
FROM SITUACAO_ROTA_VOO 
where sigla_icao_empresa_aerea = 'AZU';

SELECT *
from exploracao_faixa_atraso_chegada efac ;


DESCRIBE FORMATTED exploracao_faixa_atraso_partida;

DROP DATABASE dados_voos;
SHOW PARTITIONS exploracao_faixa_atraso_partida;

