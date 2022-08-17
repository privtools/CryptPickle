# CryptPickle
Encrypted python object serialization

Usage example:
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
pip install .
```

5. Run the sample:
```
python sample.py
```