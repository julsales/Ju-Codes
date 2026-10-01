from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Pessoa:
    nome: str
    cpf: str
    idade: int
    renda_anual: int
    patrimonio_total: int
    dividas_totais: int
    nascimento: str
    email: str

    @classmethod
    def de_linha(cls, linha: str) -> "Pessoa":
        nome, cpf, idade, renda, patrimonio, dividas, nascimento, email = linha.rstrip("\n").split(",")
        return cls(nome, cpf, int(idade), int(renda), int(patrimonio),
                   int(dividas), nascimento, email)


def carregar(caminho: str | Path, limite: int | None = None) -> list[Pessoa]:
    pessoas: list[Pessoa] = []
    with open(caminho, encoding="utf-8") as f:
        f.readline()
        for numero, linha in enumerate(f):
            if limite is not None and numero >= limite:
                break
            pessoas.append(Pessoa.de_linha(linha))
    return pessoas
