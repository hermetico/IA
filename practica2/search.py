# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util

class Node:
    """
    Clase que encapsula una codificaciion de estado y sus atributos
    estado = Representacion del estado contenido
    previous = Nodo previo
    action = Accion para llegar a este estado
    """
    def __init__(self, state, previous=None, action=None, cost=0):
        #: codificacion del estado
        self.state = state
        #: nodo padre
        self.previous = previous
        #: accion que ha llevado hasta este estado
        self.action = action
        #: coste de llegar al estado
        self.cost = cost


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:


    print "Start:", problem.getStartState()

    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"

    from util import Stack
    #: lista de nodos visitados
    visited = []
    #: pila que hace la funcion de frontera
    frontier = Stack()
    # Recogemos el primer estado, creamos un nodo y lo 
    # insertamos en la pila
    frontier.push(Node(problem.getStartState()))
    # iteramos hasta que no hayan nodos en la pila
    # o hayamos encontrado el objetivo
    while not frontier.isEmpty():
        #: siguiente nodo a expandir
        node = frontier.pop()
        # comprobamos si el estado actual nos cumple el objetivo
        if problem.isGoalState(node.state):
            # si lo cumple, salimos del bucle
            break
        # recuperamos los estados sucesores
        for successor in problem.getSuccessors(node.state):
            # si el estado sucesor no esta en la frontera, lo encapsulamos
            # y lo itroducimos
            if successor[0] not in visited:
                frontier.push(Node(
                                successor[0],
                                node,
                                successor[1],
                                successor[2]))

        # insertamos el estado en la lista de visitados
        visited.append(node.state)

    #: acciones para llegar al objetivo
    actions = []
    # recorremos mientras haya un action en el nodo previo
    while node.action:
        actions.append(node.action)
        node = node.previous
    #mostramos el resultado antes de devolverlo
    #print  actions[::-1]
    return actions[::-1]


def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    "*** YOUR CODE HERE ***"
    from util import Queue
    #: lista de nodos visitados
    visited = []
    #: pila que hace la funcion de frontera
    frontier = Queue()
    # Recogemos el primer estado, creamos un nodo y lo 
    # insertamos en la pila
    frontier.push(Node(problem.getStartState()))
    # iteramos hasta que no hayan nodos en la pila
    # o hayamos encontrado el objetivo
    while not frontier.isEmpty():
        #: siguiente nodo a expandir
        node = frontier.pop()
        #print "\nNodo actual: ", node.state
        #print "\nCola: ", frontier.imprime()
        #print "\nVisitados: ", visited

        #while (raw_input(">>> ") != ""):
        #    pass
        # comprobamos que no hayamos metido el nodo varias veces
        # antes de ser expandido
        if node.state in visited:
            continue

        # comprobamos si el estado actual nos cumple el objetivo
        if problem.isGoalState(node.state):
            # si lo cumple, salimos del bucle
            break
        # recuperamos los estados sucesores
        for successor in problem.getSuccessors(node.state):
            # si el estado sucesor no esta en la frontera, lo encapsulamos
            # y lo itroducimos
            if successor[0] not in visited:
                frontier.push(Node(
                                successor[0],
                                node,
                                successor[1],
                                successor[2]))

        # insertamos el estado en la lista de visitados
        visited.append(node.state)
        #print frontier

    #: acciones para llegar al objetivo
    actions = []
    # recorremos mientras haya un action en el nodo previo
    while node.action:
        actions.append(node.action)
        node = node.previous
    #mostramos el resultado antes de devolverlo
    #print  actions[::-1]
    return actions[::-1]


def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
