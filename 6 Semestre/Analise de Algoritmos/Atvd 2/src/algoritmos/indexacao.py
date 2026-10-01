class Indice:
    # Chaves conhecidas: CPF é string de 11 dígitos.
    _TAMANHO = 1 << 17          # 131072 baldes (potência de 2 → índice por máscara)

    def __init__(self):
        self._baldes = [[] for _ in range(self._TAMANHO)]

    def _hash(self, chave):
        return hash(chave) & (self._TAMANHO - 1)

    def _bucket(self, chave):
        return self._baldes[self._hash(chave)]

    def put(self, chave, valor):
        """Guarda `valor` associado a `chave`."""
        bucket = self._bucket(chave)
        for i, (k, _) in enumerate(bucket):
            if k == chave:
                bucket[i] = (chave, valor)
                return
        bucket.append((chave, valor))

    def get(self, chave):
        """Retorna o valor associado a `chave`, ou None se inexistente."""
        for k, valor in self._bucket(chave):
            if k == chave:
                return valor
        return None
