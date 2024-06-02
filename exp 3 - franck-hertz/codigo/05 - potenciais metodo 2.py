# esse script eh analogo ao script "03 - potenciais metodo 1.py"
import os
import json
import pandas as pd
import numpy as np
os.chdir("exp 3 - franck-hertz")
from codigo import auxiliar

# IMPORTACAO

# importando dados brutos
dados_d1, chaves = auxiliar.importar_dados_d1()

# importando dados dos picos encontrados pelo metodo 2, ja tratados
with open("resultados/dia1/picos-metodo2.json", 'r') as arquivo:
    picos_metodo2 = json.load(arquivo)

# convertendo dados dos picos em um dicionario de dataframes
# (e visualizando)
for i in range(len(picos_metodo2)):
    picos_metodo2[chaves[i]] = pd.DataFrame(picos_metodo2[chaves[i]])
    print(chaves[i], '\n', picos_metodo2[chaves[i]], '\n')


# CALCULO BASE - PERIODOS DO POTENCIAL DE EXCITACAO

# calculando potenciais de excitacao pelo metodo das diferencas
U_E_metodo2_diff = {}
for i in range(len(picos_metodo2)):
    periodos = auxiliar.diff(picos_metodo2[chaves[i]]["V_A"])
    erros = auxiliar.erro_diff(picos_metodo2[chaves[i]]["Desv_pad V_A"])
    U_E_metodo2_diff[chaves[i]] = pd.DataFrame({
        "periodo": periodos,
        "erro": erros
    })
    print(chaves[i], '\n', U_E_metodo2_diff[chaves[i]], '\n')



# MEDIAS DO POTENCIAL DE EXCITACAO EM CADA FAIXA

# calculando medias de cada conjunto e respectivo erro
medias = []
erros_medias = []
for i in range(len(U_E_metodo2_diff)):
    media = U_E_metodo2_diff[chaves[i]]["periodo"].mean()
    erro_media = auxiliar.erro_media(U_E_metodo2_diff[chaves[i]]["erro"])
    medias.append(media)
    erros_medias.append(erro_media)


# POTENCIAL DE CONTATO

# a formula eh basicamente a seguinte:
# identificar o numero n do pico,
# depois subtrair do V_A do pico U_E*(n-1)
lista_n = [auxiliar.identificar_n_pico(picos_metodo2[chaves[i]]["V_A"][0]) for i in range(len(picos_metodo2))]
lista_U_C = []
erros_U_C = []
for i in range(len(lista_n)):
    U_C = picos_metodo2[chaves[i]]["V_A"][0] - (lista_n[i] - 1)*medias[i]
    erro_U_C = np.sqrt(picos_metodo2[chaves[i]]["Desv_pad V_A"][0]**2 + ((lista_n[i]-1)*erros_medias[i])**2)
    lista_U_C.append(U_C)
    erros_U_C.append(erro_U_C)
auxiliar.media_medias(lista_U_C)
auxiliar.erro_media_medias(erros_U_C)

# juntando em uma tabela
potenciais_metodo2_diff = pd.DataFrame({
    "Faixa": chaves,
    "U_E": medias,
    "Erro U_E": erros_medias,
    "U_C": lista_U_C,
    "Erro U_C": erros_U_C
})


# U_E  e U_C PELO METODO DE AJUSTE LINEAR

# preparacao dos dados
lista_dfs_p_ajuste_linear = [
    pd.DataFrame({
        "x": list(range(9-len(picos_metodo2[chaves[i]]),9)), # numero do pico
        "y": picos_metodo2[chaves[i]]["V_A"],
        "dy": picos_metodo2[chaves[i]]["Desv_pad V_A"]
    }) for i in range(9)
]
for i in range(9):
    print(chaves[i], '\n', lista_dfs_p_ajuste_linear[i], '\n')

# ajuste
lista_ajustes_lineares = [auxiliar.encaixar_linear(df) for df in lista_dfs_p_ajuste_linear]
for i in range(9):
    print(chaves[i], '\n', lista_ajustes_lineares[i], '\n')

# consolidacao em uma tabela
potenciais_metodo2_linear = pd.DataFrame({
    "Faixa": chaves,
    "U_E": [lista_ajustes_lineares[i].iloc[0,0] for i in range(9)],
    "Erro U_E": [lista_ajustes_lineares[i].iloc[0,1] for i in range(9)],
    "U_C": [lista_ajustes_lineares[i].iloc[1,0] for i in range(9)],
    "Erro U_C": [lista_ajustes_lineares[i].iloc[1,1] for i in range(9)]
})


# MEDIA DAS DUAS ABORDAGENS

U_E_medio = []
U_E_medio_erro = []
U_C_medio = []
U_C_medio_erro = []
for i in range(9):
    U_E_medio.append((potenciais_metodo2_diff["U_E"][i] + potenciais_metodo2_linear["U_E"][i])/2)
    U_E_medio_erro.append(auxiliar.erro_media([potenciais_metodo2_diff["Erro U_E"][i], potenciais_metodo2_linear["Erro U_E"][i]]))
    U_C_medio.append((potenciais_metodo2_diff["U_C"][i] + potenciais_metodo2_linear["U_C"][i])/2)
    U_C_medio_erro.append(auxiliar.erro_media([potenciais_metodo2_diff["Erro U_C"][i], potenciais_metodo2_linear["Erro U_C"][i]]))
potenciais_metodo2_media = pd.DataFrame({
    "Faixa": chaves,
    "U_E": U_E_medio,
    "Erro U_E": U_E_medio_erro,
    "U_C": U_C_medio,
    "Erro U_C": U_C_medio_erro
})

# salvando
potenciais_metodo2_media.to_csv("resultados/dia1/potenciais_m2.csv", index=False)


# MEDIA DE MEDIAS DE CADA FAIXA DE TEMPERATURA
potenciais_metodo2_media_medias = pd.DataFrame({
    "U_E": auxiliar.media_medias(potenciais_metodo2_media["U_E"]),
    "Erro U_E": auxiliar.erro_media_medias(potenciais_metodo2_media["Erro U_E"]),
    "U_C": auxiliar.media_medias(potenciais_metodo2_media["U_C"]),
    "Erro U_C": auxiliar.erro_media_medias(potenciais_metodo2_media["Erro U_C"])
})
potenciais_metodo2_media_medias.to_csv("resultados/dia1/potenciais_m2_media_medias.csv", index=False)


# MEDIA FINAL
potenciais_metodo2_final = {
    "U_E": auxiliar.media_medias(potenciais_metodo2_media_medias["U_E"])[0],
    "Erro U_E": auxiliar.erro_media_medias(potenciais_metodo2_media_medias["Erro U_E"])[0],
    "U_C": auxiliar.media_medias(potenciais_metodo2_media_medias["U_C"])[0],
    "Erro U_C": auxiliar.erro_media_medias(potenciais_metodo2_media_medias["Erro U_C"])[0]
}




picos_metodo2[chaves[6]]

