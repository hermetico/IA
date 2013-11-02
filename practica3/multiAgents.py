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

        ghost_num = 0
        # comprobamos si los fantasmas estan en modo asustado
        for posFant in newGhostStates:
            d = manhattanDistance(newPos, posFant.getPosition())
            # si estan en modo asustado durante mas pasos que la distancia a ellos
            # sumamos un plus
            if newScaredTimes[ghost_num] > 0:
                val += 10
            if newScaredTimes[ghost_num] > d:
                val += 100
            ghost_num += 1

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

        #: infinito
        self.oo = float("inf")

        #: permitimos 'Stop' action ?
        self.enable_stop_action = False

        #actions = {}
        # la primera llamada la hemos de hacer aqui ya que devemos controlar el movimiento que vamos a hacer
        #for action in gameState.getLegalActions(self.pacman):
        #    actions[action] = self.minValue(gameState.generateSuccessor(self.pacman, action), self.depth)
        actions = {action: self.minValue(gameState.generateSuccessor(self.pacman, action), self.depth)
                   for action in gameState.getLegalActions(self.pacman)
                   if action is not 'Stop'
                   or self.enable_stop_action}
        #devolvemos la accion con maxima utilidad
        return max(actions, key=actions.get)


    def minValue(self, gameState, depth, ghost=1):
        """
        Calcula los miminos, los acumula en funcion del numero de fantasmas.
        En total hay x agentes y el pacman es el 0, asi que el primer ghost por defecto es 1
        Mientras haya fantasmas vuelve a llamar a la funcion min, en el momento que ya se han calculado
        los fantasmas, se llama a la funcion max
        """
        #: si estamos en un estado terminal
        if gameState.isWin() or gameState.isLose() or depth == 0:
            return self.evaluationFunction(gameState)
        #: infinito
        v = self.oo
        # hay varios ghost, por ello, hemos de hacer un min detras de otro
        if ghost < (gameState.getNumAgents() - 1):
            return min([v] + [self.minValue(gameState.generateSuccessor(ghost, action), depth - 1, ghost + 1)
                              for action in gameState.getLegalActions(ghost)])

        # si es el ultimo ghost, hacemos el max
        return min([v] + [self.maxValue(gameState.generateSuccessor(ghost, action), depth - 1)
                          for action in gameState.getLegalActions(ghost)])


    def maxValue(self, gameState, depth):
        """
        Calcula los maximos, aqui es donde se decide ademas si hemos llegado a la profundidad solicitada
        """
        #: si estamos en un estado terminal
        if gameState.isWin() or gameState.isLose() or depth == 0:
            return self.evaluationFunction(gameState)

        #: menos infinito
        v = -self.oo
        return max([v] + [self.minValue(gameState.generateSuccessor(self.pacman, action), depth - 1)
                          for action in gameState.getLegalActions(self.pacman)
                          if action is not 'Stop'
                          or self.enable_stop_action])


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

        #infinito
        self.oo = float("inf")

        #: aplha
        alpha = -self.oo
        #: beta
        beta = self.oo

        #: permitimos 'Stop' action ?
        self.enable_stop_action = False

        #actions = {}
        # la primera llamada la hemos de hacer aqui ya que devemos controlar el movimiento que vamos a hacer
        #for action in gameState.getLegalActions(self.pacman):
        #    actions[action] = self.minValue(gameState.generateSuccessor(self.pacman, action), self.depth)
        actions = {action: self.minValue(gameState.generateSuccessor(self.pacman, action), alpha, beta, self.depth)
                   for action in gameState.getLegalActions(self.pacman)
                   if action is not 'Stop'
        or self.enable_stop_action}
        #devolvemos la accion con maxima utilidad
        return max(actions, key=actions.get)


    def minValue(self, gameState, alpha, beta, depth, ghost=1):
        """
        Calcula los miminos, los acumula en funcion del numero de fantasmas.
        En total hay x agentes y el pacman es el 0, asi que el primer ghost por defecto es 1
        Mientras haya fantasmas vuelve a llamar a la funcion min, en el momento que ya se han calculado
        los fantasmas, se llama a la funcion max
        """
        #: si estamos en un estado terminal
        if gameState.isWin() or gameState.isLose() or depth == 0:
            return self.evaluationFunction(gameState)
        #: infinito
        v = self.oo
        # hay varios ghost, por ello, hemos de hacer un min detras de otro
        if ghost < (gameState.getNumAgents() - 1):
            for action in gameState.getLegalActions(ghost):
                # llamada recursiva
                v = min(v, self.minValue(gameState.generateSuccessor(ghost, action), alpha, beta, depth - 1,  ghost+1))
                # si el valor es menor o igual alpha
                if v <= alpha:
                    return v
                # sino, actualizamos beta y seguimos haciendo llamadas
                beta = min(beta, v)
            return v

        # si es el ultimo ghost, hacemos el max
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
        #: agente base
        self.pacman = 0

        #infinito
        self.oo = float("inf")

        #: permitimos 'Stop' action ?
        self.enable_stop_action = False

        actions = {action: self.expValue(gameState.generateSuccessor(self.pacman, action), self.depth)
                   for action in gameState.getLegalActions(self.pacman)
                   if action is not 'Stop'
        or self.enable_stop_action}
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


    def expValue(self, gameState, depth, ghost=1):
        """
        Calcula la exp, los acumula en funcion del numero de fantasmas.
        En total hay x agentes y el pacman es el 0, asi que el primer ghost por defecto es 1
        Mientras haya fantasmas vuelve a llamar a la funcion min, en el momento que ya se han calculado
        los fantasmas, se llama a la funcion max
        """
        #: si estamos en un estado terminal
        if gameState.isWin() or gameState.isLose() or depth == 0:
            return self.evaluationFunction(gameState)

        # hay varios ghost, por ello, hemos de hacer un min detras de otro
        chances = []
        if ghost < (gameState.getNumAgents() - 1):
            for action in gameState.getLegalActions(ghost):
                # llamada recursiva
                chances.append(self.expValue(gameState.generateSuccessor(ghost, action), depth - 1,  ghost+1))
            return sum(chances) / len(chances)

        # si es el ultimo ghost, hacemos el max
        for action in gameState.getLegalActions(ghost):
            # llamada recursiva
            chances.append(self.maxValue(gameState.generateSuccessor(ghost, action), depth - 1))
        return sum(chances) / len(chances)

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).
    
    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

