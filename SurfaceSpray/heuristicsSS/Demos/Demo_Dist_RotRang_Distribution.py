import random
import copy
import math

from enum import Enum

from ...utilsSS.Actions import *
from aima3.search import Problem as aimaProblem

"""
Parametros de distancia entre objetos aunque no se toquen...
"""


class Demo_Over_Dist_RotRang_Distribution(aimaProblem):

    # TODO: calcular goal 
    def __init__(self, rules_, initial, goal=None, ):
        super().__init__(initial, goal)
        self.rules = rules_

    def checkRestrictions(self, state, indexVertex):
        """
        Checks all restrictions by rules.

        state.vertices : array (1, 3) -> [position(vector), normal(vector), vertexUsed(boolean)] 

        Returns if all have passed. 
        """
        availableVertex = (state.vertices_[indexVertex][2] == False)

        #Vertex we potentially want to place an object on it.
        pCandidate = state.vertices_[indexVertex][0]
        i = 0
        satisfiesMinDistance = True
        #Como saber que no se puede satifacer dicha restriccion en ningun caso? Hay que notificarlo
        #Posibilidad de medir vertices? Taria chulo
        while (i < len(state.actionsApplied_) and satisfiesMinDistance == True):
            #Access vertices that has an object on it. 
            indexVertex = state.actionsApplied_[i].indexVertex
            vertexInUse = state.vertices_[indexVertex][0]
            #Calculates distance between 2 tridimensional points.
            distance = math.sqrt((vertexInUse[0]-pCandidate[0])**2 + (vertexInUse[1]-pCandidate[1])**2 + (vertexInUse[2]-pCandidate[2])**2)
            #Compares if distance is lesser or equals to minimum distance.
            satisfiesMinDistance = distance >= self.rules.distance_between_items

            i+= 1

        return availableVertex and satisfiesMinDistance
    
    def actions(self, state):
        """
        Defines possible vertices in current state.

        state.vertices : array (1, 3) -> [position(vector), normal(vector), vertexUsed(boolean)] 

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
            # distanciaValida = 
            if(self.checkRestrictions(state, i) == True):
                j = 0
                while ( j < len(possibleActions) and (possibleActions[j].indexVertex != i)):
                    j+= 1

                if(j < len(possibleActions) or len(possibleActions) == 0 ):
                    remaining -= 1
                    action = Actions(i, self.random_step_rotation())
                    possibleActions.append(action)
        
        return possibleActions


    def random_rotation(self):
        rot_x = random.uniform(0, self.rules.rotation_range[0])
        rot_y = random.uniform(0, self.rules.rotation_range[1])
        rot_z = random.uniform(0, self.rules.rotation_range[2])
        return (rot_x, rot_y, rot_z)

    def random_step_rotation(self):
        precision = 100.0

        rang_x = (int) (self.rules.rotation_range[0] * precision)
        rang_y = (int) (self.rules.rotation_range[1] * precision)
        rang_z = (int) (self.rules.rotation_range[2] * precision)

        step_x = (int) (self.rules.rotation_steps[0] * precision)
        step_y = (int) (self.rules.rotation_steps[1] * precision)
        step_z = (int) (self.rules.rotation_steps[2] * precision)

        rot_x = 0
        rot_y = 0
        rot_z = 0

        if(step_x != 0):
            rot_x = random.randrange(0, rang_x, step_x)
        if(step_y != 0):
            rot_y = random.randrange(0, rang_y, step_y)
        if(step_z != 0):
            rot_z = random.randrange(0, rang_z, step_z)

        return (rot_x/precision, rot_y/precision, rot_z/precision)

    def result(self, state, action):
        """
        Returns a new state in which an action has been applied.
        """
        newState = copy.deepcopy(state)
        newState.vertices_[action.indexVertex][2] = True
        newState.objectsPlaced_ += 1
        newState.actionsApplied_.append(action)
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
