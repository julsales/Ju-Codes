class Prefixo:
    """Trie (árvore de prefixos): cada nó guarda um nó por caractere seguinte."""

    # Marcador de "aqui termina um texto adicionado". É um objeto, não uma
    # string, para nunca colidir com um caractere real (texto pode ter \x00).
    _FIM = object()

    def __init__(self):
        self._raiz = {}

    def adicionar(self, texto):
        """Adiciona `texto` ao conjunto consultável."""
        atual = self._raiz
        for caractere in texto:
            atual = atual.setdefault(caractere, {})
        atual[self._FIM] = True

    def completar(self, prefixo):
        """Retorna lista com todos os textos adicionados que começam com `prefixo`."""
        atual = self._raiz
        # Desce até o nó que representa o prefixo: O(len(prefixo)).
        for caractere in prefixo:
            atual = atual.get(caractere)
            if atual is None:
                return []

        # Daqui pra baixo, todo ramo começa com o prefixo: só coletar as palavras.
        resultado = []
        pilha = [(atual, prefixo)]
        while pilha:
            no, palavra = pilha.pop()
            for caractere, filho in no.items():
                if caractere is self._FIM:
                    resultado.append(palavra)
                else:
                    pilha.append((filho, palavra + caractere))
        return resultado
