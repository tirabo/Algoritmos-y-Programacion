import math 

def exp1(x: float, n: int) -> float:
    # Calcula la serie de Taylor de e**x hasta grado n
    # e**x = \sum_{n=0}^\infty x**n / n!
    ex = 0
    for i in range(n + 1):
        ex = ex + x**i / math.factorial(i)
    return ex

# print(exp(1, 10)) # aproximación de e (e**1)
# print(exp(2,10)) # aproximación de e**2

def ln1(x: float, n: int) -> float:
    # Calcula la serie de Taylor de ln(x) hasta grado n
    lnx = 0
    for i in range(1, n + 1):
        lnx = lnx + (-1)**(i + 1) * (x)**i / i
    return lnx

print(exp1(-1,20))
print(ln1(0.36787,100))

"""
u1 =   (2.718 - 1)**1 / 1  
u2 = -  (2.718 - 1)**2 / 2
u3 = (2.718 - 1)**3 / 3  
u4 = - (2.718 - 1)**4 / 4  
u5 = (2.718 - 1)**5 / 5 
u6 = - (2.718 - 1)**6 / 6 
print(u1)
print(u2)
print(u3)
print(u4)
print(u5)
print(u6)
def f(n):
    return (-1)**(n+1) * (2.718 - 1)**n / n 



print('ln:',u1+u2+u3+u4+u5+u6)
print(f(10))
print(f(11))
"""

# l
