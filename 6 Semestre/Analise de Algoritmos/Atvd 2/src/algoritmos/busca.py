def buscar(colecao_ordenada, chave, valor):
    """Retorna o índice do item com atributo `chave` == `valor`, ou -1. A coleção está ordenada por `chave`."""
    baixo = 0
    alto = len(colecao_ordenada) - 1

    # Busca binária: a coleção já está ordenada, então descartamos metade por passo.
    while baixo <= alto:
        meio = (baixo + alto) // 2
        atual = getattr(colecao_ordenada[meio], chave)
        if atual == valor:
            return meio
        if atual < valor:
            baixo = meio + 1
        else:
            alto = meio - 1
    return -1
