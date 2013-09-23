# -*- coding: utf-8 -*-
"""
    setimig.py
    ~~~~~~~~~~




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

YOU_LOSE = "Oohhh!! You lost, you have reached the limit!"




def dar_carta(shuffle_cards):
    """Funcion que dona carta al jugador si aquet solicita"""

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

    print SALUDO

    cards = barajar_cartas()

    print PLAYER_TIME

    while can_continue:

        card = dar_carta(cards)

        if card:
            print "It is the card %s and costs %.1f" %(str(card), CARTAS[card])
            suma_jugador += CARTAS[card]
            
            if suma_jugador > 7.5:
                print YOU_LOSE
                return
                
        else:
            can_continue = False

    can_continue = True

    print MACHINE_TIME

    while can_continue:

        card = cards.pop()

        if (suma_maquina + CARTAS[card] > 7.5):
            can_continue = False
        else:
            print "The machine takes the card %s that it costs %.1f" %(str(card), CARTAS[card])
            suma_maquina += CARTAS[card]
        
        delay(2)

    print WINNER_TIME
    print "And the winner is...",
    if (suma_jugador > suma_maquina):
        print "the player 1 with %.1f points vs %.1f points!!" %(suma_jugador, suma_maquina)
    else:
        print "the machine with %.1f vs %.1f!!" %(suma_maquina, suma_jugador)



main()
