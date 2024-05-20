# pandas e o pacote mais popular para analise de dados
# vamos importar um arquivo que já havíamos gerado:

import pandas as pd

# Load the CSV file into a DataFrame
df = pd.read_csv('aprendendoPython/dados.csv')

# Display the first few rows of the DataFrame
print(df.head())

# mostra apenas a coluna 1 (ou melhor, 0):
# com base no nome:
print(df['X'])
# com base no indice 0 (jesus que complicado)
print(df.iloc[:, 0])

# digamos que eu queira selecionar uma linha, aí ficaria:
print(df.iloc[0,:])