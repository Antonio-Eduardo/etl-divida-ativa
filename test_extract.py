from src.extract import extrair

df = extrair()
print(df.shape)
print(df.head())
print(df.isnull().sum())