import pandas as pd
import glob

def extrair():
    arquivos = glob.glob("C:/Nao_Providenciario/*.csv")
    dfs = [pd.read_csv(arquivo,sep=";",encoding="latin1") for arquivo in arquivos]
    df = pd.concat(dfs,ignore_index=True)
    return df