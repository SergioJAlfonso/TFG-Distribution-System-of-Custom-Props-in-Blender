import bmesh 
import math
from mathutils import Vector
from mathutils import Euler
import bpy 

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

def getVertexBBoxLimits(vertex, half_bounding_size_x, half_bounding_size_y, half_bounding_size_z):
    """
    Returns the limits of the bounding box
    Does not use bpy
    """
    max_X = vertex[0] + half_bounding_size_x
    min_X = vertex[0] - half_bounding_size_x
    max_Y = vertex[1] + half_bounding_size_y
    min_Y = vertex[1] - half_bounding_size_y
    max_Z = vertex[2] + half_bounding_size_z
    min_Z = vertex[2] - half_bounding_size_z

    return (max_X, min_X, max_Y, min_Y, max_Z, min_Z)

def boundingBoxOverlapping(verA, verB):
    """
    Checks is the bounding box of Vertex A and Vertex B are overlapping

    verA/VerB = (max_limit_X, min_limit_X, max_limit_Y, min_limit_Y, max_limit_Z, min_limit_Z)

    Returns True or False
    """

    # Overlap Condition
    if (verA[0] >= verB[1] and verA[1] <= verB[0] and
        verA[2] >= verB[3] and verA[3] <= verB[2] and
        verA[4] >= verB[5] and verA[5] <= verB[4]):
        return True

    return False

def boundingSphereOverlapping(verA, verB, radiusA, radiusB):
    #Distance between verA and verB
    distance = math.sqrt((verB[0] - verA[0])**2 + (verB[1] - verA[1])**2 + (verB[2] - verA[2])**2)

    # True if distance < diameter
    return distance <= radiusA + radiusB

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

def scaleObject(self, obj):
    if(obj.scale[0] != 1 or obj.scale[1] != 1 or obj.scale[2] != 1):
        self.report({'WARNING'}, 'Asset scale will be applied!')
        # bpy.context.active_object.select_set(False)
        bpy.context.view_layer.objects.active = obj
        bpy.context.active_object.select_set(True)
        bpy.ops.object.transform_apply(location = False, rotation = False, scale=True)

def adjustPosition(object, boundingBoxObject, normal):
    # object.location[2] += abs(boundingBoxObject[0][2])
    for i in range(3):
        object.location[i] += abs(boundingBoxObject[0][i])* normal[i]

def adjustRotation(obj, normal, rotation):
    # Vertex Normal 
    normal_vec = Vector((normal[0], normal[1], normal[2]))
    normal_euler = normal_vec.to_track_quat('Z', 'Y').to_euler()
    
    # # Random added rotation
    rotation_euler = Euler(rotation)

    # # Save rotation mode
    previous_mode = obj.rotation_mode 
    obj.rotation_mode = "XYZ"

    # Change to normal
    obj.rotation_euler = normal_euler
    
    # Apply random rotation
    obj.rotation_euler.rotate_axis('X', rotation_euler[0])
    obj.rotation_euler.rotate_axis('Y', rotation_euler[1])
    obj.rotation_euler.rotate_axis('Z', rotation_euler[2])
    
    # # Restore rotation mode
    obj.rotation_mode = previous_mode

def adjustScale(obj, scale):

    
    # Apply random scale
    obj.scale[0] = scale
    obj.scale[1] = scale
    obj.scale[2] = scale
