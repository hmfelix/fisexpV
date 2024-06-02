# script ainda incompleto

import os
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
os.chdir("exp 3 - franck-hertz")
from codigo import auxiliar

# IMPORTACAO

# importando dados brutos
dados_d1, chaves = auxiliar.importar_dados_d1()

# preparando 
df_teste = dados_d1[chaves[1]]
df_teste.columns = ["V_A", "I", "T"]
df_teste.sort_values("V_A", inplace=True)
df_teste.reset_index(drop=True, inplace=True)

# AJUSTE POLINOMIAL

