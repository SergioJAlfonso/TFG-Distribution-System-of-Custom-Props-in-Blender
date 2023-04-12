import bpy
from mathutils import Color
from bpy.types import Menu, Panel, UIList

class PRUEBA_PT_tools_object_options(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "SurfaceSpray"
    bl_context = ".objectmode"  # dot on purpose (access from topbar)
    bl_label = "Optionss"
    bl_region_type = "UI"

    def draw(self, context):
        # layout = self.layout
        pass


class PRUEBA_PT_tools_object_options_transform(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "SurfaceSpray"
    bl_label = "Transform"
    bl_parent_id = "RULES_PT_Panel"

    def draw(self, context):
        layout = self.layout

        layout.use_property_split = True
        layout.use_property_decorate = False

        tool_settings = context.tool_settings

        col = layout.column(heading="Affect Only", align=True)
        col.prop(tool_settings, "use_transform_data_origin", text="Origins")
        col.prop(tool_settings, "use_transform_pivot_point_align", text="Locations")
        col.prop(tool_settings, "use_transform_skip_children", text="Parents")


class RULES_PT_Panel(bpy.types.Panel):
    bl_idname = "RULES_PT_Panel"
    bl_label = "Asset Rules"
    bl_category = "SurfaceSpray"
    bl_description = "Rules that specify how the asset is placed"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_parent_id = "MAIN_PT_Panel"

    def draw(self, context):
        layout = self.layout
        scn = context.scene

        # Item Rules box
        box = layout.box()

        #print(scn.asset_index)

        if scn.asset_index < 0 or scn.asset_index > len(scn.assets):
            box.label(text= "Currently Selected Asset:   None")
        else:
            box.label(text= "Currently Selected Asset:   " + scn.assets[scn.asset_index].name) 

            if scn.rules_panel_asset_index != scn.asset_index:
                box.operator("addon.reset_rules")
            else:

                rotationBox = box.box()

                rotation_row = rotationBox.row()

                rotation_row.alignment = "CENTER"

                # Rotation
                rotation_row.label(text="Allow Rotation:")
                rotation_row.prop(scn, "rotate_x")
                rotation_row.prop(scn, "rotate_y")
                rotation_row.prop(scn, "rotate_z")

                if(scn.rotate_x or scn.rotate_y or scn.rotate_z):
                    #Range and steps
                    
                    rotation_range_row = rotationBox.row()
                    rotation_step_row = rotationBox.row()

                    rotation_range_row.alignment = "CENTER"
                    rotation_step_row.alignment = "CENTER"

                    rotation_range_row.label(text="Range:")
                    rotation_step_row.label(text="Steps:")

                    if(scn.rotate_x):
                        rotation_range_row.prop(scn, "rot_range_x")
                        rotation_step_row.prop(scn, "rot_steps_x")

                    if(scn.rotate_y):
                        rotation_range_row.prop(scn, "rot_range_y")
                        rotation_step_row.prop(scn, "rot_steps_y")
                    
                    if(scn.rotate_z):
                        rotation_range_row.prop(scn, "rot_range_z")
                        rotation_step_row.prop(scn, "rot_steps_z")
                    

                # Distance
                box.row().prop(scn, "item_distance")

                # Overlap
                row = box.row()

                row.prop(scn, "overlap_bool")

                if(scn.overlap_bool):
                    row.prop(scn, "bbox_bool")

                #scale factor
                scalerow = box.row()

                scalerow.column().label(text="Random Scale Factor")
                scalerow.column().prop(scn, "scale_factor_min")
                scalerow.column().prop(scn, "scale_factor_max")

                #Percentage of appeareance
                appeareancerow = box.row()
                appeareancerow.column().label(text="Percentage Of Appeareance")
                appeareancerow.column().prop(scn, "item_percentage")
            


                normalBox = box.row()
                
                # normalRow = normalBox.column()
                # normalRow.prop(scn, "adjust_normal_bool")

                normalRow2 = normalBox.column()
                normalRow2.prop(scn, "adjust_normal_value",slider=True, index=2, text="Adjust to normal")

                # collection = bpy.data.collections.get(scn.collectName)
                # #If there are not objects distributed, cant adjust normal
                # if len(collection.objects) == 0:
                #     normalRow2.enabled = False
                
                #print(scn.asset_index,": " ,bpy.types.Scene.itemRules_HashMap, "\n")

    def register():

        bpy.types.Scene.itemRules_HashMap = {}

        bpy.types.Scene.itemRules_HashMap["rotate_x"] = [False for _ in range(10)]
        bpy.types.Scene.itemRules_HashMap["rotate_y"] = [False for _ in range(10)]
        bpy.types.Scene.itemRules_HashMap["rotate_z"] = [False for _ in range(10)]

        bpy.types.Scene.itemRules_HashMap["rot_range_x"] = [180.0 for _ in range(10)]
        bpy.types.Scene.itemRules_HashMap["rot_range_y"] = [180.0 for _ in range(10)]
        bpy.types.Scene.itemRules_HashMap["rot_range_z"] = [180.0 for _ in range(10)]

        bpy.types.Scene.itemRules_HashMap["rot_steps_x"] = [180.0 for _ in range(10)]
        bpy.types.Scene.itemRules_HashMap["rot_steps_y"] = [180.0 for _ in range(10)]
        bpy.types.Scene.itemRules_HashMap["rot_steps_z"] = [180.0 for _ in range(10)]

        bpy.types.Scene.itemRules_HashMap["item_distance"] = [0.0 for _ in range(10)]
        bpy.types.Scene.itemRules_HashMap["overlap_bool"] = [True for _ in range(10)]
        bpy.types.Scene.itemRules_HashMap["bbox_bool"] = [False for _ in range(10)]

        bpy.types.Scene.itemRules_HashMap["scale_factor_min"] = [1.0 for _ in range(10)]
        bpy.types.Scene.itemRules_HashMap["scale_factor_max"] = [1.0 for _ in range(10)]

        bpy.types.Scene.itemRules_HashMap["item_percentage"] = [1.0 for _ in range(10)]

        # Item rotation constraints
        bpy.types.Scene.rotate_x = bpy.props.BoolProperty(
            name='X',
            description = "This checkbox allows the rotation of the object in the X axis",
            default=False,
            update=update_rotate_x
        )

        bpy.types.Scene.rotate_y = bpy.props.BoolProperty(
            name='Y',
            description = "This checkbox allows the rotation of the object in the Y axis",
            default=False,
            update=update_rotate_y
        )

        bpy.types.Scene.rotate_z = bpy.props.BoolProperty(
            name='Z',
            description = "This checkbox allows the rotation of the object in the Z axis",
            default= False,
            update=update_rotate_z
        )

        #Item rotation range
        bpy.types.Scene.rot_range_x = bpy.props.FloatProperty(
            name='X',
            description = "Sets rotation range in the X axis",
            default=180.0,
            min = 0.0,
            max = 180.0,
            update=update_rot_range_x
        )

        bpy.types.Scene.rot_range_y = bpy.props.FloatProperty(
            name='Y',
            description = "Sets rotation range in the Y axis",
            default=180.0,
            min = 0.0,
            max = 180.0,
            update=update_rot_range_y
        )

        bpy.types.Scene.rot_range_z = bpy.props.FloatProperty(
            name='Z',
            description = "Sets rotation range in the Z axis",
            default=180.0,
            min = 0.0,
            max = 180.0,
            update=update_rot_range_z
        )

        # Item rotation steps
        bpy.types.Scene.rot_steps_x = bpy.props.FloatProperty(
            name='X',
            description = "Sets rotation steps in the X axis",
            default=1.0,
            min = 0.02,
            max = 360.0,
            update=update_rot_steps_x
        )

        bpy.types.Scene.rot_steps_y = bpy.props.FloatProperty(
            name='Y',
            description = "Sets rotation steps in the Y axis",
            default=1.0,
            min = 0.02,
            max = 360.0,
            update=update_rot_steps_y
        )

        bpy.types.Scene.rot_steps_z = bpy.props.FloatProperty(
            name='Z',
            description = "Sets rotation steps in the Z axis",
            default=1.0,
            min = 0.02,
            max = 360.0,
            update=update_rot_steps_z
        )

        # Item distance to other objects
        bpy.types.Scene.item_distance = bpy.props.FloatProperty(
            name='Min Distance Between Assets',
            description = "Sets minumum distance of the asset to any other object "+
            "in the scene while placing it",
            default=0,
            min = 0.0,
            max = 100.0,
            update=update_item_distance
        )

        bpy.types.Scene.overlap_bool = bpy.props.BoolProperty(
            name='Don\'t Allow Overlap',
            description = "This checkbox allows the assets to overlap with each other",
            default=True,
            update=update_overlap_bool
        )

        bpy.types.Scene.bbox_bool = bpy.props.BoolProperty(
            name='Use Box',
            description = "This checkbox determines that the overlap between assets is"+
            " going to be\nchecked using a bounding box (Recomended if the asset is not going to be rotated)."+
            "\n\nLeaving it unchecked makes use of a bounding sphere (More reliable\n if the asset allows "+
            "rotation but not very accurate with oblong objects)",
            default=False,
            update=update_bbox_bool
        )

        # Item scale vairation
        bpy.types.Scene.scale_factor_min =  bpy.props.FloatProperty(
            name='min',
            description = "Sets random variation factor for the scale of the asset between (min, max) in"+
            "this field",
            default=1.0,
            min = 0.05,
            max = 5.0,
            update=update_scale_factor_min
        )


        bpy.types.Scene.scale_factor_max =  bpy.props.FloatProperty(
            name='max',
            description = "Sets random variation factor for the scale of the asset between (min, max) in"+
            "this field",
            default=1.0,
            min = 0.0,
            max = 5.0,
            update=update_scale_factor_max
        )

        bpy.types.Scene.item_percentage = bpy.props.FloatProperty(
            name="",
            description="Percentage of appearance of each item from 0 o 1",
            default=1,
            min=0,
            max=1,
            update=update_item_percentage
        )

        bpy.types.Scene.adjust_normal_value = bpy.props.FloatProperty(
            name="Adjustment Percentage",
            description="Normal adjustment percentage",
            default=0,
            min=0,
            max=1,
            update=update_normal_rotations
        )   

        bpy.types.Scene.rules_panel_asset_index = bpy.props.IntProperty(
            default=0,
        )    

        # Not needed, already got the value (0 means false, >0 means true)      
        # bpy.types.Scene.adjust_normal_bool = bpy.props.BoolProperty(
        #     name='Adjust to Normal',
        #     description = "This checkbox determines that the object placed is going to face according to its normal vertex",
        #     default=False
        # )
        

        # # Item rotation constraints
        # bpy.types.Scene.consider_normal_inclination = bpy.props.BoolProperty(
        #     name='Consider Normal Inclination',
        #     description = "This checkbox allows the rotation of the object in the X axis",
        #     default=False
        # )

        # bpy.types.Scene.max_normal_inclin_limit = bpy.props.FloatProperty(
        #     name='Max Inclination Limit',
        #     description = "Sets limit of normal inclination (in degrees) from which an asset cannot be placed",
        #     default=0,
        #     min = 0.0,
        #     max = 180.0,
        # )
    

    def unregister():
        del (bpy.types.Scene.rotate_x, bpy.types.Scene.rotate_y, bpy.types.Scene.rotate_z, 
             bpy.types.Scene.rot_range_x, bpy.types.Scene.rot_range_y, bpy.types.Scene.rot_range_z, 
             bpy.types.Scene.item_distance, bpy.types.Scene.overlap_bool,bpy.types.Scene.bbox_bool,
             bpy.types.Scene.scale_factor_min, bpy.types.Scene.scale_factor_max, 
             bpy.types.Scene.adjust_normal_value, bpy.types.Scene.item_percentage)
        
def update_normal_rotations(self, context):
    bpy.ops.addon.rotate_normal()


def update_rotate_x(self, context):
    bpy.types.Scene.itemRules_HashMap["rotate_x"][context.scene.asset_index] = self["rotate_x"]
def update_rotate_y(self, context):
    bpy.types.Scene.itemRules_HashMap["rotate_y"][context.scene.asset_index] = self["rotate_y"]
def update_rotate_z(self, context):
    bpy.types.Scene.itemRules_HashMap["rotate_z"][context.scene.asset_index] = self["rotate_z"]
    
def update_rot_range_x(self, context):
    bpy.types.Scene.itemRules_HashMap["rot_range_x"][context.scene.asset_index] = self["rot_range_x"]
def update_rot_range_y(self, context):
    bpy.types.Scene.itemRules_HashMap["rot_range_y"][context.scene.asset_index] = self["rot_range_y"]
def update_rot_range_z(self, context):
    bpy.types.Scene.itemRules_HashMap["rot_range_z"][context.scene.asset_index] = self["rot_range_z"]

def update_rot_steps_x(self, context):
    bpy.types.Scene.itemRules_HashMap["rot_steps_x"][context.scene.asset_index] = self["rot_steps_x"]
def update_rot_steps_y(self, context):
    bpy.types.Scene.itemRules_HashMap["rot_steps_y"][context.scene.asset_index] = self["rot_steps_y"]
def update_rot_steps_z(self, context):
    bpy.types.Scene.itemRules_HashMap["rot_steps_z"][context.scene.asset_index] = self["rot_steps_z"]

def update_item_distance(self, context):
    bpy.types.Scene.itemRules_HashMap["item_distance"][context.scene.asset_index] = self["item_distance"]
def update_overlap_bool(self, context):
    bpy.types.Scene.itemRules_HashMap["overlap_bool"][context.scene.asset_index] = self["overlap_bool"]
def update_bbox_bool(self, context):
    bpy.types.Scene.itemRules_HashMap["bbox_bool"][context.scene.asset_index] = self["bbox_bool"]
def update_scale_factor_min(self, context):
    bpy.types.Scene.itemRules_HashMap["scale_factor_min"][context.scene.asset_index] = self["scale_factor_min"]
def update_scale_factor_max(self, context):
    bpy.types.Scene.itemRules_HashMap["scale_factor_max"][context.scene.asset_index] = self["scale_factor_max"]
def update_item_percentage(self, context):
    bpy.types.Scene.itemRules_HashMap["item_percentage"][context.scene.asset_index] = self["item_percentage"]