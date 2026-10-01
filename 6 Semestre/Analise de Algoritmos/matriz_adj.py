def criar_matriz(n):
    matriz = []

    for i in range(n):
        matriz.append([0] * n)

    return matriz


def adicionar_aresta(matriz, x, y):
    matriz[x-1][y-1] = 1
    matriz[y-1][x-1] = 1


def mostrar_matriz(matriz):
    for linha in matriz:
        print(linha)


def main():
    n = int(input())
    m = int(input())

    matriz = criar_matriz(n)

    for i in range(m):
        x, y = map(int, input().split(","))
        adicionar_aresta(matriz, x, y)
        
    mostrar_matriz(matriz)


if __name__ == "__main__":
    main()