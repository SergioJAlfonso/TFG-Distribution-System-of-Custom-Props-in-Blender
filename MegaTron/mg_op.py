import bpy 
from .heuristics.distribute import distributeAsset
from mathutils import Vector

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

        target = context.scene.target
        asset = context.scene.asset
        # vgroup = obj.vertex_groups[0]
        # vertices = [v for v in obj.data.vertices if v.groups]

        data_bidimensional = []
        #i = indice del vertice
        #v = el vertice 
        for i, v in enumerate(target.data.vertices):
            
            print("Vertex index: " + str(i))
            #v.groups = grupos a los que esta asignado el vertice
            for g in v.groups:
                print("Vertex group:" + target.vertex_groups[g.group].name)
                pos = target.matrix_world @ v.co
                print("Vertex position:" + str(pos))

                weight = g.weight
                #g = datos del vertice en ese grupo
                print("Which weight is: " + str(weight))

                data_bidimensional.append([pos, weight])

        # print(data_bidimensional)
        
        #Grafo que contiene informacion de los objetos con animaciones y modificadores aplicados
        depsgraph = bpy.context.evaluated_depsgraph_get() #API
        #Obtenemos el nuestro a partir de dicho grafo
        object_evaluated = context.scene.asset.evaluated_get(depsgraph) #Blender Scene

        #Bouding Box es una array bidimensional, [:] obtiene todos
        asset_bounding_box_local = [bbox_co[:] for bbox_co in object_evaluated.bound_box[:]]

        print(asset_bounding_box_local)
        # #Bounding box valores globales (sin uso)
        # asset_bounding_box_global = [context.scene.asset.matrix_world @ Vector(bbox_co) for bbox_co in asset_bounding_box_local]

        # # Crea objetos en las esquinas de la boundin box -> Depuracion
        # for co in asset_bounding_box_global:
        #     empty = bpy.data.objects.new(
        #         name='empty',
        #         object_data=None
        #     )
        #     bpy.context.scene.collection.objects.link(
        #         object=empty
        #     )
        #     empty.location = co

        #Devuelve un array de posiciones para distribuir N instancias de asset
        threshold_weight = context.scene.threshold #valor de 0, 1
        #bpy.types.Scene.num_assets != context.scene.num_assets
        num_instances = context.scene.num_assets
        print(threshold_weight)
        print(num_instances)
        sol = distributeAsset(data_bidimensional, asset_bounding_box_local, num_instances, threshold_weight)

        nameCollection = 'Objects Distributed'
        #Obtenemos la coleccion 
        collection = bpy.data.collections.get(nameCollection)

        #Si existe, borramos sus objetos, de lo contrario, 
        #creamos una coleccion nueva
        if collection is not None:
            for obj in collection.objects:
                bpy.data.objects.remove(obj, do_unlink=True)
        else:
            collection = bpy.data.collections.new(nameCollection)
            bpy.context.scene.collection.children.link(collection)

        #Por cada vector posicion de la solucion
        #creamos una instancia de Asset en dicho lugar y lo
        #añadimos a la colección
        for i in range(len(sol)):
            newObj = asset.copy()
            newObj.location = sol[i]
            newObj.location[2] += abs(asset_bounding_box_local[0][2])
            collection.objects.link(newObj)

        return {'FINISHED'}

    # static method
    @classmethod
    def poll(cls, context):

        # active object
        obj = context.object

        return (obj is not None) and (obj.mode == "OBJECT")



