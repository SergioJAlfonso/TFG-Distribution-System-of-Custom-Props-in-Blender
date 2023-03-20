import bpy

from ...utilsSS.geometry_utils import readjustRotation
from ...utilsSS.geometry_utils import adjustRotation

class Rotate_Operator(bpy.types.Operator):
    bl_idname = "addon.rotate_normal"
    bl_label = "Rotate Operator"
    bl_description = "Aligns objects to normal by factor"

    def execute(self, context):
        # TODO: Guardar el estado de la solucion del algoritmo, con sus correspondientes
        # vertices y normales asociadas, lo cual vuelve esto un problema trivial.

        solution_node = context.scene.solution_nodes[0]

        if(solution_node == None):
            self.report({'WARNING'}, 'No solution!')
            return {'FINISHED'}
        

        if not context.scene.collectName in bpy.data.collections:
            self.report({'WARNING'}, 'Collection name must exist!')
            return {'FINISHED'}
        
        # Obtener una colección específica por nombre
        collection = bpy.data.collections[context.scene.collectName]

        # Iterar a través de los objetos de la colección
        for i in range(len(solution_node)):
            normal = solution_node[i][1]
            rotation = solution_node[i][2]
            adjustRotation(collection.objects[i], normal, rotation, context.scene.adjust_normal_value)
            # readjustRotation(obj, context.scene.adjust_normal_value, context.scene.previous_normal_value)

        return {'FINISHED'}

