import hashlib
import os
import re
import secrets

import bcrypt
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from mnemonic import Mnemonic
from pycardano import Address, HDWallet, Network, PaymentSigningKey, PaymentVerificationKey

from model import Wallet


def is_email(email: str) -> bool:
    pattern = re.compile(r'[a-z0-9]+([._-]?[a-z0-9]+)*@[a-z0-9]+(\.[a-z0-9]+)+', re.I)
    if pattern.fullmatch(email):
        return True

    return False


def random_str(n: int, chars: str = '0123456789') -> str:
    return ''.join(secrets.choice(chars) for _ in range(n))


def check_pass(password: str, hashed: str) -> bool:
    password, hashed = str_to_byte(password, hashed)
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


def gen_mnemonic() -> str:
    nemo = Mnemonic()
    return nemo.generate()


def gen_address(nemo: str) -> str:
    PATH = "m/1852'/1815'/0'/0/0"
    hdwallet = HDWallet.from_mnemonic(nemo)
    spend = hdwallet.derive_from_path(PATH)
    sign_key: PaymentSigningKey = PaymentSigningKey.from_primitive(spend.public_key)
    verify_key = PaymentVerificationKey.from_signing_key(sign_key)
    address = Address(verify_key.hash(), network=Network.TESTNET)
    return address.encode()


def add_wallet(password: str, salt: str, **kw) -> Wallet:
    nemo = gen_mnemonic()
    address = gen_address(nemo)
    nemo, tag = encrypt(nemo, password, salt)
    return Wallet(address=address, mnemonic=nemo, tag=tag, **kw)
