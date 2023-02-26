import bpy

class RULES_PT_Panel(bpy.types.Panel):
    bl_idname = "RULES_PT_Panel"
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

    def register():
        # Item rotation constraints
        bpy.types.Scene.rotate_x = bpy.props.BoolProperty(
            name='X',
            description = "This checkbox allows the rotation of the object in the X axis",
            default=False
        )

        bpy.types.Scene.rotate_y = bpy.props.BoolProperty(
            name='Y',
            description = "This checkbox allows the rotation of the object in the Y axis",
            default=False
        )

        bpy.types.Scene.rotate_z = bpy.props.BoolProperty(
            name='Z',
            description = "This checkbox allows the rotation of the object in the Z axis",
            default=False
        )

        # Item rotation range
        bpy.types.Scene.rot_range_x = bpy.props.FloatProperty(
            name='X',
            description = "Sets rotation range in the X axis",
            default=180.0,
            min = 0.0,
            max = 180.0,
        )

        bpy.types.Scene.rot_range_y = bpy.props.FloatProperty(
            name='Y',
            description = "Sets rotation range in the Y axis",
            default=180.0,
            min = 0.0,
            max = 180.0,
        )

        bpy.types.Scene.rot_range_z = bpy.props.FloatProperty(
            name='Z',
            description = "Sets rotation range in the Z axis",
            default=180.0,
            min = 0.0,
            max = 180.0,
        )

        # Item rotation steps
        bpy.types.Scene.rot_steps_x = bpy.props.FloatProperty(
            name='X',
            description = "Sets rotation steps in the X axis",
            default=1.0,
            min = 0.02,
            max = 360.0,
        )

        bpy.types.Scene.rot_steps_y = bpy.props.FloatProperty(
            name='Y',
            description = "Sets rotation steps in the Y axis",
            default=1.0,
            min = 0.02,
            max = 360.0,
        )

        bpy.types.Scene.rot_steps_z = bpy.props.FloatProperty(
            name='Z',
            description = "Sets rotation steps in the Z axis",
            default=1.0,
            min = 0.02,
            max = 360.0,
        )

        # Item distance to other objects
        bpy.types.Scene.item_distance = bpy.props.FloatProperty(
            name='Min Distance Between Assets',
            description = "Sets minumum distance of the asset to any other object "+
            "in the scene while placing it",
            default=0,
            min = 0.0,
            max = 100.0,
        )

        bpy.types.Scene.overlap_bool = bpy.props.BoolProperty(
            name='Allow Overlap',
            description = "This checkbox allows the assets to overlap with each other",
            default=False
        )

        bpy.types.Scene.bbox_bool = bpy.props.BoolProperty(
            name='Use Box',
            description = "This checkbox determines that the overlap between assets is"+
            " going to be\nchecked using a bounding box (Recomended if the asset is not going to be rotated)."+
            "\n\nLeaving it unchecked makes use of a bounding sphere (More reliable\n if the asset allows "+
            "rotation but not very accurate with oblong objects)",
            default=False
        )
    
    def unregister():
        del (bpy.types.Scene.rotate_x, bpy.types.Scene.rotate_y, bpy.types.Scene.rotate_z, 
             bpy.types.Scene.rot_range_x, bpy.types.Scene.rot_range_y, bpy.types.Scene.rot_range_z, 
             bpy.types.Scene.item_distance, bpy.types.Scene.overlap_bool,bpy.types.Scene.bbox_bool)
    

