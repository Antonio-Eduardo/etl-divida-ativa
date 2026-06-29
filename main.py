from src.extract import extrair_arquivo
from src.transform import transformar
from src.load import carregar
import glob

arquivos = glob.glob("C:/Nao_Providenciario/*.csv")
for i, arquivo in enumerate(arquivos):
    df = extrair_arquivo(arquivo)
    df = transformar(df)
    carregar(df, if_exists="replace" if i==0 else "append")