# -*- coding: utf-8 -*-
"""
    spock
    ~~~~~~~~~~~~~~

    Rock Paper Scissors Spock Lizard Game
    Se solicita al jugador que escoja una jugada, despues se muestra la jugada
    del ordenador y el ganador.
    Cuando el jugador decide salir, se muestra el numero de victorias y derrotas

    :creador por Juan Marín y Dennis Quitaquís
"""

# spock.py
# programa per jugar al joc Pedra paper estissores, spock, llangardaix


from random import randint as rnd

SALUDO = '''
    Welcome to Rock Paper Scissors Spock Lizard\n
    let's play!
'''
MANO = 'Select your play:'

JUGADASALIR = 'Press -1 to exit'
SALIR = '-1'

playerStats = {
    'win'     : 0,
    'lose'    : 0
}

hands = {
    '0' : {
        'name' : 'Rock',
        'defeat' : [2, 4]
    },
    '1' : {
        'name' : 'Paper',
        'defeat' : [0, 3]
    },
    '2' : {
        'name' : 'Scissors',
        'defeat' : [1, 4]
    },
    '3' : {
       'name' : 'Spock',
        'defeat' : [0, 2]
    },
    '4' : {
        'name' : 'Lizard',
        'defeat' : [1, 3]
    }
}

def playerHand():
    print MANO
    #mostramos los numeros que puede entrar
    for key in sorted(hands.keys()):
        print 'Press %s for play with %s' %(key, hands[key]['name'])

    print JUGADASALIR
    
    return raw_input(">> ")


def showResults():
    print 'You have won %s games' % str(playerStats['win'])
    print 'And you have lost %s games' %str(playerStats['lose'])

def main():
    print
    print SALUDO
    
    while(True): 
        print
        player = playerHand()
        computer = str(rnd(0,4))

    
        #comprobamos si tenemos que salir del juego
        if player == '-1':
            return None

        if not player in hands.keys():
            pass

        elif player == computer: # draw
            print 'Draw'

        elif int(player) in hands[computer]['defeat']: # gana maquina
            playerStats['lose'] += 1
            print 'You lose : %s defeat %s ' %(hands[computer]['name'],hands[player]['name'])

        else: # gana jugador
            playerStats['win'] += 1
            print 'You win : %s defeat %s ' %(hands[player]['name'], hands[computer]['name'])


main()
showResults()

