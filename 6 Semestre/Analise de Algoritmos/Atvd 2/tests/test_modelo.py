from src.dados.modelo import Pessoa, carregar


def _escreve_csv(tmp_path, n=5):
    p = tmp_path / "dados.csv"
    with open(p, "w", encoding="utf-8", newline="") as f:
        f.write("nome,cpf,idade,renda_anual,patrimonio_total,dividas_totais,nascimento,email\n")
        for i in range(n):
            f.write(f"Pessoa {i},{i:011d},{30+i},1000,2000,3000,1995-01-0{i+1},p{i}@x.com\n")
    return p


def test_parse_linha():
    pessoa = Pessoa.de_linha("Maria Silva,12345678901,42,50000,80000,10000,1984-03-10,maria.silva@meridian.com.br")
    assert pessoa.nome == "Maria Silva"
    assert pessoa.cpf == "12345678901"
    assert pessoa.idade == 42
    assert pessoa.patrimonio_total == 80000
    assert pessoa.nascimento == "1984-03-10"


def test_carregar_streaming(tmp_path):
    p = _escreve_csv(tmp_path)
    pessoas = carregar(p)
    assert len(pessoas) == 5
    assert pessoas[0].nome == "Pessoa 0"


def test_carregar_limite(tmp_path):
    p = _escreve_csv(tmp_path, n=10)
    assert len(carregar(p, limite=3)) == 3
