# Simple class that defines the characteristics and restrictions of an Item

class ItemRules:
    def __init__(self):
        # Rotation axis 
        # Whether an item can rotate or not in a give axis
        self.rotations = [0,0,0]

        # Rotation Range
        # x (n ~ m), y (n ~ m), z (n ~ m)
        self.rotation_range = [180.0, 180.0, 180.0]

        # Rotation steps
        self.rotation_steps = [1.,1.,1.]

        # Distance offset
        self.distance_between_items = 0 

        # Close offset
        #self.object_offset = 0

        # Item can overlap with another item
        self.overlap = False

        # Uses box or sphere
        self.use_bounding_box = False

        # Scale factor (asset will be scaled a random amount between min_scale_factor and max_scale_factor)
        self.min_scale_factor = 1
        self.max_scale_factor = 1
        