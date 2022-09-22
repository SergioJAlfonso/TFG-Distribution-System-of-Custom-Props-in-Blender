import bpy

class MT_Panel(bpy.types.Panel):
    bl_idname = "Panel"
    bl_label = "Panel"
    bl_category = "Addon"
    bl_description = " "
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.operator('view3d.cursor_center', text = " ")