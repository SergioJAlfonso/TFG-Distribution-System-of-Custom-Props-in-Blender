from bpy.types import (Operator)

#Resets the values of the item rules when another one is selected in the panel
class Reset_Rules_OT_Operator(Operator):
    """Resets item rules when a different one is selected"""
    bl_idname = "addon.reset_rules"
    bl_label = "Show item rules"
    bl_description = "Shows item rules for this item"
    
    def execute(self, context):
        scn = context.scene

        scn.rules_panel_asset_index = scn.asset_index 

        scn.rotate_x = scn.itemRules_HashMap["rotate_x"][scn.asset_index]
        scn.rotate_y = scn.itemRules_HashMap["rotate_y"][scn.asset_index]
        scn.rotate_z = scn.itemRules_HashMap["rotate_z"][scn.asset_index]

        scn.rot_range_x = scn.itemRules_HashMap["rot_range_x"][scn.asset_index]
        scn.rot_range_y = scn.itemRules_HashMap["rot_range_y"][scn.asset_index]
        scn.rot_range_z = scn.itemRules_HashMap["rot_range_z"][scn.asset_index]

        scn.rot_steps_x = scn.itemRules_HashMap["rot_steps_x"][scn.asset_index]
        scn.rot_steps_y = scn.itemRules_HashMap["rot_steps_y"][scn.asset_index]
        scn.rot_steps_z = scn.itemRules_HashMap["rot_steps_z"][scn.asset_index]

        scn.overlap_bool = scn.itemRules_HashMap["overlap_bool"][scn.asset_index]
        scn.bbox_bool = scn.itemRules_HashMap["bbox_bool"][scn.asset_index]

        scn.item_distance = scn.itemRules_HashMap["item_distance"][scn.asset_index]

        scn.scale_factor_min = scn.itemRules_HashMap["scale_factor_min"][scn.asset_index]
        scn.scale_factor_max = scn.itemRules_HashMap["scale_factor_max"][scn.asset_index]

        scn.item_weight = scn.itemRules_HashMap["item_weight"][scn.asset_index]

        return {'FINISHED'}