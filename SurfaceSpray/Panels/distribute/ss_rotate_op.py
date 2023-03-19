import bpy

from ...utilsSS.geometry_utils import readjustRotation

class Rotate_Operator(bpy.types.Operator):
    bl_idname = "addon.rotate_normal"
    bl_label = "Rotate Operator"
    bl_description = "Aligns objects to normal by factor"

    def execute(self, context):
        if not context.scene.collectName in bpy.data.collections:
            #self.report({'WARNING'}, 'Collection name must exist!')
            return {'FINISHED'}
        
        # Obtener una colección específica por nombre
        collection = bpy.data.collections[context.scene.collectName]

        # Iterar a través de los objetos de la colección
        for obj in collection.objects:
            readjustRotation(obj, context.scene.adjust_normal_value, context.scene.previous_normal_value)

        return {'FINISHED'}

