import bpy

class RULES_PT_Panel(bpy.types.Panel):
    bl_idname = "Rules_PT_Panel"
    bl_label = "Asset Rules"
    bl_category = "SurfaceSpray"
    bl_description = "Rules that specify how the asset is placed"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout

        # Item Rules box
        box = layout.box()

        box.label(text="Asset Rules")

        rotationBox = box.box()

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
        box.row().prop(context.scene, "item_distance")

        # Overlap
        row = box.row()

        row.prop(context.scene, "overlap_bool")

        if(context.scene.overlap_bool):
            row.prop(context.scene, "bbox_bool")