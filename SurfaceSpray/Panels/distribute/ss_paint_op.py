import bpy 
from ...utilsSS.addon_utils import *

class PaintMode_OT_Operator(bpy.types.Operator):
    bl_idname = "addon.enter_paint_mode"
    bl_label = "Simple operator"
    bl_description = "Switch to weight vertex painting mode."

    def execute(self, context):
        bpy.ops.object.select_all(action='DESELECT')
        #Change any selected object to Target object so it can be switched to weight painting. 
        bpy.context.view_layer.objects.active = context.scene.target

        bpy.ops.object.mode_set(mode='WEIGHT_PAINT', toggle=False)

        return {'FINISHED'}

    # static method
    @classmethod
    def poll(cls, context):
        # active object
        obj = context.object
        return (obj is not None) and (obj.mode == "OBJECT")