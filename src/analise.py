# %%
from load import abrirConexao
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
engine = abrirConexao()

# %%
#Grafico de barras para quantidade de devedores por tipo
query_devedor_tipo = """
    SELECT "TIPO_DEVEDOR", COUNT(*) AS total
    FROM divida_ativa
    GROUP BY "TIPO_DEVEDOR"
"""
devedorPorTipo = pd.read_sql(query_devedor_tipo,engine)
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

# %%
#Grafico para visualização da quantidade de devedores por UF
query_devedor_uf = """
    SELECT "UF_DEVEDOR", COUNT(*) AS total
    FROM divida_ativa
    GROUP BY "UF_DEVEDOR"
    ORDER BY total DESC
"""
devedorPorUf = pd.read_sql(query_devedor_uf,engine)

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

# %%
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

# %%
#Analisar  inscrições por ano
query_inscricao_por_ano="""
    SELECT
        EXTRACT(YEAR FROM "DATA_INSCRICAO") AS ano,
        COUNT(*) AS quantidade
    FROM divida_ativa
    WHERE "DATA_INSCRICAO" >= '2020-01-01'
    GROUP BY ano
    ORDER BY ano;
"""
inscricaoAno = pd.read_sql(query_inscricao_por_ano,engine)
bars = plt.bar(inscricaoAno["ano"], inscricaoAno["quantidade"])
for bar in bars:
    altura = bar.get_height()
    plt.text(
          bar.get_x() + bar.get_width()/2,
        altura,
        f"{altura:,.0f}",
        ha="center",va="bottom",
        fontsize=8
        )
plt.xlabel("Anos")
plt.ylabel("Quantidade")
plt.show()

# %%
#qual % do valor total está nos maiores devedores
query_maiores_devedores="""
    WITH divida_por_devedor AS(
        SELECT "CPF_CNPJ",
        SUM("VALOR_CONSOLIDADO") AS valor_total_devedor
        FROM divida_ativa
        GROUP BY "CPF_CNPJ"
        )
    SELECT "CPF_CNPJ",valor_total_devedor,
    ROW_NUMBER() OVER(ORDER BY valor_total_devedor DESC) AS posicao,
    SUM(valor_total_devedor) OVER(ORDER BY valor_total_devedor DESC)
    / SUM(valor_total_devedor) OVER() AS pct_valor_acumulado,
    ROW_NUMBER() OVER(ORDER BY valor_total_devedor DESC)
    ::float / COUNT(*) OVER() as pct_devedores
    FROM divida_por_devedor
    ORDER BY valor_total_devedor DESC;
"""
concentracao = pd.read_sql(query_maiores_devedores,engine)

plt.plot(concentracao["pct_devedores"],concentracao["pct_valor_acumulado"],label="Concentração Real")
plt.plot([0,1], [0,1], linestyle="--",
         color="gray", label="Distribuição igualitária")
plt.xlabel("% dos devedores (do maior para o menor)")
plt.ylabel("% do valor total acumulado")
plt.title("Concentração do valor da dívida ativa")
plt.legend()
plt.show()
# %%
#Identificar os 20 maiores devedores com base na concentração da divida ativa
query_ident_devedores="""
    SELECT "CPF_CNPJ","NOME_DEVEDOR", SUM("VALOR_CONSOLIDADO") AS valor_total_devedor
    FROM divida_ativa
    GROUP BY "CPF_CNPJ","NOME_DEVEDOR" 
    ORDER BY valor_total_devedor DESC
    LIMIT 20
"""
devedores= pd.read_sql(query_ident_devedores,engine)
pd.options.display.float_format = '{:,.2f}'.format
print(devedores)
# %%
