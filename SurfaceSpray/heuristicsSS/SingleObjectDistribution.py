# Scale restriction
import random
import copy
import math
import numpy as np


from enum import Enum

from ..utilsSS.Actions import *
from ..utilsSS.geometry_utils import *
from aima3.search import Problem as aimaProblem


class Demo_Dist_Ov_Rot_Scale_Distrib(aimaProblem):

    def __init__(self, rules_, bbox, initial, partialSol_, goal=None, ):
        super().__init__(initial, goal)
        self.rules = rules_
        self.bounding_box = bbox
        # Bounding box magnitudes
        self.half_bounding_size_x = (bbox[4][0] - bbox[0][0])/2.0
        self.half_bounding_size_y = (bbox[2][1] - bbox[0][1])/2.0
        self.half_bounding_size_z = (bbox[1][2] - bbox[0][2])/2.0

        self.partialSol = partialSol_

    def checkRestrictions(self, state, indexVertex):
        """
        Checks all restrictions by rules.

        state.vertices : array (1, 3) -> [position(vector), normal(vector), vertexUsed(boolean)] 

        Returns if all have passed. 
        """
        # If vertex already in use
        if (state.vertices_[indexVertex][2]):
            return False, 1

        # Vertex we potentially want to place an object on it.
        pCandidate = state.vertices_[indexVertex][0]

        # We generate the new scale so it can be used to calculate the overlap
        scale = self.random_scale()

        # Get BBox/BShpere parameters
        if (self.rules.overlap):

            if (self.rules.use_bounding_box):
                # Vertex A limits
                bbox_limits_Candidate = getVertexBBoxLimits(
                    pCandidate, self.half_bounding_size_x * scale, self.half_bounding_size_y * scale, self.half_bounding_size_z * scale)

            else:
                # Vertex A radius
                bbox_limits_Candidate = max(
                    self.half_bounding_size_x * scale, self.half_bounding_size_y * scale, self.half_bounding_size_z * scale)

        i = 0
        satisfiesRestrictions = True

        while (i < len(state.actionsApplied_) and satisfiesRestrictions == True):
            # Access vertices that has an object on it.
            indexVertex = state.actionsApplied_[i].indexVertex
            vertexInUse = state.vertices_[indexVertex][0]
            vertexInUseScale = state.actionsApplied_[i].scale

            # Check bounding box overlap if needed
            if (self.rules.overlap):

                # Using box
                if (self.rules.use_bounding_box):
                    # Vertex B limits
                    vertex_B_bbox_limits = getVertexBBoxLimits(
                        vertexInUse, self.half_bounding_size_x * vertexInUseScale, self.half_bounding_size_y * vertexInUseScale, self.half_bounding_size_z * vertexInUseScale)
                    
                    # Check overlap
                    satisfiesRestrictions = not boundingBoxOverlapping(
                        bbox_limits_Candidate, vertex_B_bbox_limits)

                # Using sphere
                else:
                    # Check overlap
                    vertex_B_sphere_radius = max(
                        self.half_bounding_size_x * vertexInUseScale, self.half_bounding_size_y * vertexInUseScale, self.half_bounding_size_z * vertexInUseScale)

                    satisfiesRestrictions = not boundingSphereOverlapping(
                        pCandidate, vertexInUse, bbox_limits_Candidate, vertex_B_sphere_radius)

            # Calculates distance between 2 tridimensional points.
            distance = math.sqrt((vertexInUse[0]-pCandidate[0])**2 + (
                vertexInUse[1]-pCandidate[1])**2 + (vertexInUse[2]-pCandidate[2])**2)
            # Compares if distance is lesser or equals to minimum distance.
            satisfiesRestrictions = satisfiesRestrictions and distance >= self.rules.distance_between_items

            i += 1

            #We need to also check if this object satisfies all restrictions with partial solution objects 
        i = 0
        while(i < len(self.partialSol) and satisfiesRestrictions):
            # Check bounding box overlap if needed
            partialObjectLocation = self.partialSol[i].position

            if (self.rules.overlap):
                partial_bbox = self.partialSol[i].bounding_box
                partial_half_bounding_size_x = (partial_bbox[4][0] - partial_bbox[0][0])/2.0
                partial_half_bounding_size_y = (partial_bbox[2][1] - partial_bbox[0][1])/2.0
                partial_half_bounding_size_z = (partial_bbox[1][2] - partial_bbox[0][2])/2.0

                # Using box
                if (self.rules.use_bounding_box):               
                    bbox_limits_PartialObject = getVertexBBoxLimits(
                        partialObjectLocation, partial_half_bounding_size_x, partial_half_bounding_size_y, partial_half_bounding_size_z)

                    satisfiesRestrictions = not boundingBoxOverlapping(
                        bbox_limits_Candidate, bbox_limits_PartialObject)
                    
                # Using sphere
                else:
                    # Check overlap
                    vertex_B_sphere_radius = max(
                        partial_half_bounding_size_x, partial_half_bounding_size_y, partial_half_bounding_size_z)

                    satisfiesRestrictions = not boundingSphereOverlapping(
                        pCandidate, partialObjectLocation, bbox_limits_Candidate, vertex_B_sphere_radius)

            distance = math.sqrt((partialObjectLocation[0]-pCandidate[0])**2 + (
                partialObjectLocation[1]-pCandidate[1])**2 + (partialObjectLocation[2]-pCandidate[2])**2)
            # Compares if distance is lesser or equals to minimum distance.
            satisfiesRestrictions = satisfiesRestrictions and distance >= self.rules.distance_between_items

            i += 1

        return satisfiesRestrictions, scale

    def actions(self, state):
        """
        Defines possible vertices in current state.

        state.vertices : array (1, 3) -> [position(vector), normal(vector), vertexUsed(boolean)] 

        Returns an array of indices, indicating which indices you can place an object on. 
        """
        possibleActions = []

        #In case the state has all objects placed, we return an empty list.
        if(state.objectsPlaced_ >= self.goal.objectsPlaced_):
            return possibleActions

        sizeV = len(state.vertices_)

        # Iterate over each state vertex checking if this vertex has a object on it, otherwise
        # it'll be considered as an action. (An object can be placed on it)
        # remaining = self.goal.objectsPlaced_ - state.objectsPlaced_
        remaining = 2

        randomIndices = random.sample(range(sizeV), sizeV)
        j = 0
        while (remaining > 0 and j < sizeV):
            i = randomIndices[j]
            satisfiesRestrictions, scale = self.checkRestrictions(state, i)
            if (satisfiesRestrictions == True):
                k = 0
                
                # Check that this selected vertex is not already used as an action in this loop
                while (k < len(possibleActions) and (possibleActions[k].indexVertex != i)):
                    k += 1

                #If we have reached end of list, none actions is the same as current.
                #Or if there are no actions, we store it.
                if (k >= len(possibleActions) or len(possibleActions) == 0):
                    remaining -= 1
                    
                    action = Actions(i, self.random_rotation(), scale, type_ = ActionType.CREATE)
                    possibleActions.append(action)

            j += 1

        if len(possibleActions) == 0:
            print('Could not find any vertex that satifies all rules.')

        return possibleActions

    def random_scale(self):
        minfact = self.rules.min_scale_factor
        maxfact = self.rules.max_scale_factor

        # If min and max factors are equal (or min is higher)
        if(minfact == maxfact or minfact > maxfact):
            return minfact
        
        precision = 100.0

        newScalefactor = random.randrange((int)(minfact*precision), (int)(maxfact*precision), (int)(0.01*precision))/precision
        return newScalefactor

    def random_rotation(self):
        precision = 100.0

        rang_x = (int)(self.rules.rotation_range[0] * precision)
        rang_y = (int)(self.rules.rotation_range[1] * precision)
        rang_z = (int)(self.rules.rotation_range[2] * precision)

        step_x = (int)(self.rules.rotation_steps[0] * precision)
        step_y = (int)(self.rules.rotation_steps[1] * precision)
        step_z = (int)(self.rules.rotation_steps[2] * precision)

        rot_x = 0
        rot_y = 0
        rot_z = 0

        if (self.rules.rotations[0] != 0):
            rot_x = random.randrange(-rang_x, rang_x, step_x)
        if (self.rules.rotations[1] != 0):
            rot_y = random.randrange(-rang_y, rang_y, step_y)
        if (self.rules.rotations[2] != 0):
            rot_z = random.randrange(-rang_z, rang_z, step_z)

        return ((rot_x/precision) * (math.pi/180.0), rot_y/precision * (math.pi/180.0), rot_z/precision * (math.pi/180.0))

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
        # numero de objetos pedidos, separacion de objetos, tal.

        # Chill down
        return state.objectsPlaced_ == self.goal.objectsPlaced_
        # return True
 
    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2. If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""

        """
        Assings a higher cost value to those states whose number of objects placed is far from the goal.
           As it approaches to the goal, the cost is smaller
        """

        topLimitRange = 100 

        #Simple rule of three. More objects placed, lower the cost.
        range = int((state2.objectsPlaced_/self.goal.objectsPlaced_) * topLimitRange)


        #In case range is the top, to prevent an empty range error, we just add c to the cost 
        state2.pathCost = c + random.randrange(0, topLimitRange - range) if (range != topLimitRange) else c
        
        return state2.pathCost

    def h(self, node):
        """ 
        Return the heuristic value for a given state. Default heuristic function used is 
        h(n) = difference between number of objects placed and number of objects to place.  
        """
        diff = self.goal.objectsPlaced_ - node.state.objectsPlaced_
        print(diff)
        return diff
    
    def value(self, state):
        """For optimization problems, each state has a value. Hill Climbing
        and related algorithms try to maximize this value."""
        
        return state.objectsPlaced_