import bpy

from ...utilsSS.ItemRules import *
from ...utilsSS.Item import *

from ...utilsSS.draw_utils import *
from ...utilsSS.blender_utils import *
from ...heuristicsSS.SingleObjectDistribution import *
from ...utilsSS.StateDistribution import *

from aima3.search import astar_search as aimaAStar

# from aima3.search import breadth_first_tree_search as aimaBFTS
from ...algorithmsSS.algorithmsSS import breadth_first_tree_multiple_search as ss_breadth_fms
from ...algorithmsSS.algorithmsSS import best_first_graph_multiple_search as ss_best_fms

from aima3.search import depth_first_tree_search as aimaDFTS

from aima3.search import Node
from collections import deque

class SurfaceSpray_OT_Operator(bpy.types.Operator):
    bl_idname = "addon.distribute"
    bl_label = "Distribute Operator"
    bl_description = "Distributes an object over a surface"

    # crear diferentes grupos de vertices para cada objeto a distribuir
    # self = method defined for this class
    def execute(self, context):
        # bpy.ops.view3d.snap_cursor_to_center()
        if (context.scene.target == None):
            self.report({'WARNING'}, 'You must select a target object!')
            return {'FINISHED'}

        if (len(context.scene.assets) == 0):
            self.report({'WARNING'}, 'You must select an asset object!')
            return {'FINISHED'}

        if(context.scene.vgr_profile == " " or context.scene.vgr_profile == "" ):
            self.report({'WARNING'}, 'You must select an vertex group profile!')
            return {'FINISHED'}
          
        # Remove previous solutions AND set current search to 1
        context.scene.solution_nodes.clear()
        context.scene.current_search = 1

        # Remove previous assets data
        context.scene.objects_data.clear()
        
        # Get duplicated target if needed to subdivide
        if (context.scene.subdivide):
            target = duplicateObject(context.scene.target)
        else:
            target = context.scene.target

        asset = context.scene.asset

        # Note : bpy.types.Scene.num_assets != context.scene.num_assets
        # Get user property data
        numCutsSubdivision = context.scene.num_cuts
        nameCollection = context.scene.collectName
        threshold_weight = context.scene.threshold  # valor de 0, 1
        num_instances = context.scene.num_assets

        #Make sure there are no duplicates
        bpy.ops.partialsol.remove_duplicates()

        #Get Asset name in list
        assetsNames_ = []
        assetsNames_.append(context.scene.asset.name)

        #Check if collection name already exists and replace it
        newCollectionName = checkAndReplaceCollectioName(context, nameCollection, assetsNames_)
        if(newCollectionName is not None):
            nameCollection = newCollectionName

        collection = bpy.data.collections.get(nameCollection)
        collection = initCollection(collection, nameCollection, True)

        bpy.context.view_layer.objects.active = context.scene.target
        oldMode = context.object.mode
        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

        bpy.ops.object.select_all(action='DESELECT')
        # #Scale asset if necessary
        scaleObject(self, asset)

        # #Get bounding box
        asset_bounding_box_local = getBoundingBox(context, asset)
        target_bounding_box_local = getBoundingBox(context, target)

        # Bounding info
        # for i in range(len(asset_bounding_box_local)):
        #     print('Vertice ', i,'(x, y, z): ', asset_bounding_box_local[i])

        # #Subdivide target to fit assets in every vertex
        if (context.scene.subdivide):
            makeSubdivision(target, asset_bounding_box_local,
                            target_bounding_box_local, numCutsSubdivision)

        data_tridimensional = getVerticesData(target, context.scene.vgr_profile)
        print('Algorithm:', context.scene.algorithm_enum)

        vertices = filterVerticesByWeightThreshold(
            data_tridimensional, threshold_weight)
        
        if(len(vertices)  == 0):
            self.report({'WARNING'}, 'No vertex to place objects! Have you Painted Weight?')
            return {'FINISHED'}

        # Initial state as all possible vertices to place an asset

        initialState = StateDistribution(vertices, len(context.scene.partialsol))
        # Potential final state

        num_assets = min(num_instances, len(vertices))

        goalState = StateDistribution(None, num_assets)
        # initialState.objectsPlaced_

        # Establishes rules for the assets in order to place them correctly
        rules = setPanelItemRules(context)

        #Get objects from list.
        partialSol = []

        for i in range(len(context.scene.partialsol)):
            obj = context.scene.partialsol[i]
            # EXTRACT INFO FROM OBJ
            bbox = getBoundingBox(context, obj.obj)
            itemSol = Item(obj.name, obj.obj, obj.obj.location, bbox)
            partialSol.append(itemSol) # INJECT INFO

        distribution = Demo_Dist_Ov_Rot_Scale_Distrib(rules, asset_bounding_box_local, initialState, partialSol, goalState)
        #distribution = ThresholdRandDistribution(rules, asset_bounding_box_local, initialState, goalState)
        #DEPRECATED:distribution = Demo_Dist_Ov_Rot_Distrib_V3(rules, asset_bounding_box_local, initialState, goalState)

        option = bpy.context.scene.algorithm_enum
        name = bpy.context.scene.bl_rna.properties['algorithm_enum'].enum_items[option].name
        print(f'Algorithm: {name}')
        algorithm = context.scene.algorithms_HashMap[name]
        
        nodeSol = algorithm(distribution, context.scene.num_searches)
        actionsSol = None

        #Get just one solution
        if nodeSol is not None:
            actionsSol = nodeSol[0].solution()
        else:
            self.report({'ERROR'}, "Couldn't distribute objects!\n" + 
                        "Try to paint more, lower density or allow overlapping.")
            return {'FINISHED'}

        for node in nodeSol:
            context.scene.solution_nodes.append(node)

        objectsData = []
       #We obtain data from actions to create real objects.
        # ObjectData: [pos, normal, rotation, scale, index]
        for i in range(len(actionsSol)):
            indexVertex = actionsSol[i].indexVertex
            objRotation = actionsSol[i].rotation
            objScale = actionsSol[i].scale
            objIndex = context.scene.asset_index + 1 # actual asset
            objectsData.append(
                [vertices[indexVertex][0], vertices[indexVertex][1], objRotation, objScale, objIndex])

        # Save objectData
        context.scene.objects_data.append(objectsData)

        createObjectsInPointsNS(objectsData, asset,
                              asset_bounding_box_local, collection, context.scene.adjust_normal_value)

        if (context.scene.subdivide):
            bpy.data.meshes.remove(target.data)

        bpy.ops.object.mode_set(mode=oldMode, toggle=False)

        return {'FINISHED'}

    # static method
    @classmethod
    def poll(cls, context):
        # active object
        obj = context.object
        return (obj is not None) and ((obj.mode == "OBJECT") or (obj.mode == "WEIGHT_PAINT"))
