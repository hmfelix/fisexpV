
import os
import json
import pandas as pd
os.chdir("exp 3 - franck-hertz")
from codigo import auxiliar

# IMPORTACAO

# importando dados brutos
dados_d1, chaves = auxiliar.importar_dados_d1()

# importando dados dos picos encontrados pelo metodo 1, ja tratados
with open("resultados/dia1/picos-metodo1.json", 'r') as arquivo:
    picos_metodo1 = json.load(arquivo)

# convertendo dados dos picos em um dicionario de dataframes
# (e visualizando)
for i in range(len(picos_metodo1)):
    picos_metodo1[chaves[i]] = pd.DataFrame(picos_metodo1[chaves[i]])
    print(chaves[i], '\n', picos_metodo1[chaves[i]], '\n')


#import importlib
#importlib.reload(auxiliar)

for i in range(len(picos_metodo1)):
    print(chaves[i], '\n', picos_metodo1[chaves[i]], '\n')