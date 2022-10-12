import random

def distributeAsset(v_data, asset_bound, num_assets, threshold):
    #v_data ->[vertice Vector posicion, peso]


    #[Vertice pos, usado]
    elegibles = []
    tam_vData = len(v_data)
    n_instances = 0

    #Para que no haya más assets que vertices
    if tam_vData -1 < num_assets:
        num_assets = tam_vData -1

    #iterar por cada vertice -> if (ver peso > threshold && n_instances < num)
        # mayor -> metemos pos en elegibles
    for i in range(tam_vData):
        if(v_data[i][1] > threshold):
            elegibles.append([v_data[i][0], False])
            n_instances += 1

    """una vez rellenado elegibles
    elegir de Elegibles al azar y marcarlo como usado, 
    comprobando su bounding box que no se acerque a otro vertice marcado"""
    sol = []
    num_elegibles = len(elegibles)


    while(num_assets > 0):
        index = random.randrange(0, num_elegibles)
        if(not elegibles[index][1]):
            elegibles[index][1] = True
            sol.append(elegibles[index][0])
            num_assets -= 1

    return sol

