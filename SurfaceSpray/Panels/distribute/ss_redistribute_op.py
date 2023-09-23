import bpy 
from mathutils import Euler
from ...utilsSS.blender_utils import *
from ...utilsSS.geometry_utils import *

class Redistribute_OT_Operator(bpy.types.Operator):
    bl_idname = "addon.redistribute"
    bl_label = "Redistribute Operator"
    bl_description = "Redistribute objects over a surface"

    def execute(self, context):
        if(context.scene.solution_nodes == []):
            self.report({'WARNING'}, 'Nothing to redistribute!')
            return {'FINISHED'}
        
        if(context.scene.current_search-1 >= len(context.scene.solution_nodes)):
            self.report({'WARNING'}, 'Nothing to redistribute!')
            return {'FINISHED'}
        
        
        if (context.scene.subdivide): 
            target = duplicateObject(context.scene.target)
        else:
             target = context.scene.target
        
        assets = []
        for i in range(len(context.scene.assets)):
            assets.append(context.scene.assets[i].obj)
            
        #Get user property data
        numCutsSubdivision = context.scene.num_cuts
        nameCollection = context.scene.collectName
        threshold_weight = context.scene.threshold #valor de 0, 1
        num_instances = context.scene.num_assets

        collection = bpy.data.collections.get(nameCollection)
        collection = initCollection(collection, nameCollection, True)

        bpy.ops.object.select_all(action='DESELECT')

        #Scale asset if necessary
        for asset in assets:
            scaleObject(self, asset)

        #Get bounding box
        assets_bounding_box_local = []
        for asset in assets:
            assets_bounding_box_local.append(getBoundingBox(context, asset))

        target_bounding_box_local = getBoundingBox(context, target)

        #Subdivide target to fit assets in every vertex
        if (context.scene.subdivide):
             # Get bounding box with more cuts needed
            asset_bounding_box_local = getMinBoundingBox(assets_bounding_box_local, target_bounding_box_local)
            makeSubdivision(target, asset_bounding_box_local,
                            target_bounding_box_local, numCutsSubdivision)

        data_tridimensional = getVerticesData(target, context.scene.vgr_profile)

        vertices = filterVerticesByWeightThreshold(data_tridimensional, threshold_weight)
        #Initial state as all possible vertices to place an asset

        return change_searchN(self, context, context.scene.solution_nodes[context.scene.current_search-1], vertices, assets, assets_bounding_box_local, collection, target)