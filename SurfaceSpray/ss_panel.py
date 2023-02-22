import bpy

#definimos que lo que queremos seleccionar(target de la escena) es de tipo Object
bpy.types.Scene.target = bpy.props.PointerProperty(type=bpy.types.Object)
bpy.types.Scene.asset = bpy.props.PointerProperty(type=bpy.types.Object)

        #_PT_Panel ->Convention
class MAIN_PT_Panel(bpy.types.Panel):
    bl_idname = "Main_PT_Panel"
    bl_label = "Object To Distribute"
    bl_category = "SurfaceSpray"
    bl_description = "Entry Data Objects"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"


    def draw(self, context):
        layout = self.layout

        row = layout.row()
        col = layout.column()

        # Target and asset prop search
        col.prop_search(context.scene, "asset", context.scene, "objects", text="Asset")
        col.prop_search(context.scene, "target", context.scene, "objects", text="Target Object")
        
        # Add-on distribute buttons
        row.operator('addon.distribute', text = "Distribute")
        row.operator('addon.distributedemo', text = "DistributeDemo")
        row.operator('addon.clear', text = "Clear")

        # Distribution Parameters box
        box3 = layout.box()

        box3.label(text="Distribution Parameters")

        box3.column().prop(context.scene, "algorithm_enum")
        
        if (context.scene.algorithm_enum == "OP1"):
            box3.column().prop(context.scene, "threshold")

        box3.column().prop(context.scene, "num_assets")
        box3.column().prop(context.scene, "collectName")

        
        # # Show list of vertex groups
        # boxVGroup = layout.box()
        # boxVGroup.label(text="Vertex Groups")

        # obj = context.scene.target
        # row = boxVGroup.row()
        # row.template_list("MESH_UL_vgroups", "", obj, "vertex_groups", obj.vertex_groups, "active_index")
        
        # # Add new vertex group button
        # col = boxVGroup.column()
        # col.operator("object.vertex_group_add", icon='ADD', text="New Vertex Group")

        # # Remove vertex group button
        # if obj.vertex_groups:
        #     col.operator("object.vertex_group_remove", icon='REMOVE', text="Remove Vertex Group")
        
        # # Rename vertex group
        # row = boxVGroup.row()
        # row.prop(context.object.vertex_groups.active, "name")

        # Subdivision box
        box = layout.box()

        box.label(text="Subdivision")

        box.row().prop(context.scene, "subdivide")

        if(context.scene.subdivide):
            box.row().prop(context.scene, "num_cuts")

        # Item Rules box
        box2 = layout.box()

        box2.label(text="Asset Rules")

        rotationBox = box2.box()

        rotation_row = rotationBox.row()

        rotation_row.alignment = "CENTER"

        # Rotation
        rotation_row.label(text="Allow Rotation:")
        rotation_row.prop(context.scene, "rotate_x")
        rotation_row.prop(context.scene, "rotate_y")
        rotation_row.prop(context.scene, "rotate_z")

        if(context.scene.rotate_x or context.scene.rotate_y or context.scene.rotate_z):
            #Range and steps
            
            rotation_range_row = rotationBox.row()
            rotation_step_row = rotationBox.row()

            rotation_range_row.alignment = "CENTER"
            rotation_step_row.alignment = "CENTER"

            rotation_range_row.label(text="Range:")
            rotation_step_row.label(text="Steps:")

            if(context.scene.rotate_x):
                rotation_range_row.prop(context.scene, "rot_range_x")
                rotation_step_row.prop(context.scene, "rot_steps_x")

            if(context.scene.rotate_y):
                rotation_range_row.prop(context.scene, "rot_range_y")
                rotation_step_row.prop(context.scene, "rot_steps_y")
            
            if(context.scene.rotate_z):
                rotation_range_row.prop(context.scene, "rot_range_z")
                rotation_step_row.prop(context.scene, "rot_steps_z")
            

        # Distance
        box2.row().prop(context.scene, "item_distance")

        # Overlap
        box2.row().prop(context.scene, "overlap_bool")
        
        box2.row().prop(context.scene, "num_searches")
        box2.row().prop(context.scene, "actual_search")
        box2.row().operator('addon.redistribute', text = "Change search")
        # placeholder = context.scene.placeholder
        # col.prop(placeholder, "inc_dec_int", text="Asset Instances")

class GROUPS_PT_Panel(bpy.types.Panel):
    bl_idname = "Groups_PT_Panel"
    bl_label = "Object Distribution"
    bl_category = "SurfaceSpray"
    bl_description = "Groups"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout
    