import bpy

from ...ItemClasses.ItemRules import *
from ...ItemClasses.Item import *
from ...ItemClasses.DefaultAttributes.FurnitureAttribs import *

from ...utilsSS.draw_utils import *
from ...utilsSS.blender_utils import *
from ...heuristicsSS.ThresholdRandDistribution import *
from ...heuristicsSS.Demos.Demo_Dist_Ov_Rot_Scale_Distrib_Multi import *
#TODO: eventually remove deprecated distributions
# from ...heuristicsSS.Demos.Demo_Dist_Ov_Rot_Distrib_V3 import *
# from ...heuristicsSS.Demos.Demo_Dist_Overlap_Distribution_V2 import *
# from ...heuristicsSS.Demos.Demo_Dist_RotRang_Distribution import *
# from ...heuristicsSS.Demos.Demo_Dist_Overlap_Distribution import *
from ...utilsSS.StateGrid import *

from aima3.search import astar_search as aimaAStar

# from aima3.search import breadth_first_tree_search as aimaBFTS
from ...algorithmsSS.algorithmsSS import breadth_first_tree_multiple_search as ss_breadth_fms
from ...algorithmsSS.algorithmsSS import best_first_graph_multiple_search as ss_best_fms

from aima3.search import depth_first_tree_search as aimaDFTS

from aima3.search import Node
from collections import deque

class SurfaceSpray_OT_Operator_DEMO_MULTI(bpy.types.Operator):
    bl_idname = "addon.multidistribute"
    bl_label = "Distribute Operator"
    bl_description = "Distribute multiple objects over a surface"

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

        # Obtenemos todos los datos necesarios
        if (context.scene.subdivide):
            target = duplicateObject(context.scene.target)
        else:
            target = context.scene.target

        assets = []
        for i in range(len(context.scene.assets)):
            assets.append(context.scene.assets[i].obj)
        # Remove previous solutions AND set current search to 1
        context.scene.solution_nodes.clear()
        context.scene.current_search = 1

        # Note : bpy.types.Scene.num_assets != context.scene.num_assets
        # Get user property data
        numCutsSubdivision = context.scene.num_cuts
        nameCollection = context.scene.collectName
        threshold_weight = context.scene.threshold  # valor de 0, 1
        num_instances = context.scene.num_assets

        collection = bpy.data.collections.get(nameCollection)
        collection = initCollection(collection, nameCollection)

        bpy.ops.object.select_all(action='DESELECT')
        # #Scale asset if necessary
        for asset in assets:
            scaleObject(self, asset)

        # #Get bounding box
        assets_bounding_box_local = []
        for asset in assets:
            assets_bounding_box_local.append(getBoundingBox(context, asset))

        target_bounding_box_local = getBoundingBox(context, target)

        # Bounding info
        # for i in range(len(asset_bounding_box_local)):
        #     print('Vertice ', i,'(x, y, z): ', asset_bounding_box_local[i])

        # #Subdivide target to fit assets in every vertex
        if (context.scene.subdivide):
            # Get bounding box with more cuts needed
            asset_bounding_box_local = getMinBoundingBox(assets_bounding_box_local, target_bounding_box_local)
            makeSubdivision(target, asset_bounding_box_local,
                            target_bounding_box_local, numCutsSubdivision)

        data_tridimensional = getVerticesData(target)
        print('Algorithm:', context.scene.algorithm_enum)

        vertices = filterVerticesByWeightThreshold(
            data_tridimensional, threshold_weight)
        # Initial state as all possible vertices to place an asset

        initialState = StateGrid(vertices, 0)
        # Potential final state

        num_assets = min(num_instances, len(vertices))

        goalState = StateGrid(None, num_assets)
        # initialState.objectsPlaced_

        # Establishes rules for the assets in order to place them correctly
        rules = setPanelItemRules(context)

        distribution = Demo_Dist_Ov_Rot_Scale_Multi_Distrib(rules, assets_bounding_box_local, initialState, goalState)
        #distribution = ThresholdRandDistribution(rules, asset_bounding_box_local, initialState, goalState)
        #DEPRECATED:distribution = Demo_Dist_Ov_Rot_Distrib_V3(rules, asset_bounding_box_local, initialState, goalState)

        nodeSol = ss_best_fms(distribution,1)

        for i in range(len(nodeSol)):
            actions = nodeSol[i].solution()

            vertexes = []
            rotations = []
            scale = []
            asset_indexes = []
            for j in range(len(actions)):
                vertexes.append(actions[j].indexVertex)
                rotations.append(actions[j].rotation)
                scale.append(actions[j].scale)
                asset_indexes.append(actions[j].asset_index)
            
            # print(f"Sol {i}:")
            # print("Indices:", vertexes)
            # print("Rotations:", rotations)
            # print("Scale:", scale)

        actionsSol = None

        #Get just one solution
        if nodeSol is not None:
            actionsSol = nodeSol[0].solution()
        else:
            self.report({'ERROR'}, "Couldn't distribute objects!")
            return {'FINISHED'}

        objectsData = []
        #We obtain data from actions to create real objects.
        # ObjectData: [pos, normal, rotation, scale]
        for i in range(len(actionsSol)):
            indexVertex = actionsSol[i].indexVertex
            objRotation = actionsSol[i].rotation
            objScale = actionsSol[i].scale
            objIndex = actionsSol[i].asset_index
            objectsData.append(
                [vertices[indexVertex][0], vertices[indexVertex][1], objRotation, objScale, objIndex])

        # Save objectData
        context.scene.solution_nodes.append(objectsData)

        createObjectsInPointsNSMulti(objectsData, assets,
                              assets_bounding_box_local, collection, context.scene.adjust_normal_value)

        if (context.scene.subdivide):
            bpy.data.meshes.remove(target.data)

        return {'FINISHED'}

    # static method
    @classmethod
    def poll(cls, context):
        # active object
        obj = context.object
        return (obj is not None) and (obj.mode == "OBJECT")