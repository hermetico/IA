# -*- coding: utf-8 -*-
"""
    TODO
    ~~~~~~

    TODO task manager

    :creado por Juan Marín y Dennis Quitaquís
"""
from datetime import datetime as dt
from time import time
from os import system

#: definimos el patron del timestamp
# dia - mes - año hora:minutos-segundos
TIME_PATHERN = '%d-%m-%Y %H:%M:%S'

#: listado de tasques
tasques = {}


def timestamp(pathern=None):
    """Retorna un objecte del tipus datetime  a partir d'un timestamp
    com a parametre d'entrada.
    El format per defecte es '%d-%m-%Y'
    """
    time_pathern = pathern or '%d-%m-%Y'
    return dt.fromtimestamp(time()).strftime(time_pathern)


class Tasca:
    """Implementa l'estructura d'una tasca"""
    def __init__(self, id, descripcio):
        self.id = id
        self.descripcio = descripcio
        self.done = False
        self.creacio = timestamp()
        self.finalitzacio = None

    def __str__(self):
        values = {
            'fecha': str(self.creacio),
            'id': self.id,
            'desc': self.descripcio
        }
        return "%(fecha)s | %(id)i | %(desc)s " % values

    def finalitzar(self):
        """Posa el parametre done a True i genera un timestamp
        com a data de finalitzacio
        """
        self.done = True
        self.finalitzacio = timestamp(TIME_PATHERN)


def pausar():
    """Mostra un avis per pantalla i espera que l'usuari premi una tecla"""
    return raw_input("Prem cualsevol tecla per continuar\n>>> ")


def crear_nova_id_tasca():
    """Funcio que crea una id a per a la següent practica
    assegurant aixi que no hi hagin id's coincidents
    Retorna 1 si es la primera tasca o ultima id + 1
    """
    # comprobamos  si hay o no tasques
    if not len(tasques):
        return 1    # primera tasca con id 1
    # si te tasques, retornem el valor de la maxima id + 1
    return max(tasques.keys()) + 1


def crear_editar_tasca(id=None):
    """Funcio que serveix per crear una tasca o editarla segons el parametre
    de entrada id
    Si id == None es genera una nova id pera  la tasca
    """
    id_tasca = id or crear_nova_id_tasca()
    descripcio = raw_input("Afegeix una descripcio pera a la tasca %i:" \
                           "\n>>> "%id_tasca)
    tasques[id_tasca] = Tasca(id_tasca, descripcio)


def mostrar_tasques():
    """Mostra totes les tasques"""
    print
    print "Tasques:"
    print "--------"
    for i in [tasca for tasca in tasques.values() if tasca]:
        print i
    print "--------"



def mostrar_tasques_no_finalitzades():
    """Mostra totes les tasques no finalitzades"""
    print
    print "Tasques no finalitzades:"
    print "------------------------"
    for i in [tasca for tasca in tasques.values() if tasca and not tasca.done]:
        print i
    print "------------------------"


def mostrar_tasques_finalitzades():
    """Mostra les tasques finalitzades"""
    print
    print "Tasques finalitzades:"
    print "---------------------"
    for i in [ tasca for tasca in tasques.values() if tasca and tasca.done ]:
        print str(i) + " | " + str(i.finalitzacio)
    print "---------------------"


def eliminar_tasca():
    """Mostra totes les tasques i demana la id per eliminar
    i una confirmacio
    """
    mostrar_tasques()
    id = input("Introdueix la id de la tasca a eliminar:\n>>> ")
    if id in tasques:
        confirm = raw_input("Confirma que vols eliminar la tasca %i (y/n):" \
                            "\n>>> " % id)
        if confirm  == "y":
            tasques[id] = None
    else:
        print "Tasca no reconeguda"


def finalitzar_tasca():
    """ Mostra les tasques pendents, demana la id i una confirmacio """
    mostrar_tasques_no_finalitzades()
    id = input("Introdueix la id de la tasca a finalitzar:\n>>> ")
    if id in tasques:
        confirm = raw_input("Confirma que vols finalitzar la tasca %i (y/n):" \
                            "\n>>> " % id)
        if confirm == "y":
            tasques[id].finalitzar()
    else:
        print "Tasca no reconeguda"

def editar_tasca():
    """
    Mostra les tasques pendents de finalitzar, despres demana la id de la tasca
    a editar i finalment demana la descripcio nova
    """
    mostrar_tasques_no_finalitzades()
    id = input("Introdueix la id de la tasca a editar\n>>> ")
    if(id in tasques and tasques[id]): # tambe comprobem que tasques[i] != None
        desc = raw_input("Insereix la nova descripcio:\n>>> ")
        tasques[id].descripcio = desc
    else:
        print "Tasca no reconeguda"


def menu():
    opcions_menu = {
        1: {
            'label': 'Afegir tasca',
            'funcio': crear_editar_tasca
        },
        2: {
            'label': 'Eliminar tasca',
            'funcio': eliminar_tasca
        },
        3: {
            'label': 'Editar tasca',
            'funcio': editar_tasca
        },
        4: {
            'label': 'Finalitzar tasca',
            'funcio': finalitzar_tasca
        },
        5: {
            'label': 'Mostrar tasques finalitzades',
            'funcio': mostrar_tasques_finalitzades
        },
        9: {'label': 'Sortir'}
}

    continuar = True
    while(continuar):
        system('clear')
        for key, value in opcions_menu.items():
            print str(key) + " - " + value['label']

        opcio = input(">>> ")

        if(opcio in opcions_menu):
            if opcio == 9:
                continuar = False
            else:
                opcions_menu[opcio]['funcio']()
                pausar()
        else:
            #: si inserim debug() com a opcio de menu
            if opcio == "debug()":
                eval(opcio)


def debug():
    """Funcio que ens incorpora una petita shell per interactuar amb
    el programa, per exemple per debugar"""
    import readline # optional, will allow Up/Down/History in the console
    import code
    vars = globals().copy()
    vars.update(locals())
    shell = code.InteractiveConsole(vars)
    shell.interact()


if __name__ == "__main__":
    menu()
