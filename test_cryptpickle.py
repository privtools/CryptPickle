import pytest
import pandas as pd
import cryptpickle


# ── Happy path ────────────────────────────────────────────────────────────────

def test_dictionary(tmp_path):
    path = str(tmp_path / "file.crypt")
    ej1 = {"name1": "John Doe", "name2": "Lisa Doe"}
    cryptpickle.obj_to_encrypted(ej1, password="SecretPassword", path=path)
    ej2 = cryptpickle.obj_from_encrypted(password="SecretPassword", path=path)
    assert ej1 == ej2


def test_dataframe(tmp_path):
    path = str(tmp_path / "pd_data.crypt")
    df1 = pd.DataFrame({"A": [1, 2, 3], "B": ["one", "one", "four"]})
    cryptpickle.obj_to_encrypted(df1, password="SecretPassword", path=path)
    df2 = cryptpickle.obj_from_encrypted(password="SecretPassword", path=path)
    assert df1.equals(df2)


def test_roundtrip_arbitrary_object(tmp_path):
    path = str(tmp_path / "obj.crypt")
    obj = {"list": [1, 2, 3], "nested": {"a": True}, "tuple": (4, 5)}
    cryptpickle.obj_to_encrypted(obj, password="pw", path=path)
    assert cryptpickle.obj_from_encrypted(password="pw", path=path) == obj


# ── Password validation ───────────────────────────────────────────────────────

def test_encrypt_password_none(tmp_path):
    with pytest.raises(ValueError, match="None"):
        cryptpickle.obj_to_encrypted({}, password=None, path=str(tmp_path / "f.crypt"))


def test_encrypt_password_empty(tmp_path):
    with pytest.raises(ValueError, match="empty"):
        cryptpickle.obj_to_encrypted({}, password="", path=str(tmp_path / "f.crypt"))


def test_decrypt_password_none(tmp_path):
    path = str(tmp_path / "f.crypt")
    cryptpickle.obj_to_encrypted({}, password="pw", path=path)
    with pytest.raises(ValueError, match="None"):
        cryptpickle.obj_from_encrypted(password=None, path=path)


def test_decrypt_password_empty(tmp_path):
    path = str(tmp_path / "f.crypt")
    cryptpickle.obj_to_encrypted({}, password="pw", path=path)
    with pytest.raises(ValueError, match="empty"):
        cryptpickle.obj_from_encrypted(password="", path=path)


# ── File errors ───────────────────────────────────────────────────────────────

def test_decrypt_file_not_found(tmp_path):
    with pytest.raises(FileNotFoundError):
        cryptpickle.obj_from_encrypted(password="pw", path=str(tmp_path / "nope.crypt"))


# ── Cryptographic properties ──────────────────────────────────────────────────

def test_wrong_password_raises(tmp_path):
    path = str(tmp_path / "f.crypt")
    cryptpickle.obj_to_encrypted({"x": 1}, password="correct", path=path)
    with pytest.raises(ValueError, match="wrong password"):
        cryptpickle.obj_from_encrypted(password="wrong", path=path)


def test_tampered_file_raises(tmp_path):
    path = str(tmp_path / "f.crypt")
    cryptpickle.obj_to_encrypted({"x": 1}, password="pw", path=path)
    raw = bytearray(_read_bytes(path))
    raw[30] ^= 0xFF  # flip a bit in the ciphertext region (after 28-byte salt+nonce header)
    _write_bytes(path, bytes(raw))
    with pytest.raises(ValueError, match="tampered"):
        cryptpickle.obj_from_encrypted(password="pw", path=path)


def test_each_encryption_produces_different_bytes(tmp_path):
    path1 = str(tmp_path / "f1.crypt")
    path2 = str(tmp_path / "f2.crypt")
    cryptpickle.obj_to_encrypted({"x": 42}, password="pw", path=path1)
    cryptpickle.obj_to_encrypted({"x": 42}, password="pw", path=path2)
    assert _read_bytes(path1) != _read_bytes(path2)


# ── Helpers ───────────────────────────────────────────────────────────────────

def _read_bytes(path: str) -> bytes:
    with open(path, "rb") as f:
        return f.read()


def _write_bytes(path: str, data: bytes) -> None:
    with open(path, "wb") as f:
        f.write(data)
