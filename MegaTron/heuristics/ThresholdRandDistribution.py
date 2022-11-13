from .. heuristics.IDistribution import *
import random

"""
Realmente qué acciones tendremos? Solo distribuir no? Igual todos los posibles algoritmos?
Como se importan modulos desde la carpeta actual?

Parametros de distancia entre objetos aunque no se toquen...
"""

class ThresholdRandDistribution(IDistribution):
    def __init__(self, initial, goal=None):
        self.initial = initial
        self.goal = goal

    def distribute(self, v_data, asset_bound, num_assets, threshold):
        """
        Select (num_assets) random vertices from data as longs as 
        its vertex weight is greater than threshold. 
        
        Parameters
        ----------
        num_asset: integer value
            Number of points to select

        threshold: float value
            Value from 0 to 1.
            
        Returns
        -------
        sol : list
            Selected vertices. 
        """
        #v_data ->[vertice Vector posicion, peso, normal]

        #[Vertice pos, vertice normal, usado]
        elegibles = []
        tam_vData = len(v_data)
        n_instances = 0

        #iterar por cada vertice -> if (ver peso > threshold && n_instances < num)
            # mayor -> metemos pos en elegibles
        for i in range(tam_vData):
            #TODO: funcion estocastica, probabilidad > threshold 
            if(v_data[i][1] >= threshold):
                elegibles.append([v_data[i][0],v_data[i][2], False])
                n_instances += 1

        """una vez rellenado elegibles
        elegir de Elegibles al azar y marcarlo como usado, 
        comprobando su bounding box que no se acerque a otro vertice marcado"""
        sol = []
        num_elegibles = len(elegibles)

        #Para que no haya más assets que vertices
        num_assets = min(num_assets, num_elegibles)

        while(num_assets > 0):
            index = random.randrange(0, num_elegibles)
            if(not elegibles[index][2]):
                elegibles[index][2] = True
                sol.append([elegibles[index][0],elegibles[index][1]])
                num_assets -= 1

        return sol
