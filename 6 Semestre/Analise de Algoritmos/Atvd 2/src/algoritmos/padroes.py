def _tabela_deslocamentos(padrao):
    """Para cada caractere, quanto avançar quando ele não casa (tabela do Boyer-Moore-Horspool)."""
    tamanho = len(padrao)
    deslocamento = {}
    for i in range(tamanho - 1):        # a última posição fica de fora de propósito
        deslocamento[padrao[i]] = tamanho - 1 - i
    return deslocamento, tamanho


def achar_substring(texto, padrao):
    """Retorna lista com os índices iniciais de cada ocorrência de `padrao` em `texto`."""
    n = len(texto)
    m = len(padrao)
    if m == 0 or m > n:
        return []

    deslocamento, tamanho = _tabela_deslocamentos(padrao)
    ultimo = padrao[-1]
    ocorrencias = []
    janela = 0

    # Boyer-Moore-Horspool: compara da direita pra esquerda e, no erro,
    # pula o máximo que a tabela permite em vez de andar 1 posição.
    while janela <= n - m:
        k = m - 1
        while k >= 0 and texto[janela + k] == padrao[k]:
            k -= 1
        if k < 0:
            ocorrencias.append(janela)
            # Após casar, anda uma posição para procurar sobreposições.
            janela += 1
        else:
            janela += max(1, deslocamento.get(texto[janela + tamanho - 1], tamanho))
    return ocorrencias
