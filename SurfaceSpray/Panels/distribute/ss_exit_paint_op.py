import bpy 
from ...utilsSS.addon_utils import *

class ExitPaintMode_OT_Operator(bpy.types.Operator):
    bl_idname = "addon.exit_paint_mode"
    bl_label = "Simple operator"
    bl_description = "Switch to object mode."

    def execute(self, context):
        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

        return {'FINISHED'}

    # static method
    @classmethod
    def poll(cls, context):
        # active object
        obj = context.object
        return (obj is not None) and (obj.mode == "WEIGHT_PAINT")