def count_primes(n):
    """
    Esta función cuenta la cantidad de números primos menores o iguales a n.
    """
    # Si el número es menor o igual que 1, no hay números primos
    if n <= 1:
        return 0

    # Si el número es 2, hay un solo número primo (2)
    if n == 2:
        return 1

    # Si el número es mayor que 2, contamos los números primos
    primes = [2]
    for i in range(3, n+1):
        # Revisamos si el número es divisible por algún número primo menor^
        k = 0
        prime = primes[k]
        while i % prime != 0 and k < len(primes):
            prime = primes[k]
            k += 1
        if k == len(primes):
            primes.append(i)
    # Devolvemos la cantidad de números primos
    return len(primes)


# Contamos la cantidad de números primos hasta el 10
print(count_primes(10))  # imprime 4

# Contamos la cantidad de números primos hasta el 100
print(count_primes(100))  # imprime 25