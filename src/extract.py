import pandas as pd
import glob

def extrair():
    arquivos = glob.glob("C:/Nao_Previdenciario/*.csv")
    dfs = [pd.read_csv(arquivo,sep=";",encoding="latin1") for arquivo in arquivos]
    df = pd.concat(dfs,ignore_index=True)
    return df

#Tive que criar uma nova função pra extrair arquivo por arquivo
#em um loop, a função extrair() deu erro de memoria pelo tamanho
#total dos 6 csv

def extrair_arquivo(arquivo):
    df = pd.read_csv(arquivo, sep=";",encoding="latin1")
    return df