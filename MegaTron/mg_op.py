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
    
    inCollection =False  
    for i in range(len(points)):
        # bpy.context.view_layer.objects.active = object
        # object.select_set(True)
        newObj = duplicateObject(object)
        # bpy.ops.object.duplicate(linked=1,mode='TRANSLATION')
        # newObj = bpy.context.active_object

        newObj.location = points[i]
        newObj.location[2] += abs(boundingBoxObject[0][2]/2)
        if(inCollection == False):
            collection.objects.link(newObj)
