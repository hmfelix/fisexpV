
# SETUP

import os
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
cores = ('Verde', 'Azul', 'Amarelo', 'Vermelho', 'Violeta')



# FUNCOES

def calcula_V0_metodo_1_das_intensidades(cor, modo='s'):
    # vamos ler a partir da linha 50 porque alguns gráficos
    # cruzam de corrente positiva para corrente negativa antes disso,
    # depois voltam a cruzar para a positiva
    arquivos = os.listdir('medias de cada intensidade/' + cor)
    v0_interpolado = []
    if modo == 's':
        coluna = 'Corrente media (A)'
    else:
        coluna = 'Corrente com ruido descontado (A)'
    for arquivo in arquivos:
        df = pd.read_csv('medias de cada intensidade/' + cor + '/' + arquivo).iloc[50:,]
        # vamos inverter o gráfico!
        y = df['Tensao (V)']
        x = df[coluna]
        # ponto em que queremos interpolar:
        x_a_interpolar = 0
        # resultado da interpolação:
        y_interpolado = np.interp(x_a_interpolar, x, y)
        v0_interpolado.append(y_interpolado)
    return v0_interpolado

def calcula_V0_metodo_1(modo='s'):
    # modos: 's' = sem ruido descontado, 'r' = com ruido descontado
    cores_calculadas = []
    v0_metodo_1 = []
    desv_pads = []
    for cor in cores:
        lista_v0s = calcula_V0_metodo_1_das_intensidades(cor, modo)
        v0_metodo_1.append(np.mean(lista_v0s))
        desv_pads.append(np.std(lista_v0s))
        cores_calculadas.append(cor)
    resultado = pd.DataFrame({'Cor': cores_calculadas, 'V0 M1': v0_metodo_1, 'Desvio padrao': desv_pads})
    return resultado



# CALCULO TOTAL E SALVAMENTO

metodo_1_sem_ruido = calcula_V0_metodo_1('s')
metodo_1_com_ruido = calcula_V0_metodo_1('r')

pd.merge(metodo_1_sem_ruido, metodo_1_com_ruido, on='Cor', suffixes=(' sem ruido', ' com ruido')).to_csv('metodos v0/metodo 1/todas.csv', index=False)



# CALCULO POR INTENSIDADE E SALVAMENTO




# PLOTS

def pegar_coloracao(intensidade):
    if intensidade == "100%":
        coloracao = 'b'
    elif intensidade == "080%":
        coloracao = 'r'
    elif intensidade == "060%":
        coloracao = 'g'
    elif intensidade == "040%":
        coloracao = 'c'
    elif intensidade == "020%":
        coloracao = 'm'
    return coloracao


def plotar_V0_metodo_1(cor, anotacao, potencia=3, cols_leg=1, descontos_x=(0.5,0.5), mult_y=(1,1), modo='m'):
    v0s = calcula_V0_metodo_1_das_intensidades(cor)
    intensidades = ('020%', '040%', '060%', '080%', '100%')
    baixo = np.min(v0s) - descontos_x[0]
    cima = np.max(v0s) + descontos_x[1]

    for i in range(5):
        dados = pd.read_csv('medias de cada intensidade/' + cor + '/' + intensidades[i] + '.csv')
        dados = dados[dados['Tensao (V)'] > baixo][dados['Tensao (V)'] < cima]
        x = dados['Tensao (V)']
        y = dados['Corrente media (A)']*10**potencia
        y_baixo = y.min()*mult_y[0]
        y_cima = y.max()*mult_y[1]
        plt.grid(zorder=1)
        plt.errorbar(
            x = x,
            y = y,
            xerr = dados['Erro instrumental (V)'],
            yerr = dados['Desvio padrao (A)'],
            ecolor = pegar_coloracao(intensidades[i]), # cor das barras de erro
            elinewidth = 2.5, # espessura das barras de erro
            capsize = 0, # espessura das marcações nas extremidades das barras de erro
            color = pegar_coloracao(intensidades[i]), # cor dos pontos
            fmt = 'o', # necessario especificar esse argumento para que os pontos sejam plotados
            markersize = 7, # tamanho dos pontos
            zorder = 2 # ordena que seja plotado primeiro!
        )
        plt.plot(
            x,
            y,
            color = pegar_coloracao(intensidades[i]),
            label = '$I=$' + intensidades[i].lstrip('0'),
            linewidth=3,
            zorder = 3
        )
        plt.scatter(
            v0s[i],
            0,
            c = pegar_coloracao(intensidades[i]),
            s = 250,
            marker='x',
            linewidths=4, # a unica forma de deixar o marcador mais espesso
            zorder = 4
        )
        plt.scatter( # adicionando marcador preto para fazer a fronteira
            v0s[i],
            0,
            c = 'black',
            s = 350,
            marker='x',
            linewidths=8, # a unica forma de deixar o marcador mais espesso
            zorder = 3.9
        )

    plt.scatter( # adicionando marcador preto do ponto medio (v0 total)
        np.mean(v0s),
        0,
        c = 'black',
        s = 350,
        marker='x',
        linewidths=8, # a unica forma de deixar o marcador mais espesso
        zorder = 3.9
    )
    plt.annotate(
        anotacao,
        xy=(0.005, .985),
        xycoords='axes fraction', # torna coordenadas xy normalizadas
        verticalalignment='top',
        fontsize=30,
        bbox=dict(boxstyle='square,pad=0.01', facecolor='white', alpha=0.85, edgecolor='none') # caixa de texto
    )
    #plt.title('A', fontsize=30)
    plt.legend(
        fontsize = 22,
        loc = 'upper center',
        handlelength = 0.7, # tamanho da linha da legenda
        handletextpad = 0.1, # padding do texto entre símbolos
        #bbox_to_anchor=(0.38, 1.03),
        ncol=cols_leg,
        columnspacing=0.15, # espaçamento entre colunas
        borderpad=0.2, # padding do texto entre a caixa e a borda
    )
    plt.ylabel('Corrente [$10^{{-{}}}$ A]'.format(potencia), fontsize=28)
    plt.xlabel('$V$ [V]', fontsize=28)
    ticks = [i.round(2) for i in np.arange(baixo,cima, (cima-baixo)/5) + (cima-baixo)/10 ]
    plt.xticks(ticks, fontsize=25)
    plt.xlim(baixo+0.035, cima-0.035)
    plt.ylim(y_baixo, y_cima)
    plt.yticks(fontsize=25)
    plt.tight_layout(pad=0.1)
    plt.subplots_adjust(right=0.95) # vou precisar ajustar manualmente
    plt.axhline(0, color='black', linewidth=1.5, zorder=1.5)  # adiciona uma linha no eixo y=0
    if modo == 'm':
        plt.show()
    elif modo == 's':
        plt.savefig('metodos v0/metodo 1/Met_1_' + cor + '.svg', format='svg')
        plt.close()



plotar_V0_metodo_1('Vermelho', '(b)', potencia=5, cols_leg=2, descontos_x=(0.2,0.1), mult_y=(0.6,1.2), modo='s')
plotar_V0_metodo_1('Amarelo', '(c)', potencia=5, cols_leg=2, descontos_x=(0.2,0.1), mult_y=(0.8,1.2), modo='s')
plotar_V0_metodo_1('Verde', '(d)', potencia=4, cols_leg=2, descontos_x=(0.2,0.122), mult_y=(0.85,1.2), modo='s')
plotar_V0_metodo_1('Azul', '(e)', potencia=3, cols_leg=2, descontos_x=(0.2,0.13), mult_y=(1,1), modo='s')
plotar_V0_metodo_1('Violeta', '(f)', potencia=5, cols_leg=2, descontos_x=(0.2,0.1), mult_y=(0.3,1.5), modo='s')

# ok
