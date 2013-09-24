# -*- coding: utf-8 -*-
"""
    setimig.py
    ~~~~~~~~~~
    Pograma que juega al "setimig" con el usuario.
    Se iran dando cartas al usuario, hasta que este no quiera
    mas o se pase del limite de puntos: 7.5
    Asi mismo, la maquina tambien ira pidiendo cartas y
    parara de pedir cuando vea que con la siguiente carta se 
    pasa del limite.

    :creado por Juan Marín y Dennis Quitaquís
"""

from random import shuffle as sfl
from time import sleep as delay

CARTAS = {1:1, 2:2, 3:3, 4:4, 5:5, 6:6, 7:7, "sota":0.5, "cavall":0.5, "rei":0.5}

SALUDO = """
    Welcome to seven and half\n
    Let's play!
"""

PLAYER_TIME = """
    Player 1 starts!
"""
MACHINE_TIME = """
    Machine continues!
"""

WINNER_TIME = """
    Time to know who is the winner
"""

OTRA_CARTA = "Do you want a card? (y/n)"

GAME_OVER = """
    Oohhh!! You lost, you have reached the limit!\n
            GAME OVER!
"""


def dar_carta(shuffle_cards):
    """Funcion que da carta al jugado si este lo solicita"""

    print OTRA_CARTA
    r = raw_input(">> ")

    if (r == "y"):
        return shuffle_cards.pop()
    else:
        return False


def barajar_cartas():
    """Funcion que baraja las cartas"""

    keys = CARTAS.keys()
    sfl(keys)
    return keys


def main():
    """Funcion principal del juego"""

    can_continue = True
    suma_jugador = 0
    suma_maquina = 0

    print SALUDO # Saludamos al usuario

    cards = barajar_cartas() # Barajamos las cartas

    print PLAYER_TIME

    while can_continue:

        card = dar_carta(cards) # Preguntamos al usuario si quiere carta

        if card:
            print "It is the card %s and costs %.1f" %(str(card), CARTAS[card])
            suma_jugador += CARTAS[card] # Suamos los puntos de la carta tocada.
            
            if suma_jugador > 7.5: # Si se pasa del limite, el usuario pierdey acaba el juego.
                print GAME_OVER
                return
                
        else: #Si no quiere carta, turno de la maquina
            can_continue = False

    can_continue = True

    # Turno de la maquina
    print MACHINE_TIME

    while can_continue:

        card = cards.pop() # Cogemos carta

        if (suma_maquina + CARTAS[card] > 7.5):
            can_continue = False # Si se pasa del limite, la maquina para de jugar
        else:
            print "The machine takes the card %s that it costs %.1f" %(str(card), CARTAS[card])
            suma_maquina += CARTAS[card]
        
        delay(2) # Esperamos 2 segundos para que escoja de nuevo otra carta la maquina

    # Anunciamos el ganador
    print WINNER_TIME
    print "And the winner is...",
    if (suma_jugador > suma_maquina):
        print "the player 1 with %.1f points vs %.1f points of the machine!!" %(suma_jugador, suma_maquina)
    elif (suma_jugador == suma_maquina):
        print "That was a draw!!! No winner this time, more lucky next time :) "
    else:
        print "the machine with %.1f points vs %.1f points of the player 1!!" %(suma_maquina, suma_jugador)



main()
