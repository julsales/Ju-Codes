from math import log


def _fnv1a(texto, semente):
    """Hash FNV-1a de 64 bits — determinístico entre execuções (hash() não é)."""
    valor = 0xCBF29CE484222325 ^ semente
    for byte in texto.encode("utf-8"):
        valor ^= byte
        valor = (valor * 0x100000001B3) & 0xFFFFFFFFFFFFFFFF
    return valor


class Existencia:
    def __init__(self, esperados=100_000, falso_positivo=0.01):
        """Prepara a estrutura para até `esperados` itens, com taxa de falsos
        positivos alvo `falso_positivo`.

        Filtro de Bloom: um vetor de bits + k funções de hash. Nunca dá falso
        negativo; pode dar falso positivo (o alvo é `falso_positivo`).
        """
        esperados = max(1, int(esperados))
        alvo = min(max(float(falso_positivo), 1e-9), 0.5)

        # m = -n*ln(p) / (ln2)^2  (bits) e k = (m/n)*ln2 (funções de hash)
        bits = int(-esperados * log(alvo) / (log(2) ** 2))
        self._tamanho = max(64, bits)
        self._k = max(1, round(self._tamanho / esperados * log(2)))
        self._bits = bytearray((self._tamanho + 7) // 8)

    def _indices(self, item):
        if not isinstance(item, str):
            item = str(item)
        base = _fnv1a(item, 0)
        for i in range(self._k):
            yield _fnv1a(item, 0x9E3779B97F4A7C15 * (i + 1)) % self._tamanho if i else base % self._tamanho

    def add(self, item):
        """Marca `item` como presente."""
        for posicao in self._indices(item):
            self._bits[posicao >> 3] |= 1 << (posicao & 7)

    def contem(self, item):
        """Retorna True se `item` foi adicionado (podendo aceitar falsos positivos)."""
        return all(
            self._bits[posicao >> 3] & (1 << (posicao & 7))
            for posicao in self._indices(item)
        )
