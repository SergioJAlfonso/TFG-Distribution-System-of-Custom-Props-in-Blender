# Simple class that defines the characteristics and restrictions of an Item

class ItemAttributes:
    def __init__(self):
        # Rotation axis 
        # Whether an item can rotate or not in a give axis
        self.rotations = [1,1,1]

        # Range of rotations
        # x (n ~ m), y (n ~ m), z (n ~ m)

        # Distance offset
        self.distance_offset = 0 

        # Close offset
        #self.object_offset = 0

        # Number of appearences for an item in the scene
        # -1 for any
        self.max_repetitions = -1

        pass
        