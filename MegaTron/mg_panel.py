import bpy

#definimos que lo que queremos seleccionar(target de la escena) es de tipo Object
bpy.types.Scene.target = bpy.props.PointerProperty(type=bpy.types.Object)
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

        col.prop_search(context.scene, "asset", context.scene, "objects", text="Asset")
        col.prop_search(context.scene, "target", context.scene, "objects", text="Target Object")
        
        row.operator('addon.distribute', text = "Distribute")
        row.operator('addon.clear', text = "Clear")


        box3 = layout.box()

        box3.label(text="Distribution Parameters")

        box3.column().prop(context.scene, "algorithm_enum")
        
        if (context.scene.algorithm_enum == "OP1"):
            box3.column().prop(context.scene, "threshold")
            
        box3.column().prop(context.scene, "num_assets")
        box3.column().prop(context.scene, "collectName")


        box2 = layout.box()

        box2.label(text="Item Attributes")

        rotationBox = box2.box()

        rotation_row = rotationBox.row()

        rotation_row.alignment = "CENTER"

        rotation_row.label(text="Allow Rotation:")
        rotation_row.prop(context.scene, "rotate_x")
        rotation_row.prop(context.scene, "rotate_y")
        rotation_row.prop(context.scene, "rotate_z")

        rotation_step_row = rotationBox.row()

        rotation_step_row.alignment = "CENTER"

        rotation_step_row.label(text="Steps:")
        rotation_step_row.prop(context.scene, "rot_steps_x")
        rotation_step_row.prop(context.scene, "rot_steps_y")
        rotation_step_row.prop(context.scene, "rot_steps_z")

        box2.row().prop(context.scene, "item_distance")

        box = layout.box()

        box.label(text="Subdivision")

        box.row().prop(context.scene, "subdivide")
        box.row().prop(context.scene, "num_cuts")
       
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
    