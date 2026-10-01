from random import randint
from sympy import isprime
from math import gcd

p = randint(100, 200)
while not isprime(p):
    p = randint(100, 200)

q = randint(100, 200)
while not isprime(q) or q == p:
    q = randint(100, 200)

print("p:", p)
print("q:", q)

n = p * q
phi = (p - 1) * (q - 1)

e = 17

d = 1
while (e * d) % phi != 1:
    d += 1

print("Pub = {", e, ",", n, "}")
print("Priv = {", d, ",", n, "}")

mensagem = 0x41

cifrado = (mensagem ** e) % n

decifrado = (cifrado ** d) % n

print("Mensagem:", mensagem)
print("Cifrado:", cifrado)
print("Decifrado:", decifrado)