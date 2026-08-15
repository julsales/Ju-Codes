def hash1(element, size):
    sum = 0
    for char in element:
         sum += ord(char)
    
    return sum % size

def hash2(element, size):
    sum = 0
    i=1
    for char in element:
        sum+= ord(char) * i
        i+=1
    
    return sum % size


def bloom_insert(filter, element, k, m):
    hashes = [hash1, hash2]

    for i in range(k):
        pos = hashes[i](element, m)
        
        filter[pos]=1


def bloom_consult(filter, element, k, m):
    hashes = [hash1, hash2]

    for i in range(k):
        pos = hashes[i](element, m)

        if filter[pos]==0:
            return False

    return True


def main():
    m = 20
    k = 2
    filtro = [0]*m

    bloom_insert(filtro, "maria", k, m)
    bloom_insert(filtro, "joao", k, m)

    print(bloom_consult(filtro, "maria", k, m))
    print(bloom_consult(filtro, "joao", k, m))
    print(bloom_consult(filtro, "pedro", k, m))

if __name__ == "__main__":
    main()