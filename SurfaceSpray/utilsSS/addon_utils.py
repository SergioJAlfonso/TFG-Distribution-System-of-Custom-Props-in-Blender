import bpy 
import bmesh 
import random
from mathutils import Euler
from ..ItemClasses.ItemRules import *

def getVerticesData(object):
    """
    Returns a list of vertex, their weights and normals (vertex, weight, normal)
    """

    data_bidimensional = []
    #i = indice del vertice | v = el vertice 
    # vgroup = obj.vertex_groups[0]
    # vertices = [v for v in obj.data.vertices if v.groups]
    for i, v in enumerate(object.data.vertices):
        #v.groups = grupos a los que esta asignado el vertice
        for g in v.groups:
            # print("Vertex group:" + target.vertex_groups[g.group].name)
            pos = object.matrix_world @ v.co

            
            # print("Vertex position:" + str(pos))
            weight = g.weight
            #g = datos del vertice en ese grupo
            # print("Which weight is: " + str(weight))
            data_bidimensional.append([pos, weight, v.normal])

    # print("Vertices Weight: " + str(len(data_bidimensional)) +  str(data_bidimensional))
    return data_bidimensional

def getBoundingBox(context, object):
    """ 
    Retuns and array of points that represent the local 
    bounding box of an given object
    """ 
    #Grafo que contiene informacion de los objetos con animaciones y modificadores aplicados
    depsgraph = bpy.context.evaluated_depsgraph_get() #API
    #Obtenemos el nuestro a partir de dicho grafo
    object_evaluated = object.evaluated_get(depsgraph) #Blender Scene

    #Bouding Box es una array bidimensional, [:] obtiene todos
    asset_bounding_box_local = [bbox_co[:] for bbox_co in object_evaluated.bound_box[:]]

    # #Bounding box valores globales (sin uso)
    # asset_bounding_box_global = [context.scene.asset.matrix_world @ Vector(bbox_co) for bbox_co in asset_bounding_box_local]

    return asset_bounding_box_local

def TestBoundingBox(context, boundingBox):
    """
    Crea objetos en las esquinas de la boundin box -> Depuracion
    """
    for co in boundingBox:
        empty = bpy.data.objects.new(
            name='empty',
            object_data=None
        )
        bpy.context.scene.collection.objects.link(
            object=empty
        )
        empty.location = co

def clearCollection(collection, checkPartialSol = False):
    partialSol = bpy.context.scene.partialsol
    
    for obj in collection.objects:
        #Search if object is a partial sol. If it is, dont remove it.
        j = 0
        while(checkPartialSol and j < len(partialSol) and  obj.name != partialSol[j].name):
            j+=1

        if(j >= len(partialSol) or checkPartialSol == False):    
            bpy.data.objects.remove(obj, do_unlink=True)

def filterVerticesByWeightThreshold(vertices, weightThreshold):
    """Filters vertices array by weight threshold, so each vertex weight greater or
    equal than threshold, would stay, otherwise would be removed. 
    
    Returns an array of a 3rd dimensional vector: [position(vector), normal(vector), vertexUsed(boolean)]
    """
    elegibles = []
    tam_vData = len(vertices)
    n_instances = 0

    #iterar por cada vertice -> if (ver peso > threshold && n_instances < num)
        # mayor -> metemos pos en elegibles
    for i in range(tam_vData):
        #TODO: funcion estocastica, probabilidad > threshold 
        if(vertices[i][1] >= weightThreshold):
            elegibles.append([vertices[i][0],vertices[i][2], False])
            n_instances += 1

    return elegibles

def initCollection(collection, nameCollection, checkPartialSol = False):
    """ 
    If collection with given name exists, it's cleaned of objects.
    Else, it's created from zero.

    Returns:
    Collection initialized
    """
    #Si existe, borramos sus objetos, de lo contrario, 
    #creamos una coleccion nueva
    if collection is not None:
        clearCollection(collection, checkPartialSol)
    else:
        collection = bpy.data.collections.new(nameCollection)
        bpy.context.scene.collection.children.link(collection)

    return collection

def makeSubdivision(target, assetBoundingBox, targetBoundingBox, num_cuts):
    tData = target.data
    # New bmesh
    subdividedMesh = bmesh.new()
    # load the mesh
    subdividedMesh.from_mesh(tData)
    # subdivide
    if num_cuts == 0:
        numCuts = calculateNumCuts(assetBoundingBox, targetBoundingBox)
    else:
        numCuts = num_cuts
     
    bmesh.ops.subdivide_edges(subdividedMesh, edges=subdividedMesh.edges, cuts=numCuts, use_grid_fill=True)

    #TODO: hacerlo en mesh nueva para no modificar mesh del usuario 
    # Write back to the mesh
    subdividedMesh.to_mesh(tData)
    tData.update()

def calculateNumCuts(assetBoundingBox, targetBoundingBox):
    # get size of the asset and the target in x and y
    sizeX = assetBoundingBox[6][0] - assetBoundingBox[2][0]
    sizeY = assetBoundingBox[2][1] - assetBoundingBox[1][1]

    assetSize = max(sizeX, sizeY)

    sizeX = targetBoundingBox[6][0] - targetBoundingBox[2][0]
    sizeY = targetBoundingBox[2][1] - targetBoundingBox[1][1]

    targetSize = max(sizeX, sizeY)

    #return number of cuts to make the asset fit correctly
    return int(targetSize/assetSize)

def duplicateObject(obj, data=True, actions=True, collection=None):
    obj_copy = obj.copy()
    if data:
        obj_copy.data = obj_copy.data.copy()
    if actions and obj_copy.animation_data:
        obj_copy.animation_data.action = obj_copy.animation_data.action.copy()
    if collection != None:
        collection.objects.link(obj_copy)

        
    return obj_copy

def deleteObject(obj):
    # Deselect all
    bpy.ops.object.select_all(action='DESELECT')

    bpy.context.view_layer.objects.active = obj 
    obj.select_set(True)
    bpy.ops.object.delete() 

def scaleObject(self, obj):
    if(obj.scale[0] != 1 or obj.scale[1] != 1 or obj.scale[2] != 1):
        self.report({'WARNING'}, 'Asset scale will be applied!')
        # bpy.context.active_object.select_set(False)
        bpy.context.view_layer.objects.active = obj
        bpy.context.active_object.select_set(True)
        bpy.ops.object.transform_apply(location = False, rotation = False, scale=True)

def createObjectsInPoints(points, object, boundingBoxObject, collection):
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

        newObj.rotation_euler = Euler(points[i][2], 'XYZ')

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

def createObjectsInPointsN(objectData, object, boundingBoxObject, collection):
    inCollection = False 
    #In case something else has been selected, we deselect everything
    bpy.ops.object.select_all(action='DESELECT')
    #Set Active object in case it has changed
    bpy.context.view_layer.objects.active = object 
    #Create object in points
    
    for i in range(len(objectData)):
        object.select_set(True)
        bpy.ops.object.duplicate(linked=1)
        #We catch new object duplicated
        newObj = bpy.context.active_object
        
        newObj.location = objectData[i][0]
        #Set location relative to size
        adjustPosition(newObj, boundingBoxObject, objectData[i][1])

        #newObj.rotation_euler = Euler(points[i][2], 'XYZ')

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

def setPanelItemRules(context):
    
    # get item rules from panel
    rotation_x = context.scene.rotate_x
    rotation_y = context.scene.rotate_y
    rotation_z = context.scene.rotate_z

    rotation_range_x = context.scene.rot_range_x
    rotation_range_y = context.scene.rot_range_y
    rotation_range_z = context.scene.rot_range_z

    rotation_steps_x = context.scene.rot_steps_x
    rotation_steps_y = context.scene.rot_steps_y
    rotation_steps_z = context.scene.rot_steps_z

    can_overlap = context.scene.overlap_bool

    item_distance = context.scene.item_distance

    #Set Item rules
    rules = ItemRules()

    rules.rotations = [rotation_x, rotation_y, rotation_z]
    rules.rotation_range = [rotation_range_x, rotation_range_y, rotation_range_z]
    rules.rotation_steps = [rotation_steps_x, rotation_steps_y, rotation_steps_z]
    rules.overlap = can_overlap
    rules.distance_between_items = item_distance

    return rules