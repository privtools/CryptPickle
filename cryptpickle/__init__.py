"""
Library for encrypted python object serialization
"""

__version__ = "0.1"


import pyzipper
import pickle
import string


DATA_PATH = "./data.crypt"
NO_PASSWD = None


def obj_to_encrypted(obj, password=NO_PASSWD, path=DATA_PATH):
    buf = pickle.dumps(obj)
    pwd = password
    with pyzipper.AESZipFile(path,
                         'w',
                         compression=pyzipper.ZIP_DEFLATED,
                         encryption=pyzipper.WZ_AES) as zf:
        zf.setpassword(pwd.encode('utf-8'))
        zf.writestr('data', buf)


def obj_from_encrypted(password=NO_PASSWD, path=DATA_PATH):
    pwd = password
    with pyzipper.AESZipFile(path) as zf:
        zf.setpassword(pwd.encode('utf-8'))
        buf = zf.read('data')
    return pickle.loads(buf)