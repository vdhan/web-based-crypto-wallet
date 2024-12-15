import hashlib
import os
import re
import secrets

import bcrypt
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


def is_email(email: str) -> bool:
    pattern = re.compile(r'[a-z0-9]+([._-]?[a-z0-9]+)*@[a-z0-9]+(\.[a-z0-9]+)+', re.I)
    if pattern.fullmatch(email):
        return True

    return False


def random_str(n: int, chars: str = '0123456789') -> str:
    return ''.join(secrets.choice(chars) for _ in range(n))


def check_pass(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password, hashed)


def str_to_byte(*arg: str) -> map:
    return map(lambda x: x.encode(), arg)


def pass_to_key(password: bytes, salt: bytes) -> bytes:
    key = hashlib.pbkdf2_hmac('sha256', password, salt, 100_000)
    return key


def encrypt(data: str, password: str, salt: str) -> tuple[str, str]:
    data, password, salt = str_to_byte(data, password, salt)
    key = pass_to_key(password, salt)

    nonce = os.urandom(12)
    encryptor = Cipher(algorithms.AES(key), modes.GCM(nonce)).encryptor()
    cipher = nonce + encryptor.update(data) + encryptor.finalize()
    tag = encryptor.tag
    return cipher.hex(), tag.hex()


def decrypt(data: str, password: str, salt: str, tag: str) -> str:
    data = bytes.fromhex(data)
    tag = bytes.fromhex(tag)
    password, salt = str_to_byte(password, salt)
    key = pass_to_key(password, salt)

    nonce = data[:12]
    cipher = data[12:]
    decryptor = Cipher(algorithms.AES(key), modes.GCM(nonce, tag)).decryptor()
    plain = decryptor.update(cipher) + decryptor.finalize()
    return plain.decode()
