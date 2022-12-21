import random

from enum import Enum

from aima3.search import Problem as aimaProblem

"""
Parametros de distancia entre objetos aunque no se toquen...
"""

class ThresholdRandDistribution(aimaProblem):
    algorithm = None

    # TODO: calcular goal 
    def __init__(self, initial, goal=None):
        super().__init__(initial, goal)
    
    """
    FLUJO:
    Estado inicial.
    lista de acciones = Llamada a actions().
    por cada accion de la lista, se llama a result(?) -> que por cada result, hay un nuevo estado
    ese nuevo estado, implica nuevas acciones

    Esto es backtracking?
    """


    def actions(self, state):
        #Duelve una lista de accion posibles en el estado dado -> podemos poner en un sitio, pero que tipo de poner hay?
        """Actual
        La lista de acciones seria {poner en v1, poner en v2, poner en v3, ..., poner en vN} ?
        """

        #Algo tal que así?
        #iterar por cada vertice -> if (ver peso > threshold && n_instances < num)
        # mayor -> metemos pos en elegibles
        for i in range(tam_vData):
            #TODO: funcion estocastica, probabilidad > threshold 
            if(v_data[i][1] >= threshold): 
                #TODO si se cumple el if, añadir a la lista de acciones ->(poner asset en este vertice)
                elegibles.append([v_data[i][0],v_data[i][2], False])
                n_instances += 1


        return None

    def result(self, state, action):
        #Devuelve un nuevo estado al cual se le ha aplicado la accion.
        return None
        # return super().result(state, action)

    def goal_test(self, state):
        # TODO: goal puede ser una funcion que dado un estado calcule si esta bien no?
        # como tal nosotros no tenemos un estado final, no?
        #numero de objetos pedidos, separacion de objetos, tal.
        return state == self.goal

    def path_cost(self, c, state1, action, state2):
        
        # return super().path_cost(c, state1, action, state2)
        return c + 1
    
    def value(self, state):
        """For optimization problems, each state has a value. Hill Climbing
        and related algorithms try to maximize this value."""
        raise NotImplementedError

    def h(self, node):
        #TODO: Entendemos que esto define que tan bien vamos, no?
        # Pero eso no es como imposible?

        """ Return the heuristic value for a given state. Default heuristic function used is 
        h(n) = number of misplaced tiles """
        return 3 + 5

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
