import os
import json
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
os.chdir("exp 3 - franck-hertz")
from codigo import auxiliar

# IMPORTACAO

# importando dados brutos
dados_d1, chaves = auxiliar.importar_dados_d1()

# importando dados dos picos encontrados pelo metodo 1
with open("resultados/dia1/picos-metodo1.json", 'r') as arquivo:
    picos_metodo1 = json.load(arquivo)
# convertendo dados dos picos em um dicionario de dataframes
# (e visualizando)
for i in range(len(picos_metodo1)):
    picos_metodo1[chaves[i]] = pd.DataFrame(picos_metodo1[chaves[i]])
    print(chaves[i], '\n', picos_metodo1[chaves[i]], '\n')

# importando dados dos picos encontrados pelo metodo 2, ja tratados
with open("resultados/dia1/picos-metodo2.json", 'r') as arquivo:
    picos_metodo2 = json.load(arquivo)
# convertendo dados dos picos em um dicionario de dataframes
# (e visualizando)
for i in range(len(picos_metodo2)):
    picos_metodo2[chaves[i]] = pd.DataFrame(picos_metodo2[chaves[i]])
    print(chaves[i], '\n', picos_metodo2[chaves[i]], '\n')


# TITULOS E CORES

temps = pd.read_csv("resultados/dia1/temperaturas_media_medias.csv")
titulos = [str(round(temps.iloc[i,0],3)) + '(' + str(round(temps.iloc[i,1],3)).replace("0.00", '') + ") °C" for i in range(3)]
# consertando manualmente um titulo que nao deu certo
titulos[2] = "200.060(8) °C"
cores = ["cornflowerblue", "salmon", "limegreen"]


# PLOT METODOS 1 E 2


fig, axs = plt.subplots(1,3,figsize=(9,5))
for count, i in enumerate([0,3,6]):
    ax = axs.flat[count]
    ax.grid(True, 'major', 'y') # grid so no eixo y
    ax.set_axisbelow(True) # faz o grid ir para tras dos elementos
    ax.set_title(titulos[count], fontsize=20)
    ax.set_ylim(0.07*10,0.475*10)
    ax.set_xlim(0,45)
    ax.tick_params(axis='x', labelsize=15)
    if count == 0:
        ax.set_ylabel("$I_e$ [$10^{-1}$ A]", fontsize=15)
        ax.tick_params(axis='y', labelsize=15)
    elif count > 0:
        ax.set_yticklabels([])
    if count == 1:
        ax.set_xlabel("$V_a$ [V]", fontsize=15)
    # cada serie:
    for j in [0,1,2]:
        dados_temporario = dados_d1[chaves[i+j]]
        dados_temporario.iloc[:,1] *= 10
        # pontos
        if j == 0:
            label = "$V_r =$ 0.5V"
        elif j == 1:
            label = "$V_r =$ 1.5V"
        else:
            label = "$V_r =$ 2.5V"
        x = dados_temporario.iloc[:,0]
        y = dados_temporario.iloc[:,1]
        ax.scatter(x, y, s=6, label=label, color=cores[j], zorder=3)
        # picos (metodo 1)
        for v in range(len(picos_metodo1[chaves[i+j]])):
            x_inf = picos_metodo1[chaves[i+j]]["V_A_inf"][v]
            x_centro = picos_metodo1[chaves[i+j]]["V_A"][v]
            x_sup = picos_metodo1[chaves[i+j]]["V_A_sup"][v]
            y_inf = picos_metodo1[chaves[i+j]]["I_inf"][v] * 10
            y_centro = picos_metodo1[chaves[i+j]]["I"][v] * 10
            y_sup = picos_metodo1[chaves[i+j]]["I_sup"][v] * 10
            ax.plot([x_inf, x_inf], [0,y_inf], color=cores[j], linewidth=.5, zorder=2)
            ax.plot([x_centro, x_centro], [0,y_centro], color=cores[j], linewidth=.5, zorder=2)
            ax.plot([x_sup, x_sup], [0,y_sup], color=cores[j], linewidth=.5, zorder=2)
            ax.scatter([x_centro], [y_centro], marker='o', color="red", s=20, zorder=4)
            ax.fill_between(x, y, where=(x>x_inf) & (x<x_sup), color=cores[j], alpha=0.12, zorder=1)
        if (i+j == 8):
            ax.plot([10,20], [10,20], color="black", label="Gauss Método 2") # placeholder para aparecer legenda do método 2
            ax.scatter([10], [20], marker='o', color="red", s=10, label="FWHM Método 1")
        if count == 2:
            ax.legend(fontsize=12, markerscale=2, borderpad=0.3, framealpha=0.95)
        # gaussianas (metodo 2)
        for k in range(len(picos_metodo2[chaves[i+j]])):
            pico = picos_metodo2[chaves[i+j]]["V_A"][k]
            escopo_de_plot = dados_temporario[(dados_temporario.iloc[:,0] > pico - 2.5) & (dados_temporario.iloc[:,0] < pico + 2.5)].iloc[:,0]
            betas = [picos_metodo2[chaves[i+j]].iloc[k,2]*10, picos_metodo2[chaves[i+j]].iloc[k,0], picos_metodo2[chaves[i+j]].iloc[k,1], picos_metodo2[chaves[i+j]].iloc[k,3]*10]
            ax.plot(escopo_de_plot, auxiliar.gaussiana(betas, escopo_de_plot), color="black", linewidth=1, zorder=5)   
fig.subplots_adjust(left=0.1, right=0.99, bottom=0.13, top=0.92, wspace=0, hspace=0)
#plt.show()
plt.savefig("resultados/dia1/plot-geral-dia1.svg", format="svg")
plt.close()
