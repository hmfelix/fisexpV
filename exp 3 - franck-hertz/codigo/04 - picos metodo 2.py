import os
import json
import pandas as pd
os.chdir("exp 3 - franck-hertz")
from codigo import auxiliar

# IMPORTACAO

# importando dados brutos
dados_d1, chaves = auxiliar.importar_dados_d1()

# METODO 2

# estrutura de dados para salvar os resultados de gaussianas de cada temperatura/voltagem
# lista para cada temperatura/voltagem de lista para cada pico de lista para cada resultado de ajuste
lista_ajustes_gaussianos = []

# loop para encaixar uma gaussiana em cada pico, e ja plotar
for i in range(len(auxiliar.picos_olhometro)):
    elemento_lista_ajustes_gaussianos = []
    for j in range(len(auxiliar.picos_olhometro[chaves[i]])):
        pico = auxiliar.picos_olhometro[chaves[i]][j]
        # pegando apenas a regiao a um raio de 1.5V do pico selecionado
        escopo_de_ajuste = dados_d1[chaves[i]][(dados_d1[chaves[i]].iloc[:,0] > pico - 1.5) & (dados_d1[chaves[i]].iloc[:,0] < pico + 1.5)].iloc[:,[0,1]]
        indice_centro = int(len(escopo_de_ajuste)/2)
        ajuste = auxiliar.encaixar_gaussiana(escopo_de_ajuste, [escopo_de_ajuste.iloc[indice_centro,1], escopo_de_ajuste.iloc[indice_centro,0], 1, escopo_de_ajuste.iloc[1,0]])
        elemento_lista_ajustes_gaussianos.append(ajuste)
    lista_ajustes_gaussianos.append(elemento_lista_ajustes_gaussianos)

# pontos colhidos pelas gaussianas (metodo 2)
picos_metodo2 = {}
for i in range(len(chaves)):
    picos_metodo2[chaves[i]] = pd.DataFrame({
        "V_A": [lista_ajustes_gaussianos[i][j][0][1] for j in range(len(lista_ajustes_gaussianos[i]))],
        "Desv_pad V_A": [lista_ajustes_gaussianos[i][j][0][2] for j in range(len(lista_ajustes_gaussianos[i]))],
        "Amplitude": [lista_ajustes_gaussianos[i][j][0][0] for j in range(len(lista_ajustes_gaussianos[i]))],
        "Intercepto": [lista_ajustes_gaussianos[i][j][0][3] for j in range(len(lista_ajustes_gaussianos[i]))]
    })
    print(chaves[i], '\n', picos_metodo2[chaves[i]], '\n')


# TRATAMENTO

# vou retirar os picos com desv_pad > 4
for i in range(9):
    picos_metodo2[chaves[i]] = picos_metodo2[chaves[i]][picos_metodo2[chaves[i]]["Desv_pad V_A"] < 4]
    print(chaves[i], '\n', picos_metodo2[chaves[i]], '\n')

# apenas um ponto ficou ruim (desvpad absurdo), vamos removê-lo:
#picos_metodo2[chaves[6]] = picos_metodo2[chaves[6]].iloc[1:]



# EXPORTACAO
for i in range(9):
    df = picos_metodo2[chaves[i]]
    picos_metodo2[chaves[i]] = df.to_dict()
caminho_exportacao = "resultados/dia1/picos-metodo2.json"
with open(caminho_exportacao, 'w') as arquivo:
    json.dump(picos_metodo2, arquivo)

