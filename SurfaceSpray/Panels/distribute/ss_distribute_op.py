import bpy

from ...ItemClasses.ItemRules import *
from ...ItemClasses.Item import *
from ...ItemClasses.DefaultAttributes.FurnitureAttribs import *

from ...utilsSS.draw_utils import *
from ...utilsSS.blender_utils import *
from ...heuristicsSS.ThresholdRandDistribution import *
from ...heuristicsSS.Demos.Demo_Dist_Ov_Rot_Scale_Distrib import *
#TODO: eventually remove deprecated distributions
# from ...heuristicsSS.Demos.Demo_Dist_Ov_Rot_Distrib_V3 import *
# from ...heuristicsSS.Demos.Demo_Dist_Overlap_Distribution_V2 import *
# from ...heuristicsSS.Demos.Demo_Dist_RotRang_Distribution import *
# from ...heuristicsSS.Demos.Demo_Dist_Overlap_Distribution import *
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

        # Obtenemos todos los datos necesarios
        if (context.scene.subdivide):
            target = duplicateObject(context.scene.target)
        else:
            target = context.scene.target

        asset = context.scene.asset

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
        collection = initCollection(collection, nameCollection, True)

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
        # Initial state as all possible vertices to place an asset

        initialState = StateDistribution(vertices, 0)
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
        
        nodeSol = algorithm(distribution,1)
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
            objectsData.append(
                [vertices[indexVertex][0], vertices[indexVertex][1], objRotation, objScale])

        # Save objectData
        context.scene.solution_nodes.append(objectsData)

        createObjectsInPointsNS(objectsData, asset,
                              asset_bounding_box_local, collection, context.scene.adjust_normal_value)

        if (context.scene.subdivide):
            bpy.data.meshes.remove(target.data)

        return {'FINISHED'}

    # static method
    @classmethod
    def poll(cls, context):
        # active object
        obj = context.object
        return (obj is not None) and (obj.mode == "OBJECT")
