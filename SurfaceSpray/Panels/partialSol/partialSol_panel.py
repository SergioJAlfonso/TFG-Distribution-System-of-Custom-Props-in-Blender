import bpy

from bpy.props import (PointerProperty,IntProperty, CollectionProperty)

from bpy.types import (PropertyGroup,
                       UIList)


from .partialSol_ops import PARTIAL_SOL_OT_selectItems

class PARTIAL_SOL_PG_objectCollection(PropertyGroup):
    #name: StringProperty() -> Instantiated by default
    obj: PointerProperty(
        name="Object",
        type=bpy.types.Object)
    

class PARTIAL_SOL_UL_items(UIList):
    
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        obj = item.obj
        partialsol_icon = "OUTLINER_OB_%s" % obj.type
        split = layout.split(factor=0.3)
        # split.label(text="Index: %d" % (index))
        split.label(text="")
        split.prop(obj, "name", text="", emboss=False, translate=False, icon=partialsol_icon)
            
    def invoke(self, context, event):
        pass   

class PARTIAL_SOL_PT_Panel(bpy.types.Panel):
    bl_idname = "PARTIAL_SOL_PT_Panel"
    bl_label = "Objects Part Of The Solution"
    bl_category = "SurfaceSpray"
    bl_description = "Collection of objects in the solution."
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout

        scn = bpy.context.scene

        rows = 2
        row2 = layout.row()
        row2.template_list("PARTIAL_SOL_UL_items", "", scn, "partialsol", scn, "partialsol_index", rows=rows)

        col = row2.column(align=True)
        col.operator("partialsol.list_action", icon='ADD', text="").action = 'ADD'
        col.operator("partialsol.list_action", icon='REMOVE', text="").action = 'REMOVE'
        col.separator()
        col.operator("partialsol.list_action", icon='TRIA_UP', text="").action = 'UP'
        col.operator("partialsol.list_action", icon='TRIA_DOWN', text="").action = 'DOWN'

        row = layout.row()
        col = row.column(align=True)
        row = col.row(align=True)
        row.operator("partialsol.update_list", icon="FILE_REFRESH")

        row = col.row(align=True)
        row.operator("partialsol.clear_list", icon="X")
        row.operator("partialsol.remove_duplicates", icon="GHOST_ENABLED")
        
        row = layout.row()
        col = row.column(align=True)
        row = col.row(align=True)
        row.operator("partialsol.add_viewport_selection", icon="HAND") #LINENUMBERS_OFF, ANIM
        row = col.row(align=True)
        row.operator("partialsol.select_items", icon="VIEW3D", text="Select Item in 3D View")
        selectItems = row.operator("partialsol.select_items", icon="GROUP", text="Select All Items in 3D View")

        selectItems.select_all = True

        row = col.row(align=True)

    def register():
        bpy.types.Scene.partialsol_index = IntProperty()
        bpy.types.Scene.partialsol = CollectionProperty(type=PARTIAL_SOL_PG_objectCollection)

    def unregister():
        del bpy.types.Scene.partialsol
        del bpy.types.Scene.partialsol_index

        
