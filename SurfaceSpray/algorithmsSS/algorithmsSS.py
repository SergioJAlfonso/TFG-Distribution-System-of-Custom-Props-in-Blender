from aima3.search import Node
from collections import deque

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
            sols.append(node)
            found += 1
        frontier.extend(node.expand(problem))

    if len(sols) < 1:
        return None
    else:
        return sols