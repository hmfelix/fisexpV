# vou continuar o trabalho do primeiro script porque vou reutilizar várias funções dali



# 0) Setup

import os
import pandas as pd
import numpy as np
import scipy.odr as odr
from matplotlib import pyplot as plt






# 1) Tratamento dos arquivos

## 1.1) funções que aplicarei aos conjuntos de dados:

def substituir_virgulas(texto):
    return texto.replace(',', '.')

def substituir_ponto_e_virgula(texto):
    return texto.replace(';', ',')

def substituir_tab(texto):
    return texto.replace('	', ',')

def substituir_csv(arquivo):
    with open(arquivo, 'r') as csv:
        corpus = csv.read()
    novo_corpus = substituir_virgulas(corpus)
    novo_corpus = substituir_ponto_e_virgula(novo_corpus)
    with open(arquivo, 'w') as csv:
        csv.write(novo_corpus)

def substituir_dat(arquivo):
    with open(arquivo, 'r') as csv:
        corpus = csv.read()
    novo_corpus = substituir_virgulas(corpus)
    novo_corpus = substituir_tab(novo_corpus)
    with open(arquivo, 'w') as csv:
        csv.write(novo_corpus)



## 1.2) obtendo o caminho dos arquivos CSV:
# vou usar a estrutura de lista por ser mutável

caminhos = []
arqs_RuidoD2 = os.listdir('Ruido dia 2') 
caminhos.extend(['Ruido dia 2/' + elemento for elemento in arqs_RuidoD2])
arqs_Verde = os.listdir('Verde') 
caminhos.extend(['Verde/' + elemento for elemento in arqs_Verde])
arqs_Az = os.listdir('Azul') 
caminhos.extend(['Azul/' + elemento for elemento in arqs_Az])
arqs_Am = os.listdir('Amarelo') 
caminhos.extend(['Amarelo/' + elemento for elemento in arqs_Am])



## 1.3) aplicando as funções de substituição CSV:

for caminho in caminhos:
    substituir_csv(caminho)



## 1.4) obtendo caminho dos arquivos DAT:
caminhos_DAT_D2 = [
    'Frequencias/espectro_LED_Am.dat',
    'Frequencias/espectro_LED_Az.dat',
    'Frequencias/espectro_LED_Vd.dat'
]



## 1.5) aplicando as funções de substituição DAT:

for caminho in caminhos_DAT_D2:
    substituir_dat(caminho)

# ok







# 2) Importação, tratamento e plotagem dos dados de medidas
# desta vez vou fazer de outra forma, criando listas separadas para cada cor

## 2.1) importação em listas de dfs:
def importar_dados(pasta):
    arquivos = os.listdir(pasta)
    lista = []
    for arquivo in arquivos:
        caminho = pasta + '/' + arquivo
        df = pd.read_csv(caminho)
        lista.append(df)
    return lista

dfs_RuidoD2 = importar_dados('Ruido dia 2')
dfs_Verde = importar_dados('Verde')
dfs_Az = importar_dados('Azul')
dfs_Am = importar_dados('Amarelo')



## 2.2) gerando e salvando 1 dataframe por intensidade e LED

def gerar_df_Imédio(indice0, indice1, pasta):
    if (not 'Ruido' in pasta) and ((pasta == 'Vermelho') or (pasta == 'Violeta')):
        ruidos = pd.read_csv('Medias de cada intensidade/Ruido.csv')
    elif (not 'Ruido' in pasta) and ((pasta == 'Amarelo') or (pasta == 'Azul') or (pasta == 'Verde')):
        ruidos = pd.read_csv('Medias de cada intensidade/Ruido dia 2.csv')
    else:
        coluna = [0 for elemento in list(range(1,203))]
        ruidos = pd.DataFrame({
            'Tensao (V)': coluna,
            'Erro instrumental (V)': coluna,
            'Corrente media (A)': coluna,
            'Desvio padrao (A)': coluna
        })
    dfs_base = importar_dados(pasta)
    df_compilada = dfs_base[indice0]
    for df in dfs_base[indice0+1:indice1]:
        df_compilada = pd.concat([df_compilada, df['Corrente [A]']], axis=1)
    media_por_linha = df_compilada.iloc[:, 1:].mean(axis=1)
    # corrigindo pelos ruidos:
    media_por_linha = media_por_linha - ruidos['Corrente media (A)']
    desvio_padrao_por_linha = df_compilada.iloc[:, 1:].std(axis=1)
    # propagando com os erros dos ruidos:
    desvio_padrao_por_linha = np.sqrt(desvio_padrao_por_linha**2 + ruidos['Desvio padrao (A)']**2)

    resultado = pd.DataFrame({
        'Tensao (V)': df_compilada.iloc[:,0],
        'Erro instrumental (V)': 0.025,
        'Corrente media (A)': media_por_linha,
        'Desvio padrao (A)': desvio_padrao_por_linha
    })
    return resultado


# ruido (necessario gerar primeiro para a função acima dar certo nas demais cores)
gerar_df_Imédio(0,5,'Ruido dia 2').to_csv('Medias de cada intensidade/Ruido dia 2.csv', index=False)
gerar_df_Imédio(0,5,'Ruido').to_csv('Medias de cada intensidade/Ruido.csv', index=False)

# cores
pastas = ['Verde', 'Azul', 'Amarelo', 'Vermelho', 'Violeta']
indices_iniciais = list(range(0,41,10))
indices_finais = list(range(10,51,10))
intensidades = ['100%', '20%', '40%', '60%', '80%']
    
for pasta in pastas:
    for i in range(0,5):
        df = gerar_df_Imédio(indices_iniciais[i], indices_finais[i], pasta)
        nome_arquivo = 'Medias de cada intensidade/' + pasta + '_' + intensidades[i] + '.csv'
        df.to_csv(nome_arquivo, index=False)
    



## 2.4) plotando tudo e salvando em svg

arquivos_a_plotar = os.listdir('Medias de cada intensidade')
pasta_a_salvar = 'Curvas medias de cada intensidade/'

for arq in arquivos_a_plotar:
    df = pd.read_csv('Medias de cada intensidade/' + arq)
    plt.errorbar(
        x = df.iloc[:,0],
        y = df.iloc[:,2],
        xerr = df.iloc[:,1],
        yerr = df.iloc[:,3],
        fmt = 'o', # formato dos pontos, previne linhas ligando-os
        ecolor = 'black', # cor das barras de erro
        elinewidth = 1.3, # espessura das barras de erro
        capsize = 0, # espessura das marcações nas extremidades das barras de erro
        color = 'black', # cor dos pontos
        markersize = 3.5 # tamanho dos pontos
    )
    titulo = arq.replace('_', ' ').replace('.csv', '')
    plt.title(titulo, fontsize=30)
    plt.xlabel('Tensão (V)', fontsize=23)
    plt.ylabel('Corrente (A)', fontsize=23)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    #plt.subplots_adjust(bottom=0.2, right=0.98, left=0.2, top=0.90)
    plt.tight_layout(pad=0.1)
    plt.grid()
    nome_a_salvar = pasta_a_salvar + arq.replace('csv', 'svg')
    plt.savefig(nome_a_salvar, format='svg')
    plt.close()






# 3) Determinação de V_0

## 3.1) Método 1: interpolação linear em zero

# loop que calcula todas as intensidades e já coloca em um dataframe
arquivos_a_calcular_V0_metodo_1 = [arq for arq in arquivos_a_plotar if not 'Ruido' in arq]
df_interpolacao = pd.DataFrame(columns=['LED', 'Intensidade', 'V0 M1'])
for arquivo in arquivos_a_calcular_V0_metodo_1:
    # vamos ler a partir da linha 50 porque alguns gráficos
    # cruzam de corrente positiva para corrente negativa antes disso,
    # depois voltam a cruzar para a positiva
    df = pd.read_csv('Medias de cada intensidade/' + arquivo).iloc[50:,]
    # vamos inverter o gráfico!
    y = df['Tensao (V)']
    x = df['Corrente media (A)']
    # ponto em que queremos interpolar:
    x_a_interpolar = 0
    # resultado da interpolação:
    y_interpolado = np.interp(x_a_interpolar, x, y)
    led = arquivo.split('_')[0]
    intensidade = arquivo.split('_')[1].replace('.csv','')
    linha_resultado = pd.DataFrame({'LED': [led], 'Intensidade': [intensidade], 'V0 M1': [y_interpolado]})
    df_interpolacao = pd.concat([df_interpolacao, linha_resultado])

# salvando
df_interpolacao.to_csv('Metodos/Metodo 1/todas.csv', index=False)

# cálculo da média de cada LED com incerteza = desvpad:
# (MÉTODO DAORA PARA OBTER ELEMENTOS UNICOS DE UMA LISTA EM PYTHON:
# SIMPLESMENTE CONVERTE-LA EM CONJUNTO!)
leds = list(set(df_interpolacao['LED']))
df_medias_metodo_1 = pd.DataFrame(columns=['LED', 'V0 M1', 'Erro V0 M1'])
for led in leds:
    df = df_interpolacao[df_interpolacao['LED'] == led] # indexação booleana funciona!!!
    media = df['V0 M1'].mean()
    desvpad = df['V0 M1'].std()
    linha_resultado = pd.DataFrame({'LED': [led], 'V0 M1': [media], 'Erro V0 M1': [desvpad]})
    df_medias_metodo_1 = pd.concat([df_medias_metodo_1, linha_resultado])

# salvando
df_medias_metodo_1.to_csv('Metodos/Metodo 1/medias.csv', index=False)

# DÚVIDA: PRECISO FAZER O PLOT DA INTERPOLAÇÃO?



## 3.2) Método 2: ajuste linear duplo

# a dificuldade aqui é que cada gráfico pode exigir a seleção de pontos específicos

# vamos fazer os plots de todas as intensidades de 1 led para ver
def plot_todas(led, intervalo):
    arqs = os.listdir('Medias de cada intensidade')
    arqs = [arq for arq in arqs if led in arq]
    fig, axs = plt.subplots(3,2)
    ind = 0 
    for arq in arqs:
        df = pd.read_csv('Medias de cada intensidade/' + arq)
        df = df[df['Tensao (V)'] >= intervalo[0]]
        df = df[df['Tensao (V)'] <= intervalo[1]]
        linha = (ind+2)//2
        coluna = (ind+2)%2
        linha = linha-1
        ind = ind+1
        axs[linha, coluna].scatter(df['Tensao (V)'], df['Corrente media (A)'], s=1)
        axs[linha, coluna].set_ylim(-0.002,0.01)
        titulo = arq.replace('_', ' ').replace('.csv', '')
        axs[linha, coluna].set_title(titulo)
        axs[linha, coluna].grid()
    fig.tight_layout()
    plt.show()

plot_todas('Vermelho', [-5,5])
plot_todas('Violeta', [-5,5])
plot_todas('Amarelo', [-5,5])
plot_todas('Azul', [-5,5])
plot_todas('Verde', [-5,5])

# ok, dessa inspeção visual concluo o seguinte:
# posso pegar o ponto do método 1 (onde A = 0) e excluir
# todos os pontos em um raio de x pontos a partir de V_0, sendo x:
# p/ Vermelho: 7, negativo -3
# p/ Violeta: 15
# p/ Amarelo: 7
# p/ Azul: -11, positivo 0
# depois fazer um ajuste dos próximos 10 pontos
# PROBLEMAS:
#   . as curvas começam inclinadas para baixo
#   . seria bastante arbitrário cada gráfico
#   . azul apresenta dificuldades substanciais

# então eu vou apenas recorrer ao método dos slides mesmo...

# ajuste pelo método dos slides:
arquivos_a_calcular_V0_metodo_2 = [arq for arq in arquivos_a_plotar if not 'Ruido' in arq]
df_todas_metodo_2 = pd.DataFrame(columns=['LED', 'Intensidade', 'V0 M2'])

for arquivo in arquivos_a_calcular_V0_metodo_2:
    
    # importando dados
    df_base = pd.read_csv('Medias de cada intensidade/' + arquivo)
    # ajuste de baixo:
    df_ajuste_1 = df_base[df_base['Tensao (V)'] <= 0]
    df_ajuste_1 = df_ajuste_1[df_ajuste_1['Corrente media (A)'] <= 0]
    # ajuste de cima:
    df_ajuste_2 = df_base[df_base['Tensao (V)'] <= 0]
    df_ajuste_2 = df_ajuste_2[df_ajuste_2['Corrente media (A)'] > 0]

    # filtrando os pontos iniciais onde a corrente pode eventualmente ser positiva
    filtro = df_ajuste_1['Tensao (V)'].min()
    df_ajuste_2 = df_ajuste_2[df_ajuste_2['Tensao (V)'] > filtro]

    # função de ajuste
    def f(B, x):
        return B[0]*x + B[1]
    linear = odr.Model(f)
    
    # ajuste 1
    dados_ajuste_1 = odr.RealData(
        df_ajuste_1['Tensao (V)'],
        df_ajuste_1['Corrente media (A)'],
        df_ajuste_1['Erro instrumental (V)'],
        df_ajuste_1['Desvio padrao (A)']
    )
    obj_odr = odr.ODR(dados_ajuste_1, linear, beta0=[0.01,0.01])
    ajuste_1 = obj_odr.run()

    # ajuste 2
    dados_ajuste_2 = odr.RealData(
        df_ajuste_2['Tensao (V)'],
        df_ajuste_2['Corrente media (A)'],
        df_ajuste_2['Erro instrumental (V)'],
        df_ajuste_2['Desvio padrao (A)']
    )
    obj_odr = odr.ODR(dados_ajuste_2, linear, beta0=[0.01,0.01])
    ajuste_2 = obj_odr.run()

    # obtendo ponto de intersecao entre as retas de ajuste
    m1 = ajuste_1.beta[0]
    b1 = ajuste_1.beta[1]
    m2 = ajuste_2.beta[0]
    b2 = ajuste_2.beta[1]
    intersecao = (b2 - b1) / (m1 - m2)

    # agregando à planilha de intensidades
    led = arquivo.split('_')[0]
    intensidade = arquivo.split('_')[1].replace('.csv','')
    linha_resultado = pd.DataFrame({'LED': [led], 'Intensidade': [intensidade], 'V0 M2': [intersecao]})
    df_todas_metodo_2 = pd.concat([df_todas_metodo_2, linha_resultado])

    # plotando
    escopo_ajuste_1 = np.arange(-5, intersecao, 0.01)
    plt.plot( # ajuste 1
        escopo_ajuste_1,
        ajuste_1.beta[0]*escopo_ajuste_1 + ajuste_1.beta[1],
        color = 'red',
        linewidth=2.8
    )
    escopo_ajuste_2 = np.arange(intersecao, 0, 0.01)
    plt.plot( # ajuste 2
        escopo_ajuste_2,
        ajuste_2.beta[0]*escopo_ajuste_2 + ajuste_2.beta[1],
        color = 'red',
        linewidth=2.8
    )
    escopo_geral = df_base[df_base['Tensao (V)'] <= 0]
    plt.errorbar( # pontos do gráfico
        x = escopo_geral.iloc[:,0],
        y = escopo_geral.iloc[:,2],
        xerr = escopo_geral.iloc[:,1],
        yerr = escopo_geral.iloc[:,3],
        fmt = 'o', # formato dos pontos, previne linhas ligando-os
        ecolor = 'black', # cor das barras de erro
        elinewidth = 1.3, # espessura das barras de erro
        capsize = 0, # espessura das marcações nas extremidades das barras de erro
        color = 'black', # cor dos pontos
        markersize = 0.5 # tamanho dos pontos
    )
    titulo = 'Mét 2 - ' + arquivo.replace('_', ' ').replace('.csv', '')
    plt.title(titulo, fontsize=30)
    plt.xlabel('Tensão (V)', fontsize=23)
    plt.ylabel('Corrente (A)', fontsize=23)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    #plt.subplots_adjust(bottom=0.2, right=0.98, left=0.2, top=0.90)
    plt.tight_layout(pad=0.1)
    plt.grid()
    nome_a_salvar = 'Metodos/Metodo 2/Curvas com ajuste/' + arquivo.replace('csv', 'svg')
    plt.savefig(nome_a_salvar, format='svg')
    plt.close()



# salvando a planilha resultante do loop
df_todas_metodo_2.to_csv('Metodos/Metodo 2/todas.csv', index=False)

# cálculo da média de cada LED com incerteza = desvpad:
leds = list(set(df_todas_metodo_2['LED']))
df_medias_metodo_2 = pd.DataFrame(columns=['LED', 'V0 M2', 'Erro V0 M2'])
for led in leds:
    df = df_todas_metodo_2[df_todas_metodo_2['LED'] == led]
    media = df['V0 M2'].mean()
    desvpad = df['V0 M2'].std()
    linha_resultado = pd.DataFrame({'LED': [led], 'V0 M2': [media], 'Erro V0 M2': [desvpad]})
    df_medias_metodo_2 = pd.concat([df_medias_metodo_2, linha_resultado])

# salvando
df_medias_metodo_2.to_csv('Metodos/Metodo 2/medias.csv', index=False)

# ok




## 3.3) Método 3: método gráfico

# necessário 1º plotar os gráficos de cada LED, com todas as suas intensidades

def plotar_metodo_3(led, modo, expoente, intervalo_x = [-5,5], intervalo_y = [-1,1]):
    arquivos_a_calcular_V0_metodo_3 = [arq for arq in os.listdir('Medias de cada intensidade') if led in arq]
    for arquivo in arquivos_a_calcular_V0_metodo_3:
        df_intensidade = pd.read_csv('Medias de cada intensidade/' + arquivo)
        df_intensidade = df_intensidade[df_intensidade['Tensao (V)'] <= intervalo_x[1]]
        df_intensidade = df_intensidade[df_intensidade['Tensao (V)'] >= intervalo_x[0]]
        df_intensidade['Corrente media (A)'] = df_intensidade['Corrente media (A)'] * 10**(-expoente)
        intensidade = int(arquivo.split('_')[1].split('.')[0].replace('%',''))
        if intensidade == 100:
            cor = 'b'
        elif intensidade == 80:
            cor = 'r'
        elif intensidade == 60:
            cor = 'g'
        elif intensidade == 40:
            cor = 'c'
        elif intensidade == 20:
            cor = 'm'
        plt.errorbar( # pontos do gráfico
            x = df_intensidade.iloc[:,0],
            y = df_intensidade.iloc[:,2],
            xerr = df_intensidade.iloc[:,1],
            yerr = df_intensidade.iloc[:,3],
            fmt = 'o', # formato dos pontos, previne linhas ligando-os
            ecolor = cor, # cor das barras de erro
            elinewidth = 0.8, # espessura das barras de erro
            capsize = 0, # espessura das marcações nas extremidades das barras de erro
            color = cor, # cor dos pontos
            markersize = 3.5 # tamanho dos pontos
        )
        plt.plot(
            df_intensidade.iloc[:,0],
            df_intensidade.iloc[:,2],
            color = cor,
            label = '$I=$' + str(intensidade) + '%'
        )
    titulo = 'Mét 3 - ' + arquivo.split('_')[0]
    plt.title(titulo, fontsize=30)
    plt.legend(fontsize=15)
    plt.xlabel('Tensão (V)', fontsize=23)
    potencia = str(expoente)
    plt.ylabel('Corrente ($10^{' + potencia + '}$ A)', fontsize=23)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.ylim(intervalo_y[0], intervalo_y[1])
    plt.xlim(intervalo_x[0], intervalo_x[1])
    #plt.subplots_adjust(bottom=0.2, right=0.98, left=0.2, top=0.90)
    plt.tight_layout(pad=0.1)
    plt.grid()
    # linhas marcadas nos eixos:
    plt.axhline(0, color='black', linewidth=1) 
    plt.axvline(0, color='black', linewidth=1)

    if modo == 's':
        plt.show()
    elif modo =='c':
        nome_a_salvar = 'Metodos/Metodo 3/Plots/' + arquivo.split('_')[0] + '.svg'
        plt.savefig(nome_a_salvar, format='svg')
        plt.close()

plotar_metodo_3('Azul', 's', -3, [-1.25,-0.9], [-1,1])
plotar_metodo_3('Azul', 'c', -3, [-1.25,-0.9], [-1,1])
plotar_metodo_3('Vermelho', 's', -4, [-1.,-0.1], [-1,1])
plotar_metodo_3('Vermelho', 'c', -4, [-1.,-0.1], [-1,1])
plotar_metodo_3('Amarelo', 's', -4, [-0.7,-0.4], [-1,2])
plotar_metodo_3('Amarelo', 'c', -4, [-0.7,-0.4], [-1,2])
plotar_metodo_3('Violeta', 's', -4, [-1.9,-1.6], [-1,2])
plotar_metodo_3('Violeta', 'c', -4, [-1.9,-1.6], [-1,2])
plotar_metodo_3('Verde', 's', -3, [-1.35,-0.8], [-0.5,1])
plotar_metodo_3('Verde', 'c', -3, [-1.35,-0.8], [-0.5,1])

# consolidando e salvando tabela de medidas (vou chamar de medias só para unificar)
df_medias_metodo_3 = pd.DataFrame({
    'LED': ['Azul', 'Vermelho', 'Amarelo', 'Violeta', 'Verde'],
    'V0 M3': [-1.0698, -0.45, -0.55, -1.725, -1.125],
    'Erro V0 M3': [0.025, 0.05, 0.05, 0.075, 0.025]
})
df_medias_metodo_3.to_csv('Metodos/Metodo 3/medias.csv', index=False)

# ok



## 3.4) Consolidando tudo em 1 planilha
df_medias_todos_metodos = pd.merge(df_medias_metodo_1, df_medias_metodo_2, how='inner', on='LED')
df_medias_todos_metodos = pd.merge(df_medias_todos_metodos, df_medias_metodo_3, how='inner', on='LED')
df_medias_todos_metodos.to_csv('Metodos/todos os metodos.csv', index=False)






# 4) Determinação das frequencias

## 4.1) Plots de gaussianas superpostas (NÃO É AJUSTE)
# tentando encaixar essa gaussiana, foi possível ver que o ajuste era extremamente
# sensível aos chutes iniciais e que os resultados eram ruins, com chi^2 gigantesco
# visualmente, ficava claro que a gaussiana não descreve exatamente bem a forma da curva,
# que se parece mais com uma gaussiana assimétrica ou Poisson

# Vamos deixar isso claro usando gaussianas superpostas:
# (i.e., não ajustadas, ou seja, com parametros arbitrários definidos visualmente)
def plot_gaussiana_superposta(led, parametros, modo, intervalo=[4,9]):
    # dados é o dataframe de frequencia
    # parametros são os parametros da gaussiana
    # modo é uma string dentre duas opções: 's' mostra e 'c' salva em arquivo

    # definição da gaussiana
    def g(B, x):
        return B[0] * np.exp( - (x-B[1])**2 / (2*B[2]**2) ) + B[3]
    
    # range do eixo x
    escopo = np.arange(intervalo[0], intervalo[1], 0.001)

    # importação dos dados
    dados = pd.read_csv('Frequencias/espectro_LED_' + led + '.dat', dtype={'Frequência (Hz)': float})
    dados['Frequência (Hz)'] = dados['Frequência (Hz)'] * 10**-14
    dados['Intensidade (contagens)'] = dados['Intensidade (contagens)'] * 10**-3

    # atribuição de cor
    if led == 'Amarelo':
        cor = 'gold'  
    elif led == 'Azul':
        cor = 'royalblue'
    elif led == 'Verde':
        cor = 'mediumseagreen'
    elif led == 'Violeta':
        cor = 'darkviolet'
    elif led == 'Vermelho':
        cor = 'crimson'
    
    # plot
    plt.plot(
        escopo,
        g(parametros, escopo), # AQUI TERIA DE REINTRODUZIR OS PARAMETROS DE AJUSTE ajuste.beta
        color = cor,
        linewidth=2.8
    )
    plt.scatter(
        dados.iloc[:,0],
        dados.iloc[:,1],
        color = 'black', # cor dos pontos
        s = 10 # tamanho dos pontos
    )
    plt.title(led, fontsize=30)
    plt.ylabel('Nº fótons (mil)', fontsize=23)
    plt.xlabel('$\\nu$ ($\\times 10^{14}$ Hz)', fontsize=23)
    plt.xticks(fontsize=20)
    plt.xlim(intervalo[0], intervalo[1])
    plt.yticks(fontsize=20)
    plt.tight_layout(pad=0.1)
    if modo == 's':
        # mostrar
        plt.show()
    elif modo == 'c':
        # salvar
        plt.savefig('Frequencias/Plots gaussianas superpostas/' + led + '.svg', format='svg')
        plt.close()

# plotando e salvando
plot_gaussiana_superposta('Amarelo', [74.5, 5.04, 0.05, 0], 's', [4.9,5.2])
plot_gaussiana_superposta('Amarelo', [74.5, 5.04, 0.05, 0], 'c', [4.9,5.2])
plot_gaussiana_superposta('Azul', [127, 6.425, 0.13, 0], 's', [6,6.8])
plot_gaussiana_superposta('Azul', [127, 6.425, 0.13, 0], 'c', [6,6.8])
plot_gaussiana_superposta('Verde', [44.7, 5.78, 0.13, 0], 's', [5.1,6.3])
plot_gaussiana_superposta('Verde', [44.7, 5.78, 0.13, 0], 'c', [5.1,6.3])
plot_gaussiana_superposta('Vermelho', [140, 4.76, 0.05, 0], 's', [4.5,5.1])
plot_gaussiana_superposta('Vermelho', [140, 4.76, 0.05, 0], 'c', [4.5,5.1])
plot_gaussiana_superposta('Violeta', [260, 7.52, 0.17, 0], 's', [6.7,8])
plot_gaussiana_superposta('Violeta', [260, 7.52, 0.17, 0], 'c', [6.7,8])



## 4.2)
# em vista dessa dificuldade, podemos tentar encaixar Poisson ou gaussiana assimétrica
# problema é que vai demorar mais, e para a síntese não é estritamente necessário
# perguntei para o monitor e ele disse que é ok usar apenas média ponderada e desvio padrão
# então vamos fazer isso

# funções para importar dados e calcular média ponderada e desv pad
def media_ponderada_frequencias(led):
    # retorna tupla: media e desv pad ponderados

    # importação
    dados = pd.read_csv('Frequencias/espectro_LED_' + led + '.dat', dtype={'Frequência (Hz)': float})
    x = dados['Frequência (Hz)']
    y = dados['Intensidade (contagens)']

    # media ponderada
    resultado1 = np.average(x, weights=y)

    # desvio padrao ponderado
    soma_quadrados_desvios_ponderada = ((x - resultado1) ** 2 * y).sum()
    variancia_ponderada = soma_quadrados_desvios_ponderada / y.sum()
    resultado2 = variancia_ponderada ** 0.5


    return resultado1, resultado2

# calculando
md_Vm, dp_Vm = media_ponderada_frequencias('Vermelho')
md_Am, dp_Am = media_ponderada_frequencias('Amarelo')
md_Vd, dp_Vd = media_ponderada_frequencias('Verde')
md_Az, dp_Az = media_ponderada_frequencias('Azul')
md_Vl, dp_Vl = media_ponderada_frequencias('Violeta')

# consolidando e salvando
df_medias_frequencias = pd.DataFrame({
    'LED': ['Vermelho', 'Amarelo', 'Verde', 'Azul', 'Violeta'],
    'Media ponderada (Hz)': [md_Vm, md_Am, md_Vd, md_Az, md_Vl],
    'Desvio padrao (Hz)': [dp_Vm, dp_Am, dp_Vd, dp_Az, dp_Vl]
})

df_medias_frequencias.to_csv('Frequencias/medias ponderadas.csv', index=False)






# 5) Ajustes da constante de Planck

## 5.1) carga do eletron dada no slide
e = -1.6021766208 * 10**19



## 5.2) consolidando todos os dados em um dataframe:

# importando
V_0s = pd.read_csv('Metodos/todos os metodos.csv')
frequencias = pd.read_csv('Frequencias/medias ponderadas.csv')

# ponderando frequencia por 10^-14
frequencias.iloc[:,1:] = frequencias.iloc[:,1:] * 10**-14

# # ponderando voltagem pela carga do eletron e por 10^-19
eV_0s = V_0s
eV_0s.iloc[:,1:] = eV_0s.iloc[:,1:] * e * 10**-19

# consolidando
dados_para_ajuste = pd.merge(frequencias, eV_0s, 'inner', 'LED')



## 5.3) função geral de ajuste:
def f(B, x):
    return B[0]*x + B[1]
linear = odr.Model(f)



## 5.4) ajuste metodo 1:

# ajuste
dados_mt_1 = odr.RealData(dados_para_ajuste['Media ponderada (Hz)'], dados_para_ajuste['V0 M1'], dados_para_ajuste['Desvio padrao (Hz)'], dados_para_ajuste['Erro V0 M1'])
obj_odr = odr.ODR(dados_mt_1, linear, beta0=[1,10])
out_mt1 = obj_odr.run()

# visualizando resultados
out_mt1.pprint()
print([np.sqrt(out_mt1.cov_beta[0,0]), np.sqrt(out_mt1.cov_beta[1,1])])

# função de plot
def plot_ajuste_Planck(output, metodo, modo): # output é um obj output do modelo odr
    fim = dados_para_ajuste['Media ponderada (Hz)'].max()*1.1
    escopo = np.arange(0, fim, 0.001)
    plt.plot(
        escopo,
        f([output.beta[0], output.beta[1]], escopo), # AQUI TERIA DE REINTRODUZIR OS PARAMETROS DE AJUSTE ajuste.beta
        color = 'red',
        linewidth=2.8
    )
    coluna_y = 'V0 M' + str(metodo)
    coluna_yerr = 'Erro V0 M' + str(metodo)
    plt.errorbar(
        x = dados_para_ajuste['Media ponderada (Hz)'],
        y = dados_para_ajuste[coluna_y],
        xerr = dados_para_ajuste['Desvio padrao (Hz)'],
        yerr = dados_para_ajuste[coluna_yerr].abs(),
        fmt = 'o', # formato dos pontos, previne linhas ligando-os
        ecolor = 'black', # cor das barras de erro
        elinewidth = 1.3, # espessura das barras de erro
        capsize = 0, # espessura das marcações nas extremidades das barras de erro
        color = 'black', # cor dos pontos
        markersize = 5 # tamanho dos pontos
    )
    plt.title('Ajuste - Método ' + str(metodo), fontsize=30)
    plt.ylabel('$eV_0$ ($10^{19}$ J)', fontsize=23)
    plt.xlabel('$\\nu$ ($\\times 10^{14}$ Hz)', fontsize=23)
    plt.xticks(fontsize=20)
    plt.xlim(0, fim)
    plt.yticks(fontsize=20)
    plt.tight_layout(pad=0.1)
    plt.grid()
    plt.axhline(0, color='black', linewidth=1) 
    plt.axvline(0, color='black', linewidth=1)
    if modo == 's':
        # mostrar
        plt.show()
    elif modo == 'c':
        # salvar
        plt.savefig('Ajuste Planck/Para sintese (3 metodos)/metodo ' + str(metodo) + '.svg', format='svg')
        plt.close()

# visualizando e salvando
plot_ajuste_Planck(out_mt1, 1, 's')
plot_ajuste_Planck(out_mt1, 1, 'c')



## 5.5) ajuste metodo 2:

# ajuste
dados_mt_2 = odr.RealData(dados_para_ajuste['Media ponderada (Hz)'], dados_para_ajuste['V0 M2'], dados_para_ajuste['Desvio padrao (Hz)'], dados_para_ajuste['Erro V0 M2'])
obj_odr = odr.ODR(dados_mt_2, linear, beta0=[1,10])
out_mt2 = obj_odr.run()

# visualizando resultados
out_mt2.pprint()
print([np.sqrt(out_mt2.cov_beta[0,0]), np.sqrt(out_mt2.cov_beta[1,1])])

# plot
plot_ajuste_Planck(out_mt2, 2, 's')
plot_ajuste_Planck(out_mt2, 2, 'c')



## 5.6) ajuste metodo 3:

# ajuste
dados_mt_3 = odr.RealData(dados_para_ajuste['Media ponderada (Hz)'], dados_para_ajuste['V0 M3'], dados_para_ajuste['Desvio padrao (Hz)'], dados_para_ajuste['Erro V0 M3'])
obj_odr = odr.ODR(dados_mt_3, linear, beta0=[1,10])
out_mt3 = obj_odr.run()

# visualizando resultados
out_mt3.pprint()
print([np.sqrt(out_mt3.cov_beta[0,0]), np.sqrt(out_mt3.cov_beta[1,1])])

# plot
plot_ajuste_Planck(out_mt3, 3, 's')
plot_ajuste_Planck(out_mt3, 3, 'c')



## 5.7) consolidando em uma planilha e salvando:

# obtendo as constantes de Planck estimadas e as funções trabalho
h1 = out_mt1.beta[0] * 10 # multiplicando por 10 obtemos 10^-15
err_h1 = np.sqrt(out_mt1.cov_beta[0,0]) * 10
phi1 = -out_mt1.beta[1]/e
err_phi1 = -np.sqrt(out_mt1.cov_beta[1,1])/e
h2 = out_mt2.beta[0] * 10
err_h2 = np.sqrt(out_mt2.cov_beta[0,0]) * 10
phi2 = -out_mt2.beta[1]/e
err_phi2 = -np.sqrt(out_mt2.cov_beta[1,1])/e
h3 = out_mt3.beta[0] * 10
err_h3 = np.sqrt(out_mt3.cov_beta[0,0]) * 10
phi3 = -out_mt3.beta[1]/e
err_phi3 = -np.sqrt(out_mt3.cov_beta[1,1])/e

# consolidando e salvando
ajuste_Planck_consolidado = pd.DataFrame({
    'Parâmetro': ['h (10^-15 eVJ)', 'phi (10^-19 V)'],
    'Método 1': ['9(2)' , '-2.2(7)'],
    'Método 2': ['11(3)' , '-3(1)'],
    'Método 3': ['8(2)' , '-2.1(7)']
})

ajuste_Planck_consolidado.to_csv('Ajuste Planck/Para sintese (3 metodos)/resultados do ajuste.csv', index=False)



# ajuste:
# equação: eV0 = hf - ePhi
# ajuste: y = ax + b
# h = a
# Phi = -b/e









