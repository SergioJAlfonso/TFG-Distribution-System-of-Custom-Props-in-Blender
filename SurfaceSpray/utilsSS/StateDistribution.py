
class StateDistribution():

   def __init__(self, vertices, objectsPlaced):
      self.vertices_ = vertices
      self.objectsPlaced_ = objectsPlaced
      self.pathCost = 0
      self.actionsApplied_ = []
      self.actionsHistory = []

   def __lt__(self, otherState):
        return self.pathCost < otherState.pathCost
   
   def __gt__(self, otherState):
       return self.pathCost > otherState.pathCost

