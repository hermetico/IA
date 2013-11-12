from util import manhattanDistance
from game import Directions
import random, util

from game import Agent


class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
  """


    def getAction(self, gameState):
        """
    You do not need to change this method, but you're welcome to.

    getAction chooses among the best options according to the evaluation function.
    
    Just like in the previous project, getAction takes a GameState and returns
    some Directions.X for some X in the set {North, South, West, East, Stop}
    """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
    Design a better evaluation function here. 
    
    The evaluation function takes in the current and proposed successor
    GameStates (pacman.py) and returns a number, where higher numbers are better.
    
    The code below extracts some useful information from the state, like the 
    remaining food (oldFood) and Pacman position after moving (newPos).
    newScaredTimes holds the number of moves that each ghost will remain
    scared because of Pacman having eaten a power pellet.
    
    Print out these variables to see what you're getting, then combine them
    to create a masterful evaluation function.
    """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        oldFood = currentGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        distMin = 100
        for posFant in newGhostStates:
            d = manhattanDistance(newPos, posFant.getPosition())
            distMin = min(distMin, d)

        if (distMin < 2):
            val = -100
        else:
            val = distMin
        "*** YOUR CODE HERE ***"
        # si la distancia a los fantasmas es grande, no la tenemos en cuenta
        #if val > 8:
        #    val = 0
        """
        val /= 10
        """
        #: posicion anterior del pacman
        oldPos = currentGameState.getPacmanPosition()
        ghost_num = 0
        #inear_ghost = None

        # comprobamos si los fantasmas estan en modo asustado
        for posFant in newGhostStates:
            #d = manhattanDistance(newPos, posFant.getPosition())

            # capturamos el fantasma mas cercano
            #if not near_ghost:
            #    near_ghost = (d, posFant.getPosition())
            #else:
            #    if near_ghost[0] > d:
            #        near_ghost = (d, posFant.getPosition())

            # si estan en modo asustado durante mas pasos que la distancia a ellos
            # sumamos si el fantasma esta en modo asustado y muy cerca, val sera negativo, asi que lo ponemos
            # en valor asboluto
            if newScaredTimes[ghost_num] > 0:
                val = abs(val) #+ 10 / d
                #val += 10 * d
            #if newScaredTimes[ghost_num] > d:
            #    val = abs(val) #+ 50 / d
                #val += 20 * d
            ghost_num += 1

        """
        d_now = float("inf")
        # comprobamos la comida mas cercana ahora
        for food in successorGameState.getFood().asList():
            d_now = min(d_now, manhattanDistance(newPos, food))
        # si la distancia a la comida es menor que la distancia al fantasma mas cercano, +10
        if d_now >= distMin:
            val +=20
        """
        """
        # si moviendonos hemos comido, sumamos +10 el val
        if successorGameState.getFood().count() < oldFood.count():
            val += 10
        """
        sum_now = 0
        min_now = 999
        # comprobamos la suma de las distancias a comida ahora
        for food in successorGameState.getFood().asList():
            sum_now += manhattanDistance(newPos, food)
            min_now = min(min_now, manhattanDistance(newPos, food))

        sum_before = 0
        min_before = 999
        # comprobamos la suma de las distancias a las comidas antes
        for food in oldFood.asList():
            sum_before += manhattanDistance(oldPos, food)
            min_before = min(min_before, manhattanDistance(oldPos, food))
        # si hay menor distancia
        if min_now < min_before:
            val += 10

        # tambien consideramos que si la accion es quedarse quieto
        # solo devolvemos el score actual

        if action == 'Stop':
            return successorGameState.getScore()
        return successorGameState.getScore() + val


def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.
    
    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
  """
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.
    
    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.
    
    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.  
  """

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
            Returns the minimax action from the current gameState using self.depth
            and self.evaluationFunction.

            Here are some method calls that might be useful when implementing minimax.

            gameState.getLegalActions(agentIndex):
              Returns a list of legal actions for an agent
              agentIndex=0 means Pacman, ghosts are >= 1

            Directions.STOP:
              The stop direction, which is always legal

            gameState.generateSuccessor(agentIndex, action):
              Returns the successor game state after an agent takes an action

            gameState.getNumAgents():
              Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        """
        Configuraciones de la clase
        """
        #: agente base
        self.pacman = 0

        #:primer ghost
        self.first_ghost = 1
        #: infinito
        self.oo = float("inf")

        #: permitimos 'Stop' action ?
        self.enable_stop_action = False

        actions = {}
        # la primera llamada la hemos de hacer aqui ya que debemos controlar el movimiento que vamos a hacer
        for action in gameState.getLegalActions(self.pacman):
            if action is not 'Stop' or self.enable_stop_action:
                actions[action] = self.minValue(gameState.generateSuccessor(self.pacman, action), self.depth)

        """
        # equivalente
        actions = {action: self.minValue(gameState.generateSuccessor(self.pacman, action), self.depth)
                  for action in gameState.getLegalActions(self.pacman)
                   if action is not 'Stop'
                   or self.enable_stop_action}
        """

        #devolvemos la accion con maxima utilidad
        return max(actions, key=actions.get)

    def minValue(self, gameState, depth):
        """
        Calcula los miminos, los acumula en funcion del numero de fantasmas.
        En total hay x agentes y el pacman es el 0, asi que el primer ghost por defecto es 1
        """
        #: si estamos en un estado terminal
        if gameState.isWin() or gameState.isLose() or depth == 0:
            return self.evaluationFunction(gameState)
        #: infinito
        v = self.oo
        for ghost in range(self.first_ghost, gameState.getNumAgents()):
            for action in gameState.getLegalActions(ghost):
                v = min(v, self.maxValue(gameState.generateSuccessor(ghost, action), depth - 1))
        return v

    def maxValue(self, gameState, depth):
        """
        Calcula los maximos, aqui es donde se decide ademas si hemos llegado a la profundidad solicitada
        """
        #: si estamos en un estado terminal
        if gameState.isWin() or gameState.isLose() or depth == 0:
            return self.evaluationFunction(gameState)

        #: menos infinito
        v = -self.oo
        for action in gameState.getLegalActions(self.pacman):
            if action is not 'Stop' or self.enable_stop_action:
                v = max(v, self.minValue(gameState.generateSuccessor(self.pacman, action), depth - 1))
        return v


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        #: agente base
        self.pacman = 0

        #: primer ghost
        self.first_ghost = 1

        #infinito
        self.oo = float("inf")

        #: aplha
        alpha = -self.oo
        #: beta
        beta = self.oo

        #: permitimos 'Stop' action ?
        self.enable_stop_action = False

        actions = {}
        # la primera llamada la hemos de hacer aqui ya que debemos controlar el movimiento que vamos a hacer
        for action in gameState.getLegalActions(self.pacman):
            if action is not 'Stop' or self.enable_stop_action:
                actions[action] = self.minValue(gameState.generateSuccessor(self.pacman, action), alpha, beta, self.depth)

        """
        # equivalente
        actions = {action: self.minValue(gameState.generateSuccessor(self.pacman, action), alpha, beta, self.depth)
                   for action in gameState.getLegalActions(self.pacman)
                   if action is not 'Stop'
                   or self.enable_stop_action}
        """

        #devolvemos la accion con maxima utilidad
        return max(actions, key=actions.get)


    def minValue(self, gameState, alpha, beta, depth):
        """
        Calcula los miminos, los acumula en funcion del numero de fantasmas.
        En total hay x agentes y el pacman es el 0, asi que el primer ghost por defecto es 1
        """
        #: si estamos en un estado terminal
        if gameState.isWin() or gameState.isLose() or depth == 0:
            return self.evaluationFunction(gameState)
        #: infinito
        v = self.oo
        # hay varios ghost, por ello, hemos de hacer un min detras de otro
        for ghost in range(self.first_ghost, gameState.getNumAgents()):
            for action in gameState.getLegalActions(ghost):
            # llamada recursiva
                v = min(v, self.maxValue(gameState.generateSuccessor(ghost, action), alpha, beta, depth - 1))
                # si el valor es menor o igual alpha, podamos
                if v <= alpha:
                    return v
                # sino, actualizamos beta y seguimos haciendo llamadas
                beta = min(beta, v)
        return v


    def maxValue(self, gameState, alpha, beta, depth):
        """
        Calcula los maximos, aqui es donde se decide ademas si hemos llegado a la profundidad solicitada
        """
        #: si estamos en un estado terminal
        if gameState.isWin() or gameState.isLose() or depth == 0:
            return self.evaluationFunction(gameState)

        #: menos infinito
        v = -self.oo
        for action in gameState.getLegalActions(self.pacman):
            # comprobamos si la accion es stop y si la tenemos habilitada
            if action is not 'Stop' or self.enable_stop_action:
                v = max(v, self.minValue(gameState.generateSuccessor(self.pacman, action), alpha, beta, depth - 1))
                # si el valor de v es mayor o igual que beta, podamos
                if v >= beta:
                    return v
                alpha = max(alpha, v)
        return v


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
    Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction
        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        # import random
        from random import randint as rnd

        self.random = rnd

        #: agente base
        self.pacman = 0

        #: primer ghost
        self.first_ghost = 1

        #infinito
        self.oo = float("inf")

        #: permitimos 'Stop' action ?
        self.enable_stop_action = False

        actions = {}
        # la primera llamada la hemos de hacer aqui ya que debemos controlar el movimiento que vamos a hacer
        for action in gameState.getLegalActions(self.pacman):
            if action is not 'Stop' or self.enable_stop_action:
                actions[action] = self.expValue(gameState.generateSuccessor(self.pacman, action), self.depth)

        """
        # equivalente
        actions = {action: self.expValue(gameState.generateSuccessor(self.pacman, action), self.depth)
                   for action in gameState.getLegalActions(self.pacman)
                   if action is not 'Stop'
                   or self.enable_stop_action}
        """

        #devolvemos la accion con maxima utilidad
        return max(actions, key=actions.get)


    def maxValue(self, gameState, depth):
        """
        Calcula los maximos, aqui es donde se decide ademas si hemos llegado a la profundidad solicitada
        """
        #: si estamos en un estado terminal
        if gameState.isWin() or gameState.isLose() or depth == 0:
            return self.evaluationFunction(gameState)

        #: menos infinito
        v = -self.oo
        for action in gameState.getLegalActions(self.pacman):
            # comprobamos si la accion es stop y si la tenemos habilitada
            if action is not 'Stop' or self.enable_stop_action:
                v = max(v, self.expValue(gameState.generateSuccessor(self.pacman, action), depth - 1))
        return v


    def expValue(self, gameState, depth):
        """
        Calcula los miminos, los acumula en funcion del numero de fantasmas.
        En total hay x agentes y el pacman es el 0, asi que el primer ghost por defecto es 1
        Los fantasmas siguen una distribucion aleatoria uniforme, por lo tanto, se devolvera un resultado al azar
        """
        #: si estamos en un estado terminal
        if gameState.isWin() or gameState.isLose() or depth == 0:
            return self.evaluationFunction(gameState)

        #: posiblidades por parte de los ghost
        chances = []
        # recorremos todos los ghtst
        for ghost in range(self.first_ghost, gameState.getNumAgents()):
            # legal actions de cada ghost
            for action in gameState.getLegalActions(ghost):
                # guardamos las posibilidades
                chances.append(self.maxValue(gameState.generateSuccessor(ghost, action), depth - 1))

        # devolvemos una posibilidad aleatoria
        return chances[ self.random(0,len(chances) - 1) ]

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).
    
    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    """

    REVISAR MUY MUCHO

    """
    #: posicion del pacman
    pos = currentGameState.getPacmanPosition()
    #: comida
    food = currentGameState.getFood()
    #: posicion de las capsulas
    pills = currentGameState.getCapsules()
    #: ghosts
    ghosts_states = currentGameState.getGhostStates()
    #: tiempo que le queda a los fantasmas de estar asustados
    scared_times = [ghostState.scaredTimer for ghostState in ghosts_states]

    base = 100

    distMin = 100
    val = 0

    for posFant in ghosts_states:
        d = manhattanDistance(pos, posFant.getPosition())
        distMin = min(distMin, d)

    if distMin < 3:
        val -= 100
    else:
        val = distMin

    ghost_num = 0
    for posFant in ghosts_states:
        if scared_times[ghost_num] > 0:
            val = abs(val) #+ 50 / (d+1)
        ghost_num += 1

    """
    oo = float("inf")
    dist_min = +oo
    plus_scared = 0
    ghost_num = 0
    # guardamos la posicion de los fantasmas respecto a pacman
    for posFant in ghosts_states:
        #: distancia respecto a posFant
        d = manhattanDistance(pos, posFant.getPosition())
        #: distancia minima respecto los fantasmas
        dist_min = min(dist_min, d)

        #: valor maximo respecto fantasma asustado * su distancia
        plus_scared = max(plus_scared, scared_times[ghost_num] * d)
        ghost_num += 1
    """
    dist_food = 0
    for foodPos in food.asList():
        dist_food += manhattanDistance(pos, foodPos)

    val += 500 / (dist_food + 1)
    #val += 200 / (dist_food + 1) / (len(food.asList()) + 1)
    dist_pill = 0
    val += 100 / (len(pills) +1)

    #val += 200 / (len(food.asList()) + 1)
    #for pill in pills:
    #    dist_pill = manhattanDistance(pos, pill)
    #    if dist_pill == 1:
    #        val += 100
    """
    #inverse_food_distance *= 100

    evaluation = (0.3 * currentGameState.getScore()) + (0.1 * dist_min) + (0.3 * plus_scared) \
                 + (0.3 * inverse_food_distance)
    """
    #return evaluation
    return currentGameState.getScore() + val

# Abbreviation
better = betterEvaluationFunction

