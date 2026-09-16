from collections import Counter

from hypothesis import given, strategies as st
from src.algoritmos.ordenacao import ordenar, ordenar_cpf, ordenar_idade
from src.algoritmos.busca import buscar
from src.algoritmos.selecao import selecionar_topk


class Item:
    def __init__(self, chave, extra=""):
        self.chave = chave
        self.extra = extra

    def __repr__(self):
        return f"Item(chave={self.chave!r}, extra={self.extra!r})"


class Cliente:
    def __init__(self, cpf, idade):
        self.cpf = cpf
        self.idade = idade

    def __repr__(self):
        return f"Cliente(cpf={self.cpf!r}, idade={self.idade!r})"


@given(st.lists(st.integers(min_value=0, max_value=10**6), min_size=0, max_size=50))
def test_ordenar_equivale_a_sorted(valores):
    itens = [Item(v, f"x{v}") for v in valores]
    entrada_original = list(itens)
    saida = ordenar(itens, "chave")
    assert [i.chave for i in saida] == sorted(valores)
    assert itens == entrada_original


@given(st.lists(st.integers(min_value=0, max_value=10**9), min_size=0, max_size=50))
def test_ordenar_cpf_como_digitos_fixos(valores):
    clientes = [Cliente(f"{v:011d}", 0) for v in valores]
    saida = ordenar_cpf(clientes)
    esperados = sorted(f"{v:011d}" for v in valores)
    assert [c.cpf for c in saida] == esperados


@given(st.lists(st.integers(min_value=0, max_value=120), min_size=0, max_size=50))
def test_ordenar_idade(valores):
    clientes = [Cliente("x", v) for v in valores]
    saida = ordenar_idade(clientes)
    assert [c.idade for c in saida] == sorted(valores)


@given(st.lists(st.integers(), min_size=1, max_size=50))
def test_buscar_encontra_existentes(valores):
    itens = [Item(v) for v in valores]
    itens.sort(key=lambda i: i.chave)
    for v in valores:
        assert buscar(itens, "chave", v) >= 0


def test_buscar_ausente_retorna_negativo():
    itens = [Item(1), Item(3), Item(5)]
    assert buscar(itens, "chave", 4) < 0
    assert buscar(itens, "chave", 0) < 0
    assert buscar(itens, "chave", 9) < 0
    assert buscar([], "chave", 1) < 0


@given(st.lists(st.integers(min_value=0, max_value=1000), min_size=1, max_size=40))
def test_selecionar_topk_maiores(valores):
    itens = [Item(v) for v in valores]
    k = min(5, len(valores))
    saida = selecionar_topk(itens, "chave", k)
    assert len(saida) == k
    esperados = sorted(valores, reverse=True)[:k]
    assert Counter(i.chave for i in saida) == Counter(esperados)
    chaves = [i.chave for i in saida]
    assert chaves == sorted(chaves, reverse=True)


def test_selecionar_topk_edge_cases():
    itens = [Item(3), Item(1), Item(2)]
    assert selecionar_topk(itens, "chave", 0) == []
    assert len(selecionar_topk(itens, "chave", 10)) == 3
    assert selecionar_topk([], "chave", 2) == []
