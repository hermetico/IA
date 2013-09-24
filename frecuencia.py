# -*- coding: utf-8 -*-
"""
    frecuencia
    ~~~~~~

    

    :creado por Juan Marín y Dennis Quitaquís
"""
from unicodedata import normalize

#: valores aceptados
# obtenemos todos los caracteres entre 'a' y 'z' ambos incluidos
# utilizando las funciones chr y ord y sus valores numericos
ACEPTADOS = [ chr(x) for x in range(ord('a'), ord('z') + 1) ]

#: diccionario resultante
results = {}

#: solicitamos el archivo a abrir
archivo = raw_input("Nombre del archivo") or "text.txt"

# abrimos el archivo para trabajar con el
with open(archivo, 'r') as f:
    for line in f:
        # convertimos cada linea a unicode, necesario para despreciar acentos
        line = line.decode("utf-8")
        # normalizamos la linea y las dejamos en formato ascii ignorando alertas
        # Esto convierte letras tipo 'é' en 'e' o 'ç' en 'c'
        line = normalize('NFD', line).encode('ascii', 'ignore')
        # separamos la linea en palabras
        line = line.split()
        for word in line:
            # separamos la palabra en letras
            word = list(word)
            for char in word:
                # tendremos las letras en lowercase
                char = char.lower()
                # comprobamos que el valor este dentro de los aceptados
                if char in ACEPTADOS:
                    # sumamos 1 al caracter si se encuentra en el diccionario
                    # sino, lo insertamos a 1
                    if char in results:
                        results[char] += 1
                    else:
                        results[char] = 1


# mostramos el resultado
for key, value in results.items():
    print "%s = %i" %(key, value)


