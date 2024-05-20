# gerado pelo chatgpt

import numpy as np
import pandas as pd

# Definir parâmetros do modelo
intercepto = 5
coeficiente = 2
erro_padrao = 1.5

# Gerar variável X com erros
np.random.seed(0)
X = np.random.uniform(0, 10, 20)
erro_X = np.random.normal(0, erro_padrao, 20)


# Gerar variável Y com erros
Y = intercepto + coeficiente * X + np.random.normal(0, erro_padrao, 20)

# Gerar erro em Y diferente dos erros de X (esse código é meu)
erro_Y = np.random.normal(0, Y.max()/100, 20)

# Criar DataFrame com os dados
dados = pd.DataFrame({
    'X': X,
    'Erro_X': erro_X,
    'Y': Y,
    'Erro_Y': erro_X  # Erro aleatório para a variável Y
})

# Exportar para um arquivo CSV
dados.to_csv('aprendendoPython/dados.csv', index=False)

