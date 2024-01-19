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
    # utilizando la Criba de Eratóstenes
    primes = [2]  # lista para almacenar los números primos
    for i in range(3, n+1):
        # Asumimos que el número es primo
        is_prime = True
        # Revisamos si el número es divisible por algún número primo menor
        for prime in primes:
            if i % prime == 0:
                # Si es divisible, el número no es primo
                is_prime = False
                break
        # Si después de revisar todos los números primos menores,
        # el número sigue siendo primo, lo agregamos a la lista
        if is_prime:
            primes.append(i)
    # Devolvemos la cantidad de números primos
    return len(primes)

# Contamos la cantidad de números primos hasta el 10
print(count_primes(10))  # imprime 4

# Contamos la cantidad de números primos hasta el 100
print(count_primes(100))  # imprime 25





