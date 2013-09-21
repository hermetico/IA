# -*- coding: utf-8 -*-
"""
    spock
    ~~~~~

    Rock Paper Scissors Spock Lizard Game
    Se solicita al jugador que escoja una jugada, despues se muestra la jugada
    del ordenador y el ganador.
    Cuando el jugador decide salir, se muestra el numero de victorias y derrotas

    Los resultados de los enfrentamientos de guardan en una matriz, en la cual
    el jugador ocupa las columnas y la maquina las filas. Las consultas a la
    matriz, son entonces del tipo : [jugador][maquina] == ?
        
        == 1 gana jugador
        == 2 empate
        == 3 gana maquina


    :creado por Juan Marín y Dennis Quitaquís
"""

from random import randint as rnd

#: texto que se muestra al iniciar el juego
SALUDO = """
    Welcome to Rock Paper Scissors Spock Lizard\n
    let's play!
"""

#: texto que se muestra al solicitar la jugada
SOLICITAR = 'Select your play:'

#: valor para salir del juego
SALIR = -1

#: valor con el cual gana el jugador
GANA_JUGADOR = 1

#: valor con el cual gana la maquina
GANA_MAQUINA = 3

#: valor de empate
EMPATE = 2

#: jugadas disponibles
JUGADAS = ['Rock', 'Paper', 'Scissor', 'Spock', 'Lizard']

#: resultados de cada enfrentamiento
RESULTADOS = [
    [2, 3, 1, 2, 1],
    [1, 2, 3, 1, 3],
    [3, 1, 2, 3, 1],
    [1, 3, 1, 2, 3],
    [3, 1, 3, 1, 2]
]
    
#: stadisticas del jugador a lo largo de las partidas
estadisticas_jugador = {
    'win'     : 0,
    'lose'    : 0
}

def solicitar_jugada():
    """Funcion que solicita la jugada y devuelve el valor como int"""
    
    print
    print SOLICITAR
    # mostramos las jugadas disponibles y el numero relacionado
    for i in range(len(JUGADAS)):
        print "Press %i for play with %s" %(i, JUGADAS[i])
    
    # mostramos el valor a pulsar para salir
    print "Press %i for exit" %SALIR
    
    return input(">> ")


def mostrar_estadisticas():
    """Funcion que muestra las estadisticas del jugador"""

    print
    print 'You have won %i games' % estadisticas_jugador['win']
    print 'And lost %s games' % estadisticas_jugador['lose']


def main():
    """Funcion principal del juego"""
    #: variable que nos indica si continuamos jugando
    continue_playing = True

    print
    print SALUDO
    while continue_playing:
        # solicitamos la mano del jugdor
        jugador = solicitar_jugada()
        # comprobamos si ha introducido el valor para salir
        if jugador == SALIR:
            continue_playing = False
        # comprobamos que sea una mano valida
        elif jugador < -1 or jugador > (len(JUGADAS) - 1):
            pass
        else:
            # calculamos jugada de la maquina
            maquina = rnd(0, len(JUGADAS) - 1)
            print "You play with %s and computer plays with %s" %(
                JUGADAS[jugador], JUGADAS[maquina])
            if RESULTADOS[jugador][maquina] == EMPATE:
                print "Draw!"
            else:
                if RESULTADOS[jugador][maquina] == GANA_JUGADOR:
                    print "You win because %s defeats %s" %(JUGADAS[jugador],
                                                            JUGADAS[maquina])
                    estadisticas_jugador['win'] += 1
                else:
                    print "You lose because %s not defeats %s" %(JUGADAS[jugador],
                                                                JUGADAS[maquina])
                    estadisticas_jugador['lose'] += 1
    # mostramos las estadisticas
    mostrar_estadisticas()


main()
