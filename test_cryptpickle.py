import pandas as pd
import cryptpickle


def test_dictionary():
    ej1 = { 'name1': 'John Doe',
    'name2': 'Lisa Doe'}

    # Serialice the data in an encrypted file with a password (file.crypt)
    cryptpickle.obj_to_encrypted(ej1,password="SecretPassword",path='./file.crypt')

    # Load the serialiced data in other python object. Password is needed to unencrypt the data
    ej2 =cryptpickle.obj_from_encrypted(password="SecretPassword",path='./file.crypt')

    assert ej1 == ej2


def test_dataframe():
    df1 = pd.DataFrame({'A': [1, 2, 3],
                'B': ['one', 'one', 'four']})

    # Serialice the data in an encrypted file (path) with a password (password)
    cryptpickle.obj_to_encrypted(df1,password="SecretPassword",path='./pd_data.crypt')

    # Load the serialiced data in other Pandas DataFrame.
    df2 =cryptpickle.obj_from_encrypted(password="SecretPassword",path='./pd_data.crypt')

    assert df1.size == df2.size
