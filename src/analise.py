from load import abrirConexao
import matplotlib.pyplot as plt
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

total_geral = devedorPorTipo["total"].sum()
bars = plt.bar(devedorPorTipo["TIPO_DEVEDOR"], devedorPorTipo["total"])
for bar in bars:
    altura = bar.get_height()
    percentual = altura/total_geral * 100
    plt.text(
        bar.get_x() + bar.get_width()/2,
        altura,
        f"{altura:,.0f} ({percentual:.1f}%)",
        ha="center",va="bottom"
    )
plt.title("Quantidade de devedores por tipo")
plt.xlabel("Tipo de devedor")
plt.ylabel("Total de registros")
plt.ticklabel_format(style="plain", axis="y")
plt.yscale("log")
plt.show()