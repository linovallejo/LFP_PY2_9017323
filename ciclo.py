contador = 0
while contador < 10:
    print(contador)
    if (contador == 5):
        contador = 8
    contador += 1


cadena = "Real @Madrid3-"
print(cadena[5:])

i = 0
while i < len(cadena):
    if (cadena[i].isalnum()):
        print('alnum')
    else:
        print('NOT')
    i += 1
