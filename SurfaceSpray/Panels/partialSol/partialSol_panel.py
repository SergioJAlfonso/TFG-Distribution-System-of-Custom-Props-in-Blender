import bpy

from bpy.props import (PointerProperty)

from bpy.types import (PropertyGroup,
                       UIList)
    
class CUSTOM_UL_items(UIList):
    
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        obj = item.obj
        custom_icon = "OUTLINER_OB_%s" % obj.type
        split = layout.split(factor=0.3)
        split.label(text="Index: %d" % (index))
        split.prop(obj, "name", text="", emboss=False, translate=False, icon=custom_icon)
            
    def invoke(self, context, event):
        pass   

class CUSTOM_PG_objectCollection(PropertyGroup):
    #name: StringProperty() -> Instantiated by default
    obj: PointerProperty(
        name="Object",
        type=bpy.types.Object)

class PARTIAL_SOL_PT_Panel(bpy.types.Panel):
    bl_idname = "SolutionObject_PT_Panel"
    bl_label = "Objects part of the solution"
    bl_category = "SurfaceSpray"
    bl_description = "Collection of objects in the solution."
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout

        scn = bpy.context.scene

        rows = 2
        row2 = layout.row()
        row2.template_list("CUSTOM_UL_items", "", scn, "custom", scn, "custom_index", rows=rows)

        col = row2.column(align=True)
        col.operator("custom.list_action", icon='ADD', text="").action = 'ADD'
        col.operator("custom.list_action", icon='REMOVE', text="").action = 'REMOVE'
        col.separator()
        col.operator("custom.list_action", icon='TRIA_UP', text="").action = 'UP'
        col.operator("custom.list_action", icon='TRIA_DOWN', text="").action = 'DOWN'

        row = layout.row()
        col = row.column(align=True)
        row = col.row(align=True)
        row.operator("custom.print_items", icon="LINENUMBERS_ON")
        row = col.row(align=True)
        row.operator("custom.clear_list", icon="X")
        row.operator("custom.remove_duplicates", icon="GHOST_ENABLED")
        
        row = layout.row()
        col = row.column(align=True)
        row = col.row(align=True)
        row.operator("custom.add_viewport_selection", icon="HAND") #LINENUMBERS_OFF, ANIM
        row = col.row(align=True)
        row.operator("custom.select_items", icon="VIEW3D", text="Select Item in 3D View")
        row.operator("custom.select_items", icon="GROUP", text="Select All Items in 3D View")
        row = col.row(align=True)
        row.operator("custom.delete_object", icon="X") 