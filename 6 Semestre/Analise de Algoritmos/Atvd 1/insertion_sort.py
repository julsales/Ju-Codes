def insertion_sort(lista):
    
    for i in range(1, len(lista)):
        chave = lista[i]
        j = i - 1
        while j >= 0 and lista[j] > chave:
            lista[j + 1] = lista[j]
            j -= 1
        lista[j + 1] = chave
        
    return lista


def main():
    A = [1, 5, 676876, 8, 8, 5, 8987]
    
    insertion_sort(A)
    print(A)

if __name__ == "__main__":
    main()