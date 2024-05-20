from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import scipy.odr as odr

df = pd.read_csv('aprendendoPython/dados.csv')

#### nao deu certo esse trecho ###
# tentativa de fazer o ajuste em vez de regressão, usando erros como pesos:
# weights = 1 / (np.square(df['Erro_X']) + np.square(df['Erro_Y']))
# ajuste linear:
# np.polyfit(df['X'], df['Y'], 1, w=weights)
#### ####

# vou tentar usando o ODR:
# (fiz usando o guia da página oficial https://docs.scipy.org/doc/scipy/reference/odr.html)

# definindo a funcao teorica (modelo de ajuste):
def f(B, x):
    # B eh o vetor de parametros
    # x eh uma array no formato dado na documentacao do pacote
    return B[0]*x + B[1] # no caso, um modelo linear

# criando o objeto de classe modelo
linear = odr.Model(f)

# criando o objeto de classe dados
dados = odr.RealData(df['X'], df['Y'], df['Erro_X'], df['Erro_Y'])

# criando o objeto de classe odr 
# (aqui precisa ter estimativa de parametros iniciais)
obj_odr = odr.ODR(dados, linear, beta0=[0,1])

# criando o objeto output
myoutput = obj_odr.run()

# examinando:
myoutput.pprint()
print(myoutput.cov_beta) # matriz de covariancia (diag principal = variancia dos parametros)
print(myoutput.sd_beta) # desvio padrao (erro) dos parametros escalado pela variancia dos residuos
print([np.sqrt(myoutput.cov_beta[0,0]), np.sqrt(myoutput.cov_beta[1,1])]) # desvio padrao sem escalar nada

# notar o seguinte:
# o erro dos params. dado por este objeto eh escalado pela variancia dos residuos
# o desvio padrao normal seria apenas a raiz dos elementos da diag principal da matriz de cov
# qual das medidas eh melhor?
# vou comparar com o atus
# COMPARADO!!!
# vejamos:
# Param        | Atus      | ODR
# a ou B[0]    | 2.312118  | 2.31211381
# b ou B[1]    | 3.410546  | 3.41057805
# erro a       | 0.053759  | 0.11744663
# erro b       | 0.410925  | 0.89773677
# sqrt(var) a  | -         | 0.0537591573944188
# sqrt(var) b  | -         | 0.4109234318246743

# Conclusão:
# parametros estao mto proximos, sao equivalentes em teste Z
# porem existe diferenca e temos que ficar atentos
# erro correto dos params eh o que eu bolei:
# raiz sem escalar por residuos
# vou usar esse entao

plt.errorbar(
    df['X'],
    df['Y'],
    xerr=df['Erro_X'].abs(),
    yerr=df['Erro_Y'].abs(),
    fmt = 'o', # formato dos pontos, previne linhas ligando-os
    ecolor = 'black', # cor das barras de erro
    elinewidth = .5, # espessura das barras de erro
    capsize = 0, # espessura das marcações nas extremidades das barras de erro
    color = 'black', # cor dos pontos
    markersize = 2 # tamanho dos pontos
)
plt.plot(
    np.arange(0, 10, 0.1),
    myoutput.beta[0]*np.arange(0, 10, 0.1) + myoutput.beta[1],
    color = 'red'
)
plt.title('Teste')
plt.xlabel('Grandeza X (unid.)')
plt.ylabel('Grandeza Y (unid.)')
plt.show()

# rolou cabulosoooo!!!!
# sucesso!!!







