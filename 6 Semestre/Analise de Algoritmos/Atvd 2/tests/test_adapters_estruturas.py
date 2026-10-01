from hypothesis import given, strategies as st
from src.algoritmos.indexacao import Indice
from src.algoritmos.existencia import Existencia
from src.algoritmos.prefixo import Prefixo
from src.algoritmos.padroes import achar_substring


@given(st.lists(st.tuples(st.text(max_size=10), st.integers()), min_size=0, max_size=50))
def test_indice_roundtrip(entradas):
    idx = Indice()
    esperado = {}
    for k, v in entradas:
        idx.put(k, v)
        esperado[k] = v
    for k, v in entradas:
        assert idx.get(k) == esperado[k]


def test_indice_inexistente_retorna_none():
    idx = Indice()
    idx.put("a", 1)
    assert idx.get("b") is None


@given(st.lists(st.text(max_size=20), min_size=0, max_size=50))
def test_existencia_adicionados(itens):
    estrutura = Existencia()
    for i in itens:
        estrutura.add(i)
    for i in itens:
        assert estrutura.contem(i)


@given(st.lists(st.text(max_size=20), min_size=0, max_size=30))
def test_prefixo_retorna_todos_com_prefixo(palavras):
    estrutura = Prefixo()
    for p in palavras:
        estrutura.adicionar(p)
    prefixos = [""] + [p[:1] for p in palavras if p]
    for pref in prefixos:
        assert set(estrutura.completar(pref)) == {w for w in palavras if w.startswith(pref)}


@given(st.text(min_size=0, max_size=50), st.text(min_size=1, max_size=10))
def test_achar_substring_bate_com_referencia(texto, padrao):
    def referencia(t, p):
        return [i for i in range(len(t) - len(p) + 1) if t[i:i + len(p)] == p]
    assert achar_substring(texto, padrao) == referencia(texto, padrao)
