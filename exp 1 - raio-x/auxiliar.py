def gerar_titulo_comentario(titulo, n = 80):
    if type(titulo == 'str'):
        # aqui preciso prever a situacao de dar negativo
        titulo = '##### ' + titulo + ' '
        titulo = titulo.ljust(n, '#')
        print(titulo)
    else:
        print("Erro: o argumento fornecido não é um texto.")

