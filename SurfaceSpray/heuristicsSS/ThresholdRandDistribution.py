import random
import copy
import math
import numpy as np


from enum import Enum

from ..utilsSS.Actions import *
from aima3.search import Problem as aimaProblem



class ThresholdRandDistribution(aimaProblem):

    def __init__(self, rules_, bbox, initial, goal=None, ):
        super().__init__(initial, goal)
        self.rules = rules_
        # self.noActionsLeft = False
        self.bounding_box = bbox
        #Bounding box magnitudes
        self.half_bounding_size_x = (bbox[4][0] - bbox[0][0])/2.0
        self.half_bounding_size_y = (bbox[2][1] - bbox[0][1])/2.0
        self.half_bounding_size_z = (bbox[1][2] - bbox[0][2])/2.0

    def boundingBoxOverlapping(self, verA, verB):
        #Vertex B limits
        max_B_X = verB[0] + self.half_bounding_size_x
        min_B_X = verB[0] - self.half_bounding_size_x
        max_B_Y = verB[1] + self.half_bounding_size_y
        min_B_Y = verB[1] - self.half_bounding_size_y
        max_B_Z = verB[2] + self.half_bounding_size_z
        min_B_Z = verB[2] - self.half_bounding_size_z

        #Overlap Condition
        if(verA[0] >= min_B_X and verA[1] <= max_B_X and
           verA[2] >= min_B_Y and verA[3] <= max_B_Y and
           verA[4] >= min_B_Z and verA[5] <= max_B_Z):
            return True
        
        return False

    def checkRestrictions(self, state, indexVertex):
        """
        Checks all restrictions by rules.

        state.vertices : array (1, 3) -> [position(vector), normal(vector), vertexUsed(boolean)] 

        Returns if all have passed. 
        """
        #If vertex already in use
        if(state.vertices_[indexVertex][2]):
            return False

        #Vertex we potentially want to place an object on it.
        pCandidate = state.vertices_[indexVertex][0]
   
        if(not self.rules.overlap):
            #Vertex A limits
            max_X = pCandidate[0] + self.half_bounding_size_x
            min_X = pCandidate[0] - self.half_bounding_size_x
            max_Y = pCandidate[1] + self.half_bounding_size_y
            min_Y = pCandidate[1] - self.half_bounding_size_y
            max_Z = pCandidate[2] + self.half_bounding_size_z
            min_Z = pCandidate[2] - self.half_bounding_size_z

            vertex_bbox_limits = (max_X, min_X, max_Y, min_Y, max_Z, min_Z)

        i = 0
        satisfiesRestrictions = True

        while (i < len(state.actionsApplied_) and satisfiesRestrictions == True):
            #Access vertices that has an object on it. 
            indexVertex = state.actionsApplied_[i].indexVertex
            vertexInUse = state.vertices_[indexVertex][0]

            #Check bounding box overlap if needed
            if(not self.rules.overlap):
                satisfiesRestrictions = not self.boundingBoxOverlapping(vertex_bbox_limits, vertexInUse)

            #Calculates distance between 2 tridimensional points.
            distance = math.sqrt((vertexInUse[0]-pCandidate[0])**2 + (vertexInUse[1]-pCandidate[1])**2 + (vertexInUse[2]-pCandidate[2])**2)
            #Compares if distance is lesser or equals to minimum distance.
            satisfiesRestrictions = satisfiesRestrictions and distance >= self.rules.distance_between_items

            i+= 1

        return satisfiesRestrictions
    
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

        randomIndices = random.sample(range(sizeV), sizeV)
        j = 0
        while(remaining > 0 and j < sizeV):
            i = randomIndices[j]
            if(self.checkRestrictions(state, i) == True):
                j = 0
                #Check that is not a vertex that is already used 
                while ( j < len(possibleActions) and (possibleActions[j].indexVertex != i)):
                    j+= 1

                if(j < len(possibleActions) or len(possibleActions) == 0 ):
                    remaining -= 1
                    action = Actions(i, (0,0,0))
                    possibleActions.append(action)

            j += 1

        if len(possibleActions) == 0:
            print('Could not find any vertex that satifies all rules.')

        return possibleActions

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

        #Chill down 
        return state.objectsPlaced_ == self.goal.objectsPlaced_
        # return True

    def h(self, node):
        """ 
        Return the heuristic value for a given state. Default heuristic function used is 
        h(n) = difference between number of objects placed and number of objects to place.  
        """
        diff = self.goal.objectsPlaced_ - node.state.objectsPlaced_
        print(diff)
        return diff
