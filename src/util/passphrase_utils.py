import hashlib

from config import constants, config

def is_valid_passphrase(passphrase):
    return passphrase and all(
        character in constants.VALID_PASSPHRASE_CHARACTERS for character in passphrase
    )

def hash_scrypt(passphrase):
    n = 2 ** 17
    r = 8
    p = 1
    return hashlib.scrypt(
        password=passphrase.encode("utf-8"),
        salt=b"",
        n=n, r=r, p=p, 
        maxmem=n * 2 * r * 65
    ).hex()

def set_passphrase(passphrase):
    config.instance.passphrase_hash = hash_scrypt(passphrase)
    config.instance.passphrase_enabled = True
