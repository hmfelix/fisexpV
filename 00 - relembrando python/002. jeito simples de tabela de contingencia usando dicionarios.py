# criamos primeiro uma string:
texto = "oi oi oi meu amigo"

# depois aplicamos esse método maravilhoso chamado split, que nos retorna uma lista
palavras = texto.split()
# >>> palavras
# ['oi', 'oi', 'oi', 'meu', 'amigo']

# depois criamos um dicionario em branco:
contagem = {}

# ai aplicamos esse loop muito inteligente usando o metodo get de dicionarios:
for palavra in palavras:
    contagem[palavra] = contagem.get(palavra, 0) + 1
    pass # serve apenas para indicar que o loop terminou
         # e ai o editor nao vai mais indentar o codigo automaticamente

# o que ele faz eh primeiro add a entrada da palavra no dicionario e atribui a essa entrada o seguinte:
# o valor 0, porque a entrada ainda nao existe no dicionario (ver documentacao do metodo dict.get)
# e somar a esse valor 1
# ou seja, cada palavra tera, de inicio, o valor 1 no dicionario
# ai se a palavra ja existe no dicionario, o metodo retorna o valor atual dela
# ou seja, se a palavra soh ocorreu uma vez, retorna 1
# e em seguida somamos mais 1, para contar o fato de que ela existe e estamos contando de novo

# bom demais!!