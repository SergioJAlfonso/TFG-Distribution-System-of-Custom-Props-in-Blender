import bpy 
import bmesh 

def getVerticesWeight(object):
    """
    Returns a list of vertices and their weights
    """

    data_bidimensional = []
    #i = indice del vertice | v = el vertice 
    # vgroup = obj.vertex_groups[0]
    # vertices = [v for v in obj.data.vertices if v.groups]
    for i, v in enumerate(object.data.vertices):

        # print("Vertex index: " + str(i))
        #v.groups = grupos a los que esta asignado el vertice
        for g in v.groups:
            # print("Vertex group:" + target.vertex_groups[g.group].name)
            pos = object.matrix_world @ v.co
            # print("Vertex position:" + str(pos))
            weight = g.weight
            #g = datos del vertice en ese grupo
            # print("Which weight is: " + str(weight))
            data_bidimensional.append([pos, weight])

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

def initCollection(collection, nameCollection):
    """ 
    If collection with giveb name exits, would be cleaned of objects.
    Else,would be created from zero.
    """
    #Si existe, borramos sus objetos, de lo contrario, 
    #creamos una coleccion nueva
    if collection is not None:
        for obj in collection.objects:
            bpy.data.objects.remove(obj, do_unlink=True)
    else:
        collection = bpy.data.collections.new(nameCollection)
        bpy.context.scene.collection.children.link(collection)

def makeSubdivision(target, assetBoundingBox, targetBoundingBox):
    tData = target.data
    # New bmesh
    subdividedMesh = bmesh.new()
    # load the mesh
    subdividedMesh.from_mesh(tData)
    # subdivide

    numCuts = calculateNumCuts(assetBoundingBox, targetBoundingBox)

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