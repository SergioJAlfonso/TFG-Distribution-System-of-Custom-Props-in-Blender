from enum import Enum

class ActionType(Enum):
    CREATE = 1
    DESTROY = 2

class Actions():
    def __init__(self, indexVertex_, rotation_, scale_ = 1, asset_index = 0, type_ = ActionType.CREATE):
        self.indexVertex = indexVertex_
        self.rotation = rotation_
        self.scale = scale_
        self.asset_index = asset_index
        self.type = type_

    def setActionToRemove(self, action):
        self.actionToRemove = action 