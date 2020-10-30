from Crypto.Util import number

def gcd(a, b):
    return a if (b == 0) else gcd(b, a % b)

def lcm(a, b):
    return (a * b) // gcd(a, b)

def powmod(a, b, p):
    res = 1
    while (b > 0):
        if (b&1):
            res = (res * a) % p
        a *= a
        a %= p
        b >>= 1
    return res

def inversmod(a, p):
    return powmod(a, p-2, p)

def getPrimeNbit(n):
    return number.getPrime(n)