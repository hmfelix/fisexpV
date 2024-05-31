import numpy as np
import scipy.odr as odr
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

# ajuste linear
def linear(x, a, b):
    return a*x + b

def encaixar_linear(dados):
    # dados eh dataframe no formato x, y, erro_y
    popt, pcov = curve_fit(linear, dados.iloc[:,0], dados.iloc[:,1], sigma=dados.iloc[:,2])
    return [[popt[0], popt[1]], [np.sqrt(pcov[0,0]), np.sqrt(pcov[1,1])]]