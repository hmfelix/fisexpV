

##### 0) Setup #################################################################

# diretorio:
import os
# mudando para o subdiretorio:
os.chdir('Dia 1/')

# modularização e bibliotecas:
import auxiliar as aux
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import latex
import scipy.odr as odr
from scipy import interpolate
from scipy.optimize import curve_fit

# funcao para imprimir dataframes completos
def print_full(x):
    pd.set_option('display.max_rows', len(x))
    print(x)
    pd.reset_option('display.max_rows')

# setup da fonte de Latex:
plt.rc('text', usetex = True) # para usar a fonte do latex nos graficos
                              # (notar: requer instalação do latex no PC)
plt.rc('font', family='serif') # previne o uso de fonte sem serifa nos titulos

##### 1) Grafico 0: Teste inicial NaCl #########################################
# importando os dados
df_NaCl = pd.read_csv("NaCl.txt", sep = "	", decimal = ",")
# lindo argumento decimal, que já converte as vírgulas para pontos na importação

# inspecionando para ver se funcionou
df_NaCl.head()
print(df_NaCl.columns)

# agora vamos plotar

# variaveis
t = df_NaCl.iloc[:,0] # angulo
y_0 = df_NaCl.iloc[:,1] / 1000 # divindo por mil para melhorar o plot

# plotando
plt.plot(t, y_0, linewidth=3)
plt.suptitle('Coleta de Teste NaCl', fontsize=23)
plt.title('($U = 35$ kV e $\\Delta t = 1$ s)', fontsize=17)
plt.xlabel('$\\beta$ ($^{\\circ}$)', fontsize=18)
plt.ylabel('$I$ ($10^3$/s)', fontsize=18)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.xlim(t.min(),t.max())
plt.ylim(0,2.7)
plt.subplots_adjust(bottom=0.13, right=0.98, left=0.11, top=0.85)

# plot gráfico 0
plt.show()
plt.savefig('d1-graf0-coleta_teste_NaCl.svg', format='svg')
plt.close()


##### 2) Gráfico 1: Demais coletas #############################################

# plotando
# parece que existem várias formas de plotar vários conjuntos de dados
# poderíamos passar (x, y) onde y é uma array em que cada linha é um dos valores de y
# podemos chamar plot (x, y_1), depois plot(x, y_2) etc
# ou podemos usar grupos (que parece que aplica os mesmos estilos a todos)
# vamos usar o segundo método porque quero entender essa feature de selecionar "shape" de arrays

# selecionando apenas dados da segunda coleta
y = df_NaCl.iloc[:,2:]
# excluindo linhas NaN
y = y.dropna()
t_semNaN = t[0:len(y)]
# dividindo por mil para se mais economico no eixo y:
y = y/1000
# definindo previamente as caracteristicas das linhas
cores = ['blue', 'red', 'green', 'brown', 'purple']
legenda = ['$U = 35$ kV', '$U = 30$ kV', '$U = 26$ kV', '$U = 22$ kV', '$U = 18$ kV']

# agora tentando o plot
for col in range(y.shape[1]):
    plt.plot(t_semNaN, y.iloc[:,col], color=cores[col], label=legenda[col])
plt.legend(fontsize=12)
plt.title('Coleta NaCl', fontsize=23)
#plt.title('($U = 35$ kV e $\\Delta t = 1$ s)', fontsize=11)
plt.xlabel('$\\beta$ ($^{\\circ}$)', fontsize=18)
plt.ylabel('$I$ ($10^3$/s)', fontsize=18)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.xlim(t_semNaN.min(),t_semNaN.max())
plt.ylim(0,np.round(y.max().max(),1))
plt.grid()
plt.subplots_adjust(bottom=0.13, right=0.98, left=0.11, top=0.92)

# plot gráfico 1
plt.show()

# exportando
plt.savefig('d1-graf1-coleta_NaCl.svg', format='svg')


##### 3) Gráfico 2: Intensidade x energia ######################################

# temos de usar a formula dada nos slides para converter angulo em energia
# Lei de Bragg: n lambda = 2 d sen(theta)
# n = 1
# E = hc /  2 d sen(theta)
E = (6.62607015 * 10**(-34) * 299792458 / (2 * 0.282 * 10**(-9) * np.sin(np.deg2rad(t_semNaN)))) / (1.602176634*10**-16)

# plotando
for col in range(y.shape[1]):
    plt.plot(E, y.iloc[:,col], color=cores[col], label=legenda[col])
plt.legend(fontsize=12)
plt.title('Intensidade vs. Energia (NaCl)', fontsize=23)
#plt.title('($U = 35$ kV e $\\Delta t = 1$ s)', fontsize=11)
plt.xlabel('$E$ (keV)', fontsize=18)
plt.ylabel('$I$ ($10^3$/s)', fontsize=18)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.xlim(E.min(),E.max())
plt.ylim(0,np.round(y.max().max(),1))
plt.grid()
plt.subplots_adjust(bottom=0.13, right=0.98, left=0.11, top=0.92)

# plot gráfico 1
plt.show()

# exportando
plt.savefig('d1-graf2-IxE-NaCl.svg', format='svg')


##### 4) Gráfico 3: Teste inicial KBr ##########################################

# importando os dados
df_KBr = pd.read_csv("KBr.txt", sep = "	", decimal = ",")

# inspecionando para ver se funcionou
df_KBr
print(df_KBr.columns)

# variaveis
x = df_KBr.iloc[:,0] # angulo
y_0_KBr = df_KBr.iloc[:,1] / 100 # divindo por mil para melhorar o plot
# y_0_max = 0.5 + np.ceil((df_KBr.iloc[:,1] / 10).max()) / 10

# plotando
plt.plot(x, y_0_KBr, linewidth=3)
plt.suptitle('Coleta de Teste KBr', fontsize=23)
plt.title('($U = 35$ kV e $\\Delta t = 1$ s)', fontsize=17)
plt.xlabel('$\\beta$ ($^{\\circ}$)', fontsize=18)
plt.ylabel('$I$ ($10^2$/s)', fontsize=18)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.xlim(x.min(),x.max())
plt.ylim(0, 6)
plt.subplots_adjust(bottom=0.13, right=0.98, left=0.11, top=0.92)

# plot gráfico 0
plt.show()
plt.savefig('d1-graf3-coleta_teste_KBr.svg', format='svg')


##### 5) Gráfico 4: Demais coletas KBr #########################################

# selecionando apenas dados da segunda coleta
y_KBr = df_KBr.iloc[:,2:]
# excluindo linhas NaN
y_KBr = y_KBr.dropna()
x_semNaN = x[0:len(y_KBr)]
# dividindo por mil para se mais economico no eixo y:
y_KBr = y_KBr/100
# definindo previamente as caracteristicas das linhas
cores = ['blue', 'red', 'green', 'brown', 'purple']
legenda = ['$U = 35$ kV', '$U = 30$ kV', '$U = 26$ kV', '$U = 22$ kV', '$U = 18$ kV']

# agora tentando o plot
for col in range(y_KBr.shape[1]):
    plt.plot(x_semNaN, y_KBr.iloc[:,col], color=cores[col], label=legenda[col])
plt.legend(fontsize=12)
plt.title('Coleta KBr', fontsize=23)
#plt.title('($U = 35$ kV e $\\Delta t = 1$ s)', fontsize=11)
plt.xlabel('$\\beta$ ($^{\\circ}$)', fontsize=18)
plt.ylabel('$I$ ($10^2$/s)', fontsize=18)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.xlim(x_semNaN.min(),x_semNaN.max())
plt.ylim(0,6)
plt.grid()
plt.subplots_adjust(bottom=0.13, right=0.98, left=0.11, top=0.92)

# plot gráfico 1
plt.show()

# exportando
plt.savefig('d1-graf4-coleta_KBr.svg', format='svg')
plt.close()


##### 6) Gráfico 5: Intensidade x energia KBr ##################################

E_KBr = (6.62607015 * 10**(-34) * 299792458 / (2 * 0.329 * 10**(-9) * np.sin(np.deg2rad(x_semNaN)))) / (1.602176634*10**-16)

# plotando
for col in range(y_KBr.shape[1]):
    plt.plot(E_KBr, y_KBr.iloc[:,col], color=cores[col], label=legenda[col])
plt.legend(fontsize=12)
plt.title('Intensidade vs. Energia (KBr)', fontsize=23)
#plt.title('($U = 35$ kV e $\\Delta t = 1$ s)', fontsize=11)
plt.xlabel('$E$ (keV)', fontsize=18)
plt.ylabel('$I$ ($10^2$/s)', fontsize=18)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.xlim(E_KBr.min(),E_KBr.max())
plt.ylim(0,6)
plt.grid()
plt.subplots_adjust(bottom=0.15)
# plot gráfico 1
plt.show()
# exportando
plt.savefig('d1-graf5-IxE-KBr.svg', format='svg')
plt.close()


##### 7) Gráfico 6: Ajuste NaCl ################################################

# lambda mínimos (em pm)
l_NaCl = [3.20805057*10, 3.87515350*10, 4.46629187*10, 5.25761803*10, 6.39521951*10]
# incerteza do lambda mínimo
l_err_NaCl = [.491386007, .491019716, .490637186, .490039648, .489008520]
# tensão de aceleração
U = [35, 30, 26, 22, 18]
# incerteza da tensão
U_err = 5*[.1]
# juntando tudo em 1 dataframe:
df_Ajuste_NaCl = pd.DataFrame({
    'X': l_NaCl,
    'Erro_X': l_err_NaCl,
    'Y': U,
    'Erro_Y': U_err
})

# modelo:
def f(B, x):
    # B eh o vetor de parametros
    # x eh uma array no formato dado na documentacao do pacote
    return B[0]/x + B[1] # no caso, um modelo hiperbólico
# criando o objeto de classe modelo
linear = odr.Model(f)
# criando o objeto de classe dados
dados = odr.RealData(df_Ajuste_NaCl['X'], df_Ajuste_NaCl['Y'], df_Ajuste_NaCl['Erro_X'], df_Ajuste_NaCl['Erro_Y'])
# criando o objeto de classe odr 
# (aqui precisa ter estimativa de parametros iniciais)
obj_odr = odr.ODR(dados, linear, beta0=[1.14,2.23])
# criando o objeto output
myoutput = obj_odr.run()

# examinando
myoutput.pprint()
print(myoutput.cov_beta) # matriz de covariancia (diag principal = variancia dos parametros)
print(myoutput.sd_beta) # desvio padrao (erro) dos parametros escalado pela variancia dos residuos
print([np.sqrt(myoutput.cov_beta[0,0]), np.sqrt(myoutput.cov_beta[1,1])]) # desvio padrao sem escalar nada

# plot
plt.plot(
    np.arange(3*10, df_Ajuste_NaCl['X'].max()+.5*10, 1),
    myoutput.beta[0]/np.arange(3*10, df_Ajuste_NaCl['X'].max()+.5*10, 1) + myoutput.beta[1],
    color = 'red',
    linewidth=2.8
)
plt.errorbar(
    df_Ajuste_NaCl['X'],
    df_Ajuste_NaCl['Y'],
    xerr=df_Ajuste_NaCl['Erro_X'].abs(),
    yerr=df_Ajuste_NaCl['Erro_Y'].abs(),
    fmt = 'o', # formato dos pontos, previne linhas ligando-os
    ecolor = 'black', # cor das barras de erro
    elinewidth = 1.3, # espessura das barras de erro
    capsize = 0, # espessura das marcações nas extremidades das barras de erro
    color = 'black', # cor dos pontos
    markersize = 3.5 # tamanho dos pontos
)
plt.title('Ajuste NaCl', fontsize=23)
plt.ylabel('$U$ (kV)', fontsize=18)
plt.xlabel('$\\lambda_0$ (pm)', fontsize=18)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.subplots_adjust(bottom=0.15)
# mostrar
plt.show()
# salvar
plt.savefig('d1-graf6-ajuste_NaCl.svg', format='svg')
plt.close()

# calculando a constante de planck:
planck_NaCl = myoutput.beta[0]*1.6*10**(-19)*10**-9/299792458
# 6.091721081041774e-34
# erro:
planck_err_NaCl = np.sqrt(myoutput.cov_beta[0,0])*1.6*10**(-19)*10**-9/299792458
# 1.4594871271886667e-35
# 6.10(15) e-34
# ref:
(6.62607015*10**-34 - planck_NaCl) / planck_err_NaCl

##### 8) Gráfico 7: Ajuste KBr #################################################

# lambda mínimos (em pm)
l_KBr = [25.147672, 29.647182, 36.643514, 44.250930, 54.352796]
# incerteza do lambda mínimo
l_err_KBr = [.98338670, .98300477, .98228590, .98133123, .97978403]
# tensão de aceleração
U = [35, 30, 26, 22, 18]
# incerteza da tensão
U_err = 5*[.1]
# juntando tudo em 1 dataframe:
df_Ajuste_KBr = pd.DataFrame({
    'X': l_KBr,
    'Erro_X': l_err_KBr,
    'Y': U,
    'Erro_Y': U_err
})

# criando o objeto de classe dados
dados2 = odr.RealData(df_Ajuste_KBr['X'], df_Ajuste_KBr['Y'], df_Ajuste_KBr['Erro_X'], df_Ajuste_KBr['Erro_Y'])
# criando o objeto de classe odr 
# (aqui precisa ter estimativa de parametros iniciais)
obj_odr2 = odr.ODR(dados2, linear, beta0=[1.14,2.23])
# criando o objeto output
myoutput2 = obj_odr2.run()

# examinando
myoutput2.pprint()
print(myoutput2.cov_beta) # matriz de covariancia (diag principal = variancia dos parametros)
print(myoutput2.sd_beta) # desvio padrao (erro) dos parametros escalado pela variancia dos residuos
print([np.sqrt(myoutput2.cov_beta[0,0]), np.sqrt(myoutput2.cov_beta[1,1])]) # desvio padrao sem escalar nada

# plot
plt.plot(
    np.arange(20, 60, 1),
    myoutput2.beta[0]/np.arange(20, 60, 1) + myoutput2.beta[1],
    color = 'red',
    linewidth=2.8
)
plt.errorbar(
    df_Ajuste_KBr['X'],
    df_Ajuste_KBr['Y'],
    xerr=df_Ajuste_KBr['Erro_X'].abs(),
    yerr=df_Ajuste_KBr['Erro_Y'].abs(),
    fmt = 'o', # formato dos pontos, previne linhas ligando-os
    ecolor = 'black', # cor das barras de erro
    elinewidth = 1.3, # espessura das barras de erro
    capsize = 0, # espessura das marcações nas extremidades das barras de erro
    color = 'black', # cor dos pontos
    markersize = 3.5 # tamanho dos pontos
)
plt.title('Ajuste KBr', fontsize=23)
plt.ylabel('$U$ (kV)', fontsize=18)
plt.xlabel('$\\lambda_0$ (pm)', fontsize=18)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.subplots_adjust(bottom=0.15)
# mostrar
plt.show()
# salvar
plt.savefig('d1-graf7-ajuste_KBr.svg', format='svg')
plt.close()

# calculando a constante de planck:
planck_KBr = myoutput2.beta[0]*1.6*10**(-19)*10**-9/299792458
# 4.378229755935957e-34
# erro:
planck_err_KBr = np.sqrt(myoutput2.cov_beta[0,0])*1.6*10**(-19)*10**-9/299792458
# 2.1572848869711744e-35
(6.62607015*10**-34 - planck_KBr) / planck_err_KBr


##### 9) Gráfico 8: Coleta dia 2 ###############################################

# importando dados:
df_NaCl_d2 = pd.read_csv("NaCl-d2.txt", sep = "	", decimal = ",")
# renomeando colunas:
df_NaCl_d2 = df_NaCl_d2.set_axis(['beta', 'sem filtro', 'Zr', 'Mo', 'Al'], axis=1)
df_NaCl_d2['E'] = E
df_NaCl_d2['abs_Zr'] = df_NaCl_d2['sem filtro'] / df_NaCl_d2['Zr']
df_NaCl_d2['abs_Mo'] = df_NaCl_d2['sem filtro'] / df_NaCl_d2['Mo']
df_NaCl_d2['abs_Al'] = df_NaCl_d2['sem filtro'] / df_NaCl_d2['Al']

# plot dados brutos
cores2 = ['green', 'blue', 'red', 'orange']
legenda2 = ['S/ Filtro', 'Zr', 'Mo', 'Al']
for i in range(1,5):
    plt.plot(df_NaCl_d2['beta'], df_NaCl_d2.iloc[:,i] / 1000, color=cores2[i-1], label=legenda2[i-1], linewidth=2.5)
plt.legend(fontsize=12)
plt.title('Coleta Filtros (NaCl)', fontsize=23)
#plt.title('($U = 35$ kV e $\\Delta t = 1$ s)', fontsize=11)
plt.xlabel('$\\beta$ ($^{\\circ}$)', fontsize=18)
plt.ylabel('$I$ ($10^3$/s)', fontsize=18)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.xlim(df_NaCl_d2['beta'].min(),df_NaCl_d2['beta'].max())
# plt.ylim(0,np.round(y.max().max(),1))
plt.grid()
plt.subplots_adjust(bottom=0.13, right=0.98, left=0.11, top=0.92)
# mostrar
plt.show()
# salvar
plt.savefig('d2-graf8-coleta_NaCl.svg', format='svg')


##### 10) Gráfico 9: Int x energ dia 2 #########################################

for i in range(1,5):
    plt.plot(df_NaCl_d2['E'], df_NaCl_d2.iloc[:,i] / 1000, color=cores2[i-1], label=legenda2[i-1], linewidth=2.5)
plt.legend(fontsize=12)
plt.title('Intensidade vs Energia Filtros (NaCl)', fontsize=23)
#plt.title('($U = 35$ kV e $\\Delta t = 1$ s)', fontsize=11)
plt.xlabel('$E$ (keV)', fontsize=18)
plt.ylabel('$I$ ($10^3$/s)', fontsize=18)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.xlim(df_NaCl_d2['E'].min(),df_NaCl_d2['E'].max())
plt.ylim(0)
plt.grid()
plt.subplots_adjust(bottom=0.13, right=0.98, left=0.11, top=0.92)
# mostrar
plt.show()
# salvar
plt.savefig('d2-graf9-IxE_filtros-NaCl.svg', format='svg')
plt.close()


##### 11) Gráficos 10-12: Absortância x theta NaCl #############################

#  Zr
plt.plot(df_NaCl_d2['beta'], df_NaCl_d2['abs_Zr'], linewidth=3, color='blue')
plt.title('Absortância vs ângulo Zr (NaCl)', fontsize=23)
plt.ylabel('Absortância (s/ unid.)', fontsize=18)
plt.xlabel('$\\beta$ ($^{\\circ}$)', fontsize=18)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.subplots_adjust(bottom=0.15)
plt.xlim(df_NaCl_d2['beta'].min(), df_NaCl_d2['beta'].max())
plt.grid()
# mostrar
plt.show()
# exportar
plt.savefig('d2-graf10-AbsxBeta_Zr-NaCl.svg', format='svg')
plt.close()

# Mo
plt.plot(df_NaCl_d2['beta'], df_NaCl_d2['abs_Mo'], linewidth=3, color='red')
plt.title('Absortância vs ângulo Mo (NaCl)', fontsize=23)
plt.ylabel('Absortância (s/ unid.)', fontsize=18)
plt.xlabel('$\\beta$ ($^{\\circ}$)', fontsize=18)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.subplots_adjust(bottom=0.15)
plt.xlim(df_NaCl_d2['beta'].min(), df_NaCl_d2['beta'].max())
plt.grid()
# mostrar
plt.show()
# exportar
plt.savefig('d2-graf11-AbsxBeta_Mo-NaCl.svg', format='svg')
plt.close()

# Al
plt.plot(df_NaCl_d2['beta'], df_NaCl_d2['abs_Al'], linewidth=3, color='orange')
plt.title('Absortância vs ângulo Al (NaCl)', fontsize=23)
plt.ylabel('Absortância (s/ unid.)', fontsize=18)
plt.xlabel('$\\beta$ ($^{\\circ}$)', fontsize=18)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.subplots_adjust(bottom=0.15)
plt.xlim(df_NaCl_d2['beta'].min(), df_NaCl_d2['beta'].max())
plt.grid()
# mostrar
plt.show()
# exportar
plt.savefig('d2-graf12-AbsxBeta_Al-NaCl.svg', format='svg')
plt.close()


##### 12) Gráficos 13-15: Absortância x energia NaCl ###########################

#  Zr
plt.plot(df_NaCl_d2['E'], df_NaCl_d2['abs_Zr'], linewidth=3, color='blue')
plt.title('Absortância vs Energia Zr (NaCl)', fontsize=23)
plt.ylabel('Absortância (s/ unid.)', fontsize=18)
plt.xlabel('$E$ (keV)', fontsize=18)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.subplots_adjust(bottom=0.15)
plt.xlim(df_NaCl_d2['E'].min(), df_NaCl_d2['E'].max())
plt.grid()
# mostrar
#plt.show()
# exportar
plt.savefig('d2-graf13-AbsxE_Zr-NaCl.svg', format='svg')
plt.close()

# Mo
plt.plot(df_NaCl_d2['E'], df_NaCl_d2['abs_Mo'], linewidth=3, color='red')
plt.title('Absortância vs Energia Mo (NaCl)', fontsize=23)
plt.ylabel('Absortância (s/ unid.)', fontsize=18)
plt.xlabel('$E$ (keV)', fontsize=18)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.subplots_adjust(bottom=0.15)
plt.xlim(df_NaCl_d2['E'].min(), df_NaCl_d2['E'].max())
plt.grid()
# mostrar
#plt.show()
# exportar
plt.savefig('d2-graf14-AbsxE_Mo-NaCl.svg', format='svg')
plt.close()

# Al
plt.plot(df_NaCl_d2['E'], df_NaCl_d2['abs_Al'], linewidth=3, color='orange')
plt.title('Absortância vs Energia Al (NaCl)', fontsize=23)
plt.ylabel('Absortância (s/ unid.)', fontsize=18)
plt.xlabel('$E$ (keV)', fontsize=18)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.subplots_adjust(bottom=0.15)
plt.xlim(df_NaCl_d2['E'].min(), df_NaCl_d2['E'].max())
plt.grid()
# mostrar
#plt.show()
# exportar
plt.savefig('d2-graf15-AbsxE_Al-NaCl.svg', format='svg')
plt.close()


##### 13) Gráficos 16-23: Mesmos p/ KBr ########################################

# importando dados:
df_KBr_d2 = pd.read_csv("KBr-d2.txt", sep = "	", decimal = ",")
# renomeando colunas:
df_KBr_d2 = df_KBr_d2.set_axis(['beta', 'sem filtro', 'Zr', 'Mo', 'Al'], axis=1)
df_KBr_d2['E'] = E_KBr
df_KBr_d2['abs_Zr'] = df_KBr_d2['sem filtro'] / df_KBr_d2['Zr']
df_KBr_d2['abs_Mo'] = df_KBr_d2['sem filtro'] / df_KBr_d2['Mo']
df_KBr_d2['abs_Al'] = df_KBr_d2['sem filtro'] / df_KBr_d2['Al']

# plot dados brutos
cores2 = ['green', 'blue', 'red', 'orange']
legenda2 = ['S/ Filtro', 'Zr', 'Mo', 'Al']
for i in range(1,5):
    plt.plot(df_KBr_d2['beta'], df_KBr_d2.iloc[:,i] / 100, color=cores2[i-1], label=legenda2[i-1], linewidth=2.5)
plt.legend(fontsize=12)
plt.title('Coleta Filtros (KBr)', fontsize=23)
#plt.title('($U = 35$ kV e $\\Delta t = 1$ s)', fontsize=11)
plt.xlabel('$\\beta$ ($^{\\circ}$)', fontsize=18)
plt.ylabel('$I$ ($10^2$/s)', fontsize=18)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.xlim(df_KBr_d2['beta'].min(),df_KBr_d2['beta'].max())
# plt.ylim(0,np.round(y.max().max(),1))
plt.grid()
plt.subplots_adjust(bottom=0.13, right=0.98, left=0.11, top=0.92)
# mostrar
plt.show()
# salvar
plt.savefig('d2-graf16-coleta_KBr.svg', format='svg')
plt.close()


# Int x energ 

for i in range(1,5):
    plt.plot(df_KBr_d2['E'], df_KBr_d2.iloc[:,i] / 100, color=cores2[i-1], label=legenda2[i-1], linewidth=2.5)
plt.legend(fontsize=12)
plt.title('Intensidade vs Energia Filtros (KBr)', fontsize=23)
#plt.title('($U = 35$ kV e $\\Delta t = 1$ s)', fontsize=11)
plt.xlabel('$E$ (keV)', fontsize=18)
plt.ylabel('$I$ ($10^2$/s)', fontsize=18)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.xlim(df_KBr_d2['E'].min(),df_KBr_d2['E'].max())
plt.ylim(0)
plt.grid()
plt.subplots_adjust(bottom=0.13, right=0.98, left=0.11, top=0.92)
# mostrar
plt.show()
# salvar
plt.savefig('d2-graf17-IxE_filtros-KBr.svg', format='svg')
plt.close()

# Absortância x theta

#  Zr
plt.plot(df_KBr_d2['beta'], df_KBr_d2['abs_Zr'], linewidth=3, color='blue')
plt.title('Absortância vs ângulo Zr (KBr)', fontsize=23)
plt.ylabel('Absortância (s/ unid.)', fontsize=18)
plt.xlabel('$\\beta$ ($^{\\circ}$)', fontsize=18)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.subplots_adjust(bottom=0.15)
plt.xlim(df_KBr_d2['beta'].min(), df_KBr_d2['beta'].max())
plt.grid()
# mostrar
plt.show()
# exportar
plt.savefig('d2-graf18-AbsxBeta_Zr-KBr.svg', format='svg')
plt.close()

# Mo
plt.plot(df_KBr_d2['beta'], df_KBr_d2['abs_Mo'], linewidth=3, color='red')
plt.title('Absortância vs ângulo Mo (KBr)', fontsize=23)
plt.ylabel('Absortância (s/ unid.)', fontsize=18)
plt.xlabel('$\\beta$ ($^{\\circ}$)', fontsize=18)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.subplots_adjust(bottom=0.15)
plt.xlim(df_KBr_d2['beta'].min(), df_KBr_d2['beta'].max())
plt.grid()
# mostrar
plt.show()
# exportar
plt.savefig('d2-graf19-AbsxBeta_Mo-KBr.svg', format='svg')
plt.close()

# Al
plt.plot(df_KBr_d2['beta'], df_KBr_d2['abs_Al'], linewidth=3, color='orange')
plt.title('Absortância vs ângulo Al (KBr)', fontsize=23)
plt.ylabel('Absortância (s/ unid.)', fontsize=18)
plt.xlabel('$\\beta$ ($^{\\circ}$)', fontsize=18)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.subplots_adjust(bottom=0.15)
plt.xlim(df_KBr_d2['beta'].min(), df_KBr_d2['beta'].max())
plt.grid()
# mostrar
plt.show()
# exportar
plt.savefig('d2-graf20-AbsxBeta_Al-KBr.svg', format='svg')
plt.close()

# Absortância x energia 

#  Zr
plt.plot(df_KBr_d2['E'], df_KBr_d2['abs_Zr'], linewidth=3, color='blue')
plt.title('Absortância vs Energia Zr (KBr)', fontsize=23)
plt.ylabel('Absortância (s/ unid.)', fontsize=18)
plt.xlabel('$E$ (keV)', fontsize=18)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.subplots_adjust(bottom=0.15)
plt.xlim(df_KBr_d2['E'].min(), df_KBr_d2['E'].max())
plt.grid()
# mostrar
#plt.show()
# exportar
plt.savefig('d2-graf21-AbsxE_Zr-KBr.svg', format='svg')
plt.close()

# Mo
plt.plot(df_KBr_d2['E'], df_KBr_d2['abs_Mo'], linewidth=3, color='red')
plt.title('Absortância vs Energia Mo (KBr)', fontsize=23)
plt.ylabel('Absortância (s/ unid.)', fontsize=18)
plt.xlabel('$E$ (keV)', fontsize=18)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.subplots_adjust(bottom=0.15)
plt.xlim(df_KBr_d2['E'].min(), df_KBr_d2['E'].max())
plt.grid()
# mostrar
#plt.show()
# exportar
plt.savefig('d2-graf22-AbsxE_Mo-KBr.svg', format='svg')
plt.close()

# Al
plt.plot(df_KBr_d2['E'], df_KBr_d2['abs_Al'], linewidth=3, color='orange')
plt.title('Absortância vs Energia Al (KBr)', fontsize=23)
plt.ylabel('Absortância (s/ unid.)', fontsize=18)
plt.xlabel('$E$ (keV)', fontsize=18)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.subplots_adjust(bottom=0.15)
plt.xlim(df_KBr_d2['E'].min(), df_KBr_d2['E'].max())
plt.grid()
# mostrar
#plt.show()
# exportar
plt.savefig('d2-graf23-AbsxE_Al-KBr.svg', format='svg')
plt.close()


##### 14) Gráficos 24-26: ajustes de espessura #################################

"""
1a tentativa: com interpolação (deprecada)
# manipulação alternativa:
# eu estava fazendo tudo errado.
# acho que agora eu entendi.
# temos de encaixar a parte de decaimento exponencial que vem DEPOIS do pico de absorção
# isso porque mu em função de E não é biunívoca, sequer contínua
# em um único ponto ela assume meio que dois valores, que é o degrau de absorção
# não dá para encaixar nada nessa região
# no entanto é justamente a região que eu estava tentando encaixar

# vamos primeiro selecionar a região de interesse:
print_full(df_NaCl_d2)

# peguemos os valores de índice 17 até 42 (pico), equivalentes a cerca de 18.84 keV até 30 keV
E_selec_Zr_NaCl = df_NaCl_d2['E'][17:43]

# da referência XCOM (valores a interpolar):
E_Zr_raw = [17.9976, 20, 30, 40]
mu_Zr_raw = [94.7, 72.37, 24.85, 11.39]

# interpolação:
f_interp = interpolate.CubicSpline(E_Zr_raw, mu_Zr_raw)
Zr_interpolado = f_interp(E_selec_Zr_NaCl)
plt.scatter(E_Zr_raw, mu_Zr_raw, linewidths=5)
plt.scatter(E_selec_Zr_NaCl, Zr_interpolado, linewidths=1)
plt.ylabel('$\\mu/\\rho$ (cm$^2$/g)', fontsize=15)
plt.xlabel('E (keV)', fontsize=15)
plt.show()
# notar: há uma diferença brutal entre interpolação linear e polinomial
# entre as diferentes técnicas polinomiais, no entanto, não há tanta diferença

# agora vamos proceder ao ajuste
# notar que não temos incerteza para os valores interpolados
# isso é um problema
# como averiguar a incerteza nesse caso?
# a simples propagação de erro apenas propagaria, mas não nos diria o desvio da curva
# interpolada até a curva real
# além disso só essa propagação já seria um pesadelo de calcular
# então por enquanto vou usar a função curve_fit, pressupondo x sem incerteza

# de todo modo eu preciso propagar os erros da absortância
erro_lnA = np.sqrt((6/df_NaCl_d2['sem filtro'][17:43])**2 + (6/df_NaCl_d2['Zr'][17:43])**2) # considerei como erro 6 fótons/s
# e a absortância em si:
lnA = np.log(df_NaCl_d2['abs_Zr'][17:43])

# também preciso transformar de mu/rho para mu, multiplicando os valores interpolados pela densidade do elemento
Zr_interpolado = Zr_interpolado*6.49

# ajuste
def linear_func(x, a, b):
    return a * x + b
popt, pcov = curve_fit(linear_func, Zr_interpolado, lnA, sigma=erro_lnA, absolute_sigma=True)

# resultado:
# 0.00417571(1) cm

# largura do eixo x do plot:
escopo = np.arange(Zr_interpolado.min(), Zr_interpolado.max(), .5)
# plot
plt.plot(
    escopo,
    popt[0]*escopo + popt[1],
    color = 'red',
    linewidth=2.8
)
plt.errorbar(
    Zr_interpolado,
    lnA,
    #xerr= ,
    yerr=erro_lnA,
    fmt = 'o', # formato dos pontos, previne linhas ligando-os
    ecolor = 'black', # cor das barras de erro
    elinewidth = 1.3, # espessura das barras de erro
    capsize = 0, # espessura das marcações nas extremidades das barras de erro
    color = 'black', # cor dos pontos
    markersize = 3.5 # tamanho dos pontos
)
plt.title('Ajuste: espessura do filtro de Zr', fontsize=23)
plt.ylabel('$\\ln(A)$ (s/ unid.)', fontsize=18)
plt.xlabel('$\\mu$ (cm$^{-1}$)', fontsize=18)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.subplots_adjust(bottom=0.13, right=0.98, left=0.13, top=0.92)
# mostrar
plt.show()
# salvar
plt.savefig('d1-graf7-ajuste_KBr.svg', format='svg')

"""

# agora sem interpolação:
mu_Zr = pd.read_csv('mu_Zr.txt')
mu_Zr = mu_Zr['Mu'] * 6.49 * 10 # densidade e potência
# olha o malabarismo que eu tenho que fazer para conseguir inverter a ordem dessa merda:
mu_Zr = mu_Zr.iloc[::-1].values
# enfim
erro_Mu = len(mu_Zr)*[0.0005 * 6.49]
lnA = np.log(df_NaCl_d2['abs_Zr'])
erro_lnA = np.sqrt((6/df_NaCl_d2['sem filtro'])**2 + (6/df_NaCl_d2['Zr'])**2) # considerei como erro 6 fótons/s

# juntando tudo em 1 dataframe:
df_Ajuste_Espessura_Zr_NaCl = pd.DataFrame({
    'X': mu_Zr,
    'Erro_X': erro_Mu,
    'Y': lnA,
    'Erro_Y': erro_lnA
})
df_Ajuste_Espessura_Zr_NaCl = df_Ajuste_Espessura_Zr_NaCl[17:43]

# modelo:
def f(B, x):
    # B eh o vetor de parametros
    # x eh uma array no formato dado na documentacao do pacote
    return B[0]*x + B[1] # no caso, um modelo hiperbólico
# criando o objeto de classe modelo
linear = odr.Model(f)
# criando o objeto de classe dados
dados4 = odr.RealData(df_Ajuste_Espessura_Zr_NaCl['X'], df_Ajuste_Espessura_Zr_NaCl['Y'], df_Ajuste_Espessura_Zr_NaCl['Erro_X'], df_Ajuste_Espessura_Zr_NaCl['Erro_Y'])
# criando o objeto de classe odr 
# (aqui precisa ter estimativa de parametros iniciais)
obj_odr = odr.ODR(dados4, linear, beta0=[1.14,2.23])
# criando o objeto output
myoutput4 = obj_odr.run()

myoutput4.pprint()
print(myoutput4.cov_beta) # matriz de covariancia (diag principal = variancia dos parametros)
print(myoutput4.sd_beta) # desvio padrao (erro) dos parametros escalado pela variancia dos residuos
print([np.sqrt(myoutput4.cov_beta[0,0]), np.sqrt(myoutput4.cov_beta[1,1])]) # desvio padrao sem escalar nada

escopo = np.arange(df_Ajuste_Espessura_Zr_NaCl['X'].min()*0.95, df_Ajuste_Espessura_Zr_NaCl['X'].max()*1.05)
# plot
plt.plot(
    escopo,
    myoutput4.beta[0]*escopo + myoutput4.beta[1],
    color = 'red',
    linewidth=2.8
)
plt.errorbar(
    df_Ajuste_Espessura_Zr_NaCl['X'],
    df_Ajuste_Espessura_Zr_NaCl['Y'],
    xerr=df_Ajuste_Espessura_Zr_NaCl['Erro_X'],
    yerr=df_Ajuste_Espessura_Zr_NaCl['Erro_Y'],
    fmt = 'o', # formato dos pontos, previne linhas ligando-os
    ecolor = 'black', # cor das barras de erro
    elinewidth = 1.3, # espessura das barras de erro
    capsize = 0, # espessura das marcações nas extremidades das barras de erro
    color = 'black', # cor dos pontos
    markersize = 3.5 # tamanho dos pontos
)
plt.title('Ajuste: espessura do filtro de Zr', fontsize=23)
plt.ylabel('$\\ln(A)$ (s/ unid.)', fontsize=18)
plt.xlabel('$\\mu$ (cm$^{-1}$)', fontsize=18)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.subplots_adjust(bottom=0.13, right=0.98, left=0.13, top=0.92)
# mostrar
plt.show()
# salvar
plt.savefig('d2-graf24-ajuste_espessura_Zr_NaCl.svg', format='svg')
plt.close()

# calculando a espessura:
myoutput4.beta[0]
# 0.004180115956886091 cm
# erro:
np.sqrt(myoutput4.cov_beta[0,0])
# 6.76444769633473e-05
# final:
# 0.0042(7) cm


# Mo
mu_Mo = pd.read_csv('mu_Mo.txt')
mu_Mo = mu_Mo['Mu'] * 10.223 * 10 # densidade e potência de 10 dos dados
# olha o malabarismo que eu tenho que fazer para conseguir inverter a ordem dessa merda:
mu_Mo = mu_Mo.iloc[::-1].values
# enfim
erro_Mu = len(mu_Mo)*[0.0005 * 6.49]
lnA = np.log(df_NaCl_d2['abs_Mo'])
erro_lnA = np.sqrt((3/df_NaCl_d2['sem filtro'])**2 + (3/df_NaCl_d2['Mo'])**2) # mudei! considerei como erro 3 fótons/s

# juntando tudo em 1 dataframe:
df_Ajuste_Espessura_Mo_NaCl = pd.DataFrame({
    'X': mu_Mo,
    'Erro_X': erro_Mu,
    'Y': lnA,
    'Erro_Y': erro_lnA
})
df_Ajuste_Espessura_Mo_NaCl = df_Ajuste_Espessura_Mo_NaCl[13:31]

# modelo:
def f(B, x):
    # B eh o vetor de parametros
    # x eh uma array no formato dado na documentacao do pacote
    return B[0]*x + B[1] # no caso, um modelo hiperbólico
# criando o objeto de classe modelo
linear = odr.Model(f)
# criando o objeto de classe dados
dados5 = odr.RealData(df_Ajuste_Espessura_Mo_NaCl['X'], df_Ajuste_Espessura_Mo_NaCl['Y'], df_Ajuste_Espessura_Mo_NaCl['Erro_X'], df_Ajuste_Espessura_Mo_NaCl['Erro_Y'])
# criando o objeto de classe odr 
# (aqui precisa ter estimativa de parametros iniciais)
obj_odr = odr.ODR(dados5, linear, beta0=[1.14,2.23])
# criando o objeto output
myoutput5 = obj_odr.run()

myoutput5.pprint()
print([np.sqrt(myoutput5.cov_beta[0,0]), np.sqrt(myoutput5.cov_beta[1,1])]) # desvio padrao sem escalar nada

escopo = np.arange(df_Ajuste_Espessura_Mo_NaCl['X'].min()*0.95, df_Ajuste_Espessura_Mo_NaCl['X'].max()*1.05)
# plot
plt.plot(
    escopo,
    myoutput5.beta[0]*escopo + myoutput5.beta[1],
    color = 'red',
    linewidth=2.8
)
plt.errorbar(
    df_Ajuste_Espessura_Mo_NaCl['X'],
    df_Ajuste_Espessura_Mo_NaCl['Y'],
    xerr=df_Ajuste_Espessura_Mo_NaCl['Erro_X'],
    yerr=df_Ajuste_Espessura_Mo_NaCl['Erro_Y'],
    fmt = 'o', # formato dos pontos, previne linhas ligando-os
    ecolor = 'black', # cor das barras de erro
    elinewidth = 1.3, # espessura das barras de erro
    capsize = 0, # espessura das marcações nas extremidades das barras de erro
    color = 'black', # cor dos pontos
    markersize = 3.5 # tamanho dos pontos
)
plt.title('Ajuste: espessura do filtro de Mo', fontsize=23)
plt.ylabel('$\\ln(A)$ (s/ unid.)', fontsize=18)
plt.xlabel('$\\mu$ (cm$^{-1}$)', fontsize=18)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.subplots_adjust(bottom=0.13, right=0.98, left=0.13, top=0.92)
# mostrar
plt.show()
# salvar
plt.savefig('d2-graf25-ajuste_espessura_Mo_NaCl.svg', format='svg')
plt.close()

# calculando a espessura:
myoutput5.beta[0]
# 0.005088366880380227 cm
# erro:
np.sqrt(myoutput5.cov_beta[0,0])
# 0.00023766072082715656
# final:
# 0.005(2) cm

# Al
mu_Al = pd.read_csv('mu_Al.txt')
mu_Al = mu_Al['Mu'] * 10.223 * 10 # densidade e potência de 10 dos dados
# olha o malabarismo que eu tenho que fazer para conseguir inverter a ordem dessa merda:
mu_Al = mu_Al.iloc[::-1].values
# enfim
erro_Mu = len(mu_Al)*[0.0005 * 6.49]
lnA = np.log(df_NaCl_d2['abs_Al'])
erro_lnA = np.sqrt((1/df_NaCl_d2['sem filtro'])**2 + (1/df_NaCl_d2['Al'])**2) # mudei! considerei como erro 1 fótons/s

# juntando tudo em 1 dataframe:
df_Ajuste_Espessura_Al_NaCl = pd.DataFrame({
    'X': mu_Al,
    'Erro_X': erro_Mu,
    'Y': lnA,
    'Erro_Y': erro_lnA
})
df_Ajuste_Espessura_Al_NaCl = df_Ajuste_Espessura_Al_NaCl[3:10]

# modelo:
def f(B, x):
    # B eh o vetor de parametros
    # x eh uma array no formato dado na documentacao do pacote
    return B[0]*x + B[1] # no caso, um modelo hiperbólico
# criando o objeto de classe modelo
linear = odr.Model(f)
# criando o objeto de classe dados
dados6 = odr.RealData(df_Ajuste_Espessura_Al_NaCl['X'], df_Ajuste_Espessura_Al_NaCl['Y'], df_Ajuste_Espessura_Al_NaCl['Erro_X'], df_Ajuste_Espessura_Al_NaCl['Erro_Y'])
# criando o objeto de classe odr 
# (aqui precisa ter estimativa de parametros iniciais)
obj_odr = odr.ODR(dados6, linear, beta0=[0.005,-10])
# criando o objeto output
myoutput6 = obj_odr.run()

myoutput6.pprint()
print([np.sqrt(myoutput6.cov_beta[0,0]), np.sqrt(myoutput6.cov_beta[1,1])]) # desvio padrao sem escalar nada

escopo = np.arange(df_Ajuste_Espessura_Al_NaCl['X'].min()*0.95, df_Ajuste_Espessura_Al_NaCl['X'].max()*1.05)
# plot
plt.plot(
    escopo,
    myoutput6.beta[0]*escopo + myoutput6.beta[1],
    color = 'red',
    linewidth=2.8
)
plt.errorbar(
    df_Ajuste_Espessura_Al_NaCl['X'],
    df_Ajuste_Espessura_Al_NaCl['Y'],
    xerr=df_Ajuste_Espessura_Al_NaCl['Erro_X'],
    yerr=df_Ajuste_Espessura_Al_NaCl['Erro_Y'],
    fmt = 'o', # formato dos pontos, previne linhas ligando-os
    ecolor = 'black', # cor das barras de erro
    elinewidth = 1.3, # espessura das barras de erro
    capsize = 0, # espessura das marcações nas extremidades das barras de erro
    color = 'black', # cor dos pontos
    markersize = 3.5 # tamanho dos pontos
)
plt.title('Ajuste: espessura do filtro de Al', fontsize=23)
plt.ylabel('$\\ln(A)$ (s/ unid.)', fontsize=18)
plt.xlabel('$\\mu$ (cm$^{-1}$)', fontsize=18)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.subplots_adjust(bottom=0.13, right=0.98, left=0.13, top=0.92)
# mostrar
plt.show()
# salvar
plt.savefig('d2-graf26-ajuste_espessura_Al_NaCl.svg', format='svg')
plt.close()

# calculando a espessura:
myoutput6.beta[0]
# 0.008277336750646297 cm
# erro:
np.sqrt(myoutput6.cov_beta[0,0])
# 0.0004973055855218576
# final:
# 0.008(4) cm


##### 15) Gráficos 27-30: Gaussianas ###########################################

# vamos usar os dados do dia 2
# e selecionar a região ao redor dos picos
# erro de y é dado pela distribuição de poisson sqrt(y)/deltat
# erro de x (theta) é 0.01

# identificando picos do NaCl
print_full(df_NaCl_d2)
# pico 1: 35 até 42 [35:43]
# pico 2: 43 até 51 [43:52]

# picos do KBr
print_full(df_KBr_d2)
# pico 1: 25 até 33 [25:34]
# pico 2: 33 até 40 [33:41]

# NaCl
df_Gaussiana1_NaCl = pd.DataFrame({
    'X': df_NaCl_d2['beta'],
    'Erro_X': 0.01,
    'Y': df_NaCl_d2['sem filtro'],
    'Erro_Y': np.sqrt(df_NaCl_d2['sem filtro'])/10
}).iloc[37:43,:] # primeiros pontos ficaram ruins, excluindo dois

# modelo:
def g(B, x):
    # B eh o vetor de parametros
    # x eh uma array no formato dado na documentacao do pacote
    return B[0] * np.exp( - (x-B[1])**2 / (2*B[2]**2) ) + B[3] # no caso, um modelo gaussiano
# criando o objeto de classe modelo
gauss = odr.Model(g)
# criando o objeto de classe dados
dados7 = odr.RealData(df_Gaussiana1_NaCl['X'], df_Gaussiana1_NaCl['Y'], df_Gaussiana1_NaCl['Erro_X'], df_Gaussiana1_NaCl['Erro_Y'])
# criando o objeto de classe odr 
# (aqui precisa ter estimativa de parametros iniciais)
obj_odr = odr.ODR(dados7, gauss, beta0=[1000,6.5,0.3, 600])
# criando o objeto output
myoutput7 = obj_odr.run()

myoutput7.pprint()
print([np.sqrt(myoutput7.cov_beta[0,0]), np.sqrt(myoutput7.cov_beta[1,1])]) # desvio padrao sem escalar nada

escopo = np.arange(df_Gaussiana1_NaCl['X'].min(), df_Gaussiana1_NaCl['X'].max()*1.005,0.01)
# plot
plt.plot(
    escopo,
    g(myoutput7.beta, escopo),
    color = 'red',
    linewidth=2.8
)
plt.errorbar(
    df_Gaussiana1_NaCl['X'],
    df_Gaussiana1_NaCl['Y'],
    xerr=df_Gaussiana1_NaCl['Erro_X'],
    yerr=df_Gaussiana1_NaCl['Erro_Y'],
    fmt = 'o', # formato dos pontos, previne linhas ligando-os
    ecolor = 'black', # cor das barras de erro
    elinewidth = 1.3, # espessura das barras de erro
    capsize = 0, # espessura das marcações nas extremidades das barras de erro
    color = 'black', # cor dos pontos
    markersize = 3.5 # tamanho dos pontos
)
plt.title('Ajuste: pico $K\\beta$ NaCl sem filtro', fontsize=23)
plt.ylabel('$I$ (fótons/s)', fontsize=18)
plt.xlabel('$\\beta$ ($^{\\circ}$)', fontsize=18)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.subplots_adjust(bottom=0.13, right=0.98, left=0.13, top=0.92)
# mostrar
plt.show()
# salvar
plt.savefig('d2-graf26-ajuste_espessura_Al_NaCl.svg', format='svg')
plt.close()

# calculando o valor esperado do ângulo:
myoutput7.beta[1]
# 6.4462503295093905 °
# erro:
np.sqrt(myoutput7.cov_beta[1,1])
# 0.004433088496537881 °
# desvio padrão da gaussiana:
myoutput7.beta[2]
# -0.17345862669026632 °

# valor esperado da energia:
# em keV
h = 6.62607015 * 10**-34
c = 299792458
d_NaCl = 0.282 * 10**-9
h*c / (2*d_NaCl*np.sin(np.deg2rad(myoutput7.beta[1]))*1.602176634*10**-19*1000)
# 19.5802986812123
# incerteza do valor esperado:

# sigma da energia:
h*c / (2*d_NaCl*np.sin(np.deg2rad(np.abs(myoutput7.beta[2])))*1.602176634*10**-19*1000)








# vamos tentar outra abordagem
# fazer o ajuste direto no gráfico I x E

# identificando picos do NaCl
print_full(df_NaCl_d2)
# pico 1: 37 até 42 [37:43]
# pico 2: 43 até 51 [43:52]

# picos do KBr
print_full(df_KBr_d2)
# pico 1: 25 até 33 [25:34]
# pico 2: 33 até 40 [33:41]


# NaCl
erro_E = np.abs(0.01*h*c*np.cos(np.deg2rad(df_NaCl_d2['beta'])) / (2*d_NaCl*np.sin(np.deg2rad(df_NaCl_d2['beta']))**2))
df_Gaussiana1_NaCl = pd.DataFrame({
    'X': df_NaCl_d2['E'],
    'Erro_X': erro_E,
    'Y': df_NaCl_d2['sem filtro'],
    'Erro_Y': np.sqrt(df_NaCl_d2['sem filtro'])/10
}).iloc[37:43,:] # primeiros pontos ficaram ruins, excluindo dois

# modelo:
def g(B, x):
    # B eh o vetor de parametros
    # x eh uma array no formato dado na documentacao do pacote
    return B[0] * np.exp( - (x-B[1])**2 / (2*B[2]**2) ) + B[3] # no caso, um modelo gaussiano
# criando o objeto de classe modelo
gauss = odr.Model(g)
# criando o objeto de classe dados
dados7 = odr.RealData(df_Gaussiana1_NaCl['X'], df_Gaussiana1_NaCl['Y'], df_Gaussiana1_NaCl['Erro_X'], df_Gaussiana1_NaCl['Erro_Y'])
# criando o objeto de classe odr 
# (aqui precisa ter estimativa de parametros iniciais)
obj_odr = odr.ODR(dados7, gauss, beta0=[0,19.6,.5, 300])
# criando o objeto output
myoutput7 = obj_odr.run()

myoutput7.pprint()
print([np.sqrt(myoutput7.cov_beta[0,0]), np.sqrt(myoutput7.cov_beta[1,1])]) # desvio padrao sem escalar nada

escopo = np.arange(df_Gaussiana1_NaCl['X'].min(), df_Gaussiana1_NaCl['X'].max()*1.005,0.01)
# plot
plt.plot(
    escopo,
    g(myoutput7.beta, escopo),
    color = 'red',
    linewidth=2.8
)
plt.errorbar(
    df_Gaussiana1_NaCl['X'],
    df_Gaussiana1_NaCl['Y'],
    xerr=df_Gaussiana1_NaCl['Erro_X'],
    yerr=df_Gaussiana1_NaCl['Erro_Y'],
    fmt = 'o', # formato dos pontos, previne linhas ligando-os
    ecolor = 'black', # cor das barras de erro
    elinewidth = 1.3, # espessura das barras de erro
    capsize = 0, # espessura das marcações nas extremidades das barras de erro
    color = 'black', # cor dos pontos
    markersize = 3.5 # tamanho dos pontos
)
plt.title('Ajuste: pico $K_\\beta$ NaCl sem filtro', fontsize=23)
plt.ylabel('$I$ (fótons/s)', fontsize=18)
plt.xlabel('$\\beta$ ($^{\\circ}$)', fontsize=18)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.subplots_adjust(bottom=0.13, right=0.98, left=0.13, top=0.92)
# mostrar
plt.show()
# salvar
plt.savefig('d2-graf27-gaussiana_K_beta_NaCl.svg', format='svg')
plt.close()

# calculando o valor esperado da energia:
myoutput7.beta[1]
# 19.6129931664527 keV
# erro:
np.sqrt(myoutput7.cov_beta[1,1])
# 0.0014171729115933125 keV
# desvio padrão da gaussiana:
myoutput7.beta[2]
# 0.5175387538677563 keV
# erro
np.sqrt(myoutput7.cov_beta[2,2])
# 0.0103540601196013
# valor final:
# 19.6(5) keV


# NaCl K alpha
erro_E = np.abs(0.01*h*c*np.cos(np.deg2rad(df_NaCl_d2['beta'])) / (2*d_NaCl*np.sin(np.deg2rad(df_NaCl_d2['beta']))**2))
df_Gaussiana1_NaCl = pd.DataFrame({
    'X': df_NaCl_d2['E'],
    'Erro_X': erro_E,
    'Y': df_NaCl_d2['sem filtro'],
    'Erro_Y': np.sqrt(df_NaCl_d2['sem filtro'])/10
}).iloc[43:51,:] # tirando 2 últimos e primeiro

# modelo:
def g(B, x):
    # B eh o vetor de parametros
    # x eh uma array no formato dado na documentacao do pacote
    return B[0] * np.exp( - (x-B[1])**2 / (2*B[2]**2) ) + B[3] # no caso, um modelo gaussiano
# criando o objeto de classe modelo
gauss = odr.Model(g)
# criando o objeto de classe dados
dados7 = odr.RealData(df_Gaussiana1_NaCl['X'], df_Gaussiana1_NaCl['Y'], df_Gaussiana1_NaCl['Erro_X'], df_Gaussiana1_NaCl['Erro_Y'])
# criando o objeto de classe odr 
# (aqui precisa ter estimativa de parametros iniciais)
obj_odr = odr.ODR(dados7, gauss, beta0=[0,17.4,.5, 300])
# criando o objeto output
myoutput7 = obj_odr.run()

myoutput7.pprint()
print([np.sqrt(myoutput7.cov_beta[0,0]), np.sqrt(myoutput7.cov_beta[1,1])]) # desvio padrao sem escalar nada

escopo = np.arange(df_Gaussiana1_NaCl['X'].min(), df_Gaussiana1_NaCl['X'].max()*1.005,0.01)
# plot
plt.plot(
    escopo,
    g(myoutput7.beta, escopo),
    color = 'red',
    linewidth=2.8
)
plt.errorbar(
    df_Gaussiana1_NaCl['X'],
    df_Gaussiana1_NaCl['Y'],
    xerr=df_Gaussiana1_NaCl['Erro_X'],
    yerr=df_Gaussiana1_NaCl['Erro_Y'],
    fmt = 'o', # formato dos pontos, previne linhas ligando-os
    ecolor = 'black', # cor das barras de erro
    elinewidth = 1.3, # espessura das barras de erro
    capsize = 0, # espessura das marcações nas extremidades das barras de erro
    color = 'black', # cor dos pontos
    markersize = 3.5 # tamanho dos pontos
)
plt.title('Ajuste: pico $K_\\alpha$ NaCl sem filtro', fontsize=23)
plt.ylabel('$I$ (fótons/s)', fontsize=18)
plt.xlabel('$\\beta$ ($^{\\circ}$)', fontsize=18)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.subplots_adjust(bottom=0.13, right=0.98, left=0.13, top=0.92)
# mostrar
plt.show()
# salvar
plt.savefig('d2-graf28-gaussiana_K_alpha_NaCl.svg', format='svg')
plt.close()

# calculando o valor esperado da energia:
myoutput7.beta[1]
# 17.42778802618393 keV
# erro:
np.sqrt(myoutput7.cov_beta[1,1])
# 0.0005742502709466721 keV
# desvio padrão da gaussiana:
myoutput7.beta[2]
# 0.3107318921920885 keV
# erro
np.sqrt(myoutput7.cov_beta[2,2])
# 0.0006824113679541027
# valor final:
# 17.4(3) keV


# KBr K beta
erro_E = np.abs(0.01*h*c*np.cos(np.deg2rad(df_KBr_d2['beta'])) / (2*d_KBr*np.sin(np.deg2rad(df_KBr_d2['beta']))**2))
df_Gaussiana1_KBr = pd.DataFrame({
    'X': df_KBr_d2['E'],
    'Erro_X': erro_E,
    'Y': df_KBr_d2['sem filtro'],
    'Erro_Y': np.sqrt(df_KBr_d2['sem filtro'])/10
}).iloc[28:34,:] # tirando 2 últimos e primeiro

# modelo:
def g(B, x):
    # B eh o vetor de parametros
    # x eh uma array no formato dado na documentacao do pacote
    return B[0] * np.exp( - (x-B[1])**2 / (2*B[2]**2) ) + B[3] # no caso, um modelo gaussiano
# criando o objeto de classe modelo
gauss = odr.Model(g)
# criando o objeto de classe dados
dados7 = odr.RealData(df_Gaussiana1_KBr['X'], df_Gaussiana1_KBr['Y'], df_Gaussiana1_KBr['Erro_X'], df_Gaussiana1_KBr['Erro_Y'])
# criando o objeto de classe odr 
# (aqui precisa ter estimativa de parametros iniciais)
obj_odr = odr.ODR(dados7, gauss, beta0=[0,19.6,.5, 150])
# criando o objeto output
myoutput7 = obj_odr.run()

myoutput7.pprint()
print([np.sqrt(myoutput7.cov_beta[0,0]), np.sqrt(myoutput7.cov_beta[1,1])]) # desvio padrao sem escalar nada

escopo = np.arange(df_Gaussiana1_KBr['X'].min(), df_Gaussiana1_KBr['X'].max()*1.005,0.01)
# plot
plt.plot(
    escopo,
    g(myoutput7.beta, escopo),
    color = 'red',
    linewidth=2.8
)
plt.errorbar(
    df_Gaussiana1_KBr['X'],
    df_Gaussiana1_KBr['Y'],
    xerr=df_Gaussiana1_KBr['Erro_X'],
    yerr=df_Gaussiana1_KBr['Erro_Y'],
    fmt = 'o', # formato dos pontos, previne linhas ligando-os
    ecolor = 'black', # cor das barras de erro
    elinewidth = 1.3, # espessura das barras de erro
    capsize = 0, # espessura das marcações nas extremidades das barras de erro
    color = 'black', # cor dos pontos
    markersize = 3.5 # tamanho dos pontos
)
plt.title('Ajuste: pico $K_\\beta$ KBr sem filtro', fontsize=23)
plt.ylabel('$I$ (fótons/s)', fontsize=18)
plt.xlabel('$\\beta$ ($^{\\circ}$)', fontsize=18)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.subplots_adjust(bottom=0.13, right=0.98, left=0.13, top=0.92)
# mostrar
plt.show()
# salvar
plt.savefig('d2-graf29-gaussiana_K_beta_KBr.svg', format='svg')
plt.close()

# calculando o valor esperado da energia:
myoutput7.beta[1]
# 19.670595778475036 keV
# erro:
np.sqrt(myoutput7.cov_beta[1,1])
# 0.006463276718447975 keV
# desvio padrão da gaussiana:
myoutput7.beta[2]
# 0.6737536395837178 keV
# erro
np.sqrt(myoutput7.cov_beta[2,2])
# 0.03826083558279809
# valor final:
# 19.7(7) keV
# teste T:
(19.6083 - myoutput7.beta[1]) / myoutput7.beta[2]
# 0.01


# KBr K alpha
erro_E = np.abs(0.01*h*c*np.cos(np.deg2rad(df_KBr_d2['beta'])) / (2*d_KBr*np.sin(np.deg2rad(df_KBr_d2['beta']))**2))
df_Gaussiana1_KBr = pd.DataFrame({
    'X': df_KBr_d2['E'],
    'Erro_X': erro_E,
    'Y': df_KBr_d2['sem filtro'],
    'Erro_Y': np.sqrt(df_KBr_d2['sem filtro'])/10
}).iloc[35:40,:] # tirando 2 últimos e primeiro

# modelo:
def g(B, x):
    # B eh o vetor de parametros
    # x eh uma array no formato dado na documentacao do pacote
    return B[0] * np.exp( - (x-B[1])**2 / (2*B[2]**2) ) + B[3] # no caso, um modelo gaussiano
# criando o objeto de classe modelo
gauss = odr.Model(g)
# criando o objeto de classe dados
dados7 = odr.RealData(df_Gaussiana1_KBr['X'], df_Gaussiana1_KBr['Y'], df_Gaussiana1_KBr['Erro_X'], df_Gaussiana1_KBr['Erro_Y'])
# criando o objeto de classe odr 
# (aqui precisa ter estimativa de parametros iniciais)
obj_odr = odr.ODR(dados7, gauss, beta0=[0,17.4,.5, 150])
# criando o objeto output
myoutput7 = obj_odr.run()

myoutput7.pprint()
print([np.sqrt(myoutput7.cov_beta[0,0]), np.sqrt(myoutput7.cov_beta[1,1])]) # desvio padrao sem escalar nada

escopo = np.arange(df_Gaussiana1_KBr['X'].min(), df_Gaussiana1_KBr['X'].max()*1.005,0.01)
# plot
plt.plot(
    escopo,
    g(myoutput7.beta, escopo),
    color = 'red',
    linewidth=2.8
)
plt.errorbar(
    df_Gaussiana1_KBr['X'],
    df_Gaussiana1_KBr['Y'],
    xerr=df_Gaussiana1_KBr['Erro_X'],
    yerr=df_Gaussiana1_KBr['Erro_Y'],
    fmt = 'o', # formato dos pontos, previne linhas ligando-os
    ecolor = 'black', # cor das barras de erro
    elinewidth = 1.3, # espessura das barras de erro
    capsize = 0, # espessura das marcações nas extremidades das barras de erro
    color = 'black', # cor dos pontos
    markersize = 3.5 # tamanho dos pontos
)
plt.title('Ajuste: pico $K_\\alpha$ KBr sem filtro', fontsize=23)
plt.ylabel('$I$ (fótons/s)', fontsize=18)
plt.xlabel('$\\beta$ ($^{\\circ}$)', fontsize=18)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.subplots_adjust(bottom=0.13, right=0.98, left=0.13, top=0.92)
# mostrar
plt.show()
# salvar
plt.savefig('d2-graf30-gaussiana_K_alpha_KBr.svg', format='svg')
plt.close()

# calculando o valor esperado da energia:
myoutput7.beta[1]
# 17.486309488172797 keV
# erro:
np.sqrt(myoutput7.cov_beta[1,1])
# 0.002192490622349063 keV
# desvio padrão da gaussiana:
myoutput7.beta[2]
# 0.45660838740833926 keV
# erro
np.sqrt(myoutput7.cov_beta[2,2])
# 0.030226850947780062
# valor final:
# 17.5(5) keV
# teste T:
(17.47934 - myoutput7.beta[1]) / myoutput7.beta[2]
# 0.01










# pico 1: 25 até 33 [25:34]
# pico 2: 33 até 40 [33:41]