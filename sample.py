import cryptpickle

ej1 = { 'name1': 'John Doe',
        'name2': 'Lisa Doe'}

print(ej1)

cryptpickle.obj_to_encrypted(ej1,password="SecretPassword",path='./file.crypt')

ej2 =cryptpickle.obj_from_encrypted(password="SecretPassword",path='./file.crypt')

print(ej2)