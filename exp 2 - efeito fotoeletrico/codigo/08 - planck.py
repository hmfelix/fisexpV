
# SETUP

import os
import pandas as pd
import numpy as np
import scipy.odr as odr
from matplotlib import pyplot as plt
cores = ('Verde', 'Azul', 'Amarelo', 'Vermelho', 'Violeta')
e = -1.6021766208 # (sem potencia de 10)


# TRATAMENTO INICIAL
# o objetivo aqui eh consolidar todos os v0 por cor obtidos de cada metodo, com respectivos erros

# metodo 1
df_M1 = pd.read_csv('metodos v0/metodo 1/cores.csv').iloc[:,:3]
df_M1 = df_M1.rename(columns={'V0 M1 sem ruido':'V0 M1', 'Desvio padrao sem ruido':'Erro V0 M1'})

# metodo 2
df_M2 = pd.read_csv('metodos v0/metodo 2/intensidadesDani.csv') # ARQUIVO PROVISORIO
v0_m2 = []
dp_m2 = []
for i in range(5):
    base = (i+1)
    fim = base*5
    inicio = fim - 5
    temp_df = df_M2.iloc[inicio:fim]
    media = temp_df['V0 M2'].mean()
    desv_pad = temp_df['V0 M2'].std()
    v0_m2.append(media)
    dp_m2.append(desv_pad)
df_M2 = pd.DataFrame({'Cor': cores, 'V0 M2': v0_m2, 'Erro V0 M2': dp_m2})

# metodo 3
df_M3 = pd.read_csv('metodos v0/metodo 3/cores.csv').iloc[:,:3]
df_M3 = df_M3.rename(columns={'Valores':'V0 M3', 'LED': 'Cor'})
df_M3 = pd.concat([df_M3, pd.DataFrame({'Erro V0 M3': [0.025]*5})], axis=1)

# frequencias
df_freq = pd.read_csv('analise de frequencias/frequencias estimadas (consolidado).csv')
df_freq['Cor'] = ['Verde', 'Azul', 'Amarelo', 'Vermelho', 'Violeta']

# consolidando
df = pd.merge(df_freq, df_M1, on='Cor')
df = pd.merge(df, df_M2, on='Cor')
df = pd.merge(df, df_M3, on='Cor')

# salvando
df.to_csv('planck/dados_para_ajuste.csv', index=False)



# FUNCOES

# função de ajuste
def f(B, x):
    return B[0]*x + B[1]

def ajustar_reta(df, metodo):
    # definindo dados
    y = df.iloc[:,metodo*2 + 1]
    erro_y = df.iloc[:,metodo*2 + 2]
    dados = pd.concat([df['Frequencia (10^14 Hz)'], df['Sigma (10^14 Hz)'], y, erro_y], axis=1)
    # ajuste
    linear = odr.Model(f)
    dados_ajuste = odr.RealData(
        dados.iloc[:,0],
        e*dados.iloc[:,2],
        dados.iloc[:,1],
        e*dados.iloc[:,3]
    )
    obj_odr = odr.ODR(dados_ajuste, linear, beta0=[0.6,-2])
    resultado = obj_odr.run()
    return resultado



# AJUSTES

# realizando ajustes
ajuste_m1 = ajustar_reta(df, 1)
ajuste_m2 = ajustar_reta(df, 2)
ajuste_m3 = ajustar_reta(df, 3)

# selecionando cada dado
plancks = [ajuste_m1.beta[0], ajuste_m2.beta[0], ajuste_m3.beta[0]]
erros_plancks = [np.sqrt(ajuste_m1.cov_beta[0,0]), np.sqrt(ajuste_m2.cov_beta[0,0]), np.sqrt(ajuste_m3.cov_beta[0,0])]
phis = [ajuste_m1.beta[1], ajuste_m2.beta[1], ajuste_m3.beta[1]]
erros_phis = [np.sqrt(ajuste_m1.cov_beta[1,1]), np.sqrt(ajuste_m2.cov_beta[1,1]), np.sqrt(ajuste_m3.cov_beta[1,1])]

# consolidacao inicial
df_ajustes = pd.DataFrame({
    'Metodo': ['M1', 'M2', 'M3'],
    'h (10^-34)': plancks,
    'Erro h (10^-34)': erros_plancks,
    'Phi (unid?)': phis,
    'Erro Phi (unid?)': erros_phis
})

# re-escalando dados
df_ajustes_escalado = df_ajustes.copy()
df_ajustes_escalado.iloc[:,1:3] = df_ajustes_escalado.iloc[:,1:3]*10
df_ajustes_escalado.iloc[:,3:5] = df_ajustes_escalado.iloc[:,3:5]/e

# salvando
df_ajustes_escalado.to_csv('planck/resultados.csv', index=False)



# PLOTS

def plot_planck(metodo, anotacao='(a)', modo='m'):
    x = df['Frequencia (10^14 Hz)']
    x_err = df['Sigma (10^14 Hz)']
    y = df['V0 M{}'.format(metodo)]*e
    y_err = -df['Erro V0 M{}'.format(metodo)]*e
    escopo = np.arange(0, 9, 0.1)
    m = df_ajustes.iloc[metodo-1,1]
    b = df_ajustes.iloc[metodo-1,3]
    reta = f([m,b], escopo)
    plt.grid(zorder=1)
    plt.errorbar(
        x = x,
        y = y,
        xerr = x_err,
        yerr = y_err,
        ecolor = 'black', # cor das barras de erro
        elinewidth = 2.5, # espessura das barras de erro
        capsize = 0, # espessura das marcações nas extremidades das barras de erro
        color = 'black', # cor dos pontos
        fmt = 'o', # necessario especificar esse argumento para que os pontos sejam plotados
        markersize = 8, # tamanho dos pontos
        zorder = 2 # ordem de plotagem!
    )
    plt.plot(
        escopo,
        reta,
        color = 'red',
        linewidth=3,
        zorder = 3
    )
    plt.annotate(
        anotacao,
        xy=(0.005, .985),
        xycoords='axes fraction', # torna coordenadas xy normalizadas
        verticalalignment='top',
        fontsize=30,
        bbox=dict(boxstyle='square,pad=0.01', facecolor='white', alpha=0.85, edgecolor='none') # caixa de texto
    )
    plt.ylabel('$eV_0$ [$10^{-19}$ J]', fontsize=28)
    plt.xlabel('$f$ [$10^{-14}$ Hz]', fontsize=28)
    #ticks = [i.round(2) for i in np.arange(baixo,cima, (cima-baixo)/5) + (cima-baixo)/10 ]
    plt.xticks(fontsize=25)
    plt.xlim(escopo[0], escopo[-1])
    # plt.ylim(y_baixo, y_cima)
    plt.yticks(fontsize=25)
    plt.tight_layout(pad=0.1)
    #plt.subplots_adjust(right=0.95)
    plt.axhline(0, color='black', linewidth=1.5, zorder=1.5)  # adiciona uma linha no eixo y=0
    if modo == 'm':
        plt.show()
    elif modo == 's':
        plt.savefig('planck/Met_{}'.format(metodo) + '_ajuste_planck.svg', format='svg')
        plt.close()

# plotando e salvando
plot_planck(1, '(a)', 's')
plot_planck(2, '(b)', 's')
plot_planck(3, '(c)', 's')