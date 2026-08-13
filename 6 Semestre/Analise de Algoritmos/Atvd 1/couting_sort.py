
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



def main():
    A = [1, 5, 6, 8, 8, 5, 82]
    
    counting_sort(A,len(A),max(A))



if __name__ == "__main__":
    main()