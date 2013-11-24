import mdp, util

from learningAgents import ValueEstimationAgent


class ValueIterationAgent(ValueEstimationAgent):
    """
      * Please read learningAgents.py before reading this.*

      A ValueIterationAgent takes a Markov decision process
      (see mdp.py) on initialization and runs value iteration
      for a given number of iterations using the supplied
      discount factor.
    """

    def __init__(self, mdp, discount=0.9, iterations=100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0

        "*** YOUR CODE HERE ***"
        #: S, conjunto de estados
        states = mdp.getStates()

        #: Descuento
        self.phi = 0.9

        #: Vector de utilidades por estado en S, inicialmente a zero
        #vector_utilidad = {}
        vector_utilidad_iter = {}
        for i in range(len(states)):
            vector_utilidad_iter[states[i]] = 0

        #: Contador del numero de iteraciones
        k = 0

        while k <= iterations:
            self.values = vector_utilidad_iter.copy()
            delta = 0

            for state in states:
                actions = mdp.getPossibleActions(state)
                valores = []
                for action in actions:
                    #Rusell
                    #transition = [t[1] * self.values[t[0]]
                    #              for t in mdp.getTransitionStatesAndProbs(state, action)]

                    #Sutton
                    transition = [t[1] * (mdp.getReward(state, action, t[0]) + self.phi * self.values[t[0]])
                                  for t in mdp.getTransitionStatesAndProbs(state, action)]

                    valores.append(sum(transition))

                if state is not 'TERMINAL_STATE':
                    vector_utilidad_iter[state] = max(valores)

                if abs(vector_utilidad_iter[state] - self.values[state]) > delta:
                    delta = abs(vector_utilidad_iter[state] - self.values[state])

            k += 1

    def getValue(self, state):
        """
        Return the value of the state (computed in __init__).
        """

        return self.values[state]


    def getQValue(self, state, action):
        """
        The q-value of the state action pair
        (after the indicated number of value iteration
        passes).  Note that value iteration does not
        necessarily create this quantity and you may have
        to derive it on the fly.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

    def getPolicy(self, state):
        """
        The policy is the best action in the given state
        according to the values computed by value iteration.
        You may break ties any way you see fit.  Note that if
        there are no legal actions, which is the case at the
        terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"

        if state is not 'TERMINAL_STATE':

            actions = self.mdp.getPossibleActions(state)
            valores = {}
            for action in actions:
                transition = [t[1] * (self.mdp.getReward(state, action, t[0]) + self.phi * self.values[t[0]])
                              for t in self.mdp.getTransitionStatesAndProbs(state, action)]

                valores[sum(transition)] = action

            return valores[max(valores)]
        return None

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.getPolicy(state)
  
