#RADIX-SORT(A, n, d)
# 1. Para i = 1 a d:
# a. Use um algoritmo de ordenação estável para ordenar o arranjo A segundo o
# dígito i (usando COUNTING-SORT(A, n, 9), aplicado ao dígito i de cada chave).
# 2. Devolva A.

def counting_sort(A,n,k):
    # K é o maior valor do array, n é o tamanho do array, A é o array 
    C = [0] * (k + 1)
    B = [0] * n
    
    for i in range (n):
        #A[i] retorna o valor do array e incrementa 1 na posição correspondente do array C
        C[A[i]] += 1
        print(f"1 step C: {C}")
    for i in range(1,k+1):
        C[i] = C[i] + C[i-1]
        print(f"2 step C: {C}")
    for i in range(n-1,-1,-1):
        print(f"i: {i}")
        C[A[i]] -= 1
        B[C[A[i]]] = A[i]
        print(f"3 step C: {C}")
        print(f"3 step B: {B}")
    
    return B    


def radix_sort(A,n,d):
    
    for i in range(d):
        counting_sort(A,n,i)
        
    return A




def main():
    A = [1, 5, 6, 8, 8, 5, 82]
    
    lista_digitos = [len(str(abs(num))) for num in A]
        
    for i in range(len(lista_digitos)):
        print(radix_sort(A, len(A), lista_digitos[i]))
    return



if __name__ == "__main__":
    main()