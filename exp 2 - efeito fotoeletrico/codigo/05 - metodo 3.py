
# SETUP


import os
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
cores = ('Verde', 'Azul', 'Amarelo', 'Vermelho', 'Violeta')



# esse metodo eh por determinacao visual, entao teremos que ficar plotando, 
# inserindo o valor encontrado, e replotando ate ficar bom

# PLOTS

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


def plotar_V0_metodo_3(cor, anotacao, v0=(-1,0), potencia=3, cols_leg=1, x_lims=(0.5,0.5), mult_y=(1,1), modo='m'):
    intensidades = ('020%', '040%', '060%', '080%', '100%')
    baixo = x_lims[0]
    cima = x_lims[1]

    for i in range(5):
        dados = pd.read_csv('medias de cada intensidade/' + cor + '/' + intensidades[i] + '.csv')
        dados = dados[dados['Tensao (V)'] > baixo-0.2][dados['Tensao (V)'] < cima+0.2]
        x = dados['Tensao (V)']
        y = dados['Corrente media (A)']*10**potencia
        y_baixo = y.min()*mult_y[0]
        y_cima = y.max()*mult_y[1]
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
            zorder = 2.5 # ordem de plotagem
        )
        plt.plot(
            x,
            y,
            color = pegar_coloracao(intensidades[i]),
            label = '$I=$' + intensidades[i].lstrip('0'),
            linewidth=3,
            zorder = 3
        )


    plt.scatter( # adicionando marcador preto do ponto escolhido como v0
        v0[0],
        v0[1],
        c = 'black',
        s = 850,
        marker='x',
        linewidths=4, # a unica forma de deixar o marcador mais espesso
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
        bbox_to_anchor=(0.5, 1.03),
        ncol=cols_leg,
        columnspacing=0.15, # espaçamento entre colunas
        borderpad=0.2, # padding do texto entre a caixa e a borda
    )
    plt.grid(zorder=0.5)
    plt.ylabel('Corrente [$10^{{-{}}}$ A]'.format(potencia), fontsize=28)
    plt.xlabel('$V$ [V]', fontsize=28)
    tick_baixo = baixo - 0.05
    tick_cima = cima + 0.05
    ticks = [i.round(2) for i in np.arange(tick_baixo, tick_cima, (tick_cima-tick_baixo)/5) + (tick_cima-tick_baixo)/10 ]
    plt.xticks(ticks, fontsize=25)
    plt.xlim(baixo, cima)
    plt.ylim(y_baixo, y_cima)
    plt.yticks(fontsize=25)
    plt.tight_layout(pad=0.1)
    plt.subplots_adjust(top=0.99, right=0.93) # vou precisar ajustar manualmente
    plt.axhline(-0.01, color='black', linewidth=2, zorder=2)  # adiciona uma linha no eixo y=0
    if modo == 'm':
        plt.show()
    elif modo == 's':
        plt.savefig('metodos v0/metodo 3/Met_3_' + cor + '.svg', format='svg')
        plt.close()



plotar_V0_metodo_3('Vermelho', '(b)', v0=(-.4,68), potencia=6, cols_leg=2, x_lims=(-0.7,-0.3), mult_y=(0.3,.05), modo='s')
plotar_V0_metodo_3('Amarelo', '(c)', v0=(-.5,12), potencia=5,cols_leg=2, x_lims=(-.8,-.4), mult_y=(0.8,0.1), modo='s')
plotar_V0_metodo_3('Verde', '(d)', v0=(-1.1,0.2), potencia=4,cols_leg=2, x_lims=(-1.3,-0.9), mult_y=(1,.3), modo='s')
plotar_V0_metodo_3('Azul', '(e)', v0=(-1.05,0.3), potencia=3,cols_leg=2, x_lims=(-1.3,-0.9), mult_y=(1,.3), modo='s')
plotar_V0_metodo_3('Violeta', '(f)', v0=(-1.7,5), potencia=5,cols_leg=2, x_lims=(-2,-1.6), mult_y=(0.3,0.5), modo='s')



# VALORES FINAIS

valores_metodo_3 = pd.DataFrame({
    'LED': ['Vermelho', 'Amarelo', 'Verde', 'Azul', 'Violeta'],
    'Valores': ['-0.4', '-0.5', '-1.1', '-1.05', '-1.7']
})
valores_metodo_3.to_csv('metodos v0/metodo 3/todas.csv', index=False)

# ok