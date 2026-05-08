"""
Library for encrypted python object serialization.

CryptPickle allows you to easily encrypt python objects into a file and decrypt,
regardless of their content.
It may be any python object, including for example a Pandas DataFrame.

File format (v1.0):
    [salt: 16 bytes][nonce: 12 bytes][ciphertext + GCM tag: N+16 bytes]

Cryptographic design:
    - Key derivation: PBKDF2-HMAC-SHA256, 600_000 iterations, 16-byte random salt
    - Encryption: AES-256-GCM (authenticated encryption, detects tampering)
"""


__version__ = "1.0"


import os
import pickle
from typing import Any

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidTag

DATA_PATH = "./data.crypt"
NO_PASSWD = None

_PBKDF2_ITERATIONS = 600_000
_SALT_BYTES = 16
_NONCE_BYTES = 12
_KEY_BYTES = 32  # AES-256


def _derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=_KEY_BYTES,
        salt=salt,
        iterations=_PBKDF2_ITERATIONS,
    )
    return kdf.derive(password.encode("utf-8"))


def _validate_password(password: Any) -> str:
    if password is None:
        raise ValueError("password must not be None")
    if not isinstance(password, str):
        raise TypeError(f"password must be a str, got {type(password).__name__}")
    if not password:
        raise ValueError("password must not be empty")
    return password


def obj_to_encrypted(obj: Any, password: str = NO_PASSWD, path: str = DATA_PATH) -> None:
    """Serialize and encrypt a Python object to a file (AES-256-GCM + PBKDF2).

    Args:
        obj: Any picklable Python object.
        password: Encryption password (non-empty string).
        path: Destination file path. Defaults to './data.crypt'.

    Raises:
        ValueError: If password is None or empty.
        TypeError: If password is not a string.
    """
    pwd = _validate_password(password)
    buf = pickle.dumps(obj)

    salt = os.urandom(_SALT_BYTES)
    nonce = os.urandom(_NONCE_BYTES)
    key = _derive_key(pwd, salt)
    ciphertext = AESGCM(key).encrypt(nonce, buf, None)

    with open(path, "wb") as f:
        f.write(salt + nonce + ciphertext)


def obj_from_encrypted(password: str = NO_PASSWD, path: str = DATA_PATH) -> Any:
    """Decrypt and deserialize a Python object from a file.

    Args:
        password: Decryption password (must match the one used to encrypt).
        path: Source file path. Defaults to './data.crypt'.

    Returns:
        The original Python object.

    Raises:
        ValueError: If password is None or empty, file is too small, or decryption fails.
        TypeError: If password is not a string.
        FileNotFoundError: If the file does not exist at the given path.
        PermissionError: If the file cannot be read due to OS permissions.
    """
    pwd = _validate_password(password)

    try:
        with open(path, "rb") as f:
            data = f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Encrypted file not found: {path!r}")
    except PermissionError:
        raise PermissionError(f"Cannot read file (permission denied): {path!r}")

    min_size = _SALT_BYTES + _NONCE_BYTES + 16  # 16 = minimum GCM tag size
    if len(data) < min_size:
        raise ValueError(
            f"File {path!r} is too small to be a valid CryptPickle v1.0 file. "
            "It may have been created with an older version of CryptPickle."
        )

    salt = data[:_SALT_BYTES]
    nonce = data[_SALT_BYTES:_SALT_BYTES + _NONCE_BYTES]
    ciphertext = data[_SALT_BYTES + _NONCE_BYTES:]
    key = _derive_key(pwd, salt)

    try:
        buf = AESGCM(key).decrypt(nonce, ciphertext, None)
    except InvalidTag:
        raise ValueError(
            "Decryption failed: wrong password or the file has been tampered with."
        )

    return pickle.loads(buf)
