import os
import numpy as np
import json
os.chdir("exp 3 - franck-hertz")
from codigo import auxiliar

# diferente do que foi feito na sintese,
# em vez de olhometro vamos usar o metodo do FWHM
# (Full Width Half Maximum)

# importando dados
dados_d1, chaves = auxiliar.importar_dados_d1()

# dicionario para estocar dados obtidos do metodo 1:
picos_metodo1 = {}

# metodo FWHM (Full Width Half Maximum)
# para cada pico encontrado no olhometro,
# filtrar um escopo de 3V a frente
# e pegar o ponto minimo, depois encontrar a corrente half maxima,
# e obter V_A desta corrente, reproduzindo o mesmo intervalo no lado
# esquerdo e obtendo V_A media entre half max esquerda e direita:
for i in range(len(dados_d1)):
    df = dados_d1[chaves[i]]
    V_A = df.iloc[:,0]
    picos_estimados_V_A = []
    picos_estimados_corrente = []
    erros_V_A = []
    V_A_infs = []
    V_A_sups = []
    for pico in auxiliar.picos_olhometro[chaves[i]]:
        pico_no_dominio = auxiliar.pegar_ponto(V_A, pico)
        sup_corte_1 = auxiliar.pegar_ponto(V_A, pico_no_dominio + 2.75)
        indice_pico = auxiliar.pegar_indice(V_A, pico_no_dominio)
        indice_sup_corte_1 = auxiliar.pegar_indice(V_A, sup_corte_1)
        corte_1 = df.iloc[indice_pico:indice_sup_corte_1]
        corrente_vale = min(corte_1.iloc[:,1])
        half_max = (df.iloc[:,1][indice_pico] - corrente_vale)/2
        indice_half_max_corte_1 = auxiliar.pegar_indice(corte_1.iloc[:,1], auxiliar.pegar_ponto(corte_1.iloc[:,1], corrente_vale + half_max))
        indice_half_max_direita = indice_pico + indice_half_max_corte_1
        indice_half_max_esquerda = indice_pico - indice_half_max_corte_1
        # resultados
        pico_estimado_V_A = (V_A[indice_half_max_esquerda] + V_A[indice_half_max_direita])/2
        indice_pico_estimado_corrente = auxiliar.pegar_indice(V_A, auxiliar.pegar_ponto(V_A, pico_estimado_V_A))
        pico_estimado_corrente = df.iloc[:,1][indice_pico_estimado_corrente]
        erro_V_A = (V_A[indice_half_max_direita] - V_A[indice_half_max_esquerda]) / 2
        V_A_inf = V_A[indice_half_max_esquerda]
        V_A_sup = V_A[indice_half_max_direita]
        # registro:
        picos_estimados_V_A.append(pico_estimado_V_A)
        picos_estimados_corrente.append(pico_estimado_corrente)
        erros_V_A.append(erro_V_A)
        V_A_infs.append(V_A_inf)
        V_A_sups.append(V_A_sup)
    resultados = {
        "V_A": picos_estimados_V_A,
        "I": picos_estimados_corrente,
        "Erro V_A": erros_V_A,
        "V_A_inf": V_A_infs,
        "V_A_sup": V_A_sups
    }
    picos_metodo1[chaves[i]] = resultados
    
# visualizacao:
#for i in range(9):
#    print(picos_metodo1[chaves[i]], '\n')

# exportando:
caminho_exportacao = "resultados/dia1/picos-metodo1.json"
with open(caminho_exportacao, 'w') as arquivo:
    json.dump(picos_metodo1, arquivo)


