import bpy
import re
from ...utilsSS.Blender_utils import *

class ReplaceExistingCollectionName_ADD_OT_Operator(bpy.types.Operator):
    bl_idname = "addon.replace_collec_name"
    bl_label = "Collection Operator"
    bl_description = "Replace a existing collection name ."

    def replaceCollectionName(self, nameCollection):
        base_nombre = re.sub(r'(_\d+)?$', '', nameCollection)
        counterOcurr = 1
        newName = base_nombre + "_" + str(counterOcurr)
        #While keeps existing ocurrencies, increase counter
        while existsCollectionName(newName):
            counterOcurr += 1
            newName = base_nombre + "_" + str(counterOcurr)

        return newName

    def execute(self, context):
        nameCollection = context.scene.collectName

        newName = self.replaceCollectionName(nameCollection)

        ShowMessageBox('Distribution Assets with Collection Name Already Exists!', f'{nameCollection} will be replaced by {newName}.', 'ERROR')

        context.scene.collectName = newName
        return {'FINISHED'}