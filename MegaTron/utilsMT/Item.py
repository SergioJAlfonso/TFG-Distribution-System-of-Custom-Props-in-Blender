# Custom class for every object. Algorithm will use this as a ruleset for the asset it represents.
# 1 is created for every asset that is selected. 

import ItemAttributes

class Item:
    def __init__(self, name, obj, attr, type = "none"):
        self.name = name
        self.type = type
        self.blender_obj = obj
        self.attributes = attr

    