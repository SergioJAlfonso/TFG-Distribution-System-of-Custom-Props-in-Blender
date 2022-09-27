import bpy 
import numpy as np

class MegaTron_OT_Operator(bpy.types.Operator):
    bl_idname = "view3d.cursor_center"
    bl_label = "Simple operator"
    bl_description = "Center 3D Cursor"

#crear diferentes grupos de vertices para cada objeto a distribuir


    # self = method defined for this class 
    def execute(self, context):
        # bpy.ops.view3d.snap_cursor_to_center()
        # print(context.scene.target.name)
        # print(context.scene.asset.name)


        obj = context.scene.target
        # vgroup = obj.vertex_groups[0]

        # vertices = [v for v in obj.data.vertices if v.groups]
        #i = indice del vertice
        #v = el vertice 

        data_bidimensional = np.empty(shape=[0, 2])
        vertices_weight = []
        for i, v in enumerate(obj.data.vertices):
            
            print("Vertex index: " + str(i))
            #v.groups = grupos a los que esta asignado el vertice
            for g in v.groups:
                print("Vertex group:" + obj.vertex_groups[g.group].name)
                #g = datos del vertice en ese grupo
                print("Which weight is: " + str(g.weight))

        return {'FINISHED'}

    # static method
    @classmethod
    def poll(cls, context):

        # active object
        obj = context.object

        return (obj is not None) and (obj.mode == "OBJECT")



