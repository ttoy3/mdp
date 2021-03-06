# valueIterationAgents.py
# -----------------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

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
  def __init__(self, mdp, discount = 0.9, iterations = 100):
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
    # init values
    for s in mdp.getStates():
      self.values[s]=0
    #print self.values
    # iteration loop
    i = iterations
    while i>0:
      for s in mdp.getStates():
        if mdp.isTerminal(s):
          self.values[s]=0
          continue
        # explore all actions form state s
        actions = mdp.getPossibleActions(s)
        can = util.Counter()  # can = candidates for argmax
        for a in actions:
          can[a]=0
          # calc transition probability
          TR = mdp.getTransitionStatesAndProbs(s,a)
          for ns,prob in TR:
            expr = mdp.getReward(s,a,ns) + discount * self.values[ns]
            #print ns,prob,expr
            can[a] += (prob * expr)
          #print 'can[a]=',can[a]
        #print 'can=',can
        best_action = can.argMax()
        best_value  = can[best_action]
        #print 'best.action=',best_action
        #print 'best.value=',best_value
        self.values[s]=best_value
      #print i
      i-=1
      print self.values
      #raw_input('....')
    #exit(0)
    """
    print 'get states:',mdp.getStates()
    print 'get possible actions:',mdp.getPossibleActions(state)
    print 'get transition state and probs:',mdp.getTransitionStatesAndProbs(state, action)
    print 'get reward:',mdp.getReward(state, action, nextState)
    """
    
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
    print 'get QValue(state=',state,' action=',action,')'
    s=state
    a=action
    q=0
    TR = self.mdp.getTransitionStatesAndProbs(s,a)
    for ns,prob in TR:
      expr = self.mdp.getReward(s,a,ns) + self.discount * self.values[ns]
      #print ns,prob,expr
      q += (prob * expr)
    return q
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
    print 'get policy(state=',state,')'
    actions = self.mdp.getPossibleActions(state)
    if len(actions)==0:
      return 0
    return max([(self.getQValue(state,a),a) for a in actions])[1]
    util.raiseNotDefined()

  def getAction(self, state):
    "Returns the policy at the state (no exploration)."
    return self.getPolicy(state)
  
