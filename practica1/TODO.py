# -*- coding: utf-8 -*-
"""
    TODO
    ~~~~~~

    TODO task manager

    :creado por Juan Marín y Dennis Quitaquís
"""
from datetime import datetime as dt
from time import time

#: definimos el patron del timestamp
TIME_PATHERN = '%d-%m-%Y %H:%M:%S'

#: listado de tasques
tasques = {}
class Tasca:
    def __init__(self, id, descripcio):
        
        self.id = id
        self.descripcio = descripcio
        self.done = False
        self.creacio = dt.fromtimestamp(time()).strftime(TIME_PATHERN)
        self.finalitzacio = None
    
    def __str__(self):
        values = { 'fecha' : str(self.creacio), 'id' : self.id, 
            'desc' : self.descripcio 
        }
        return "%(fecha)s %(id)i %(desc)s " % values

    def finalitzar_tasca(self):
        self.done = True
        self.finalitzar_tasca = dt.fromtimestamp(time()).strftime(TIME_PATHERN)


fake_task = Tasca(1, 'test')


def crear_nova_id_tasca():
    # comprobamos  si hay o no tasques
    if not len(tasques):
        return 1    # primera tasca con id 1
    # si te tasques, retornem el valor de la maxima id + 1
    return max(tasques.keys()) + 1


def crear_editar_tasca(id = None):
    id_tasca = id or crear_nova_id_tasca()
    descripcio = raw_input("Afegeix una descripcio pera a la tasca %i: " % id_tasca)
    tasques[id_tasca] = Tasca(id_tasca, descripcio)

def mostrar_tasques():
    for i in [tasca for tasca in tasques.values() if tasca and not tasca.done]:
        print i


def mostrar_tasques_finalitzades():
    for i in [ tasca for tasca in tasques.values() if tasca and tasca.done ]:
        print i


crear_editar_tasca()
crear_editar_tasca(1)
crear_editar_tasca()

tasques[1].finalitzar_tasca()
print "finalitzades:"
mostrar_tasques_finalitzades()
print "No finalitzades"
mostrar_tasques()
