import hashlib
import os
from pathlib import Path
import re
import secrets
from datetime import datetime

import bcrypt
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import jwt
from mnemonic import Mnemonic
from pycardano import Address, HDWallet, Network, PaymentSigningKey, PaymentVerificationKey
from ulid import ULID


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


def gen_ulid() -> str:
    return str(ULID())


def gen_rsa_token(iss: str, sub: str, key_path: Path, duration: int = 86400) -> str:
    with open(key_path) as f:
        private_key = f.read()

    current = datetime.now().timestamp()
    payload = {
        'iss': iss,
        'sub': sub,
        'jti': gen_ulid(),
        'iat': current,
        'exp': current + duration
    }

    token = jwt.encode(payload, private_key, 'RS256')
    return token


def decode_rsa_token(token: str, key_path: Path) -> dict:
    with open(key_path) as f:
        public_key = f.read()

    try:
        payload = jwt.decode(token, public_key, ['RS256'])
        return payload
    except jwt.InvalidTokenError:
        return {'error': 'Invalid token'}
    except jwt.ExpiredSignatureError:
        return {'error': 'Token expired'}
