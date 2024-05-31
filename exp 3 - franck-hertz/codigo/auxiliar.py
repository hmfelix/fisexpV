import numpy as np
import scipy.odr as odr
import pandas as pd
import os

# funcao para modelo gaussiano
def gaussiana(B, x):
    # B eh o vetor de parametros
    # x eh uma array de valores do eixo x
    # na funcao encaixar
    return B[0] * np.exp( - (x-B[1])**2 / (2*B[2]**2) ) + B[3]
gauss = odr.Model(gaussiana)

# ajuste gaussiano
def encaixar_gaussiana(dados, chutes):
    # dados eh um data frame com valores do eixo x e y
    # retorna lista com duas listas: valores estimados para B[i]; respectivas incertezas
    dados = odr.RealData(dados.iloc[:,0],dados.iloc[:,1])
    obj_odr = odr.ODR(dados, gauss, beta0=chutes)
    output = obj_odr.run()
    resultado = [
        list(output.beta),
        [
            np.sqrt(output.cov_beta[0,0]),
            np.sqrt(output.cov_beta[1,1]),
            np.sqrt(output.cov_beta[2,2]),
            np.sqrt(output.cov_beta[3,3])
        ]
    ]
    return resultado

# funcao para importar os dados
def importar_dados_d1():
    # caminho dos dados
    diretorio_d1 = "dados brutos/dia 1/"
    caminhos_d1 = os.listdir(diretorio_d1)
    # importacao em um dicionario
    dados_d1 = {caminho.replace(".tsv", ''): pd.read_csv(diretorio_d1 + caminho, sep='\t') for caminho in caminhos_d1}
    chaves = list(dados_d1.keys())
    return (dados_d1, chaves)

# funcao para calcular media das medias de cada trinca de tensões de retardo
def media_medias(coluna_resultados): # coluna_resultados a coluna de interesse, com um resultado para cada par (V_r, T)
    return [np.sum(coluna_resultados[i:(i+3)])/3 for i in [0,3,6]]

# funcao para propagar o erro da media de medias quando as incertezas sao diferentes entre as medias
def erro_media_medias(coluna_erros): # coluna_erros a coluna com as incertezas das medias de interesse, com um resultado para cada par (V_r, T)
    return [np.sqrt(np.sum(np.square(coluna_erros[i:(i+3)]))) for i in [0,3,6]]