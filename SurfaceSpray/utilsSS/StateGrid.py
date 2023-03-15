
class StateGrid():

   def __init__(self, vertices, objectsPlaced):
      self.vertices_ = vertices
      self.objectsPlaced_ = objectsPlaced
      self.actionsApplied_ = []
      self.pathCost = 0

   def __lt__(self, otherState):
        return self.pathCost < otherState.pathCost
   
   def __gt__(self, otherState):
       return self.pathCost > otherState.pathCost

