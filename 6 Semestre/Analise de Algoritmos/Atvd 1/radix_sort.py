#RADIX-SORT(A, n, d)
# 1. Para i = 1 a d:
# a. Use um algoritmo de ordenação estável para ordenar o arranjo A segundo o
# dígito i (usando COUNTING-SORT(A, n, 9), aplicado ao dígito i de cada chave).
# 2. Devolva A.

def counting_sort(A,n,pos):
    # Ao invés de K se passa a posição do digito 
    C = [0] * 10 # C é assim pq só tem como ter 0 a 9 como digito inteiro
    B = [0] * n
    divisor = 10 ** pos
    
    digitos = []
    for i in range(n):
        digitos.append((A[i] // divisor) % 10)
        
    for i in range (n):
        C[digitos[i]] += 1
        print(f"1 step C: {C}")
    for i in range(1,10):
        C[i] = C[i] + C[i-1]
        print(f"2 step C: {C}")
    for i in range(n-1,-1,-1):
        print(f"i: {i}")
        C[digitos[i]] -= 1
        B[C[digitos[i]]] = A[i]
        print(f"3 step C: {C}")
        print(f"3 step B: {B}")
    
    return B    


def radix_sort(A,n,d): 
    
    for pos in range(d):
        A = counting_sort(A,n,pos) 
        
    return A



def main():
    A = [1, 5, 6, 8, 1872, 5, 82]
    
    d = len(str(max(A))) # Pega o maior valor do array e transforma em string para pegar a quantidade de digitos
    result = radix_sort(A, len(A), d)
    print(result)    




if __name__ == "__main__":
    main()