import bpy

#definimos que lo que queremos seleccionar(target de la escena) es de tipo Object
bpy.types.Scene.target = bpy.props.PointerProperty(type=bpy.types.Object)

bpy.types.Scene.subdivTarget = bpy.props.PointerProperty(type=bpy.types.Object)

bpy.types.Scene.asset = bpy.props.PointerProperty(type=bpy.types.Object)

      #_PT_Panel ->Convention
class Main_PT_Panel(bpy.types.Panel):
    bl_idname = "Main_PT_Panel"
    bl_label = "Object To Distribute"
    bl_category = "MegaTron"
    bl_description = "Entry Data Objects"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        col = layout.column()
        row.operator('view3d.cursor_center', text = "Distribute")

        col.prop(context.scene, "threshold")
        col.prop(context.scene, "num_assets")
        
        

        self.layout.prop_search(context.scene, "asset", context.scene, "objects", text="Asset")

        self.layout.prop_search(context.scene, "target", context.scene, "objects", text="Target Object")
        # placeholder = context.scene.placeholder
        # col.prop(placeholder, "inc_dec_int", text="Asset Instances")

class Groups_PT_Panel(bpy.types.Panel):
    bl_idname = "Groups_PT_Panel"
    bl_label = "Object Distribution"
    bl_category = "MegaTron"
    bl_description = "Groups"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout

#Subdivision surface panel
class Subdivision_PT_Panel(bpy.types.Panel):
    bl_idname = "Subdivision_PT_Panel"
    bl_label = "Subdivide Target Surface"
    bl_category = "MegaTron"
    bl_description = "Subdivision"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout
        
        #Asset that determines the distance between subdivisions
        layout.prop_search(context.scene, "subdivTarget", context.scene, "objects", text="Asset")
        #Surface to subdivide
        layout.prop_search(context.scene, "subdivTarget", context.scene, "objects", text="Target Object")
    