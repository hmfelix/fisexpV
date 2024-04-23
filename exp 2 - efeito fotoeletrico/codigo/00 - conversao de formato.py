
# SETUP

import os



# DEFINICAO DE FUNCOES

def substituir_virgulas(texto):
    return texto.replace(',', '.')

def substituir_ponto_e_virgula(texto):
    return texto.replace(';', ',')

def substituir_tab(texto):
    return texto.replace('	', ',')

def substituir_csv(arquivo, novo_arquivo):
    # cria a pasta se não existir
    nova_pasta = os.path.dirname(novo_arquivo)
    if not os.path.exists(nova_pasta):
        os.makedirs(nova_pasta)
    # abre o arquivo e substitui as vírgulas
    with open(arquivo, 'r', encoding='utf-8') as csv:
        corpus = csv.read()
    novo_corpus = substituir_virgulas(corpus)
    novo_corpus = substituir_ponto_e_virgula(novo_corpus)
    # salva novo arquivo em outra pasta
    with open(novo_arquivo, 'w', encoding='utf-8') as novo_csv:
        novo_csv.write(novo_corpus)

def substituir_dat(arquivo, novo_arquivo):
    with open(arquivo, 'r') as dat:
        corpus = dat.read()
    novo_corpus = substituir_virgulas(corpus)
    novo_corpus = substituir_tab(novo_corpus)
    with open(novo_arquivo, 'w') as novo_dat:
        novo_dat.write(novo_corpus)

def substituir_cabecalho(arquivo): # apenas para os arquivos dat
    with open(arquivo, 'r') as dat:
        linhas = dat.readlines()
    del linhas[:2]
    linhas.insert(0, 'Frequencia (Hz),Intensidade (contagem)\n')
    with open(arquivo, 'w') as dat:
        dat.writelines(linhas)



# CAMINHO DOS ARQUIVOS CSV

# pastas
diretorios_csv_leitura = ['dados coletados/formato original/' + elemento for elemento in os.listdir('dados coletados/formato original')]

# listas a serem estocados os caminhos
caminhos_csv_leitura = []
caminhos_csv_escrita = []

# obtendo os caminhos
for diretorio in diretorios_csv_leitura:
    arquivos = os.listdir(diretorio)
    cor = diretorio.split('/')[-1]
    for arquivo in arquivos:
        caminhos_csv_leitura.append(diretorio + '/' + arquivo)
        caminhos_csv_escrita.append('dados coletados/formato anglo/' + cor + '/' + arquivo)



# SUBSTITUIÇÃO CSV:

for i in range(len(caminhos_csv_leitura)):
    substituir_csv(caminhos_csv_leitura[i], caminhos_csv_escrita[i])



# CAMINHO DOS ARQUIVOS DAT

# caminhos de leitura
caminhos_dat_leitura = ['analise de frequencias/dados brutos/formato original/' + elemento for elemento in os.listdir('analise de frequencias/dados brutos/formato original')]

# lista a serem estocados os caminhos de escrita
caminhos_dat_escrita = []

# obtendo os caminhos
for arquivo in caminhos_dat_leitura:
    cor = arquivo.split('/')[-1]
    caminhos_dat_escrita.append('analise de frequencias/dados brutos/formato anglo/' + cor)



# SUBSTITUICAO DAT:

for i in range(len(caminhos_dat_leitura)):
    substituir_dat(caminhos_dat_leitura[i], caminhos_dat_escrita[i])
    substituir_cabecalho(caminhos_dat_escrita[i])

# ok