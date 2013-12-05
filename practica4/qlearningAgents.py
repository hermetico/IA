from game import *
from learningAgents import ReinforcementAgent
from featureExtractors import *

import random, util, math


class QLearningAgent(ReinforcementAgent):
    """
    Q-Learning Agent

    Functions you should fill in:
      - getQValue
      - getAction
      - getValue
      - getPolicy
      - update
      
    Instance variables you have access to
      - self.epsilon (exploration prob)
      - self.alpha (learning rate)
      - self.gamma (discount rate)

    Functions you should use
      - self.getLegalActions(state) 
        which returns legal actions
        for a state
    """

    def __init__(self, **args):
        "You can initialize Q-values here..."
        ReinforcementAgent.__init__(self, **args)

        "*** YOUR CODE HERE ***"
        #: diccionario de valor q para parejas(s,a) [estado, accion] inicializado a 0
        self.q = util.Counter()

        #: diccionario de frecuencias para parejas (s,a) inicializado a 0
        self.n = util.Counter()


    def getQValue(self, state, action):
        """
          Returns Q(state,action)    
          Should return 0.0 if we never seen
          a state or (state,action) tuple 
        """
        "*** YOUR CODE HERE ***"
        # devolvemos el qValor, si no existe retorna 0, en ese caso retornamos 0.0
        return self.q[(state, action)] or 0.0


    def getValue(self, state):
        """
          Returns max_action Q(state,action)        
          where the max is over legal actions.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return a value of 0.0.
        """
        "*** YOUR CODE HERE ***"
        # devolvemos el qValor mas alto para las parejas (estado, accion) entre las acciones legales
        # si no hay ninguna retornara 0.0
        if not self.getLegalActions(state):
            return 0.0
        return max([self.getQValue(state, action) for action in self.getLegalActions(state)])


    def getPolicy(self, state):
        """
          Compute the best action to take in a state.  Note that if there
          are no legal actions, which is the case at the terminal state,
          you should return None.
        """
        "*** YOUR CODE HERE ***"
        # devolvemos la mejor accion posible para el estado y sus acciones legales
        # si no hay acciones retornamos None
        # si hay acciones empatadas, retornamos una al azar

        # para ello, recuperamos las posibles acciones con su q valor
        policies = util.Counter(
            {action: self.getQValue(state, action) for action in self.getLegalActions(state)}
        )

        # comprobamos que hay acciones
        if not policies:
            return None
            #: el q valor mas alto
        best_q_value = policies[policies.sortedKeys()[0]]

        #: creamos una lista con las acciones que tienen un valor igual al valor maximo
        best_policies = [action for action in policies.sortedKeys() if policies[action] == best_q_value]

        # devolvemos una al azar
        return random.choice(best_policies)

    def getAction(self, state):
        """
          Compute the action to take in the current state.  With
          probability self.epsilon, we should take a random action and
          take the best policy action otherwise.  Note that if there are
          no legal actions, which is the case at the terminal state, you
          should choose None as the action.

          HINT: You might want to use util.flipCoin(prob)
          HINT: To pick randomly from a list, use random.choice(list)
        """
        # Pick Action
        legalActions = self.getLegalActions(state)
        action = None
        "*** YOUR CODE HERE ***"

        # comprobamos si hay legal actions, sino, retornamos None
        if not legalActions:
            return action

        # lanzamos la moneda con epsilon para decidir que accion retornamos, al azar o best policy
        if util.flipCoin(self.epsilon):
            # retornamos una accion al azar, si no devuelve nada retornamos None
            return random.choice(legalActions) or None

        # retornamos bestPolicy
        return self.getPolicy(state)


    def update(self, state, action, nextState, reward):
        """
          The parent class calls this to observe a 
          state = action => nextState and reward transition.
          You should do your Q-Value update here
          
          NOTE: You should never call this function,
          it will be called on your behalf
        """
        "*** YOUR CODE HERE ***"
        # actualizamos el qValor
        """
        para ello el qValor pasa a ser la suma del qValor actual + alpha * ( recompensa + (gamma * el qValor mas
         alto para el estado s' )) - el qValor actual
        """
        if state:
            #: gamma dinamico
            #self.n[(state, action)] += 1
            #learning_rate = self.alpha / self.n[(state, action)]
            learning_rate = self.alpha
            #: update
            self.q[state, action] += learning_rate * (
                reward + ((self.gamma * self.getValue(nextState)) - self.getQValue(state, action)))


class PacmanQAgent(QLearningAgent):
    "Exactly the same as QLearningAgent, but with different default parameters"

    def __init__(self, epsilon=0.05, gamma=0.8, alpha=0.2, numTraining=0, **args):
        """
        These default parameters can be changed from the pacman.py command line.
        For example, to change the exploration rate, try:
            python pacman.py -p PacmanQLearningAgent -a epsilon=0.1

        alpha    - learning rate
        epsilon  - exploration rate
        gamma    - discount factor
        numTraining - number of training episodes, i.e. no learning after these many episodes
        """
        args['epsilon'] = epsilon
        args['gamma'] = gamma
        args['alpha'] = alpha
        args['numTraining'] = numTraining
        QLearningAgent.__init__(self, **args)

    def getAction(self, state):
        """
        Simply calls the getAction method of QLearningAgent and then
        informs parent of action for Pacman.  Do not change or remove this
        method.
        """
        action = QLearningAgent.getAction(self, state)
        self.doAction(state, action)
        return action


class ApproximateQAgent(PacmanQAgent):
    """
     ApproximateQLearningAgent
     
     You should only have to overwrite getQValue
     and update.  All other QLearningAgent functions
     should work as is.
    """

    def __init__(self, extractor='IdentityExtractor', **args):
        self.featExtractor = util.lookup(extractor, globals())()
        PacmanQAgent.__init__(self, **args)

        # You might want to initialize weights here.
        "*** YOUR CODE HERE ***"
        self.features = util.Counter()
        self.weigths = util.Counter()

    def getQValue(self, state, action):
        """
          Should return Q(state,action) = w * featureVector
          where * is the dotProduct operator
        """
        "*** YOUR CODE HERE ***"
        # recuperamos las features del estado|accion
        self.features = self.featExtractor.getFeatures(state, action)

        # devolvemos la suma de cada caracteristica * su peso
        return sum(self.weigths[feature] * self.features[feature] for feature in self.features)

    def update(self, state, action, nextState, reward):
        """
           Should update your weights based on transition  
        """
        "*** YOUR CODE HERE ***"

        #: definimos el valor de correccion
        correction = (reward + (self.gamma * self.getValue(nextState))) - self.getQValue(state, action)
        # actualizamos el peso de cada feature, para ello, recuperamos las features
        self.features = self.featExtractor.getFeatures(state, action)
        # y actulizamos las que tenemos, o las ponemos nuevas
        for feature in self.features:
            self.weigths[feature] += self.alpha * correction * self.features[feature]

    def final(self, state):
        "Called at the end of each game."
        # call the super-class final method
        PacmanQAgent.final(self, state)

        # did we finish training?
        if self.episodesSoFar == self.numTraining:
            # you might want to print your weights here for debugging
            "*** YOUR CODE HERE ***"
            pass
