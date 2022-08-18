# CryptPickle
## Encrypted python object serialization

[![python](https://img.shields.io/pypi/pyversions/cryptpickle)](https://www.python.org/downloads/)
[![python](https://img.shields.io/github/license/privtools/CryptPickle)](https://github.com/privtools/CryptPickle/blob/main/LICENSE.txt)
[![Downloads](https://static.pepy.tech/personalized-badge/cryptpickle?period=total&units=international_system&left_color=grey&right_color=blue&left_text=Downloads)](https://pepy.tech/project/cryptpickle)
![Issues](https://img.shields.io/github/issues/privtools/CryptPickle)

CryptPickle allows you to easily encrypt python objects into a file and decrypt, regardless of their content. It may be any python object, including for example a Pandas DataFrame.
## Install
```
pip install cryptpickle
```

## Examples

Usage example 1 (Encrypt and Decrypt a dict with some sensible data):
```
import cryptpickle

# Create a dictionary with some data
# It could be any other python object. ie: a Pandas Dataframe 
ej1 = { 'name1': 'John Doe',
        'name2': 'Lisa Doe'}

# Print the data
print(ej1)

# Serialice the data in an encrypted file with a password (file.crypt)
cryptpickle.obj_to_encrypted(ej1,password="SecretPassword",path='./file.crypt')

# Load the serialiced data in other python object. Password is needed to unencrypt the data
ej2 =cryptpickle.obj_from_encrypted(password="SecretPassword",path='./file.crypt')

# Print the data
print(ej2)
```

Usage example 2 (Encrypt and Decrypt a Pandas DataFrame with some sensible data):
```
import cryptpickle
import pandas as pd

# Create a dictionary with some data
df1 = pd.DataFrame({'A': [1, 2, 3],
                   'B': ['one', 'one', 'four']})

# Print the data
print(df1)

# Serialice the data in an encrypted file (path) with a password (password)
cryptpickle.obj_to_encrypted(df11,password="SecretPassword",path='./pd_data.crypt')

# Load the serialiced data in other Pandas DataFrame.
df2 =cryptpickle.obj_from_encrypted(password="SecretPassword",path='./pd_data.crypt')

# Print the data
print(df2)
```


## Install and try it (Linux)

1. Clone this repository and enter in the directory:
```
git clone https://github.com/privtools/CryptPickle.git
cd CryptPickle
```

2. Create a vitual environment:
```
python3 -m venv .venv
```

3. Activate the virtual environment:
```
source .venv/bin/activate
```

4. Install the package:
```
pip install -r requirements.txt
```

5. Run sample1:
```
python sample1.py
```

5. Run sample2:
```
python sample2.py
```