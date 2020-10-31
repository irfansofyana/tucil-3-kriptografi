from src.utils.math import *
from src.utils.file import *

class DiffieHellman():
    def __init__(self, n, g, x, y):
        self.n = n
        self.g = g
        self.x = x
        self.y = y
        self.session_key = self.generate_session_key()
    
    def generate_session_key(self):
        X = powmod(self.g, self.x, self.n)
        Y = powmod(self.g, self.y, self.n)
        K = powmod(X, self.y, self.n)
        K_ = powmod(Y, self.x, self.n)
        
        assert (K == K_)
        return K

# if (__name__=="__main__"):
#     d = DiffieHellman(17, 2, 5, 7)
#     print(d.session_key)