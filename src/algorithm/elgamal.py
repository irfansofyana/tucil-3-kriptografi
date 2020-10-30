from src.utils.math import *
from src.utils.file import *
import random
import math

def encode(plaintext, num_bits):
    bytes_array = bytearray(plaintext, 'utf-16')
    encoded = []
    byte_size = num_bits // 8
    idx_encoded = -byte_size

    for i in range(len(bytes_array)):
        if (i % byte_size == 0):
            idx_encoded += byte_size
            encoded.append(0)
        val = (2 ** (8 * (i % byte_size)))
        encoded[idx_encoded//byte_size] += bytes_array[i] * val

    return encoded

def decode(plaintext, num_bits):
    bytes_array = []
    byte_size = num_bits // 8

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

def generate_key(num_bits=256):
    p = getPrimeNbit(num_bits)
    g = random.randint(1, p-1)
    x = random.randint(1, p-2)
    y = powmod(g, x, p)

    public_key = { 'y' : y, 'g' : g, 'p' : p }
    private_key = { 'x' : x, 'p' : p }

    return {'public': public_key, 'private': private_key}

def encrypt(plaintext, key, num_bits):
    encoded = encode(plaintext, num_bits)
    ciphers = []
    y, g, p = key.values()

    for val in encoded:
        k = random.randint(1, p-2)
        a = powmod(g, k, p)
        b = ((val % p) * powmod(y, k, p)) % p
        ciphers.append([a, b])
    
    encrypted_str = ""
    for cipher in ciphers:
        encrypted_str += str(cipher[0]) + ' ' + str(cipher[1]) + ' '
    
    return encrypted_str

def decrypt(ciphertext, key, num_bits):
    plaintext = []
    ciphers_array = ciphertext.split()
    x, p = key.values()

    if (not len(ciphers_array) % 2 == 0):
        return "BAD Ciphertext found!, can't decrypt it!"
    
    for i in range(0, len(ciphers_array), 2):
        a = int(ciphers_array[i])
        b = int(ciphers_array[i + 1])
        a = powmod(a, x, p)
        plain = (b * powmod(a, p-2, p)) % p
        plaintext.append(plain)
    
    decrypted_str = decode(plaintext, num_bits)
    decrypted_str = "".join([ch for ch in decrypted_str if (ch != '\x00')])

    return decrypted_str

def save_key(key, is_public, filename):
    filename += '.pub' if is_public else '.pri'
    key_type = 'public' if is_public else 'private'

    write_file(filename, key[key_type]) 

if (__name__=="__main__"):
    # plaintext = "this is only a plaintext for testing encode and decode"
    # encoded = encode(plaintext, 256)
    # print(encoded)
    # decoded = decode(encoded, 256)
    # print(decoded)

    keys = generate_key(num_bits=256)
    plaintext = "irfan sofyana putra adalah orang yang mengerjakan tugas bagian ini gan. Duh kok masih ada tugas padahal long weekend"
    encrypted = encrypt(plaintext, keys['public'], num_bits=256)
    print(encrypted)
    decrypted = decrypt(encrypted, keys['private'], num_bits=256)
    print(decrypted)