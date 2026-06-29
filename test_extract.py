from src.extract import extrair
from src.transform import transformar
df = extrair()

df = transformar(df)

print(df.dtypes)