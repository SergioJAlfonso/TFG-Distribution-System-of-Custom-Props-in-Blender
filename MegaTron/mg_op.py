import bpy 
from .utils.draw_utils import *
from .heuristics.distribute import *
from .utils.addon_utils import *
from mathutils import Vector

class MegaTron_OT_Operator(bpy.types.Operator):
    bl_idname = "addon.distribute"
    bl_label = "Simple operator"
    bl_description = "Distribute object over a surface"


#crear diferentes grupos de vertices para cada objeto a distribuir
    # self = method defined for this class 
    def execute(self, context):
        # bpy.ops.view3d.snap_cursor_to_center()
        target = duplicateObject(context.scene.target)
        #target = context.scene.target
        asset = context.scene.asset

        asset_bounding_box_local = getBoundingBox(context, asset)
        target_bounding_box_local = getBoundingBox(context, target)

        #Subdivide target to fit assets in every vertex
        if (context.scene.subdivide):
            makeSubdivision(target, asset_bounding_box_local, target_bounding_box_local)

        data_bidimensional = getVerticesWeight(target)

        #Nota : bpy.types.Scene.num_assets != context.scene.num_assets
        #Get user property data
        nameCollection = context.scene.collectName
        threshold_weight = context.scene.threshold #valor de 0, 1
        num_instances = context.scene.num_assets
        
        sol = distributeAsset(data_bidimensional, asset_bounding_box_local, num_instances, threshold_weight)

        #Obtenemos la coleccion 
        collection = bpy.data.collections.get(nameCollection)
        initCollection(collection, nameCollection)

        #TODO: NORMALIZAR LA ESCALA DEL ASSET 
        #TODO: Sumar bounding box a la normal donde se está posicionando
        createObjectsInPoints(sol, asset, asset_bounding_box_local, collection)

        #Delete the newly created target (Not used, the target deletes when context )
        #deleteObject(target)

        return {'FINISHED'}

    # static method
    @classmethod
    def poll(cls, context):
        # active object
        obj = context.object
        return (obj is not None) and (obj.mode == "OBJECT")

def createObjectsInPoints(points, object, boundingBoxObject, collection):
    for i in range(len(points)):
        newObj = object.copy()
        newObj.location = points[i]
        newObj.location[2] += abs(boundingBoxObject[0][2]/2)
        collection.objects.link(newObj)