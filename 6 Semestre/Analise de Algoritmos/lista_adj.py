def criar_lista(n):
    lista = []
    for i in range(n):
        lista.append([])
        
    return lista

def adicionar_aresta(lista, x, y):
    lista[x-1].append(y)
    if x!=y:
        lista[y-1].append(x)


def mostrar_lista(lista):
    for i in range(len(lista)):
        print(i + 1, "--", lista[i])


def main():
    n = int(input())
    m = int(input())

    lista = criar_lista(n)

    for i in range(m):
        x, y = map(int, input().split(","))
        adicionar_aresta(lista, x, y)

    mostrar_lista(lista)


if __name__ == "__main__":
    main()