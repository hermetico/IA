# -*- coding: utf-8 -*-
"""
    frecuencia
    ~~~~~~
    
    Programa que llegeix un fitxer de text i compta la frequencia
    de les lletres
    No te en compte signes de puntuacio, les lletres amb accent
    son evaluades com sense accent i la 'ñ' o 'ç' son evaluades
    com 'n' o 'c' respectivament
   
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
archivo = raw_input("Nombre del archivo: ") or "text.txt"

def main():
    """Funcio principal del programa"""
    # abrimos el archivo para trabajar con el
    with open(archivo, 'r') as f:
        for line in f:
            #: convertimos cada linea a unicode, necesario para despreciar acentos
            line = line.decode("utf-8")
            #: normalizamos la linea y las dejamos en formato ascii ignorando alertas
            # Esto convierte letras tipo 'é' en 'e' o 'ç' en 'c'
            line = normalize('NFD', line).encode('ascii', 'ignore')
            #: separamos la linea en palabras, con esto nos deshacemos
            # de los espacios
            line = line.split()
            for word in line:
                # separamos la palabra en letras
                word = list(word)
                for char in word:
                    # tendremos las letras en lowercase
                    # para simplificar comparaciones
                    char = char.lower()
                    # comprobamos que el valor este dentro de los aceptados, con
                    # esto nos deshacemos de signos de puntuación
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


if __name__ == "__main__":
    main()
