import bpy

from ...ItemClasses.ItemRules import *
from ...ItemClasses.Item import *
from ...ItemClasses.DefaultAttributes.FurnitureAttribs import *

from ...utilsSS.draw_utils import *
from ...utilsSS.addon_utils import *
from ...heuristicsSS.ThresholdRandDistribution import *
from ...heuristicsSS.Demos.Demo_Dist_Ov_Rot_Distrib_V3 import *
#TODO: eventually remove deprecated distributions
# from ...heuristicsSS.Demos.Demo_Dist_Overlap_Distribution_V2 import *
# from ...heuristicsSS.Demos.Demo_Dist_RotRang_Distribution import *
# from ...heuristicsSS.Demos.Demo_Dist_Overlap_Distribution import *
from ...utilsSS.addon_utils import *
from ...utilsSS.StateGrid import *

from aima3.search import astar_search as aimaAStar
from aima3.search import breadth_first_tree_search as aimaBFTS
from aima3.search import depth_first_tree_search as aimaDFTS

from aima3.search import Node
from collections import deque


class ALG(Enum):
    A_STAR = 1
    BACKTRACKING = 2
    BEST_FIST_SEARCH = 3


class SurfaceSpray_OT_Operator(bpy.types.Operator):
    bl_idname = "addon.distribute"
    bl_label = "Distribute Operator"
    bl_description = "Distribute object over a surface"

    # crear diferentes grupos de vertices para cada objeto a distribuir
    # self = method defined for this class
    def execute(self, context):
        # bpy.ops.view3d.snap_cursor_to_center()
        if (context.scene.target == None):
            self.report({'WARNING'}, 'You must select a target object!')
            return {'FINISHED'}

        if (context.scene.asset == None):
            self.report({'WARNING'}, 'You must select an asset object!')
            return {'FINISHED'}

        # Obtenemos todos los datos necesarios
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

        collection = bpy.data.collections.get(nameCollection)
        collection = initCollection(collection, nameCollection)

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

        #distribution = ThresholdRandDistribution(rules, asset_bounding_box_local, initialState, goalState)
        distribution = Demo_Dist_Ov_Rot_Distrib_V3(rules, asset_bounding_box_local, initialState, goalState)

        nodeSol = aimaBFTS(distribution)

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
            objectsData.append(
                [vertices[indexVertex][0], vertices[indexVertex][1], objRotation])

        # sol = distribution.distribute(data_tridimensional, asset_bounding_box_local,
        #                               num_instances, threshold_weight, )

        createObjectsInPoints(objectsData, asset,
                              asset_bounding_box_local, collection)

        if (context.scene.subdivide):
            bpy.data.meshes.remove(target.data)

        return {'FINISHED'}

    # static method
    @classmethod
    def poll(cls, context):
        # active object
        obj = context.object
        return (obj is not None) and (obj.mode == "OBJECT")


def breadth_first_tree_search(problem, limit=5):
    """
    [Figure 3.7]
    Search the shallowest nodes in the search tree first.
    Search through the successors of a problem to find a goal.
    The argument frontier should be an empty queue.
    Repeats infinitely in case of loops.
    """

    frontier = deque([Node(problem.initial)])  # FIFO queue

    sols = []
    found = 0
    while frontier and found < limit:
        node = frontier.popleft()
        if problem.goal_test(node.state):
            sols.append(node)
            found += 1
        frontier.extend(node.expand(problem))

    if len(sols) < 1:
        return None
    else:
        return None
