# SETUP

import os
import pandas as pd
import numpy as np
import scipy.odr as odr
import math
import statistics
from matplotlib import pyplot as plt



cores = ["Verde", "Azul", "Amarelo", "Vermelho", "Violeta"]



# FUNCOES

def importa_dados(cor):
    # 0 = Verde, 1 = Azul, 2 = Amarelo, 3 = Vermelho, 4 = Violeta
    pastas = []
    arquivos = []
    dados = []
    for i in range(len(cor)):
        pastas.append("medias de cada intensidade/" + cor[i])
        temp = os.listdir(pastas[i])
        for j in temp:
            arquivos.append("{}/{}".format(pastas[i],j))
    for arquivo in arquivos:
        dados.append(pd.read_csv(arquivo))
    return dados, arquivos



dados, arquivos = importa_dados(cores)
dados_y = []
dados_x = []
dados_sigmay = []
dados_sigmax = []

for i in range(len(dados)):
    dados_y.append(dados[i].iloc[:,2])
    dados_x.append(dados[i].iloc[:,0])
    dados_sigmay.append(dados[i].iloc[:,3]) #Desvio padrão (3) Ruido (4)
    dados_sigmax.append(dados[i].iloc[:,1])

dados_x_1 = dados_x[:]
dados_y_1 = dados_y[:]
dados_sigmay_1 = dados_sigmay[:]
dados_sigmax_1 = dados_sigmax[:]
dados_x_2 = dados_x[:]
dados_y_2 = dados_y[:]
dados_sigmay_2 = dados_sigmay[:]
dados_sigmax_2 = dados_sigmax[:]

for j in range(len(dados_y_1)):
    dados_x_1[j] = dados_x_1[j][:75]
    dados_y_1[j] = dados_y_1[j][:75]
    dados_sigmay_1[j] = dados_sigmay_1[j][:75]
    dados_sigmax_1[j] = dados_sigmax_1[j][:75]

for j in range(len(dados_y_2)):
    for i in range(len(dados_y_2[0])):
        if dados_y_2[j][i] < 0 or dados_x_2[j][i] > 1:
            dados_y_2[j] = dados_y_2[j].drop(i)
            dados_x_2[j] = dados_x_2[j].drop(i)
            dados_sigmay_2[j] = dados_sigmay_2[j].drop(i)
            dados_sigmax_2[j] = dados_sigmax_2[j].drop(i)


#print(dados_y_2[0],dados_x_2[0],dados_sigmay_2[0],dados_sigmax_2[0])

angulos = []

for j in range(len(dados_y_2)):
    angulos.append([])
    for i in range(dados_y_2[j].index[0],dados_y_2[j].index[-1]):
        angulos[j].append(math.degrees(math.atan((dados_y_2[j][i+1]-dados_y_2[j][i])/(dados_x_2[j][i+1]-dados_x_2[j][i]))))

media = []
mediana = []
maximo = []
stdev = []
for i in range(len(angulos)):
    media.append(statistics.mean(angulos[i]))
    mediana.append(statistics.median(angulos[i]))
    maximo.append(max(angulos[i]))
    stdev.append(statistics.stdev(angulos[i]))

for i in range(len(stdev)):
    if stdev[i] > 5:
        stdev[i] = 5
    if stdev[i] < 2:
        stdev[i] = stdev[i]


for i in range(len(media)):
    print(media[i],mediana[i],maximo[i],stdev[i])


menor = []
maior = []

for i in range(len(angulos)):
    menor.append(-1)
    maior.append(-1)
    for j in range(len(angulos[i])):
        if angulos[i][j] < maximo[i]+stdev[i] and angulos[i][j] > maximo[i]-1.5*stdev[i]:
            maior[i] = j
        if angulos[i][j] < maximo[i]+stdev[i] and angulos[i][j] > maximo[i]-1.5*stdev[i] and menor[i] == -1:
            menor[i] = j

for j in range(len(dados_y_2)):
    rangemin = dados_y_2[j].index[0]+menor[j]
    rangemax = dados_y_2[j].index[0]+maior[j]+1
    dados_y_2[j] = dados_y_2[j].drop(dados_y_2[j].index[0:menor[j]])
    dados_y_2[j] = dados_y_2[j].drop(dados_y_2[j].index[(maior[j]-menor[j]+2):dados_y_2[j].index[-1]])
    dados_x_2[j] = dados_x_2[j].drop(dados_x_2[j].index[0:menor[j]])
    dados_x_2[j] = dados_x_2[j].drop(dados_x_2[j].index[(maior[j]-menor[j]+2):dados_y_2[j].index[-1]])
    dados_sigmax_2[j] = dados_sigmax_2[j].drop(dados_sigmax_2[j].index[0:menor[j]])
    dados_sigmax_2[j] = dados_sigmax_2[j].drop(dados_sigmax_2[j].index[(maior[j]-menor[j]+2):dados_y_2[j].index[-1]])
    dados_sigmay_2[j] = dados_sigmay_2[j].drop(dados_sigmay_2[j].index[0:menor[j]])
    dados_sigmay_2[j] = dados_sigmay_2[j].drop(dados_sigmay_2[j].index[(maior[j]-menor[j]+2):dados_y_2[j].index[-1]])

print(dados_sigmay_2[5])

def f(B, x):
    return B[0]*x + B[1]

df_todas_metodo_2 = pd.DataFrame(columns=['LED', 'V0 M2'])

LED = []
Intensidades = []
Inten = ["100","80","60","40","20"]

for i in range(len(arquivos)):
    for cor in cores:
        if cor in arquivos[i]:
            LED.append(cor)
for i in range(len(arquivos)):
    for j in Inten:
        if j in arquivos[i]:
            Intensidades.append(j)
print(LED,Intensidades)

for j in range(len(dados_y_2)):
    linear = odr.Model(f)
    dados_ajuste_1 = odr.RealData(
        dados_x_1[j],
        dados_y_1[j],
        dados_sigmax_1[j],
        dados_sigmay_1[j]
    )
    obj_odr = odr.ODR(dados_ajuste_1, linear, beta0=[0.01,0.01])
    ajuste_1 = obj_odr.run()

    dados_ajuste_2 = odr.RealData(
            dados_x_2[j],
            dados_y_2[j],
            dados_sigmax_2[j],
            dados_sigmay_2[j]
        )
    obj_odr = odr.ODR(dados_ajuste_2, linear, beta0=[0.01,0.01])
    ajuste_2 = obj_odr.run()
    m1 = ajuste_1.beta[0]
    b1 = ajuste_1.beta[1]
    m2 = ajuste_2.beta[0]
    b2 = ajuste_2.beta[1]
    intersecao = (b2 - b1) / (m1 - m2)
    linha_resultado = pd.DataFrame({'LED': [arquivos[j][-15:]], 'V0 M2': [intersecao]})
    df_todas_metodo_2 = pd.concat([df_todas_metodo_2, linha_resultado])
    escopo_ajuste_1 = np.arange(-5, intersecao, 0.01)
    plt.grid(zorder=1)
    plt.errorbar( # pontos do gráfico
        x = dados_x[j],
        y = dados_y[j],
        xerr = dados_sigmax[j],
        yerr = dados_sigmay[j],
        fmt = 'o', # formato dos pontos, previne linhas ligando-os
        ecolor = 'black', # cor das barras de erro
        elinewidth = 2.5, # espessura das barras de erro
        capsize = 0, # espessura das marcações nas extremidades das barras de erro
        color = 'black', # cor dos pontos
        markersize = 7, # tamanho dos pontos
        zorder = 2
    )
    plt.plot( # ajuste 1
        escopo_ajuste_1,
        ajuste_1.beta[0]*escopo_ajuste_1 + ajuste_1.beta[1],
        color = 'red',
        linewidth=3,
        zorder = 3.9
    )
    escopo_ajuste_2 = np.arange(intersecao, 0.75, 0.01)
    plt.plot( # ajuste 2
        escopo_ajuste_2,
        ajuste_2.beta[0]*escopo_ajuste_2 + ajuste_2.beta[1],
        color = 'red',
        linewidth=3,
        zorder = 3
    )
    plt.ylabel('Corrente [A]', fontsize=28)
    plt.xlabel('$V$ [V]', fontsize=28)
    plt.xlim(-2, 1)
    plt.ylim(top=max(dados_y[j][:120]))
    plt.yticks(fontsize=25)
    plt.xticks(fontsize=25)
    plt.tight_layout(pad=0.1)
    plt.subplots_adjust(top=0.99) # vou precisar ajustar manualmente
    plt.axhline(0, color='black', linewidth=1.5, zorder=1.5)  # adiciona uma linha no eixo y=0
    anotacao = LED[j] + '\n$I=$' + Intensidades[j] + '%'
    plt.annotate(
        anotacao,
        xy=(0.05, .98),
        xycoords='axes fraction', # torna coordenadas xy normalizadas
        verticalalignment='top',
        fontsize=30,
        bbox=dict(boxstyle='square,pad=0.02', facecolor='white', alpha=0.85, edgecolor='none') # caixa de texto
    )
    nome_a_salvar = 'Met_2_' + LED[j] + '_' + Intensidades[j] + '.svg'
    plt.savefig('metodos v0/metodo 2/graficos/' + nome_a_salvar, format='svg')
    plt.close()

df_todas_metodo_2.to_csv('todas.csv', index=False)













