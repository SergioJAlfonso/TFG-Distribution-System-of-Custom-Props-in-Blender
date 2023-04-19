import bpy
import time

from ...ItemClasses.ItemRules import *
from ...ItemClasses.Item import *
from ...ItemClasses.DefaultAttributes.FurnitureAttribs import *

from ...utilsSS.draw_utils import *
from ...utilsSS.blender_utils import *
from ...heuristicsSS.ThresholdRandDistribution import *
from ...heuristicsSS.ThresholdRandDistributionV4_PartialSol_MultiAction import *
# from ...heuristicsSS.Demos.Demo_Dist_Ov_Rot_Scale_Distrib_Multi import *

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

class SurfaceSpray_OT_Operator_DEMO_MULTI(bpy.types.Operator):
    bl_idname = "addon.multidistribute"
    bl_label = "Distribute Operator"
    bl_description = "Distributes multiple objects over a surface"

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

        assets = []
        for i in range(len(context.scene.assets)):
            assets.append(context.scene.assets[i].obj)
        # Remove previous solutions AND set current search to 1
        context.scene.solution_nodes.clear()
        context.scene.current_search = 1
        # Remove previous assets data
        context.scene.objects_data.clear()
        
        # Note : bpy.types.Scene.num_assets != context.scene.num_assets
        # Get user property data
        numCutsSubdivision = context.scene.num_cuts
        nameCollection = context.scene.collectName
        threshold_weight = context.scene.threshold  # valor de 0, 1
        num_instances = context.scene.num_assets

        #Make sure there are no duplicates
        bpy.ops.partialsol.remove_duplicates()

        collection = bpy.data.collections.get(nameCollection)
        collection = initCollection(collection, nameCollection, True)

        bpy.ops.object.select_all(action='DESELECT')
        # #Scale asset if necessary
        for asset in assets:
            scaleObject(self, asset)

        # #Get bounding box
        assets_bounding_box_local = []
        for asset in assets:
            assets_bounding_box_local.append(getBoundingBox(context, asset))

        target_bounding_box_local = getBoundingBox(context, target)


        #Get objects from list.
        partialSol = []

        for i in range(len(context.scene.partialsol)):
            obj = context.scene.partialsol[i]
            # EXTRACT INFO FROM OBJ
            bbox = getBoundingBox(context, obj.obj)
            itemSol = Item(obj.name, obj.obj, obj.obj.location, bbox)
            partialSol.append(itemSol) # INJECT INFO
       
        # #Subdivide target to fit assets in every vertex
        if (context.scene.subdivide):
            # Get bounding box with more cuts needed
            asset_bounding_box_local = getMinBoundingBox(assets_bounding_box_local, target_bounding_box_local)
            makeSubdivision(target, asset_bounding_box_local,
                            target_bounding_box_local, numCutsSubdivision)

        data_tridimensional = getVerticesData(target, context.scene.vgr_profile)
        print('Algorithm:', context.scene.algorithm_enum)

        vertices = filterVerticesByWeightThreshold(
            data_tridimensional, threshold_weight)
        # Initial state as all possible vertices to place an asset

        initialState = StateDistribution(vertices, len(context.scene.partialsol))
        # Potential final state

        num_assets = min(num_instances, len(vertices))

        goalState = StateDistribution(None, num_assets)
        # initialState.objectsPlaced_

        # Establishes rules for the assets in order to place them correctly
        rules = []
        for i in range(len(assets)):
            rules.append(setPanelItemRules(context, i))

        distribution = ThresholdRandDistributionPartialSol_MultiAction_MultiDistribution(rules, assets_bounding_box_local, initialState, partialSol, goalState)

        option = bpy.context.scene.algorithm_enum
        name = bpy.context.scene.bl_rna.properties['algorithm_enum'].enum_items[option].name
        print(f'Algorithm: {name}')
        algorithm = context.scene.algorithms_HashMap[name]

        start_time = time.time()

        nodeSol = algorithm(distribution, context.scene.num_searches)

        
        #debemos tener dos listas de acciones aplicadas. Una para saber como historial para saber que ha ido ocurriendo
        #para no repetir posiciones
        #y otra que nos indique el estado actual del tablero, con todo aplicado, para que las comprobaciones
        #no hagan calculos con posiciones inexistentes 

        #Por cada lista de acciones de cada nodeSol, applicar las acciones para eliminar
        #las acciones que remueven otras (que a su vez seran eliminadas)
        #deberian tener "num_assets" numero de acciones en total en la lista.
        
        #Ir del final al inicio? es lo mas probable que tengan Actiones para destruir.
        
        #pillar el indice a eliminar, e ir almacenando en un vector para luego usar el metodo de np.del
        
        if(nodeSol is None):
            self.report({'ERROR'}, "Couldn't distribute objects! No solutions found.")
            return {'FINISHED'}

        #solution_nodes now is a list of actions, rather than a object to ask for it list of actions.
        for node in nodeSol:
            
            actions_path = node.solution()

            actions_applied = []

            indexes_toRemove = []
            #Get indexes to remove actions.
            for action in reversed(actions_path):
                if(action.type == ActionType.DESTROY):
                    indexDestroyAction = actions_path.index(action)                
                    indexActionToRmv = action.actionToRemove

                    indexes_toRemove.append(indexDestroyAction)                
                    indexes_toRemove.append(indexActionToRmv) 
            
            #Remove actions based on indexes_toRemove list.
            for i in range(len(actions_path)):
                if i not in indexes_toRemove:
                    actions_applied.append(actions_path[i])

            context.scene.solution_nodes.append(actions_applied)

        actionsSol = None
        #Get just one solution
        actionsSol = context.scene.solution_nodes[0]

        objectsData = []
        #We obtain data from actions to create real objects.
        # ObjectData: [pos, normal, rotation, scale, index]

        # actionsSol[-1].

        for i in range(len(actionsSol)):
            indexVertex = actionsSol[i].indexVertex
            objRotation = actionsSol[i].rotation
            objScale = actionsSol[i].scale
            objIndex = actionsSol[i].asset_index
            objectsData.append(
                [vertices[indexVertex][0], vertices[indexVertex][1], objRotation, objScale, objIndex])

        # Save objectData
        context.scene.objects_data.append(objectsData)

        createObjectsInPointsNSMulti(objectsData, assets,
                              assets_bounding_box_local, collection, context.scene.adjust_normal_value)

        if (context.scene.subdivide):
            bpy.data.meshes.remove(target.data)

        end_time = time.time()

        elapsed_time = end_time - start_time
        # convertir a minutos, segundos y milisegundos
        minutes = int(elapsed_time / 60)
        seconds = int(elapsed_time % 60)
        milliseconds = int((elapsed_time - int(elapsed_time)) * 1000)

        # mostrar en formato MM:SS.mmm
        print("It lasted: {:02d}min:{:02d} sec.{:03d}".format(minutes, seconds, milliseconds))

        return {'FINISHED'}

    # static method
    @classmethod
    def poll(cls, context):
        # active object
        obj = context.object
        return (obj is not None) and (obj.mode == "OBJECT")
