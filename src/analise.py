from load import abrirConexao
import pandas as pd

engine = abrirConexao()

query_column_name = """
    SELECT column_name
    FROM information_schema.columns
    WHERE table_name = 'divida_ativa'
"""
query_devedor_tipo = """
    SELECT "TIPO_DEVEDOR", COUNT(*) AS total
    FROM divida_ativa
    GROUP BY "TIPO_DEVEDOR"
"""
query_devedor_uf = """
    SELECT "TIPO_DEVEDOR", "UF_DEVEDOR", COUNT(*) AS total
    FROM divida_ativa
    GROUP BY "TIPO_DEVEDOR","UF_DEVEDOR"
"""
colunas = pd.read_sql(query_column_name,engine)
devedorPorTipo = pd.read_sql(query_devedor_tipo,engine)
devedorPorUf = pd.read_sql(query_devedor_uf,engine)

print(colunas)
print(devedorPorTipo)
print(devedorPorUf)