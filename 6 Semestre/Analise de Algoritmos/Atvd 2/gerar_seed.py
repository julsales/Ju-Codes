from src.dados.gerador import main

SEED = 3
TOTAL = 5_000_000
CAMINHO = "clientes.csv"


if __name__ == "__main__":
    main(total=TOTAL, seed=SEED, caminho=CAMINHO)