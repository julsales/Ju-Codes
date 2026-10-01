import random
import sys
from datetime import date, datetime, timedelta

PRIMEIROS_NOMES = [
    "Ana", "Beatriz", "Camila", "Daniela", "Eduarda", "Fernanda", "Gabriela",
    "Helena", "Isabela", "Juliana", "Larissa", "Mariana", "Natália", "Patrícia",
    "Rafaela", "Sofia", "Tatiane", "Vanessa", "Yasmin", "Alice", "Bianca",
    "Carla", "Débora", "Elisa", "Flávia", "Giovana", "Hortência", "Inês",
    "Júlia", "Luana", "Michele", "Núbia", "Olívia", "Paula", "Renata",
    "Sandra", "Talita", "Úrsula", "Vitória", "Clara", "Laura", "Manuela",
    "Antônio", "Bruno", "Carlos", "Diego", "Eduardo", "Felipe", "Gabriel",
    "Henrique", "Igor", "João", "Lucas", "Marcos", "Nicolas", "Otávio",
    "Paulo", "Rafael", "Samuel", "Thiago", "Vinícius", "Wesley", "Yuri",
    "André", "Bernardo", "Caio", "Danilo", "Enzo", "Fábio", "Gustavo",
    "Heitor", "Ítalo", "Joaquim", "Leonardo", "Murilo", "Pedro", "Renan",
    "Rodrigo", "Sérgio", "Tomás", "Vitor", "William", "Alexandre", "Cauã",
    "Davi", "Emerson", "Fernando", "Guilherme", "Hugo", "Jorge", "Matheus",
]

SOBRENOMES = [
    "Silva", "Santos", "Oliveira", "Souza", "Pereira", "Costa", "Rodrigues",
    "Almeida", "Nascimento", "Lima", "Araújo", "Fernandes", "Carvalho", "Gomes",
    "Martins", "Rocha", "Ribeiro", "Alves", "Monteiro", "Barbosa", "Cardoso",
    "Correia", "Dias", "Freitas", "Melo", "Moreira", "Moura", "Nunes", "Pinto",
    "Ramos", "Rezende", "Teixeira", "Vieira", "Xavier", "Azevedo", "Campos",
    "Coelho", "Duarte", "Farias", "Lopes", "Machado", "Mendes", "Pires",
    "Sales", "Siqueira", "Teles", "Vasconcelos", "Andrade", "Brito", "Cavalcanti",
    "Figueiredo", "Fonseca", "Guimarães", "Matos", "Peixoto", "Prado", "Queiroz",
    "Santana", "Soares", "Tavares", "Viana", "Borges", "Castro", "Chaves",
    "Dantas", "Ferraz", "Franco", "Lacerda", "Leal", "Maia", "Marques",
    "Medeiros", "Moraes", "Negreiros", "Padilha", "Pinheiro", "Reis", "Rosa",
    "Sanches", "Santiago", "Saraiva", "Trindade", "Valente", "Amorim",
]

DIGITOS = list(range(10))
DOMINIOS = ["meridian.com.br", "meridian.com", "webmail.meridian.com.br"]
ANO_ATUAL = 2026
HOJE = date(ANO_ATUAL, 9, 15)


def gerar_cpf() -> str:
    base = [random.choice(DIGITOS) for _ in range(9)]
    soma = sum((10 - i) * base[i] for i in range(9))
    d1 = (soma * 10) % 11
    d1 = 0 if d1 == 10 else d1
    base.append(d1)
    soma = sum((11 - i) * base[i] for i in range(10))
    d2 = (soma * 10) % 11
    d2 = 0 if d2 == 10 else d2
    base.append(d2)
    return "".join(map(str, base))


def gerar_nascimento(idade: int) -> str:
    dia_nasc = HOJE - timedelta(days=idade * 365 + random.randint(0, 365))
    return dia_nasc.isoformat()


def gerar_email(nome: str) -> str:
    slug = ".".join(p.lower() for p in nome.split())
    return f"{slug}@{random.choice(DOMINIOS)}"


def gerar_bloco(cpf_utilizados, n):
    primeiros = random.choices(PRIMEIROS_NOMES, k=n)
    sobrenomes = random.choices(SOBRENOMES, k=n)
    linhas = []
    for i in range(n):
        cpf = gerar_cpf()
        while cpf in cpf_utilizados:
            cpf = gerar_cpf()
        cpf_utilizados.add(cpf)
        idade = random.randint(0, 120)
        nascimento = gerar_nascimento(idade)
        nome = f"{primeiros[i]} {sobrenomes[i]}"
        renda_anual = int(random.random() ** 2 * 2_000_000)
        patrimonio_total = int(random.random() ** 2.5 * 20_000_000)
        dividas_totais = int(random.random() ** 2 * 5_000_000)
        linhas.append(
            f"{nome},{cpf},{idade},{renda_anual},{patrimonio_total},"
            f"{dividas_totais},{nascimento},{gerar_email(nome)}\n"
        )
    return linhas


def main(total=5_000_000, seed=None, caminho=None):
    if seed is not None:
        random.seed(seed)
    caminho = caminho or f"pessoas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    cpf_utilizados = set()
    tamanho_bloco = 100_000
    gerados = 0
    with open(caminho, "w", encoding="utf-8", newline="") as arquivo:
        arquivo.write("nome,cpf,idade,renda_anual,patrimonio_total,dividas_totais,nascimento,email\n")
        while gerados < total:
            bloco = min(tamanho_bloco, total - gerados)
            arquivo.writelines(gerar_bloco(cpf_utilizados, bloco))
            gerados += bloco
            print(f"{gerados:,} linhas geradas", file=sys.stderr)
    print(f"Arquivo criado: {caminho}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Gera CSV de clientes do Banco Meridian")
    parser.add_argument("total", nargs="?", type=int, default=5_000_000, help="Número de linhas")
    parser.add_argument("--seed", type=int, default=None, help="Seed para reproduzibilidade")
    parser.add_argument("--caminho", default=None, help="Caminho do arquivo de saída")
    args = parser.parse_args()
    main(total=args.total, seed=args.seed, caminho=args.caminho)
