import random
import copy
import math
import numpy as np

from enum import Enum

from ..utilsSS.Actions import *
from ..utilsSS.geometry_utils import *
from aima3.search import Problem as aimaProblem

"""
This class use actions as a tuple of mini actions to apply for each state.
Instead of applying just one action at a time.
"""
class ThresholdRandDistributionPartialSol_MultiAction_MultiDistribution(aimaProblem):

    def __init__(self, rules_, bbox, initial, partialSol_, goal=None):
        super().__init__(initial, goal)
        self.rules = rules_
        self.bounding_box = bbox
        # Bounding box magnitudes
        self.half_bounding_size_x = []
        self.half_bounding_size_y = []
        self.half_bounding_size_z = []
        
        for box in bbox:
            self.half_bounding_size_x.append((box[4][0] - box[0][0])/2.0)
            self.half_bounding_size_y.append((box[2][1] - box[0][1])/2.0)
            self.half_bounding_size_z.append((box[1][2] - box[0][2])/2.0)

        # Establish probability of appearance of each item
        self.total_item_probability = 0
        self.item_weights = []
        cont = 0
        for rule in rules_:
            self.total_item_probability += rule.appear_weight
            self.item_weights.append((self.total_item_probability, cont))
            cont += 1

        #Partial Sol Objects
        self.partialSol = partialSol_

    def checkRestrictions(self, state, indexVertex, assetIndex):
        """
        Checks all restrictions by rules.

        state.vertices : array (1, 3) -> [position(vector), normal(vector), vertexUsed(boolean)] 

        Returns if all have passed. 
        """
        # If vertex already in use
        if (state.vertices_[indexVertex][2]):
            return False, 0

        # Vertex we potentially want to place an object on
        pCandidate = state.vertices_[indexVertex][0]

        # We generate the new scale so it can be used to calculate the overlap
        scale = self.random_scale(assetIndex)

        # Take bounding box of chosen asset
        half_bounding_size_x = self.half_bounding_size_x[assetIndex]
        half_bounding_size_y = self.half_bounding_size_y[assetIndex]
        half_bounding_size_z = self.half_bounding_size_z[assetIndex]

        # Get BBox/BShpere parameters
        if (self.rules[assetIndex].overlap):

            if (self.rules[assetIndex].use_bounding_box):
                # Vertex A limits
                bbox_limits_Candidate = getVertexBBoxLimits(
                    pCandidate, half_bounding_size_x * scale, half_bounding_size_y * scale, half_bounding_size_z * scale)

            else:
                # Vertex A radius
                bbox_limits_Candidate = max(
                    half_bounding_size_x * scale, half_bounding_size_y * scale, half_bounding_size_z * scale)

        i = 0
        satisfiesRestrictions = True

        #While all restrictions are acomplished and we are checking all actions applied. 
        while (i < len(state.actionsApplied_) and satisfiesRestrictions):
            # Access vertices that has an object on it.
            applied_indexVertex = state.actionsApplied_[i].indexVertex

            vertexInUse = state.vertices_[applied_indexVertex][0]
            vertexInUseScale = state.actionsApplied_[i].scale

            # Check bounding box overlap if needed
            if (self.rules[assetIndex].overlap):

                # Using box
                if (self.rules[assetIndex].use_bounding_box):
                    # Vertex B limits
                    vertex_B_bbox_limits = getVertexBBoxLimits(
                        vertexInUse, half_bounding_size_x * vertexInUseScale, half_bounding_size_y * vertexInUseScale, half_bounding_size_z * vertexInUseScale)
                    
                    # Check overlap
                    satisfiesRestrictions = not boundingBoxOverlapping(
                        bbox_limits_Candidate, vertex_B_bbox_limits)

                # Using sphere
                else:
                    # Check overlap
                    vertex_B_sphere_radius = max(
                        half_bounding_size_x * vertexInUseScale, half_bounding_size_y * vertexInUseScale, half_bounding_size_z * vertexInUseScale)

                    satisfiesRestrictions = not boundingSphereOverlapping(
                        pCandidate, vertexInUse, bbox_limits_Candidate, vertex_B_sphere_radius)

            # Calculates distance between 2 tridimensional points.
            distance = math.sqrt((vertexInUse[0]-pCandidate[0])**2 + (
                vertexInUse[1]-pCandidate[1])**2 + (vertexInUse[2]-pCandidate[2])**2)
            # Compares if distance is lesser or equals to minimum distance.
            satisfiesRestrictions = satisfiesRestrictions and distance >= self.rules[assetIndex].distance_between_items

            i += 1

        #We need to also check if this object satisfies all restrictions with partial solution objects 
        i = 0
        while(i < len(self.partialSol) and satisfiesRestrictions):
            # Check bounding box overlap if needed
            partialObjectLocation = self.partialSol[i].position

            if (self.rules[assetIndex].overlap):
                partial_bbox = self.partialSol[i].bounding_box
                partial_half_bounding_size_x = (partial_bbox[4][0] - partial_bbox[0][0])/2.0
                partial_half_bounding_size_y = (partial_bbox[2][1] - partial_bbox[0][1])/2.0
                partial_half_bounding_size_z = (partial_bbox[1][2] - partial_bbox[0][2])/2.0

                # Using box
                if (self.rules[assetIndex].use_bounding_box):               
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
            satisfiesRestrictions = satisfiesRestrictions and distance >= self.rules[assetIndex].distance_between_items

            i += 1

        return satisfiesRestrictions, scale

    def actions(self, state):
        """
        Defines possible vertices in current state.

        state.vertices : array (1, 3) -> [position(vector), normal(vector), vertexUsed(boolean)] 

        Returns an array of indices, indicating which indices you can place an object on. 
        """
        possibleActions = []


        #A set of actions that removes objects placed can be triggered in the following cases if and only if:
        #the progress of solution list determines a probability to remove actions. The lower the progress, bigger the chances. 
        
        #If the solution list is empty, the probability is close to 0.5%
        #If is mostly filled is close to 0.1%
        probRemoval = self.m * len(self.solutionList) +  self.b
        random_num = random.random()
        removeChance = random_num <= probRemoval

        #Then, the following cases have to happen:
        #1. In case the state has all objects placed.
        reachedGoal = state.objectsPlaced_ >= self.goal.objectsPlaced_
        #2. In case the state has reached a acceptable Progress so we can remove actions. 
        progressState = state.objectsPlaced_/self.goal.objectsPlaced_
        reachedAcceptedProgressBegin = 0.45 <= progressState <= 0.55
        reachedAcceptedProgressEnd = 0.85 <= progressState <= 0.95
        
        canRemove = ( removeChance and (reachedGoal or reachedAcceptedProgressBegin or reachedAcceptedProgressEnd))
        
        #Particular case, if the state has reached goal but the chances does not allowed removal
        #we return a empty list, losing the state.
        if(reachedGoal):
            return possibleActions 
        
        # if(reachedGoal and not removeChance):
        #     return possibleActions    


        # if(canRemove):
        #     numActionsToRemove = 1 + 4.0*probRemoval

        #     totalActionsApplied = len(state.actionsApplied_)

        #     numActionsToRemove = min(round(numActionsToRemove),totalActionsApplied)

        #     #Search among solutions applied
        #     #We choose randomly a set of applied actions to remove
        #     indexex_actionToRemove = random.sample(range(totalActionsApplied), numActionsToRemove)

        #     j = 0
        #     while (j < numActionsToRemove):
        #         actionApplied = state.actionsApplied_[indexex_actionToRemove[j]]
                
        #         #Save occupied vertex so it can be freed. 
        #         newAction = Actions(0, (0,0,0), 1, 1, ActionType.DESTROY)
        #         #Store action to remove
        #         newAction.setActionToRemove(actionApplied)
        #         possibleActions.append(newAction)
        #         j += 1


        #     return possibleActions

        sizeV = len(state.vertices_)

        # Iterate over each state vertex checking if this vertex has a object on it, otherwise
        # it'll be considered as an action. (An object can be placed on it)
        # remaining = self.goal.objectsPlaced_ - state.objectsPlaced_
        
        if(state == self.initial):
            remaining = self.limitSolutionList/2 #Half width of tree node.
        elif (state.objectsPlaced_ == 1): 
            remaining = 2
        else:
            remaining = 1

        randomIndices = random.sample(range(sizeV), sizeV)
        j = 0
        while (remaining > 0 and j < sizeV):
            i = randomIndices[j]

            assetIndex = self.random_asset()

            satisfiesRestrictions, scale = self.checkRestrictions(state, i, assetIndex)
            
            if (satisfiesRestrictions):
                k = 0
                
                # Check that this selected vertex is not already used as an action in this loop
                while (k < len(possibleActions) and (possibleActions[k].indexVertex != i)):
                    k += 1

                #If we have reached end of list, none actions is the same as current.
                #Or if there are no actions, we store it.
                if (k >= len(possibleActions) or len(possibleActions) == 0):
                    remaining -= 1
                    newAction = Actions(i, self.random_step_rotation(assetIndex), scale, assetIndex, ActionType.CREATE)
                    possibleActions.append(newAction)

            j += 1

        if len(possibleActions) == 0:
            print('Could not find any vertex that satifies all rules.')

        return possibleActions
    
    def random_scale(self,assetIndex):
        minfact = self.rules[assetIndex].min_scale_factor
        maxfact = self.rules[assetIndex].max_scale_factor

        # If min and max factors are equal (or min is higher)
        if(minfact == maxfact or minfact > maxfact):
            return minfact
        
        precision = 100.0

        newScalefactor = random.randrange((int)(minfact*precision), (int)(maxfact*precision), (int)(0.01*precision))/precision
        return newScalefactor
    
    def random_asset(self):     
        # Selects a random asset taking percentage of appearance in account  
        random_percent = self.total_item_probability * random.random()
        for asset_weight, asset_index in self.item_weights:
            if asset_weight >= random_percent:
                return asset_index

    def random_step_rotation(self,assetIndex):
        precision = 100.0

        rang_x = (int)(self.rules[assetIndex].rotation_range[0] * precision)
        rang_y = (int)(self.rules[assetIndex].rotation_range[1] * precision)
        rang_z = (int)(self.rules[assetIndex].rotation_range[2] * precision)

        step_x = (int)(self.rules[assetIndex].rotation_steps[0] * precision)
        step_y = (int)(self.rules[assetIndex].rotation_steps[1] * precision)
        step_z = (int)(self.rules[assetIndex].rotation_steps[2] * precision)

        rot_x = 0
        rot_y = 0
        rot_z = 0

        if (self.rules[assetIndex].rotations[0] != 0):
            rot_x = random.randrange(-rang_x, rang_x, step_x)
        if (self.rules[assetIndex].rotations[1] != 0):
            rot_y = random.randrange(-rang_y, rang_y, step_y)
        if (self.rules[assetIndex].rotations[2] != 0):
            rot_z = random.randrange(-rang_z, rang_z, step_z)

        return ((rot_x/precision) * (math.pi/180.0), rot_y/precision * (math.pi/180.0), rot_z/precision * (math.pi/180.0))

    def result(self, state, action):
        """
        Returns a new state in which an action has been applied.
        """

        newState = copy.deepcopy(state)

        #If create, or destroy
        if(action.type == ActionType.CREATE):
            newState.vertices_[action.indexVertex][2] = True
            newState.objectsPlaced_ += 1
            newState.actionsApplied_.append(action)
        else:

            if(action.actionToRemove in state.actionsApplied_):
                #Get actionToRemove index
                indexToRemove = state.actionsApplied_.index(action.actionToRemove)

                #Old vertex occupied, now is free. But can not be occupied again. (?)
                # newState.vertices_[action.indexVertex][2] = False

                newState.objectsPlaced_ -= 1

                #We remove old applied action 
                newState.actionsApplied_.pop(indexToRemove) #we could also use -> del actionsApplied_[indexToRemove]

                #Update actionToRemove (?)
                if(action.actionToRemove in state.actionsHistory):
                    indexHistoryToRemove = state.actionsHistory.index(action.actionToRemove)
                    action.actionToRemove = indexHistoryToRemove 
                    # print(indexHistoryToRemove)

        newState.actionsHistory.append(action)

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
        
        return state2.pathCost + len(state2.actionsHistory)

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
    
    def registerSolutionList(self, list, limitList):
        self.solutionList = list
        self.limitSolutionList = limitList

        self.m = (0.1 - 0.5)/(limitList- 0)
        self.b = 0.5

