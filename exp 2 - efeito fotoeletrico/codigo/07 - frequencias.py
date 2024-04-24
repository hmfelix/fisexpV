
# SETUP

import pandas as pd
import numpy as np
import scipy.odr as odr
from matplotlib import pyplot as plt
from scipy.special import erf
cores = ('Vd', 'Az', 'Am', 'Vm', 'Viol')



# IMPORTACAO DOS DADOS

# notar: dados sao re-escalados para otimizar o ajuste
# frequencia eh dividida por 10^14
# intensidade eh dividida por 1000
for cor in cores:
    # DAORA MÉTODO DE CRIAR VARIÁVEIS!!! NOSSA GENIAL
    globals()['df_{}'.format(cor)] = pd.read_csv('analise de frequencias/dados brutos/formato anglo/espectro_LED_{}.dat'.format(cor))
    globals()['df_{}'.format(cor)]['Frequencia (Hz)'] = globals()['df_{}'.format(cor)]['Frequencia (Hz)']/10**14
    globals()['df_{}'.format(cor)]['Intensidade (contagem)'] = globals()['df_{}'.format(cor)]['Intensidade (contagem)']/1000



# FUNCOES DE AJUSTE

def gaussiana_assimetrica(B, x):
    # B[0] eh a amplitude
    # B[1] eh o valor esperado (que temos interesse)
    # B[2] eh o desvio padrão (que tb temos interesse)
    # B[3] eh o parametro de assimetria (nao temos interesse)
    # B[4] eh alguma constante de reajuste de altura (pode ser de interesse ou nao)
    amp = B[0]
    spread = np.exp( -(x-B[1])**2 / (2*B[2]**2))
    skew = 1 + erf( (B[3] * (x-B[1])) / (B[2]*np.sqrt(2)) )
    return amp * spread * skew + B[4]

def ajustar_gaussiana_assimetrica(dados, chutes):
    dados['erro_f'] = dados['Frequencia (Hz)'].iloc[0] - dados['Frequencia (Hz)'].iloc[1] # erro na frequencia
    dados['erro_i'] = dados['Intensidade (contagem)']**0.5 # erro na intensidade
    curva = odr.Model(gaussiana_assimetrica)
    dados_odr = odr.RealData(
        dados['Frequencia (Hz)'], 
        dados['Intensidade (contagem)'], 
        dados['erro_f'], 
        dados['erro_i']
    ) # cria o objeto de classe dados
    obj_odr = odr.ODR(dados_odr, curva, beta0=chutes) # cria o objeto de classe odr 
    g_output = obj_odr.run() # cria o objeto output
    return g_output



# FUNCOES AUXILIARES PARA AJUSTE E PLOT:

def chutar(cor, sigma=0.25, skew=1, intercepto=0.01):
    chutes = [globals()['df_{}'.format(cor)]['Intensidade (contagem)'].max()]
    chutes.append(globals()['df_{}'.format(cor)]['Frequencia (Hz)'][np.where(globals()['df_{}'.format(cor)]['Intensidade (contagem)'] == globals()['df_{}'.format(cor)]['Intensidade (contagem)'].max())[0].tolist()[0]])
    chutes.extend([sigma, skew, intercepto])
    return chutes

def filtrar(dados, baixo, cima):
    return dados[dados['Frequencia (Hz)'] > baixo][dados['Frequencia (Hz)'] < cima]

def atribuir_cor(cor):
    if cor == 'Am':
        resultado = 'gold'  
    elif cor == 'Az':
        resultado = 'royalblue'
    elif cor == 'Vd':
        resultado = 'seagreen'
    elif cor == 'Viol':
        resultado = 'darkviolet'
    elif cor == 'Vm':
        resultado = 'red'
    return resultado

def plotar_e_tabelar(cor, baixo, cima, anotacao, modo='m', chutes=chutar(cor)):
    # modos: 'm' para mostrar, 's' para salvar
    dados = filtrar(globals()['df_{}'.format(cor)], baixo, cima)
    ajuste = ajustar_gaussiana_assimetrica(dados, chutar(cor))
    parametros_de_interesse = pd.DataFrame({'Frequencia (10^14 Hz)': ajuste.beta[1], 'Sigma (10^14 Hz)': abs(ajuste.beta[2])}, index=[0])
    parametros_de_interesse.to_csv('analise de frequencias/parametros estimados/{}.csv'.format(cor), index=False)
    x = dados['Frequencia (Hz)']
    plt.grid(zorder=1)
    plt.errorbar(
        x = dados['Frequencia (Hz)'],
        y = dados['Intensidade (contagem)'],
        xerr = dados['erro_f'],
        yerr = dados['erro_i'],
        fmt = 'o', # formato dos pontos, previne linhas ligando-os
        ecolor = 'black', # cor das barras de erro
        elinewidth = 0.2, # espessura das barras de erro
        capsize = 0, # espessura das marcações nas extremidades das barras de erro
        color = 'black', # cor dos pontos
        markersize = 5, # tamanho dos pontos
        zorder = 2 # ordena que seja plotado primeiro!
    )
    plt.plot(
        x,
        gaussiana_assimetrica(ajuste.beta, x),
        color = atribuir_cor(cor),
        linewidth=6,
        zorder = 3 # ordena que seja plotado segundo!
    )
    plt.annotate(
        anotacao,
        xy=(0.002, .985),
        xycoords='axes fraction', # torna coordenadas xy normalizadas
        verticalalignment='top',
        fontsize=30,
        bbox=dict(boxstyle='square,pad=0.01', facecolor='white', alpha=0.85, edgecolor='none') # caixa de texto
    )
    #plt.title('A', fontsize=30)
    plt.ylabel('$N$ [mil]', fontsize=28)
    plt.xlabel('$f$ [$\\times 10^{14}$ Hz]', fontsize=28)
    plt.xticks(fontsize=25)
    plt.xlim(baixo, cima)
    plt.yticks(fontsize=25)
    plt.tight_layout(pad=0.1)
    if modo == 'm':
        plt.show()
    elif modo == 's':
        plt.savefig('analise de frequencias/graficos/Assimetrica_' + cor + '.svg', format='svg')
        plt.close()



# PLOTS

plotar_e_tabelar('Vm', 4.5, 5.5, anotacao='(a)', modo='s')
plotar_e_tabelar('Am', 4.8, 5.4, anotacao='(b)',  modo='s')
plotar_e_tabelar('Vd', 5, 6.3, anotacao='(c)', modo='s')
plotar_e_tabelar('Az', 5.9, 6.8, anotacao='(d)', modo='s')
plotar_e_tabelar('Viol', 6.5, 8, anotacao='(e)', modo='s')



# TABELA FINAL COM TODOS OS VALORES
df_base = pd.read_csv('analise de frequencias/parametros estimados/Vd.csv')
df_base.insert(0, 'Cor', 'Vd')
for cor in cores[1:]:
    df = pd.read_csv('analise de frequencias/parametros estimados/{}.csv'.format(cor))
    df.insert(0, 'Cor', cor)
    df_base = pd.concat([df_base, df])
df_base.to_csv('analise de frequencias/frequencias estimadas (consolidado).csv', index=False)

# ok