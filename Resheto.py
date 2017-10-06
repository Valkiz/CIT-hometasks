import math
import array
n=10000 #берем 10к чисел
A = [True] * n
for i in range(2,math.floor(math.sqrt(n))):
    if A[i]:
        for j in range(i**2,n, i):
            A[j] = False
#Построили решето
c=0; i=1
while c<=1000:
    c += A[i]
    i += 1
    if A[i]: print(i)
