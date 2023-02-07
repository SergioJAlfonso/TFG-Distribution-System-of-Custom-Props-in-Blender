# Simple class that defines the characteristics and restrictions of an Item

class ItemRules:
    def __init__(self):
        # Rotation axis 
        # Whether an item can rotate or not in a give axis
        self.rotations = [1,1,1]

        # Range of rotations
        # x (n ~ m), y (n ~ m), z (n ~ m)

        # Rotation steps
        self.rotation_steps = [0.,0.,0.]

        # Distance offset
        self.distance_between_items = 0 

        # Item can overlap with another item
        self.overlap = False

        # Close offset
        #self.object_offset = 0

        # Number of appearences for an item in the scene
        # -1 for any
        # self.max_repetitions = -1
    
    def set_ItemDistance(self, distance):
        self.distance_offset = distance