import numpy as np
import scipy.odr as odr
import pandas as pd
import os
from scipy.optimize import curve_fit

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
    return [np.sqrt(np.sum(np.square(coluna_erros[i:(i+3)])))/3 for i in [0,3,6]]

# variavel contendo os picos identificados no olhometro
picos_olhometro = {
    "180C - 0.5V": [12.0, 16.375, 21.16, 26.14, 31.05, 36.09, 41.2],
    "180C - 1.5V": [12.34, 16.62, 21.3, 26.05, 30.92, 35.83, 40.868],
    "180C - 2.5V": [12.65, 16.94, 21.52, 26.37, 31.27, 36.1, 41.09],
    "190C - 0.5V": [17.34, 21.58, 26.355, 31.14, 35.976, 40.932],
    "190C - 1.5V": [12.83, 17.08, 21.533, 26.194, 30.845, 35.769, 40.555],
    "190C - 2.5V": [12.87, 17.39, 21.844, 26.57, 31.184, 36.048, 40.87],
    "200C - 0.5V": [17.58, 22.15, 26.8, 31.466, 36.098, 40.945],
    "200C - 1.5V": [17.54, 21.91, 26.455, 31.11, 35.822, 40.614],
    "200C - 2.5V": [17.51, 22.09, 26.91, 31.47, 36.16, 41.06]
}

# funcao que pega um ponto no continuo e retorna
# o argumento mais proximo num dominio discreto
def pegar_ponto(serie, ponto):
    # serie eh uma lista ou vetor
    # ponto eh o ponto para o qual queremos achar o mais poximo
    return min(serie, key=lambda x: abs(ponto-x))

# funcao que pega um ponto da serie
# e retorna o indice desse ponto
def pegar_indice(serie, ponto):
    return np.argmax([ponto == j for j in serie])

# funcao para calcular o potencial de excitacao pelo metodo das diferencas
def diff(serie):
    return [serie[i+1] - serie[i] for i in range(len(serie)-1)]

# funcao para propagar erro do metodo das diferencas
def erro_diff(serie):
    return [np.sqrt(serie[i+1]**2 + serie[i]**2) for i in range(len(serie)-1)]

# funcao para calcular erro da media por propagacao
def erro_media(serie):
    return np.sqrt((np.square([i/len(serie) for i in serie])).sum())

def identificar_n_pico(pico):
    if pico < 15:
        return 3
    if pico < 20:
        return 4
    if pico < 25:
        return 5
    if pico < 30:
        return 6
    

# ajuste linear
def linear(x, a, b):
    return a*x + b
def encaixar_linear(dados):
    # dados eh dataframe no formato x, y, erro_y
    popt, pcov = curve_fit(linear, dados.iloc[:,0], dados.iloc[:,1], sigma=dados.iloc[:,2])
    return pd.DataFrame({
        "parametros": [popt[0], popt[1]],
        "erros": [np.sqrt(pcov[0,0]), np.sqrt(pcov[1,1])]
    })