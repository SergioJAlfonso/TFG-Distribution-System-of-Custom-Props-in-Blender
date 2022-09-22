import bpy

      #_PT_Panel ->Convention
class MegaTron_PT_Panel(bpy.types.Panel):
    bl_idname = "Test_PT_Panel"
    bl_label = "MegaTron Panel"
    bl_category = "MegaTron Addon"
    bl_description = "Center 3D Cursor"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.operator('view3d.cursor_center', text = "Center 3D cursor ")