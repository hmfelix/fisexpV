import os
import pandas as pd
import numpy as np
os.chdir("exp 3 - franck-hertz")
from codigo import auxiliar

# importacao de dados
dados_d1, chaves = auxiliar.importar_dados_d1()

# temperaturas medias e erro de cada tensão de retardo e faixa de temperatura
temp_media_d1 = [dados_d1[df].iloc[:,2].mean() for df in dados_d1]
desv_pad_temp_media_d1 = [dados_d1[df].iloc[:,2].std() for df in dados_d1]
temperaturas_d1 = pd.DataFrame({"T_med": temp_media_d1, "T_med_desvpad": desv_pad_temp_media_d1})

# medias de medias e respectivas incertezas
temp_media_media_d1 = auxiliar.media_medias(temp_media_d1)
erro_temp_media_media_d1 = auxiliar.erro_media_medias(desv_pad_temp_media_d1)
temperaturas_media_medias_d1 = pd.DataFrame({"T_med_med": temp_media_media_d1, "T_med_med_erro": erro_temp_media_media_d1})


# exportando dados
temperaturas_d1.to_csv("resultados/dia1/temperaturas.csv", index=False)
temperaturas_media_medias_d1.to_csv("resultados/dia1/temperaturas_media_medias.csv", index=False)
