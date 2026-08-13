#1. Crie um arranjo auxiliar B[1..n], onde cada B[i] é uma lista (balde) vazia.
#2. Para i = 1 a n:
#a. Insira A[i] na lista B[⌊n · A[i]⌋].
#3. Para i = 1 a n:
#a. Ordene a lista B[i] com INSERTION-SORT.
#4. Concatene as listas B[1], B[2], ..., B[n], nessa ordem, e devolva o resultado.

def insertion_sort(lista):
    
    for i in range(1, len(lista)):
        chave = lista[i]
        j = i - 1
        while j >= 0 and lista[j] > chave:
            lista[j + 1] = lista[j]
            j -= 1
        lista[j + 1] = chave
        
    return lista


def bucket_sort(A, n):
    # arranjo auxiliar, cada balde é uma lista vazia
    B = [[] for _ in range(n)]

    # A[i] vai pro balde ⌊n·A[i]⌋
    for i in range(n):
        balde = int(n * A[i])      
        B[balde].append(A[i])

    for i in range(n):
        B[i] = insertion_sort(B[i])

    resultado = []
    for balde in B:
        resultado.extend(balde)
    return resultado


def main():
    A = [0.42, 0.32, 0.93, 0.23, 0.51, 0.1, 0.12, 0.68]
    print(bucket_sort(A, len(A)))

if __name__ == "__main__":
    main()