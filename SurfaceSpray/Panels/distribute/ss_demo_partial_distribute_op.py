import bpy 

from mathutils import Euler

from ...ItemClasses.ItemRules import *
from ...ItemClasses.Item import *
from ...ItemClasses.DefaultAttributes.FurnitureAttribs import *

from ...utilsSS.draw_utils import *
from ...utilsSS.blender_utils import *
# from ...heuristicsSS.ThresholdRandDistribution import *
from ...heuristicsSS.ThresholdRandDistributionV2_PartialSol import *
from ...heuristicsSS.ThresholdRandDistributionV3_PartialSol_MultiAction import *
from ...heuristicsSS.Demos.Demo_Dist_RotRang_Distribution import *
from ...heuristicsSS.Demos.Demo_Dist_Overlap_Distribution import *
from ...utilsSS.blender_utils import *
from ...utilsSS.StateGrid import *

from aima3.search import astar_search as aimaAStar
from aima3.search import depth_first_tree_search as aimaDFTS
# from aima3.search import breadth_first_tree_search as aimaBFTS

from ...algorithmsSS.algorithmsSS import breadth_first_tree_multiple_search as ss_breadth_fms
from ...algorithmsSS.algorithmsSS import best_first_graph_multiple_search as ss_best_fms

class SurfaceSpray_OT_Operator_DEMO_PARTIAL_SELECTION(bpy.types.Operator):
    bl_idname = "addon.distribute_partialdemo"
    bl_label = "Distribute Operator"
    bl_description = "Distribute object over a surface"

    def execute(self, context):
        # bpy.ops.view3d.snap_cursor_to_center()
        if(context.scene.target == None):
            self.report({'WARNING'}, 'You must select a target object!')
            return {'FINISHED'}

        if(context.scene.asset == None):
            self.report({'WARNING'}, 'You must select an asset object!')
            return {'FINISHED'}

        context.scene.solution_nodes.clear()
        context.scene.current_search = 1

        #Obtenemos todos los datos necesarios
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
        num_instances = context.scene.num_assets
        
        collection = bpy.data.collections.get(nameCollection)
        
        collection = initCollection(collection, nameCollection, True)

        bpy.ops.object.select_all(action='DESELECT')
        #Scale asset if necessary
        scaleObject(self, asset)

        #Get bounding box
        asset_bounding_box_local = getBoundingBox(context, asset)
        target_bounding_box_local = getBoundingBox(context, target)

        #Make sure there are no duplicates
        bpy.ops.partialsol.remove_duplicates()

        #Get objects from list
        partialSol = []

        for i in range(len(context.scene.partialsol)):
            obj = context.scene.partialsol[i]
            # EXTRACT INFO FROM OBJ
            bbox = getBoundingBox(context, obj.obj)
            itemSol = Item(obj.name, obj.obj, obj.obj.location, bbox)
            partialSol.append(itemSol) # INJECT INFO


        #Subdivide target to fit assets in every vertex
        if (context.scene.subdivide):
            makeSubdivision(target, asset_bounding_box_local, target_bounding_box_local, numCutsSubdivision)

        data_tridimensional = getVerticesData(target)
        print('Algorithm:', context.scene.algorithm_enum)

        vertices = filterVerticesByWeightThreshold(data_tridimensional, threshold_weight)
        
        if context.scene.solution_nodes == []:
            self.report({'INFO'}, "Solution nodes empty, refilling")
            
            #Initial state as all possible vertices to place an asset
            initialState = StateGrid(vertices, len(context.scene.partialsol))

            #Limit num asset to number of vertices
            num_assets = min(num_instances, len(vertices))

            #Potential final state 
            goalState = StateGrid(None, num_assets)

            # Establishes rules for the assets in order to place them correctly
            rules = setPanelItemRules(context)
            
            distribution = ThresholdRandDistributionPartialSol_MultiAction(rules, asset_bounding_box_local, initialState, partialSol, goalState)    
            #distribution = Demo_Over_Dist_RotRang_Distribution(rules, initialState, goalState)
            #DEPRECATED: distribution = Demo_Dist_Overlap_Distribution(rules, asset_bounding_box_local, initialState, goalState)

            #Get list of solution actions            
            nodeSol = ss_best_fms(distribution,context.scene.num_searches)
            
            for i in range(len(nodeSol)):
                context.scene.solution_nodes.append(nodeSol[i])

        return change_search(self, context, context.scene.solution_nodes[context.scene.current_search-1], vertices, asset, asset_bounding_box_local, collection, target)
        
    # static method
    @classmethod
    def poll(cls, context):
        # active object
        obj = context.object
        return (obj is not None) and (obj.mode == "OBJECT")
