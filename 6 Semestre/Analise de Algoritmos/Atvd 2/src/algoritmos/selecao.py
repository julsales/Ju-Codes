import heapq


def selecionar_topk(colecao, chave, k):
    """Retorna os k itens com maiores valores do atributo `chave` em ordem decrescente.

    Se k >= tamanho da coleção, retorna todos ordenados; k=0 retorna lista vazia.
    """
    if k <= 0:
        return []

    # Min-heap de tamanho k: guarda só os k maiores vistos até agora.
    # Cada novo item entra se for maior que o menor do heap (O(log k) por item).
    # Empate de valor: o contador de ordem de entrada desempata, para o heap
    # nunca comparar os itens entre si (nem precisar de comparadores).
    heap = []
    contador = 0
    for item in colecao:
        valor = getattr(item, chave)
        if len(heap) < k:
            heapq.heappush(heap, (valor, contador, item))
            contador += 1
        elif valor > heap[0][0]:
            heapq.heapreplace(heap, (valor, contador, item))
            contador += 1

    return [item for _, _, item in sorted(heap, key=lambda t: t[0], reverse=True)]
