# Simple class that defines the characteristics and restrictions of an Item

class ItemRules:
    def __init__(self):
        # Rotation axis 
        # Whether an item can rotate or not in a give axis
        self.rotations = [1,1,1]

        # Rotation Range
        # x (n ~ m), y (n ~ m), z (n ~ m)
        self.rotation_range = [180.0, 180.0, 180.0]

        # Rotation steps
        self.rotation_steps = [0.,0.,0.]

        # Distance offset
        self.distance_between_items = 0 

        # Close offset
        #self.object_offset = 0

        # Item can overlap with another item
        self.overlap = False

        # TODO: Distance percentage to the center of the target
        
    
    def set_ItemDistance(self, distance):
        self.distance_offset = distance