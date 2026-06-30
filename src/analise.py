from load import abrirConexao
import pandas as pd

engine = abrirConexao()
df = pd.read_sql("SELECT * FROM divida_ativa", engine)

print(df.columns)

print("Devedores Principal")
devedorPrincipal = df[df["TIPO_DEVEDOR"] == "PRINCIPAL"]

print("Devedores Corresponsavel")
devedorCorresponsavel = df[df["TIPO_DEVEDOR"] == "CORRESPONSAVEL"]
print("Devedir principal Info")
devedorPrincipal.info()
print("Devedir corresponsavel Info")
devedorCorresponsavel.info()
print("Devedor por UF")
devedorPorUf = df.groupby(["TIPO_DEVEDOR","UF_DEVEDOR"]).size()
print("Devedor principal por Pessoa fisica")
devedorPrincipalFisica = df[(df["TIPO_DEVEDOR"] == "PRINCIPAL") & (df["TIPO_PESSOA"] == "Pessoa física")]
print("Devedor principal por Pessoa juridica")
devedorPrincipalJuridica = df[(df["TIPO_DEVEDOR"] == "PRINCIPAL") & (df["TIPO_PESSOA"] == "Pessoa jurídica")]
print("Devedor corresponsavel por pessoa Fisica")
devedorCorresponsavelFisica = df[(df["TIPO_DEVEDOR"] == "CORRESPONSAVEL") & (df["TIPO_PESSOA"] == "Pessoa física")]
print("Devedor corresponsavel por pessoa Juridica")
devedorCorresponsavelJuridica = df[(df["TIPO_DEVEDOR"] == "CORRESPONSAVEL") & (df["TIPO_PESSOA"] == "Pessoa jurídica")]
