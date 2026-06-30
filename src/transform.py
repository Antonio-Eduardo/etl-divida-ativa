import pandas as pd

def transformar(df):
    df["INDICADOR_AJUIZADO"] = df["INDICADOR_AJUIZADO"] == "SIM"
    df["NUMERO_INSCRICAO"] = df["NUMERO_INSCRICAO"].astype(str)
    df["DATA_INSCRICAO"] = pd.to_datetime(df["DATA_INSCRICAO"], format="%d/%m/%Y")
    colunas_texto = df.select_dtypes(include="object").columns
    df[colunas_texto] = df[colunas_texto].apply(lambda x: x.str.strip())
    return df