from src.utils.math import *
from src.utils.file import *
import random
import math

class Elgamal():
    def __init__(self, num_bits, key):
        self.num_bits = num_bits
        self.key = key if (len(key) > 0) else self.generate_key()
    
    def encode(self, plaintext):
        bytes_array = bytearray(plaintext, 'utf-16')
        encoded = []
        byte_size = self.num_bits // 8
        idx_encoded = -byte_size

        for i in range(len(bytes_array)):
            if (i % byte_size == 0):
                idx_encoded += byte_size
                encoded.append(0)
            val = (2 ** (8 * (i % byte_size)))
            encoded[idx_encoded//byte_size] += bytes_array[i] * val

        return encoded

    def decode(self, plaintext):
        bytes_array = []
        byte_size = self.num_bits // 8

        for num in plaintext:
            for i in range(byte_size):
                temp = num
                for j in range(i+1, byte_size):
                    temp = temp % (2 ** (8 * j))
                letter = temp // 2 ** (8 * i)
                bytes_array.append(letter)
                num -= (letter * (2 ** (8 * i)))
        
        decoded_text = bytearray(b for b in bytes_array).decode('utf-16')
        return decoded_text

    def generate_key(self):
        p = getPrimeNbit(self.num_bits)
        g = random.randint(1, p-1)
        x = random.randint(1, p-2)
        y = powmod(g, x, p)

        public_key = { 'y' : y, 'g' : g, 'p' : p }
        private_key = { 'x' : x, 'p' : p }

        return {'public': public_key, 'private': private_key}

    def encrypt(self, plaintext):
        encoded = self.encode(plaintext)
        ciphers = []
        y, g, p = self.key['public'].values()

        for val in encoded:
            k = random.randint(1, p-2)
            a = powmod(g, k, p)
            b = ((val % p) * powmod(y, k, p)) % p
            ciphers.append([a, b])
        
        encrypted_str = ""
        for cipher in ciphers:
            encrypted_str += str(cipher[0]) + ' ' + str(cipher[1]) + ' '
        
        return encrypted_str

    def decrypt(self, ciphertext):
        plaintext = []
        ciphers_array = ciphertext.split()
        x, p = self.key['private'].values()

        if (not len(ciphers_array) % 2 == 0):
            return "BAD Ciphertext found!, can't decrypt it!"
        
        for i in range(0, len(ciphers_array), 2):
            a = int(ciphers_array[i])
            b = int(ciphers_array[i + 1])
            a = powmod(a, x, p)
            plain = (b * powmod(a, p-2, p)) % p
            plaintext.append(plain)
        
        decrypted_str = self.decode(plaintext)
        decrypted_str = "".join([ch for ch in decrypted_str if (ch != '\x00')])

        return decrypted_str

    def save_key(self, is_public, filename):
        filename += '.pub' if is_public else '.pri'
        key_type = 'public' if is_public else 'private'

        write_file(filename, self.key[key_type]) 

# if (__name__=="__main__"):
    # plaintext = "this is only a plaintext for testing encode and decode"
    # elgamal = Elgamal(num_bits = 256)
    # encoded = elgamal.encode(plaintext)
    # print(encoded)
    # decoded = elgamal.decode(encoded)
    # print(decoded)

    # elgamal = Elgamal(num_bits = 256)
    # plaintext = "irfan sofyana putra adalah orang yang mengerjakan tugas bagian ini gan. Duh kok masih ada tugas padahal long weekend"
    # encrypted = elgamal.encrypt(plaintext)

    # print(encrypted)
    # decrypted = elgamal.decrypt(encrypted)
    # print(decrypted)