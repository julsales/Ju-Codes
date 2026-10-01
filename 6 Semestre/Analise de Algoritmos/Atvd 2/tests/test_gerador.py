import csv
from src.dados import gerador

def test_cabecalho_e_linhas(tmp_path):
    alvo = tmp_path / "pessoas.csv"
    gerador.main(total=10, seed=1, caminho=str(alvo))
    with open(alvo, encoding="utf-8") as f:
        linhas = list(csv.DictReader(f))
    assert len(linhas) == 10
    assert set(linhas[0]) == {"nome", "cpf", "idade", "renda_anual",
                              "patrimonio_total", "dividas_totais",
                              "nascimento", "email"}
    for r in linhas:
        assert len(r["cpf"]) == 11 and r["cpf"].isdigit()
        assert r["nascimento"][:4].isdigit()
        assert "@" in r["email"]

def test_nascimento_coerente_com_idade(tmp_path):
    alvo = tmp_path / "pessoas.csv"
    gerador.main(total=200, seed=1, caminho=str(alvo))
    with open(alvo, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            ano_nasc = int(r["nascimento"][:4])
            assert 2026 - ano_nasc - 1 <= int(r["idade"]) <= 2026 - ano_nasc
