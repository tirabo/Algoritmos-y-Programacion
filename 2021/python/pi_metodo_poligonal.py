import mpmath as mp

# https://math.dartmouth.edu/archive/m56s13/public_html/Han_proj.pdf
# Pseudo-Archimedes: I ignore all the ceilings and the floors that Archimedes had to deal with.
# I wrote this to check my convergence rate.
d = 10 # How many digits you want

mp.mp.dps= d + 1 #I take this precaution since I am not thinking about ceilings and floors.PI AND ARCHIMEDES POLYGON METHOD 9
def BoundPi(n,o): #n is number of Archimedes' iterations, o is the starting regular o-gon; Archimedes started with o=6, a hexagon
    a=mp.mpf(mp.cot(mp.pi/o))
    b=mp.mpf(mp.csc(mp.pi/o))
    for i in range (0,n):
        a=a+b #cot(k)+csc(k)=cot(k/2)
        b=mp.sqrt(a**2+1) #csc(k/2)=sqrt(cot^2(k/2)+1)
    return [1/a*o*2**n,1/b*o*2**n]

print(BoundPi(10, 6))

"""

def DigitsAcc(n,o):
    #Finds the digits in common between UB_o*2^n and LB_o*2^n
    a=BoundPi(n,o)[0]-BoundPi(n,o)[1]
    b=0
    while a<=1:
    a=a*10
    b=b+1
    return b
# A Fractional Archimedes:
#More Historical Archimedes: I try my best to keep to what he did, but hard to do
#since I do not know the exact method through which he approximated square roots.
#But it makes this one is more realistic, uses "fractions"
d=80
import mpmath as mp
mp.mp.dps=d+1 #I do this so I can find correct ceilings and floors.
def UBoundPi(n,acc): # acc=the initial decimal digit accuracy desired of sqrt(3)
    a=floor(sqrt(mp.mpf('3'))*10**(acc-1)) # For the Upper bound, we needed lower
    #bound estimates for the square roots.
    b=10^(acc-1) # The denominator of cot(30 deg)
    c=2*10^(acc-1) # numerator of csc(30)
    d=10^(acc-1) # Denominator of csc(30)
    for i in range (0,n):
    a=a+c #Just add numerators
    c=floor(sqrt(a^2+b^2)) #Just take the integer part of square root
    return b/a*6*2**n


def LBoundPi(n,acc): # acc=the initial decimal digit accuracy desired of sqrt(3)
    a=ceil(sqrt(mp.mpf('3'))*10**(acc-1)) # For the Lower bound, we needed Upper
    #bound estimates for the square roots.
    b=10^(acc-1) # The denominator of cot(30 deg)
    c=2*10^(acc-1) # numerator of csc(30)
    d=10^(acc-1) # Denominator of csc(30)
    for i in range (0,n):
    a=a+c #Just add numerators
    c=ceil(sqrt(a^2+b^2)) #Just raise it by 1
    return d/c*6*2**n


def HistDigitsAcc(n,acc):
    #Finds the digits in common between UB_6*2^n and LB_6*2^n
    #When they started with an initial accuracy of sqrt(3)
    a=UBoundPi(n,acc)-LBoundPi(n,acc)
    b=0
    while a<=1:
    a=a*10
    b=b+1
"""