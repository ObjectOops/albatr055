import hashlib

def hash(passphrase):
    n = 2 ** 17
    r = 8
    p = 1
    return hashlib.scrypt(
        password=passphrase.encode("utf-8"),
        salt=b"",
        n=n, r=r, p=p, 
        maxmem=n * 2 * r * 65
    ).hex()
