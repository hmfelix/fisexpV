# desta vez vou incrementar mais ainda em relacao ao codigo das sinteses anteriores
# vou criar um dicionario para cada cor/ruido
# ai armanezar a lista de dfs de cada cor como valores do dicionario



# SETUP

import os
import pandas as pd


# DEFINICAO DE FUNCOES

def importar_dados_coletados_lista(pasta):
    arquivos = os.listdir(pasta)
    lista = []
    for arquivo in arquivos:
        caminho = pasta + '/' + arquivo
        df = pd.read_csv(caminho)
        lista.append(df)
    return lista

def escolher_ruido(cor):
    if cor == 'Vermelho' or cor == 'Violeta':
        return 'Ruido dia 1'
    else:
        return 'Ruido dia 2'

def gerar_df_media_sem_ruido(lista_dfs):
    # argumento deve ser a lista de dfs de uma mesma intensidade
    # (por exemplo, 10 do Amarelo 20%, ou 5 de ruido)
    df_base = lista_dfs[0]['Corrente [A]']
    for df in lista_dfs[1:]:
        df_base = pd.concat([df_base, df['Corrente [A]']], axis=1)
    coluna_medias = df_base.mean(axis=1)
    desvio_padrao = df_base.std(axis=1)
    resultado = pd.DataFrame({
        'Tensao (V)': df['Tensao [V]'],
        'Erro instrumental (V)': 0.025,
        'Corrente media (A)': coluna_medias,
        'Desvio padrao (A)': desvio_padrao
    })
    return resultado

def gerar_df_media_ruido_como_erro(lista_dfs, ruido):
    # o argumento ruido eh uma string que deve ser 'Ruido dia 1' ou 'Ruido dia 2'
    # (resultado da funcao escolher_ruido)
    df_base = gerar_df_media_sem_ruido(lista_dfs)
    coluna_ruidos = gerar_df_media_sem_ruido(dicionario_dados_coletados[ruido])['Corrente media (A)']
    df_base['Ruido como erro (A)'] = coluna_ruidos
    resultado = df_base
    return resultado

def gerar_df_media_descontando_ruido(lista_dfs, ruido):
    # o argumento ruido eh uma string que deve ser 'Ruido dia 1' ou 'Ruido dia 2'
    # (resultado da funcao escolher_ruido)
    df_base = gerar_df_media_ruido_como_erro(lista_dfs, ruido)
    coluna_descontada = df_base['Corrente media (A)'] - df_base['Ruido como erro (A)']
    df_base['Corrente com ruido descontado (A)'] = coluna_descontada
    desvio_padrao_ruido = gerar_df_media_sem_ruido(dicionario_dados_coletados[ruido])['Desvio padrao (A)']
    df_base['Erro propagado (media e ruido) (A)'] = (df_base['Desvio padrao (A)']**2 + desvio_padrao_ruido**2)**0.5
    resultado = df_base
    return resultado

def gerar_df_media_total(cor):
    ruido = escolher_ruido(cor)
    intensidades = ['20%', '40%', '60%', '80%', '100%']
    indices_iniciais = list(range(0,41,10))
    indices_finais = list(range(10,51,10))
    for i in range(0,5):
        lista = dicionario_dados_coletados[cor][indices_iniciais[i]:indices_finais[i]]
        df = gerar_df_media_descontando_ruido(lista, ruido)
        nome_arquivo = 'medias de cada intensidade/' + cor + '/' + intensidades[i] + '.csv'
        df.to_csv(nome_arquivo, index=False)



# IMPORTACAO

# criando um dicionario de cores
chaves = os.listdir('dados coletados/formato anglo')
dicionario_dados_coletados = {}
for chave in chaves:
    dicionario_dados_coletados[chave] = importar_dados_coletados_lista('dados coletados/formato anglo/' + chave)



# CALCULO DA MEDIA DOS RUIDOS

df_R1 = gerar_df_media_sem_ruido(dicionario_dados_coletados['Ruido dia 1'])
df_R2 = gerar_df_media_sem_ruido(dicionario_dados_coletados['Ruido dia 2'])



# CALCULO DAS MEDIAS DE CADA COR

cores = ['Verde', 'Azul', 'Amarelo', 'Vermelho', 'Violeta']
for cor in cores:
    gerar_df_media_total(cor)

# ok

    