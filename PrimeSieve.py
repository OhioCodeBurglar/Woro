# Python program to print all Primes Smaller
# than or equal to N using Sieve of Eratosthenes
import time

def SieveOfEratosthenes(num):
    prime = [True for i in range(num+1)]
    # boolean array
    p = 2
    while (p * p <= num):
 
        # If prime[p] is not
        # changed, then it is a prime
        if (prime[p] == True):
 
            # Updating all multiples of p
            for i in range(p * p, num+1, p):
                prime[i] = False
        p += 1
 
    # Print all prime numbers
    for p in range(2, num+1):
        if prime[p]:
            print(p)
 
 
# Driver code
if __name__ == '__main__':
    num = 20000000
    print("Following are the prime numbers smaller\n")
    print("than or equal to", num)
    start_time = time.time()
    SieveOfEratosthenes(num)
    end_time = time.time()    # Record the end time
    elapsed_time = end_time - start_time
    print("Time taken:", elapsed_time, "seconds")
