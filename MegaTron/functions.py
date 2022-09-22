import bpy 

class MT_Functions(bpy.types.Operator):
    bl_idname = "view3d.cursor_center"
    bl_label = " "
    bl_description = " "

    def execute(self, context):
        # bpy.ops.view3d.snap_cursor_to_center()
        return {'FINISHED'}
