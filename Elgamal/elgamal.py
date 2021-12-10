import random

lowPrimes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443,
             449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997]

def rabinMiller(n, d, a):
    #a = random.randint(2, (n - 2) - 2)
    x = pow(a, int(d), n)  # a^d%n
    if x == 1 or x == n - 1:
        return True

    # square x
    while d != n - 1:
        x = pow(x, 2, n)
        d *= 2

        if x == 1:
            return False
        elif x == n - 1:
            return True

    # is not prime
    return False


def isPrime(n):
    """
        return True if n prime
        fall back to rabinMiller if uncertain
    """

    # 0, 1, -ve numbers not prime
    if n < 2:
        return False

    # if in lowPrimes
    if n in lowPrimes:
        return True

    # if low primes divide into n
    for prime in lowPrimes:
        if n % prime == 0:
            return False

    # find number c such that 2 ^ r * d= n - 1
    d = n - 1  # c even because n not divisible by 2
    while d % 2 == 0:
        d /= 2  # make c odd
    #In this time, c 
    # prove not prime 128 times
    for a in temp_check:
        if not rabinMiller(n, d, a):
            return False

    return True

def generateLargePrime(keysize):
    """
        return random large prime number of keysize bits in size
    """

    while True:
        num = random.randrange(2 ** (keysize - 1), 2 ** keysize - 1)
        if (isPrime(num)):
            return num

def bezout(a, b):
    s = 0
    old_s = 1
    t = 1
    old_t = 0
    r = b
    old_r = a

    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t

    return old_r, old_s, old_t


def modularInv(a, b):
    gcd, x, y = bezout(a, b)

    if x < 0:
        x += b

    return x

def isCoPrime(p, q):
    """
        return True if gcd(p, q) is 1
        relatively prime
    """

    return gcd(p, q) == 1


def gcd(p, q):
    """
        euclidean algorithm to find gcd of p and q
    """

    while q:
        p, q = q, p % q
    return p

def generateKeys(keysize):
    p = generateLargePrime(keysize)
    d = generateLargePrime(keysize)
    g = generateLargePrime(keysize)
    e = pow(g, d, p)
    return p, d, g , e
class Elgamal:
    def set_pubKey(self, keys):
        self.p, self.g, self.e = keys
    def set_priKey(self, key):
        self.d = key
    y = generateLargePrime(8)

    def encrypt(self, msg):
        c2 = ""
        c1 = pow(self.g, self.y, self.p)

        for c in msg:
            m = ord(c)
            c2 += str((m%self.p)*pow(self.e, self.y, self.p)) + " "
        return str(c1) + " " + c2

    def decrypt(self, cipher):
        cipher = cipher.strip().split()
        
        cipher = [int(cipher[i]) for i in range(len(cipher))]
        #print(cipher)
        c1 = cipher[0]
        msg = ""
        for i in range(1, len(cipher)):
            m = (cipher[i] * modularInv(pow(c1, self.d), self.p)) % self.p
            msg += chr(m)
        return msg

if __name__ == "__main__":

    #p, d, g, e = generateKeys(8)
    #elgamal = Elgamal()
    #elgamal.set_pubKey([p, g, e])
    #elgamal.set_priKey(d)

    #msg = input()
    #cipher = elgamal.encrypt(msg)
    #text = elgamal.decrypt(cipher)

    
    while(True):
        choose = input("Encryption, decrpytion or generate keys?   E/D/G\t")
        if choose == "E":
            path_key = input("Input path file Elgamal pulic key:\t")
            path_plain = input("Input path file plain text:\t")
            file_keys = open(path_key, 'r')
            keys = file_keys.readline().split()
            file_keys.close()

            keys = [int(keys[i]) for i in range(len(keys))]
            
            elgamal = Elgamal()
            elgamal.set_pubKey(keys)
             
            file_plain = open(path_plain, 'r')
            file_encrypt = open("encrypted.txt", 'w')
            for line in file_plain.readlines():
                cipher = elgamal.encrypt(line)
                file_encrypt.write(cipher)
                file_encrypt.write('\n')
            file_plain.close()
            file_encrypt.close()
            print("Done!")
                
        elif choose == "D":
            path_key = input("Input path file Elgamal private key:\t")
            path_pub = input("Input path file Elgamal public key:\t")
            path_cipher = input("Input path file cipher text:\t")

            elgamal = Elgamal()
            
            file_keys = open(path_key, 'r')
            keys = file_keys.readline()
            file_keys.close()
            keys = int(keys)
            elgamal.set_priKey(keys)
            
            
            file_pub = open(path_pub, 'r')
            keys_pub = file_pub.readline().split()
            file_pub.close()
            keys_pub = [int(keys_pub[i]) for i in range(len(keys_pub))]
            elgamal.set_pubKey(keys_pub)
            
            file_cipher = open(path_cipher, 'r')
            file_decrypt = open("decrypted.txt", 'w')
            for line in file_cipher.readlines():
                plain = elgamal.decrypt(line)
                file_decrypt.write(plain)
                #file_decrypt.write('\n')
            file_cipher.close()
            file_decrypt.close()
            print("Done!")
            
        elif choose == "G":
            p, d, g ,e = generateKeys(8)
            key_pri = str(d)
            key_pub = str(p) + " " + str(g) + " " + str(e)
            file_pri = open("el.txt", "w")
            file_pri.write(key_pri)
            file_pri.close()

            file_pub = open("el_pub.txt", 'w')
            file_pub.write(key_pub)
            file_pub.close()
            print("Done!")
        else:
            print("Syntax Error, the program is ending .....")
    
    
                  
        
        
            
            
        

    




























        
