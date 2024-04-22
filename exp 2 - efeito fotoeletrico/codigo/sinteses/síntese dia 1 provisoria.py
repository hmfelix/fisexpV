

# A síntese é exigida como apresentação inicial dos resultados à turma.
# para comentários e correções. Não necessita de escrita de relatório.

# Assim, o código abaixo é voltado a produzir esta análise inicial.




# gráficos a serem feitos:

# curva I x V - ok nao precisa manipular nenhum dado - gráfico de linha
# pera, precisa fazer de todos? meu deus são muitos, talvez nao seja isso

# desta curva, obter V_0 - é a média?

# obter incerteza do ruído

# encaixar gaussiana nos leds (2 gauss)

# métodos para obter V_0

"""
 Tá acho que entendi o q deve ser feito:

 . tirar a média da corrente pela voltagem para cada intensidade de cada laser
 . obter V_0, fechando um V_0 para cada laser para cada um dos 3 métodos
    - interpolação linear + média das intensidades
    - ajuste de 2 curvas p/ cada intensidade + interseção + média das intensidades
    - ponto de encontro das curvas interpoladas
 . fazer a gaussiana das frequencias, obtendo a frequencia de cada laser
 . plotar V_0 x f, só que com as manipulações que o slide indica
 . teste Z Planck
 . compilar valores
"""

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

# OLHA QUE LINDO ESSE TIPO DE LOOP CHAMADO COMPRESSÃO DE LISTA (LIST COMPRESSION)
arqs_Ruido = os.listdir('Ruido') 
caminhos.extend(['Ruido/' + elemento for elemento in arqs_Ruido])
# e lindo também esse método extend, que evita que a lista comprimida seja adicionada à lista original
# (sendo adicionados os seus elementos, elemento-a-elemento!)

# mesma coisa agora com os arquivos de Vermelho e Violeta:
arqs_Verm = os.listdir('Vermelho') 
caminhos.extend(['Vermelho/' + elemento for elemento in arqs_Verm])
arqs_Viol = os.listdir('Violeta') 
caminhos.extend(['Violeta/' + elemento for elemento in arqs_Viol])



## 1.3) aplicando as funções de substituição CSV:

for caminho in caminhos:
    substituir_csv(caminho)



## 1.4) obtendo caminho dos arquivos DAT:
caminhos_DAT = ['Frequencias/espectro_LED_Vm.dat', 'Frequencias/espectro_LED-Viol.dat']



## 1.5) aplicando as funções de substituição DAT:

for caminho in caminhos_DAT:
    substituir_dat(caminho)

# ok







# 2) Importação e tratamento dos dados de medidas

## 2.1) importando todos os dataframes de medidas em listas:

lista_dfs = []

for caminho in caminhos:
    lista_dfs.append(pd.read_csv(caminho, dtype={'Corrente [A]': float}))
# ESSE ÚLTIMO ARGUMENTO MARAVILHOSO PERMITE ENTENDER TEXTOS DO TIPO 1.2E-05
# COMO FLOATS EM POTÊNCIAS DE 10!!



## 2.2) apenas checando se deu certo:

def print_full(x):
    pd.set_option('display.max_rows', len(x))
    print(x)
    pd.reset_option('display.max_rows')

print_full(lista_dfs[0])
# ok



## 2.3) obtendo indices para pegar os caminhos separados por LED:

indices_Ruido = ['Ruido' in elemento for elemento in caminhos] # de novo usei list compression aqui
indices_Ruido = [i for i, valor in enumerate(indices_Ruido) if valor] # aqui tb
"""
Obs.: a linha acima é equivalente à função 'which' em R.
      o que ela significa é: i,valor é uma tupla
      enumerate retorna uma sequencia de tuplas
      nesse contexto, a palavra sequencia significa qualquer tipo de objeto iteravel
      e iteravel significa qualquer objeto passivel de figurar em um loop for
      exemplos de iteraveis: listas, tuplas, strings e intervalos (range) 
      se dermos print em enumerate(indices_Ruido) apenas seremos informados do 
      seu tipo e seu endereço de memoria
      para ver os elementos de um iteravel, usar list(interavel)
      nesse caso, list(enumerate(indices_Ruido))
      teremos algo do tipo: [(0,True), (1,True), ..., (5,False)...]
      por isso o loop pede para me retornar i (1º elemento da tupla) caso valor (2º elemento)
      seja verdadeiro
      TUDO ISSO EU TENHO QUE FAZER PORQUE PYTHON NÃO ACEITA INDEXAÇÃO LÓGICA COMO R
      existe outro jeito de fazer isso usando a função where de numpy,
      que é igual which mas nesse caso me retorna um array de 2 dimensoes (2ª dim é o tipo os elementos)
      aí eu reconverto para lista usando o método tolist de numpy sobre a 1ª dimensão
      é o que faço abaixo:
"""
indices_Verm = ['Vermelho' in elemento for elemento in caminhos]
indices_Verm = np.where(indices_Verm)[0].tolist()
indices_Viol = ['Violeta' in elemento for elemento in caminhos]
indices_Viol = np.where(indices_Viol)[0].tolist()
# ok



## 2.4) separando as dfs de cada LED e os indices de cada intensidade:

# dfs de cada LED:
dfs_Verm = lista_dfs[indices_Verm[0]:indices_Verm[-1]+1]
dfs_Viol = lista_dfs[indices_Viol[0]:indices_Viol[-1]+1]
dfs_Ruido = lista_dfs[indices_Ruido[0]:indices_Ruido[-1]+1]
# OBS.: NOVAMENTE NÃO FUNCIONA USAR O MESMO MÉTODO DE R PARA INDEXAR UMA LISTA
#       USANDO UMA SEQUÊNCIA ARBITRÁRIA DE INTEIROS
#       teria que usar list compression
#       tipo assim: [caminhos[i] for i in indices]

# indices de cada intensidade:
# por inspeção visual, notei que sao 10 tabelas por intensidade, na seguinte ordem:
# 100%, 20%, 40%, 60%, 80%
# ou seja:
# I1 = [0,10]
# I2 = [10,20]
# I3 = [20,30]
# I4 = [30,40]
# I5 = [40,50]



## 2.5) gerando 1 dataframe por intensidade e LED

def gerar_df_Imédio(indice0, indice1, cor):
    # indices permitem escolher a intensidade
    if cor == 'Vermelho':
        dfs_base = dfs_Verm
    elif cor == 'Violeta':
        dfs_base = dfs_Viol
    elif cor == 'Ruido':
        dfs_base = dfs_Ruido
    df_compilada = dfs_base[indice0]
    for df in dfs_base[indice0+1:indice1]:
        df_compilada = pd.concat([df_compilada, df['Corrente [A]']], axis=1)
    media_por_linha = df_compilada.iloc[:, 1:].mean(axis=1)
    desvio_padrao_por_linha = df_compilada.iloc[:, 1:].std(axis=1)
    resultado = pd.DataFrame({
        'Tensao (V)': df_compilada.iloc[:,0],
        'Corrente media (A)': media_por_linha,
        'Desvio padrao (A)': desvio_padrao_por_linha
    })
    return resultado

# LED vermelho, intensidade 100%:
df_VermI1 = gerar_df_Imédio(0,10,'Vermelho')
# LED vermelho, intensidade 20%:
df_VermI2 = gerar_df_Imédio(10,20,'Vermelho')
# LED vermelho, intensidade 40%:
df_VermI3 = gerar_df_Imédio(20,30,'Vermelho')
# LED vermelho, intensidade 60%:
df_VermI4 = gerar_df_Imédio(30,40,'Vermelho')
# LED vermelho, intensidade 80%:
df_VermI5 = gerar_df_Imédio(40,50,'Vermelho')

# LED violeta, intensidade 100%:
df_ViolI1 = gerar_df_Imédio(0,10,'Violeta')
# LED violeta, intensidade 20%:
df_ViolI2 = gerar_df_Imédio(10,20,'Violeta')
# LED violeta, intensidade 40%:
df_ViolI3 = gerar_df_Imédio(20,30,'Violeta')
# LED violeta, intensidade 60%:
df_ViolI4 = gerar_df_Imédio(30,40,'Violeta')
# LED violeta, intensidade 80%:
df_ViolI5 = gerar_df_Imédio(40,50,'Violeta')

# Ruidos:
df_RuidoMedio = gerar_df_Imédio(0,5,'Ruido')

## 2.6) salvando os resultados:

df_VermI1.to_csv('Medias de cada intensidade/Vermelho_100%.csv', index=False)
df_VermI2.to_csv('Medias de cada intensidade/Vermelho_20%.csv', index=False)
df_VermI3.to_csv('Medias de cada intensidade/Vermelho_40%.csv', index=False)
df_VermI4.to_csv('Medias de cada intensidade/Vermelho_60%.csv', index=False)
df_VermI5.to_csv('Medias de cada intensidade/Vermelho_80%.csv', index=False)
df_ViolI1.to_csv('Medias de cada intensidade/Violeta_100%.csv', index=False)
df_ViolI2.to_csv('Medias de cada intensidade/Violeta_20%.csv', index=False)
df_ViolI3.to_csv('Medias de cada intensidade/Violeta_40%.csv', index=False)
df_ViolI4.to_csv('Medias de cada intensidade/Violeta_60%.csv', index=False)
df_ViolI5.to_csv('Medias de cada intensidade/Violeta_80%.csv', index=False)
df_RuidoMedio.to_csv('Medias de cada intensidade/Ruido.csv', index=False)



## 2.7) construindo dados de média das médias
# Trata-se de tirar, para cada LED, a média das médias das intensidades,
# resultando em 1 única curva por LED
# OBS: tem duas formas de calcular a incerteza aqui:
#       - desvio padrão simples
#       - desvio padrão da média
# slide manda usar desvio padrão simples, então é isso que eu vou fazer

# primeiro adaptando a função acima para ser geral:
def gerar_df_media_das_medias(cor):
    # indices permitem escolher a intensidade
    if cor == 'Vermelho':
        dfs_base = [df_VermI1, df_VermI2, df_VermI3, df_VermI4, df_VermI5]
    elif cor == 'Violeta':
        dfs_base = [df_ViolI1, df_ViolI2, df_ViolI3, df_ViolI4, df_ViolI5]
    df_compilada = dfs_base[0].drop('Desvio padrao (A)', axis=1)
    for df in dfs_base[1:]:
        df_compilada = pd.concat([df_compilada, df['Corrente media (A)']], axis=1)
    media_por_linha = df_compilada.iloc[:, 1:].mean(axis=1)
    desvio_padrao_por_linha = df_compilada.iloc[:, 1:].std(axis=1)
    resultado = pd.DataFrame({
        'Tensao (V)': df_compilada.iloc[:,0],
        'Corrente media das medias (A)': media_por_linha,
        'Desvio padrao (A)': desvio_padrao_por_linha
    })
    return resultado

# (a) Vermelho:
df_Verm_media_das_medias = gerar_df_media_das_medias('Vermelho')
df_Verm_media_das_medias.to_csv('Medias das medias/Vermelho.csv', index=False)

# (b) Violeta: 
df_Viol_media_das_medias = gerar_df_media_das_medias('Violeta')
df_Viol_media_das_medias.to_csv('Medias das medias/Violeta.csv', index=False)



## 2.8) Outra perspectiva sobre o erro das médias: ruido
# Ainda não sabemos se devemos usar o ruido como erro
# Vamos tirar dúvida na aula
# De qualquer forma já antecipamos o trabalho desses dados:
caminhos = os.listdir('Medias de cada intensidade')
lista_dfs = []
for caminho in caminhos:
    lista_dfs.append(pd.read_csv('Medias de cada intensidade/'+caminho, dtype={'Corrente media (A)': float}))
ruidos = lista_dfs[0]['Corrente media (A)']    
for df in lista_dfs[1:]:
    df.iloc[:,2] = ruidos
for i in range(1,len(lista_dfs)):
    df = lista_dfs[i]
    df.to_csv('Medias de cada intensidade (ruidos como erro)/'+caminhos[i], index=False)







# 3) Obtenção das frequencias com ajuste gaussiano

## 3.1) importando os dados:
df_LED_Verm = pd.read_csv('Frequencias/espectro_LED_Vm.dat', dtype={'Frequência (Hz)':float})
df_LED_Viol = pd.read_csv('Frequencias/espectro_LED-Viol.dat', dtype={'Frequência (Hz)':float})



## 3.2) transformando para escalas melhores:
# frequencia será em 10^14
# contagem será em milhares
df_LED_Verm.iloc[:,0] = df_LED_Verm.iloc[:,0]/10**14
df_LED_Verm.iloc[:,1] = df_LED_Verm.iloc[:,1]/1000
df_LED_Viol.iloc[:,0] = df_LED_Viol.iloc[:,0]/10**14
df_LED_Viol.iloc[:,1] = df_LED_Viol.iloc[:,1]/1000



## 3.3) função geral de ajuste gaussiano (sem erro em nenhuma das variáveis!)

def ajustar_gaussiana(dados, chutes):
    # Parâmetros:
    # dados deve ser um dataframe com x na coluna 0 e y na coluna 1
    # chutes é uma lista com 4 chutes, na seguinte ordem: amplitude, média, desvpad, constante

    # definição do modelo:
    def g(B, x):
        # B eh o vetor de parametros
        # x eh uma array no formato dado na documentacao do pacote
        return B[0] * np.exp( - (x-B[1])**2 / (2*B[2]**2) ) + B[3] # no caso, um modelo gaussiano
        # onde:
        # B[0] é a amplitude
        # B[1] é o valor esperado (que temos interesse)
        # B[2] é o desvio padrão (que tb temos interesse)
        # B[3] é alguma constante de reajuste de altura (pode ser de interesse ou não)

    # rodando o modelo:
    # criando o objeto de classe modelo
    gauss = odr.Model(g)
    # criando o objeto de classe dados
    dados_odr = odr.RealData(dados.iloc[:,0], dados.iloc[:,1])
    # criando o objeto de classe odr 
    # (aqui precisa ter estimativa de parametros iniciais)
    obj_odr = odr.ODR(dados_odr, gauss, beta0=chutes)
    # criando o objeto output
    g_output = obj_odr.run()
    
    return g_output







## 3.4) função geral de plot das gaussianas (de novo: sem incerteza em nenhum dos eixos!!):

def plot_ajuste_gaussiano(dados, ajuste, titulo, modo, caminho='gauss.svg'):
    # dados é o mesmo dataframe passado para a função do ajuste
    # ajuste é o modelo retornado pela função de ajuste
    # modo é uma string dentre duas opções:
    #   . 's' chama plt.show()
    #   . 'c' chama plt.savefig() no caminho especificado, formato svg, depois fecha com plt.close()
    # caminho deve ser fornecido se o modo for 'c': uma string com o caminho e nome de arquivo

    # definição da função gaussiana a ser plotada
    # PROVISORIAMENTE ESTOU USANDO UMA GAUSSIANA ARBITRÁRIA
    def g(B, x):
        return B[0] * np.exp( - (x-B[1])**2 / (2*B[2]**2) ) + B[3]
    escopo = np.arange(dados.iloc[:,0].min(), dados.iloc[:,0].max()*1.005,0.001)
    # plot
    plt.plot(
        escopo,
        g(ajuste, escopo), # AQUI TERIA DE REINTRODUZIR OS PARAMETROS DE AJUSTE ajuste.beta
        color = 'violet',
        linewidth=2.8
    )
    plt.scatter(
        dados.iloc[:,0],
        dados.iloc[:,1],
        #xerr=df_Gaussiana1_NaCl['Erro_X'],
        #yerr=df_Gaussiana1_NaCl['Erro_Y'],
        #fmt = 'o', # formato dos pontos, previne linhas ligando-os
        #ecolor = 'black', # cor das barras de erro
        #elinewidth = 1.3, # espessura das barras de erro
        #capsize = 0, # espessura das marcações nas extremidades das barras de erro
        color = 'black', # cor dos pontos
        s = 10 # tamanho dos pontos
    )
    plt.title(titulo, fontsize=30)
    plt.ylabel('Nº fótons (mil)', fontsize=23)
    plt.xlabel('$\\nu$ ($\\times 10^{14}$ Hz)', fontsize=23)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.subplots_adjust(bottom=0.2, right=0.98, left=0.2, top=0.90)
    if modo == 's':
        # mostrar
        plt.show()
    elif modo == 'c':
        # salvar
        plt.savefig(caminho, format='svg')
        plt.close()



# está muito difícil encaixar esse ajuste
# extremamente sensível aos parâmetros iniciais
# vou tentar fazer duas coisas:
#   . limitar a uma região de interesse (visualmente)
#   . pegar apenas uma pequena amostra de pontos nessa região
# escolhendo apenas a região de interesse e amostra
df_LED_Verm_regiao_de_interesse = df_LED_Verm.iloc[3262:4113,:]
ajuste_gauss_Verm = ajustar_gaussiana(df_LED_Verm_regiao_de_interesse, [144, 4.82, 0.05, 0.01])
ajuste_gauss_Verm.pprint()
plot_ajuste_gaussiano(df_LED_Verm_regiao_de_interesse, [143, 4.755, 0.05, 0.02], 'Gaussiana - $f$ vermelho', 's')
# parametros usados na gaussiana não-ajustada:
# 143 4.755 0.05 0.02


# vamos tentar no atus:
df_LED_Verm_regiao_de_interesse.to_csv('amostra.csv', index=False)


# estudando agora o violeta:
plt.scatter(df_LED_Viol.iloc[:,0], df_LED_Viol.iloc[:,1])
plt.show()

df_LED_Viol_regiao_de_interesse = df_LED_Viol.iloc[67:156,:]
plot_ajuste_gaussiano(df_LED_Viol_regiao_de_interesse, [264,7.52,0.2,0.2], 'Gaussiana - $f$ violeta', 's')








print([np.sqrt(ajuste_gauss_Verm.cov_beta[1,1]), np.sqrt(ajuste_gauss_Verm.cov_beta[2,2])]) # desvio padrao sem escalar nada

# calculando o valor esperado do ângulo:
myoutput7.beta[1]
# 6.4462503295093905 °
# erro:
np.sqrt(myoutput7.cov_beta[1,1])
# 0.004433088496537881 °
# desvio padrão da gaussiana:
myoutput7.beta[2]
# -0.17345862669026632 °







# 4) Análise dos dados de medidas para obtenção da voltagem V_0

## 4.1) Método 1:
# Média das médias das intensidades, resultando em 1 única curva por LED
# Interpolação linear e escolha do valor em 0


