import random
import copy
from enum import Enum

from ..utilsSS.Actions import *
from aima3.search import Problem as aimaProblem

"""
Parametros de distancia entre objetos aunque no se toquen...
"""


class ThresholdRandDistribution(aimaProblem):

    # TODO: calcular goal 
    def __init__(self, initial, goal=None):
        super().__init__(initial, goal)
    
    def actions(self, state):
        """
        Defines possible vertices in current state.

        Returns an array of indices, indicating which indices you can place an object on. 
        """
        possibleActions = [] 

        sizeV = len(state.vertices_)

        #Iterate over each state vertex checking if this vertex has a object on it, otherwise 
        # it'll be considered as an action. (An object can be placed on it) 
        # remaining = self.goal.objectsPlaced_ - state.objectsPlaced_
        remaining = 1
        
        while(remaining > 0):
            i = random.randrange(0, sizeV)
            if(state.vertices_[i][2] == False):
                j = 0
                print("indexing")
                while ( j < len(possibleActions) and (possibleActions[j].indexVertex != i)):
                    j+= 1

                if(j < len(possibleActions) or len(possibleActions) == 0 ):
                    remaining -= 1
                    action = Actions(i, -1)
                    possibleActions.append(action)
        
        # for i in range(sizeV):
        #     if(state.vertices_[i][2] == False):
        #         possibleActions.append(i)

        #Randomize so the solution is not always the same
        # random.shuffle(possibleActions)
        return possibleActions

    def result(self, state, action):
        """
        Returns a new state in which an action has been applied.
        """
        newState = copy.deepcopy(state)
        newState.vertices_[action.indexVertex][2] = True
        newState.objectsPlaced_ += 1
        return newState

    def goal_test(self, state):
        """
        Returns if the number of placed objects so far is equal to number of objects defined as goal.
        """
        #numero de objetos pedidos, separacion de objetos, tal.
        return state.objectsPlaced_ == self.goal.objectsPlaced_
        # return True

    # def path_cost(self, c, state1, action, state2):
        
    #     # return super().path_cost(c, state1, action, state2)
    #     return c + 1
    
    # def value(self, state):
    #     """For optimization problems, each state has a value. Hill Climbing
    #     and related algorithms try to maximize this value."""
    #     raise NotImplementedError

    def h(self, node):
        """ 
        Return the heuristic value for a given state. Default heuristic function used is 
        h(n) = difference between number of objects placed and number of objects to place.  
        """
        diff = self.goal.objectsPlaced_ - node.state.objectsPlaced_
        print(diff)
        return diff

    # def distribute(self, v_data, asset_bound, num_assets, threshold):
    #     """
    #     Select (num_assets) random vertices from data as longs as 
    #     its vertex weight is greater than threshold. 
        
    #     Parameters
    #     ----------
    #     num_asset: integer value
    #         Number of points to select

    #     threshold: float value
    #         Value from 0 to 1.
            
    #     Returns
    #     -------
    #     sol : list
    #         Selected vertices. 
    #     """
    #     #v_data ->[vertice Vector posicion, peso, normal]

    #     #[Vertice pos, vertice normal, usado]
    #     elegibles = []
    #     tam_vData = len(v_data)
    #     n_instances = 0

    #     #iterar por cada vertice -> if (ver peso > threshold && n_instances < num)
    #         # mayor -> metemos pos en elegibles
    #     for i in range(tam_vData):
    #         #TODO: funcion estocastica, probabilidad > threshold 
    #         if(v_data[i][1] >= threshold):
    #             elegibles.append([v_data[i][0],v_data[i][2], False])
    #             n_instances += 1

    #     """una vez rellenado elegibles
    #     elegir de Elegibles al azar y marcarlo como usado, 
    #     comprobando su bounding box que no se acerque a otro vertice marcado"""
    #     sol = []
    #     num_elegibles = len(elegibles)

    #     #Para que no haya más assets que vertices
    #     num_assets = min(num_assets, num_elegibles)

    #     while(num_assets > 0):
    #         index = random.randrange(0, num_elegibles)
    #         if(not elegibles[index][2]):
    #             elegibles[index][2] = True
    #             sol.append([elegibles[index][0],elegibles[index][1]])
    #             num_assets -= 1

    #     return sol
