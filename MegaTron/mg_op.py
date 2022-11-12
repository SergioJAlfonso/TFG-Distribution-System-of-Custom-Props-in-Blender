import bpy 
from .utils.draw_utils import *
from .heuristics.ThresholdRandDistribution import *
from .utils.addon_utils import *

class MegaTron_OT_Operator(bpy.types.Operator):
    bl_idname = "addon.distribute"
    bl_label = "Simple operator"
    bl_description = "Distribute object over a surface"

    #crear diferentes grupos de vertices para cada objeto a distribuir
    # self = method defined for this class 
    def execute(self, context):
        # bpy.ops.view3d.snap_cursor_to_center()
        if(context.scene.target == None):
            self.report({'WARNING'}, 'You must select a target object!')
            return {'FINISHED'}

        if(context.scene.asset == None):
            self.report({'WARNING'}, 'You must select a target object!')
            return {'FINISHED'}


        #Obtenemos todos los datos necesarios 
        target = duplicateObject(context.scene.target)
        asset = context.scene.asset

        #Nota : bpy.types.Scene.num_assets != context.scene.num_assets
        #Get user property data
        nameCollection = context.scene.collectName
        threshold_weight = context.scene.threshold #valor de 0, 1
        num_instances = context.scene.num_assets
        
        collection = bpy.data.collections.get(nameCollection)
        collection = initCollection(collection, nameCollection)

        #Scale asset if necessary
        if(asset.scale[0] != 1 or asset.scale[1] != 1 or asset.scale[2] != 1):
            self.report({'WARNING'}, 'Asset scale will be applied!')
            bpy.context.active_object.select_set(False)
            bpy.context.view_layer.objects.active = asset
            bpy.ops.object.transform_apply(location = False, rotation = False, scale=True)

        #Get bounding box
        asset_bounding_box_local = getBoundingBox(context, asset)
        target_bounding_box_local = getBoundingBox(context, target)

        #Subdivide target to fit assets in every vertex
        if (context.scene.subdivide):
            makeSubdivision(target, asset_bounding_box_local, target_bounding_box_local)

        data_bidimensional = getVerticesWeight(target)
        bpy.data.meshes.remove(target.data)
        # print('Algorithm:', context.scene.algorithm_enum)
        distribution = ThresholdRandDistribution(None)
        sol = distribution.distribute(data_bidimensional, asset_bounding_box_local, 
                                      num_instances, threshold_weight)
        
        #TODO: Sumar bounding box a la normal donde se está posicionando
        createObjectsInPoints(sol, asset, asset_bounding_box_local, collection)

        #Delete the newly created target (Not used, the target deletes when context )
        # deleteObject(target)

        return {'FINISHED'}

    # static method
    @classmethod
    def poll(cls, context):
        # active object
        obj = context.object
        return (obj is not None) and (obj.mode == "OBJECT")

def createObjectsInPoints( points, object, boundingBoxObject, collection):
    #TODO duplicate mesh data and asign to new objects
    
    # collection = bpy.data.collections.get("cosa")

    # if collection is not None:
    #     for obj in collection.objects:
    #         bpy.data.objects.remove(obj, do_unlink=True)
    # else:
    #     collection = bpy.data.collections.new("cosa")
    #     bpy.context.scene.collection.children.link(collection)
        
    # asset = context.scene.target 

    # inCollection = False
    # for i in range(10):
    #     bpy.ops.object.duplicate(linked=1)
        
    #     ob = bpy.context.object
        
    #     if(inCollection == False):
    #         bpy.context.scene.collection.objects.unlink(ob)
    #         collection.objects.link(ob)
    #         inCollection = True

    inCollection =False 
    bpy.context.view_layer.objects.active = object 
    for i in range(len(points)):
        
        object.select_set(True)
        # newObj = duplicateObject(object)
        bpy.ops.object.duplicate(linked=1)
        newObj = bpy.context.active_object
        
        newObj.location = points[i]
        newObj.location[2] += abs(boundingBoxObject[0][2]/2)
        #Unlink from all collections and link in desired collection
        if(inCollection == False):
            linkedCollection = newObj.users_collection
            collection.objects.link(newObj)
            for col in linkedCollection:
                # colLinked = bpy.data.collections.get(col)
                if(col is not None):
                    col.objects.unlink(newObj)
            inCollection = True

        object = bpy.context.active_object
