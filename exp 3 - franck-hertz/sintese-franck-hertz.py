import os
import pandas as pd
from matplotlib import pyplot as plt
import auxiliar

### DIA 1

## importando dados:

# caminho dos dados
os.chdir("exp 3 - franck-hertz")
diretorio_d1 = "dados brutos/dia 1/"
caminhos_d1 = os.listdir(diretorio_d1)

# importacao em um dicionario
dados_d1 = {caminho.replace(".tsv", ''): pd.read_csv(diretorio_d1 + caminho, sep='\t') for caminho in caminhos_d1}
chaves = list(dados_d1.keys())

## primeiro dado: media e desv pad de temperaturas
temp_media_d1 = [dados_d1[df].iloc[:,2].mean() for df in dados_d1]
desv_pad_temp_media_d1 = [dados_d1[df].iloc[:,2].std() for df in dados_d1]
resultados_d1 = pd.DataFrame({"T_med": temp_media_d1, "T_med_desvpad": desv_pad_temp_media_d1})

## metodo 1:

# plot inicial para determinacao pelo metodo 1
fig, axs = plt.subplots(3,3,figsize=(9,9))
for i in range(9):
    ax = axs.flat[i]
    x = dados_d1[chaves[i]].iloc[:,0]
    y = dados_d1[chaves[i]].iloc[:,1]
    ax.set_title(chaves[i])
    ax.plot(x,y)
fig.tight_layout()
plt.show()

# pontos colhidos na analise visual (metodo 1)
picos_metodo1 = {
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

# resultados do metodo 1 pela tomada de diferencas
periodos_metodo1 = [pd.DataFrame(picos_metodo1[chave]).diff().dropna() for chave in chaves]
u_exc_metodo1_diff = [df.iloc[:,0].mean() for df in periodos_metodo1]
u_exc_desvpad_metodo1_diff = [df.iloc[:,0].std() for df in periodos_metodo1]
u_cont_metodo1_diff = []
for i in range(len(picos_metodo1)):
    pico = picos_metodo1[chaves[i]][0]
    u_exc = u_exc_metodo1_diff[i]
    if pico > 13:
        u_cont = pico - 3*u_exc
    else:
        u_cont = pico - 2*u_exc
    u_cont_metodo1_diff.append(u_cont)
u_cont_metodo1_erro_diff = u_exc_desvpad_metodo1_diff # pressupondo valor do pico sem erro
resultados_metodo1 = pd.DataFrame({
    "U_exc_m1_diff": u_exc_metodo1_diff,
    "U_exc_m1_desvpad_diff": u_exc_desvpad_metodo1_diff,
    "U_cont_m1_diff": u_cont_metodo1_diff,
    "U_cont_m1_erro_diff": u_cont_metodo1_erro_diff
})
resultados_d1 = pd.concat([resultados_d1, resultados_metodo1], axis=1)

# resultados do metodo 1 por ajuste linear


## metodo 2:

# estrutura de dados para salvar os resultados de gaussianas de cada temperatura/voltagem
# lista para cada temperatura/voltagem de lista para cada pico de lista para cada resultado de ajuste
lista_ajustes_gaussianos = []

# loop para encaixar uma gaussiana em cada pico, e ja plotar
for i in range(len(picos_metodo1)):
    elemento_lista_ajustes_gaussianos = []
    for j in range(len(picos_metodo1[chaves[i]])):
        pico = picos_metodo1[chaves[i]][j]
        # pegando apenas a regiao a um raio de 1.5V do pico selecionado
        escopo_de_ajuste = dados_d1[chaves[i]][(dados_d1[chaves[i]].iloc[:,0] > pico - 1.5) & (dados_d1[chaves[i]].iloc[:,0] < pico + 1.5)].iloc[:,[0,1]]
        indice_centro = int(len(escopo_de_ajuste)/2)
        ajuste = auxiliar.encaixar_gaussiana(escopo_de_ajuste, [escopo_de_ajuste.iloc[indice_centro,1], escopo_de_ajuste.iloc[indice_centro,0], 1, escopo_de_ajuste.iloc[1,0]])
        elemento_lista_ajustes_gaussianos.append(ajuste)
    lista_ajustes_gaussianos.append(elemento_lista_ajustes_gaussianos)

# pontos colhidos nas gaussianas (metodo 2)
picos_metodo2 = {}
for i in range(len(chaves)):
     picos_metodo2[chaves[i]] = [lista_ajustes_gaussianos[i][j][0][1] for j in range(len(lista_ajustes_gaussianos[i]))]
     
# desvios padrao estimados pelas gaussianas (metodo 2)
desvios_picos_metodo2 = {}
for i in range(len(chaves)):
     desvios_picos_metodo2[chaves[i]] = [lista_ajustes_gaussianos[i][j][0][2] for j in range(len(lista_ajustes_gaussianos[i]))]
     print("a")

## plot metodos 1 e 2
fig, axs = plt.subplots(1,3,figsize=(9,5))
for count, i in enumerate([0,3,6]):
    ax = axs.flat[count]
    ax.grid(True, 'major', 'y') # grid so no eixo y
    ax.set_axisbelow(True) # faz o grid ir para tras dos elementos
    ax.set_title(chaves[i].split(' ')[0].replace('C', " °C"), fontsize=20)
    ax.set_ylim(0.07,0.475)
    ax.set_xlim(0,45)
    ax.tick_params(axis='x', labelsize=15)
    if count == 0:
        ax.set_ylabel("$I_e$ (A)", fontsize=15)
        ax.tick_params(axis='y', labelsize=15)
    elif count > 0:
        ax.set_yticklabels([])
    if count == 1:
        ax.set_xlabel("$V_a$ (V)", fontsize=15)
    # cada serie:
    for j in [0,1,2]:
        dados_temporario = dados_d1[chaves[i+j]]
        # pontos
        if j == 0:
            label = "$V_r =$ 0.5V"
        elif j == 1:
            label = "$V_r =$ 1.5V"
        else:
            label = "$V_r =$ 2.5V"
        x = dados_temporario.iloc[:,0]
        y = dados_temporario.iloc[:,1]
        ax.scatter(x, y, s=6, label=label)
        # picos (metodo 1)
        pontos_metodo1_x = [ponto for ponto in picos_metodo1[chaves[i+j]]]
        linhas_metodo1 = [min(dados_temporario.iloc[:,0], key=lambda x:abs(ponto-x)) for ponto in pontos_metodo1_x]
        pontos_metodo1_y = [dados_temporario[dados_temporario.iloc[:,0] == linha] for linha in linhas_metodo1]
        pontos_metodo1_y = pd.concat(pontos_metodo1_y)
        pontos_metodo1_y.columns = ['a', 'b', 'c']
        pontos_metodo1_y = pontos_metodo1_y.drop_duplicates(subset='a')
        pontos_metodo1_y = pontos_metodo1_y.iloc[:,1]
        if (i+j == 8):
            ax.scatter(pontos_metodo1_x, pontos_metodo1_y, marker='+', color='darkviolet', s=200, label="Picos Método 1")
        else:
            ax.scatter(pontos_metodo1_x, pontos_metodo1_y, marker='+', color='darkviolet', s=200)
        if count == 2:
            ax.legend(fontsize=12, markerscale=1, borderpad=0.3, framealpha=0.95)
        # gaussianas (metodo 2)
        for k in range(len(picos_metodo2[chaves[i+j]])):
            pico = picos_metodo2[chaves[i+j]][k]
            escopo_de_plot = dados_temporario[(dados_temporario.iloc[:,0] > pico - 2.5) & (dados_temporario.iloc[:,0] < pico + 2.5)].iloc[:,0]
            betas = lista_ajustes_gaussianos[i+j][k][0]
            ax.plot(escopo_de_plot, auxiliar.gaussiana(betas, escopo_de_plot), color="black", linewidth=1)   
fig.subplots_adjust(left=0.1, right=0.99, bottom=0.13, top=0.92, wspace=0, hspace=0)
#plt.show()
plt.savefig("sintese/resultados-dia1.svg", format="svg")

## ajuste linear metodo 2

# dados em formato de ajuste
lista_dados = [pd.DataFrame({"picos": picos_metodo2[chaves[i]], "desvios": desvios_picos_metodo2[chaves[i]]}) for i in range(len(picos_metodo2))]
for i in range(len(lista_dados)):
    df = lista_dados[i]
    if len(df) == 7:
        n = list(range(2,9))
    else:
        n = list(range(3,9))
    n = pd.DataFrame({"n": n})
    lista_dados[i] = pd.concat([n, df], axis=1)
    print(lista_dados[i], '\n')

# ajuste
lista_ajustes_lineares = [auxiliar.encaixar_linear(df) for df in lista_dados]

# resultados
u_exc_metodo2_lin = [lista_ajustes_lineares[i][0][0] for i in range(len(lista_ajustes_lineares))]
u_exc_erro_metodo2_lin = [lista_ajustes_lineares[i][1][0] for i in range(len(lista_ajustes_lineares))]
u_cont_metodo2_lin = [lista_ajustes_lineares[i][0][1] for i in range(len(lista_ajustes_lineares))]
u_cont_metodo2_erro_lin = [lista_ajustes_lineares[i][1][1] for i in range(len(lista_ajustes_lineares))]
resultados_metodo2 = pd.DataFrame({
    "U_exc_m2_lin": u_exc_metodo2_lin,
    "U_exc_m2_erro_lin": u_exc_erro_metodo2_lin,
    "U_cont_m2_lin": u_cont_metodo2_lin,
    "U_cont_m2_erro_lin": u_cont_metodo2_erro_lin 
})
resultados_d1 = pd.concat([resultados_d1, resultados_metodo2], axis=1)



# plot ajuste linear




## salvando resultados
resultados_d1.to_csv("sintese/resultados-dia1.csv", index=False)





for el in lista_ajustes_gaussianos:
    for el2 in el:
        print(el2,'\n')    
    print("\n\n")

for el in desvios_picos_metodo2:
    print(desvios_picos_metodo2[el],'\n')

for el in picos_metodo2:
    print(picos_metodo2[el],'\n')

importlib.reload(auxiliar)