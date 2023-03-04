import bpy 
from mathutils import Euler
from ...utilsSS.addon_utils import *

class Redistribute_OT_Operator(bpy.types.Operator):
    bl_idname = "addon.redistribute"
    bl_label = "Redistribute Operator"
    bl_description = "Redistribute objects over a surface"

    def execute(self, context):
        if(context.scene.solution_nodes == []):
            self.report({'WARNING'}, 'Nothing to redistribute!')
            return {'FINISHED'}
        

        if (context.scene.subdivide): 
            target = duplicateObject(context.scene.target)
        else:
             target = context.scene.target
        asset = context.scene.asset

        #Note : bpy.types.Scene.num_assets != context.scene.num_assets
        #Get user property data
        numCutsSubdivision = context.scene.num_cuts
        nameCollection = context.scene.collectName
        threshold_weight = context.scene.threshold #valor de 0, 1
        
        collection = bpy.data.collections.get(nameCollection)
        collection = initCollection(collection, nameCollection, True)

        bpy.ops.object.select_all(action='DESELECT')

        # #Get bounding box
        asset_bounding_box_local = getBoundingBox(context, asset)
        target_bounding_box_local = getBoundingBox(context, target)

        # #Subdivide target to fit assets in every vertex
        if (context.scene.subdivide):
            makeSubdivision(target, asset_bounding_box_local, target_bounding_box_local, numCutsSubdivision)

        data_tridimensional = getVerticesData(target)
        print('Algorithm:', context.scene.algorithm_enum)

        vertices = filterVerticesByWeightThreshold(data_tridimensional, threshold_weight)
        #Initial state as all possible vertices to place an asset

        return self.change_search(context, context.scene.solution_nodes[context.scene.actual_search-1], vertices, asset, asset_bounding_box_local, collection, target)
    
    def change_search(self, context, nodeSol, vertices, asset, asset_bounding_box_local, collection, target):
        actionsSol = None
        if nodeSol is not None:
            actionsSol = nodeSol.solution()
        else:
            # bpy.context.window_manager.popup("Couldn't distribute objects!", title="Error", icon='ERROR')
            self.report({'ERROR'}, "Couldn't distribute objects!")
            return {'FINISHED'}

        objectsData = []
        for i in range(len(actionsSol)):
            indexVertex = actionsSol[i].indexVertex
            objRotation = actionsSol[i].rotation
            objectsData.append([vertices[indexVertex][0], vertices[indexVertex][1], objRotation])

        # sol = distribution.distribute(data_tridimensional, asset_bounding_box_local, 
        #                               num_instances, threshold_weight, )
        
        createObjectsInPoints(objectsData, asset, asset_bounding_box_local, collection)

        if (context.scene.subdivide):
            bpy.data.meshes.remove(target.data)

        return {'FINISHED'}