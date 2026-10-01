def _intercalar(esquerda, direita, valor):
    """Junta duas listas já ordenadas (<= mantém a ordem estável)."""
    saida = []
    i = j = 0
    while i < len(esquerda) and j < len(direita):
        if valor(esquerda[i]) <= valor(direita[j]):
            saida.append(esquerda[i])
            i += 1
        else:
            saida.append(direita[j])
            j += 1
    saida.extend(esquerda[i:])
    saida.extend(direita[j:])
    return saida


def _mergesort(itens, valor):
    """Merge sort: O(n log n) no pior caso e estável."""
    if len(itens) <= 1:
        return itens
    meio = len(itens) // 2
    esquerda = _mergesort(itens[:meio], valor)
    direita = _mergesort(itens[meio:], valor)
    return _intercalar(esquerda, direita, valor)


def ordenar(colecao, chave):
    """Retorna nova lista com os itens em ordem crescente pelo atributo `chave`."""
    return _mergesort(list(colecao), lambda item: getattr(item, chave))


def ordenar_cpf(colecao):
    """Retorna nova lista com os itens em ordem crescente pelo atributo `cpf`.

    A chave é uma string de 11 dígitos (ex.: CPF).
    """
    itens = list(colecao)
    if len(itens) <= 1:
        return itens

    cpfs = [item.cpf for item in itens]
    # Fora do caso "11 dígitos" cai no merge sort genérico (mesmo resultado).
    if any(len(c) != 11 or not c.isdigit() for c in cpfs):
        return ordenar(colecao, "cpf")

    # Radix sort LSD: um dígito por vez, do menos significativo ao mais.
    # Dígitos que são iguais em todos os CPFs não separam nada, então são pulados.
    primeiro = cpfs[0]
    comum = 11
    for c in cpfs:
        k = 0
        while k < 11 and c[k] == primeiro[k]:
            k += 1
        comum = min(comum, k)
    if comum == 11:          # todos os CPFs são idênticos
        return itens

    ordem = itens
    for posicao in range(10, comum - 1, -1):
        baldes = [[] for _ in range(10)]
        for item in ordem:
            baldes[ord(item.cpf[posicao]) - 48].append(item)
        if sum(1 for balde in baldes if balde) == 1:
            continue         # todos têm o mesmo dígito aqui: nada a reordenar
        ordem = [item for balde in baldes for item in balde]
    return ordem


def ordenar_idade(colecao):
    """Retorna nova lista com os itens em ordem crescente pelo atributo `idade`.

    A idade é um inteiro de 0 a 120 (até 3 dígitos).
    """
    itens = list(colecao)
    if len(itens) <= 1:
        return itens

    idades = [item.idade for item in itens]
    if min(idades) < 0 or max(idades) > 120:
        return ordenar(colecao, "idade")   # fora da faixa conhecida: genérico

    # Counting sort: o domínio é pequeno (0..120) e a chave já é o índice.
    contagem = [0] * 121
    for idade in idades:
        contagem[idade] += 1

    posicao = [0] * 121
    acumulado = 0
    for idade in range(121):
        posicao[idade] = acumulado
        acumulado += contagem[idade]

    saida = [None] * len(itens)
    for i, idade in enumerate(idades):     # percorrer na ordem de entrada mantém estável
        saida[posicao[idade]] = itens[i]
        posicao[idade] += 1
    return saida
