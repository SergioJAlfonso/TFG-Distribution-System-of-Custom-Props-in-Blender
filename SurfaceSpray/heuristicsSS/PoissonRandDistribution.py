from utilsSS.random_queue import *
import random
import math

from aima3 import search
from aima3.search import Problem

class PoissonRandDistribution(Problem):
    grid = []
    processList = []
    samplePoints = []
    cellsize = 0
    
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
        #v_data ->[vertice Vector posicion, peso]

        #[Vertice pos, usado]
        elegibles = []
        tam_vData = len(v_data)
        n_instances = 0

        #iterar por cada vertice -> if (ver peso > threshold && n_instances < num)
            # mayor -> metemos pos en elegibles
        for i in range(tam_vData):
            #TODO: funcion estocastica, probabilidad > threshold 
            if(v_data[i][1] >= threshold):
                elegibles.append([v_data[i][0], False])
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
            if(not elegibles[index][1]):
                elegibles[index][1] = True
                sol.append(elegibles[index][0])
                num_assets -= 1

        return sol

    def generate_poisson(self, width, height, min_dist, new_points_count):
        # Cellsize 
        self.cellsize = min_dist /  math.sqrt(2)

        # 2D array of the grid, initialized to 0
        self.grid = [[(0,0)] * math.ceil(width/self.cellsize)] * math.ceil(height/self.cellsize)

        # RandomQueue works like a queue, except that it
        # pops a random element from the queue instead of
        # the element at the head of the queue
        self.processList = RandomQueue()
        self.samplePoints = []

        # generate the first point randomly
        # and updates 

        firstPoint = (random.randint(width), random.randint(height))

        # update containers
        self.processList.enqueue(firstPoint)
        self.samplePoints.append(firstPoint)
        self.grid[self.imageToGrid(firstPoint, self.cellSize)] = firstPoint

        # generate other points from points in queue
        while(not self.processList.isEmpty()):
            point = self.processList.dequeue()
            for i in range(0, new_points_count):
                newPoint = self.generateRandomPointAround(point, min_dist)
                # check that the point is in the image region
                # and no points exists in the point's neighbourhood
                if(self.inRectangle(newPoint) and not self.inNeighbourhood(newPoint, min_dist)):
                    # update containers
                    self.processList.enqueue(newPoint)
                    self.samplePoints.append(newPoint)
                    self.grid[self.imageToGrid(firstPoint, self.cellSize)] = newPoint


    def imageToGrid(self, point):
        gridX = (int)(point.x / self.cellSize)
        gridY = (int)(point.y / self.cellSize)
        return gridX, gridY

    def generateRandomPointAround(point, min_dist):
        # non-uniform, favours points closer to the inner ring, leads to denser packings
        r1 = random.random()
        r2 = random.random()
        
        # random radius between mindist and 2 * mindist
        radius = min_dist * (r1 + 1)

        # random angle
        angle = 2 * math.pi * r2

        # the new point is generated around the point (x, y)
        newX = point[0] + radius * math.cos(angle)
        newY = point[1] + radius * math.sin(angle)

        return (newX, newY)

    def inNeighbourhood(self, point, min_dist):
        gridPoint = self.imageToGrid(point)
        # get the neighbourhood of the point in the grid
        cellsAroundPoint = self.squareAroundPoint(gridPoint, 5)

        for cell in cellsAroundPoint:
            if(self.distance(cell, point) < min_dist):
                return True
        return False

    def inRectangle(self, point):
        if point[0] < 0 or point[1] < 0:
            return False
        if point[0] >= len(self.grid) * self.cellsize or point[1] >= len(self.grid[0]) * self.cellsize:
            return False
        return True

    def distance(cell, point):
        return math.dist([cell[0], cell[1]], [point[0], point[1]])

    def squareAroundPoint(gridPoint, radius):
        cellsAroundPoint = []

        # for i in range(radius/2):
        #     for e in range(radius/2):
        #         if 

        return cellsAroundPoint
        


