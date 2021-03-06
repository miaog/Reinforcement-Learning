# policyIterationAgents.py
# ------------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import mdp, util
import numpy as np

from learningAgents import ValueEstimationAgent

class PolicyIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PolicyIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs policy iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 20):
        """
          Your policy iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        states = self.mdp.getStates()
        # initialize policy arbitrarily
        self.policy = {}
        for state in states:
            if self.mdp.isTerminal(state):
                self.policy[state] = None
            else:
                self.policy[state] = self.mdp.getPossibleActions(state)[0]
        # initialize policyValues dict
        self.policyValues = {}
        for state in states:
            self.policyValues[state] = 0

        for i in range(self.iterations):
            # step 1: call policy evaluation to get state values under policy, updating self.policyValues
            self.runPolicyEvaluation()
            # step 2: call policy improvement, which updates self.policy
            self.runPolicyImprovement()

    def runPolicyEvaluation(self):
        """ Run policy evaluation to get the state values under self.policy. Should update self.policyValues.
        Implement this by solving a linear system of equations using numpy. """

        states = self.mdp.getStates()
        numStates = len(states)
    

        reward = np.zeros(numStates)
        transProbs = np.zeros(shape=(numStates,numStates))
    
        i = 0
        for state in states:
    
            reward[i] = self.mdp.getReward(state)
            

            j = 0
            nextStates = {}
            action = self.policy[state]
           
            if action is not None:
                for nextState, probability in self.mdp.getTransitionStatesAndProbs(state, action):
                    nextStates[nextState] = probability
            for state in states:
            
                if state in nextStates:
                    transProbs[i][j] = nextStates[state]
                else:
                    transProbs[i][j] = 0
                j += 1

            i += 1


        matrix = np.eye(numStates, numStates) - self.discount * transProbs
        x = np.linalg.solve(matrix, reward)

        k = 0
        for state in states:
            self.policyValues[state] = x[k]
            k += 1

    def runPolicyImprovement(self):
        """ Run policy improvement using self.policyValues. Should update self.policy. """

        states = self.mdp.getStates()

        for state in states:
            if self.mdp.isTerminal(state):
                self.policy[state] = None
            else:
                maxValue = -1*float('inf')
                maxAction = ""
                for action in self.mdp.getPossibleActions(state):
                    val = self.computeQValueFromValues(state, action)
                    if val > maxValue:
                        maxValue = val
                        maxAction = action
                self.policy[state] = maxAction


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.policyValues.
        """
        value = 0
        for nextState, probability in self.mdp.getTransitionStatesAndProbs(state, action):
            value += probability * (self.mdp.getReward(state) + (self.discount * self.policyValues[nextState]))
        return value

    def getValue(self, state):
        return self.policyValues[state]

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

    def getPolicy(self, state):
        return self.policy[state]

    def getAction(self, state):
        return self.policy[state]
