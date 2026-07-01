from load import abrirConexao
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

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
    SELECT "UF_DEVEDOR", COUNT(*) AS total
    FROM divida_ativa
    GROUP BY "UF_DEVEDOR"
    ORDER BY total DESC
"""
query_valor_medio_uf = """
    SELECT "UF_DEVEDOR", AVG("VALOR_CONSOLIDADO") AS valor_medio
    FROM divida_ativa
    GROUP BY "UF_DEVEDOR"
    """
query_valor_medio_tipo_pessoa = """
    SELECT "TIPO_PESSOA", AVG("VALOR_CONSOLIDADO) AS valor_medio
    FROM divida_ativa
    GROUP BY "TIPO_PESSOA"
"""
colunas = pd.read_sql(query_column_name,engine)
devedorPorTipo = pd.read_sql(query_devedor_tipo,engine)
devedorPorUf = pd.read_sql(query_devedor_uf,engine)

print(colunas)
print(devedorPorTipo)
print(devedorPorUf["UF_DEVEDOR"].unique())

#Grafico de barras para quantidade de devedores por tipo
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

#Grafico para visualização da quantidade de devedores por UF
bars = plt.bar(devedorPorUf["UF_DEVEDOR"], devedorPorUf["total"])
for bar in bars:
    altura = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width()/2,
        altura,
        f"{altura:,.0f}",
        ha="center",va="bottom",
        fontsize=8, rotation=10
    )
plt.title("Quantidade de devedores por UF")
plt.xlabel("UF do devedor")
plt.ylabel("Total de registros")
plt.ticklabel_format(style="plain", axis="y")
plt.show()

#Grafico tipo devedor por UF
query_tipo_devedor_por_uf = """
    SELECT "UF_DEVEDOR", "TIPO_PESSOA", COUNT(*) as total
    FROM divida_ativa
    GROUP BY "UF_DEVEDOR","TIPO_PESSOA"
"""
tipoDevedor_UF = pd.read_sql(query_tipo_devedor_por_uf,engine)
pivot =tipoDevedor_UF.pivot(index="UF_DEVEDOR", columns="TIPO_PESSOA",values="total")
x = np.arange(len(pivot.index))
largura = 0.4
barPF = plt.bar(x - largura/2, pivot["Pessoa física"], largura,label="PF")
barPJ = plt.bar(x + largura/2, pivot["Pessoa jurídica"], largura, label="PJ")
plt.xticks(x,pivot.index)
plt.title("Tipo devedor por UF")
plt.xlabel("UF do devedor")
plt.ylabel("Total de devedores")
plt.ticklabel_format(style="plain", axis="y")
plt.yscale("log")
plt.legend()
plt.show()