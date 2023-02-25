import bpy 
from ...utilsSS.addon_utils import *

class Clear_OT_Operator(bpy.types.Operator):
    bl_idname = "addon.clear"
    bl_label = "Simple operator"
    bl_description = "Clear collection of object"

    def execute(self, context):
        nameCollection = context.scene.collectName
        
        collection = bpy.data.collections.get(nameCollection)

        if(collection is not None): 
            clearCollection(collection)
        else:
            self.report({'WARNING'}, 'Collection does not exists!')
            return {'FINISHED'}

        return {'FINISHED'}

    # static method
    @classmethod
    def poll(cls, context):
        # active object
        obj = context.object
        return (obj is not None) and (obj.mode == "OBJECT")