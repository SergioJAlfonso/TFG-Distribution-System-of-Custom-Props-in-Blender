import bpy 

from .ItemClasses.ItemAttributes import *
from .ItemClasses.Item import *
from .ItemClasses.SolutionItem import *
from .ItemClasses.DefaultAttributes.FurnitureAttribs import *

from .utilsMT.draw_utils import *
from .utilsMT.addon_utils import *
from .heuristicsMT.ThresholdRandDistribution import *
from .utilsMT.addon_utils import *
from .utilsMT.StateGrid import *

from aima3.search import astar_search as aimaAStar
from aima3.search import breadth_first_tree_search as aimaBFTS

class ALG(Enum):
    A_STAR = 1
    BACKTRACKING = 2
    BEST_FIST_SEARCH = 3

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
            self.report({'WARNING'}, 'You must select an asset object!')
            return {'FINISHED'}

        #Obtenemos todos los datos necesarios
        if (context.scene.subdivide): 
            target = duplicateObject(context.scene.target)
        else:
             target = context.scene.target

        asset = context.scene.asset

        #Nota : bpy.types.Scene.num_assets != context.scene.num_assets
        #Get user property data
        numCutsSubdivision = context.scene.num_cuts
        nameCollection = context.scene.collectName
        threshold_weight = context.scene.threshold #valor de 0, 1
        num_instances = context.scene.num_assets
        
        collection = bpy.data.collections.get(nameCollection)
        collection = initCollection(collection, nameCollection)

        bpy.ops.object.select_all(action='DESELECT')
        # #Scale asset if necessary
        scaleObject(self, asset)

        # #Get bounding box
        asset_bounding_box_local = getBoundingBox(context, asset)
        target_bounding_box_local = getBoundingBox(context, target)
        
        # #Subdivide target to fit assets in every vertex
        if (context.scene.subdivide):
            makeSubdivision(target, asset_bounding_box_local, target_bounding_box_local, numCutsSubdivision)

        # Establishes rules for the assets in order to place them correctly
        # TODO: Seleccionable desde panel
        # TODO: Generico para cualquier attrib + dependiente de num assets
        attribs = FurnitureAttribs()

        item = Item("sample", asset, attribs)

        data_tridimensional = getVerticesData(target)
        #print('Algorithm:', context.scene.algorithm_enum)

        vertices = filterVerticesByWeightThreshold(data_tridimensional, threshold_weight)
        #Initial state as all possible vertices to place an asset
        
        initialState = StateGrid(vertices, 0)
        #Potential final state 
        goalState = StateGrid(None, num_instances)
        initialState.objectsPlaced_
        distribution = ThresholdRandDistribution(initialState, goalState)
        
        sol = aimaBFTS(distribution).solution()


        m = 0 + 3

        print(m)
        # sol = distribution.distribute(data_tridimensional, asset_bounding_box_local, 
        #                               num_instances, threshold_weight)
        
        # createObjectsInPoints(sol, asset, asset_bounding_box_local, collection, target)
        
        # if (context.scene.subdivide):
        #     bpy.data.meshes.remove(target.data)

        return {'FINISHED'}

    # static method
    @classmethod
    def poll(cls, context):
        # active object
        obj = context.object
        return (obj is not None) and (obj.mode == "OBJECT")

def createObjectsInPoints(points, object, boundingBoxObject, collection, target):
    inCollection = False 
    #In case something else has been selected, we deselect everything
    bpy.ops.object.select_all(action='DESELECT')
    #Set Active object in case it has changed
    bpy.context.view_layer.objects.active = object 
    #Create object in points
    
    for i in range(len(points)):
        object.select_set(True)
        bpy.ops.object.duplicate(linked=1)
        #We catch new object duplicated
        newObj = bpy.context.active_object
        
        newObj.location = points[i][0]
        #Set location relative to size
        adjustPosition(newObj, boundingBoxObject, points[i][1])
        #Unlink from all collections and link in desired collection
        if(inCollection == False):
            linkedCollection = newObj.users_collection
            #Link before unlink from everything
            collection.objects.link(newObj)
            for col in linkedCollection:
                if(col is not None): col.objects.unlink(newObj)
            inCollection = True
        #Set Active object to new object so we can duplicate from this point
        object = bpy.context.active_object

def adjustPosition(object, boundingBoxObject, normal):
    # object.location[2] += abs(boundingBoxObject[0][2])
    for i in range(3):
        object.location[i] += abs(boundingBoxObject[0][i])* normal[i]
