
# SETUP

import os
import pandas as pd
import numpy as np
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



# CALCULO E SALVAMENTO

metodo_1_sem_ruido = calcula_V0_metodo_1('s')
metodo_1_com_ruido = calcula_V0_metodo_1('r')

pd.merge(metodo_1_sem_ruido, metodo_1_com_ruido, on='Cor', suffixes=(' sem ruido', ' com ruido')).to_csv('metodos v0/metodo 1/todas.csv', index=False)

# ok, mas falta plotar e calcular de cada intensidade... a fazer






