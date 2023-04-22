from aima3.search import (Node, exp_schedule)
from collections import deque
from aima3.utils import (memoize, argmax_random_tie, probability,PriorityQueue)

import sys
import numpy as np
import random

def breadth_first_tree_multiple_search(problem, limit=5):
    """
    AIMA ALGORITHM ADAPTATION.
    
    [Figure 3.7]
    Search the shallowest nodes in the search tree first.
    Search through the successors of a problem to find a goal.
    The argument frontier should be an empty queue.
    Repeats infinitely in case of loops.

    Aima algorithm adapted to find more than one solution.
    """

    frontier = deque([Node(problem.initial)])  # FIFO queue

    sols = []
    found = 0
    while frontier and found < limit:
        node = frontier.popleft()
        if problem.goal_test(node.state):
            #We save solution
            sols.append(node)
            found += 1
        frontier.extend(node.expand(problem))

    if len(sols) < 1:
        return None
    else:
        return sols
    

def best_first_graph_multiple_search(problem, limit=5, f = lambda node: node.path_cost, display=False):
    """
    
    AIMA ALGORITHM ADAPTATION.

    Search the nodes with the lowest f scores first.
    You specify the function f(node) that you want to minimize; for example,
    if f is a heuristic estimate to the goal, then we have greedy best
    first search; if f is node.depth then we have breadth-first search.
    There is a subtlety: the line "f = memoize(f, 'f')" means that the f
    values will be cached on the nodes as they are computed. So after doing
    a best first search you can examine the f values of the path returned.
    
    Aima algorithm adapted to find more than one solution.

    """
    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    sols = []
    
    if(hasattr(problem, "registerSolutionList")):
        problem.registerSolutionList(sols, limit)

    found = 0
    while frontier and found < limit:
        node = frontier.pop()
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            #We save solution
            sols.append(node)
            print("Solutions found:",len(sols))
            found += 1
            
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    
    if len(sols) < 1:
        return None
    else:
        return sols
    
def hill_climbing(problem, limit=5):
    """
    AIMA ALGORITHM ADAPTATION.

    [Figure 4.2]
    From the initial node, keep choosing the neighbor with highest value,
    stopping when no neighbor is better.

    """

    sols = []
    found = 0
    current = Node(problem.initial)

    # found < limit
    while True:
        neighbors = current.expand(problem)
        if not neighbors:
            break
        neighbor = argmax_random_tie(neighbors, key=lambda node: problem.value(node.state))
        if problem.value(neighbor.state) <= problem.value(current.state):
            break
        current = neighbor

    sols.append(current)
    # return current.state
    return sols


def simulated_annealing_multiples(problem, limit = 5, schedule=exp_schedule()):
    """
    AIMA ALGORITHM ADAPTATION.

    [Figure 4.5] CAUTION: This differs from the pseudocode as it
    returns a state instead of a Node.
    
    """

    sols = []

    current = Node(problem.initial)

    if(hasattr(problem, "registerSolutionList")):
        problem.registerSolutionList(sols, limit)

    for t in range(sys.maxsize):
        T = schedule(t)
        if T == 0:
            sols.append(current)
            return sols
        neighbors = current.expand(problem)
        if not neighbors:
            sols.append(current)
            return sols
        next_choice = random.choice(neighbors)
        delta_e = problem.value(next_choice.state) - problem.value(current.state)
        if delta_e > 0 or probability(np.exp(delta_e / T)):
            current = next_choice