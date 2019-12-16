# Fall 2012 6.034 Lab 2: Search
#
# Your answers for the true and false questions will be in the following form.  
# Your answers will look like one of the two below:
#ANSWER1 = True
#ANSWER1 = False

# 1: True or false - Hill Climbing search is guaranteed to find a solution
#    if there is a solution
from collections import Set

ANSWER1 = False

# 2: True or false - Best-first search will give an optimal search result
#    (shortest path length).
#    (If you don't know what we mean by best-first search, refer to
#     http://courses.csail.mit.edu/6.034f/ai3/ch4.pdf (page 13 of the pdf).)
ANSWER2 = False

# 3: True or false - Best-first search and hill climbing make use of
#    heuristic values of nodes.
ANSWER3 = True

# 4: True or false - A* uses an extended-nodes set.
ANSWER4 = True

# 5: True or false - Breadth first search is guaranteed to return a path
#    with the shortest number of nodes.
ANSWER5 = True

# 6: True or false - The regular branch and bound uses heuristic values
#    to speed up the search for an optimal path.
ANSWER6 = False


from graphs import NEWGRAPH1, AGRAPH, NEWGRAPH2

# Import the Graph data structure from 'search.py'
# Refer to search.py for documentation
from search import Graph

## Optional Warm-up: BFS and DFS
# If you implement these, the offline tester will test them.
# If you don't, it won't.
# The online tester will not test them.
import pdb

def is_node_deadEnd(graph,Node):
    if len(graph.get_connected_nodes(Node)) == 1:
        return True
    else:
        return False

def bfs(graph, start, goal):
    if start == goal:
        print("give different goal input")
    else:
        closed_nodes = set()
        extended_paths = [[start]]
        path_to_extend = [[start]]
        while extended_paths != []:
            print(extended_paths)
            for path in path_to_extend:
                closed_nodes.update({closed_node for closed_node in path})
                for adjacentNodes in graph.get_connected_nodes(path[-1]):
                    if is_node_deadEnd(graph, adjacentNodes) and adjacentNodes != goal:
                        extended_paths.pop()
                    elif adjacentNodes not in closed_nodes and not is_node_deadEnd(graph,adjacentNodes):
                        path.append(adjacentNodes)
                        extended_paths.append(path.copy())
                        path.pop()
            path_removed = extended_paths.pop(0)
            if path_removed[-1] == goal:
                return path_removed
            path_to_extend = extended_paths
            closed_nodes.clear()
        return "Not found"
#   print(bfs(NEWGRAPH2, 'A', 'G'))

## Once you have completed the breadth-first search,
## this part should be very simple to complete.
def dfs(graph, start, goal):
    if start == goal:
        print("give different goal input")
    else:
        closed_nodes = set()
        extended_paths = [[start]]
        path_to_extend = [start]
        while extended_paths != []:
            closed_nodes.update({closed_node for closed_node in path_to_extend})
            for adjacentNodes in graph.get_connected_nodes(path_to_extend[-1]):
                """if is_node_deadEnd(graph, adjacentNodes) and adjacentNodes != goal:
                    extended_paths.pop()"""
                if adjacentNodes not in closed_nodes and not is_node_deadEnd(graph,adjacentNodes):
                    path_to_extend.append(adjacentNodes)
                    extended_paths.append(path_to_extend.copy())
                    path_to_extend = path_to_extend[:-1]
            print(extended_paths)
            path_last_explored = extended_paths.pop()
            if path_last_explored[-1] == goal:
                return path_last_explored
            path_to_extend = path_last_explored
            closed_nodes.clear()
        return "Not found"

##print(dfs(NEWGRAPH1,"S","Y"))

## Now we're going to add some heuristics into the search.
## Remember that hill-climbing is a modified version of depth-first search.
## Search direction should be towards lower heuristic values to the goal.
def hill_climbing(graph, start, goal):
    if start == goal:
        print("Give different goal input")
    else:
        closed_nodes = set()
        paths = [[start]]
        extended_paths = [[start]]
        while True:
            for path in paths:
                print(path)
                closed_nodes.update({node for node in path})
                for adjacentNodes in graph.get_connected_nodes(path[-1]):
                    """f is_node_deadEnd(graph,adjacentNodes) and adjacentNodes == goal:
                        path.append(goal)
                        return path"""
                    if is_node_deadEnd(graph, adjacentNodes) and adjacentNodes == goal:
                        path.append(adjacentNodes)
                        return path
                    elif adjacentNodes not in closed_nodes:
                        path.append(adjacentNodes)
                        if path[-1][-1] == goal:
                            return path
                        else:
                            extended_paths.append(path.copy())
                            path.pop()
                closed_nodes.clear()
            sorted_paths = sorted(extended_paths, key=lambda path: graph.get_heuristic(path[-1], goal))
            paths_to_extend = sorted_paths[:1]
            extended_paths = []
            paths = paths_to_extend.copy()


#print(hill_climbing(NEWGRAPH2,"E","H"))

## Now we're going to implement beam search, a variation on BFS
## that caps the amount of memory used to store paths.  Remember,
## we maintain only k candidate paths of length n in our agenda at any time.
## The k top candidates are to be determined using the
## graph get_heuristic function, with lower values being better values.
def beam_search(graph, start, goal, beam_width):
    if start == goal:
        print("Give different goal input")
    else:
        closed_nodes = set()
        extended_paths = [[start]]
        path_to_extend = [[start]]
        while extended_paths != [] :
            print(extended_paths)
            for path in path_to_extend:
                closed_nodes.update({closed_node for closed_node in path})
                for adjacentNodes in graph.get_connected_nodes(path[-1]):
                    if is_node_deadEnd(graph, adjacentNodes) and adjacentNodes != goal:
                        extended_paths.pop()
                    elif adjacentNodes == goal:
                        path.append(adjacentNodes)
                        path_to_goal = path
                        return path_to_goal
                    elif adjacentNodes not in closed_nodes:
                        path.append(adjacentNodes)
                        extended_paths.append(path.copy())
                        path.pop()
            extended_paths.pop(0)
            sorted_list = sorted(extended_paths,key = lambda path: graph.get_heuristic(path[-1],goal))
            extended_paths = sorted_list[:beam_width]
            path_to_extend = extended_paths
            closed_nodes.clear()
        return "Not found"
#print(beam_search(NEWGRAPH1,'S','G',2))

## Now we're going to try optimal search.  The previous searches haven't
## used edge distances in the calculation.

## This function takes in a graph and a list of node names, and returns
## the sum of edge lengths along the path -- the total distance in the path.
def path_length(graph, node_names):
    distance_traveled = 0
    start_node = node_names[0]
    for nextNode in node_names[1:]:
        distance_traveled += graph.get_edge(start_node,nextNode).length
        start_node = nextNode
    return distance_traveled


def branch_and_bound(graph, start, goal):
    if start == goal:
        print("Give different goal input")
    else:
        closed_nodes = set()
        least_cost_partial_path = [start]
        remaining_paths = []
        bound = []
        while len(least_cost_partial_path) != 0:
            print(remaining_paths)
            print("least cost {0}".format(least_cost_partial_path))
            for adjacentNode in graph.get_connected_nodes(least_cost_partial_path[-1]):
                closed_nodes.update({closed_node for closed_node in least_cost_partial_path})
                if adjacentNode == goal:
                    least_cost_partial_path.append(adjacentNode)
                    if len(bound) == 0:
                        bound = least_cost_partial_path.copy()
                        least_cost_partial_path.pop()
                    elif path_length(graph,least_cost_partial_path) < path_length(graph,bound):
                        bound = least_cost_partial_path.copy()
                        least_cost_partial_path.pop()
                elif adjacentNode not in closed_nodes and not is_node_deadEnd(graph, adjacentNode):
                    least_cost_partial_path.append(adjacentNode)
                    remaining_paths.append(least_cost_partial_path.copy())
                    least_cost_partial_path.pop()
                closed_nodes.clear()
            if len(remaining_paths) != 0:
                if len(bound) == 0:
                    least_cost_partial_path = sorted(remaining_paths,
                                                     key=lambda partial_paths: path_length(graph, partial_paths))[0]
                    remaining_paths.remove(least_cost_partial_path)
                else:
                    remaining_paths = [path_in_bound for path_in_bound in remaining_paths
                                       if path_length(graph,path_in_bound) < path_length(graph,bound)]
                    if len(remaining_paths) != 0:
                        least_cost_partial_path = sorted(remaining_paths,
                                                         key=lambda partial_paths: path_length(graph, partial_paths))[0]
                        remaining_paths.remove(least_cost_partial_path)
                    else:
                        return bound
        else:
            return "Not found"

#print(branch_and_bound(NEWGRAPH1,"S","H"))

def a_star(graph, start, goal):
    if start == goal:
        print("give different goal input")
    else:
        closed_nodes = set()
        least_cost_partial_path = [start]
        remaining_paths = []
        bound = []
        while len(least_cost_partial_path) != 0:
            for adjacentNode in graph.get_connected_nodes(least_cost_partial_path[-1]):
                closed_nodes.update({closed_node for closed_node in least_cost_partial_path})
                if adjacentNode == goal:
                    least_cost_partial_path.append(adjacentNode)
                    if len(bound) == 0:
                        bound = least_cost_partial_path.copy()
                        least_cost_partial_path.pop()
                    elif path_length(graph, least_cost_partial_path) < path_length(graph, bound):
                        bound = least_cost_partial_path.copy()
                        least_cost_partial_path.pop()
                elif adjacentNode not in closed_nodes and not is_node_deadEnd(graph, adjacentNode):
                    least_cost_partial_path.append(adjacentNode)
                    remaining_paths.append(least_cost_partial_path.copy())
                    least_cost_partial_path.pop()
                closed_nodes.clear()
            for path in remaining_paths:
                latest_visited_node = path[-1]
                paths_intersected = [paths_intersected for paths_intersected in remaining_paths if paths_intersected[-1] == latest_visited_node]
                if ["S","B","A"] in paths_intersected:
                    pdb.set_trace()
                sorted_redundant_paths = sorted(paths_intersected,key=lambda shortest_path: path_length(graph,shortest_path))
                for r_path in sorted_redundant_paths[:-1]:
                    remaining_paths.remove(r_path)
            if len(remaining_paths) != 0:
                if len(bound) == 0:
                    least_cost_partial_path = sorted(remaining_paths,
                                                     key=lambda partial_paths:
                                                     graph.get_heuristic(partial_paths[-1],goal)+path_length(graph, partial_paths))[0]
                    remaining_paths.remove(least_cost_partial_path)
                else:
                    remaining_paths = [path_in_bound for path_in_bound in remaining_paths
                                       if (path_length(graph, path_in_bound ) + graph.get_heuristic(path_in_bound[-1],goal)) <
                                          path_length(graph, bound) + graph.get_heuristic(path_in_bound[-1],goal)
                                       ]
                    if len(remaining_paths) != 0:
                        least_cost_partial_path = sorted(remaining_paths,
                                                         key=lambda partial_paths: path_length(graph, partial_paths))[0]
                        remaining_paths.remove(least_cost_partial_path)
                    else:
                        return bound

        else:
            return "Not found"

##print(a_star(AGRAPH,"S","C"))

## It's useful to determine if a graph has a consistent and admissible
## heuristic.  You've seen graphs with heuristics that are
## admissible, but not consistent.  Have you seen any graphs that are
## consistent, but not admissible?

def is_admissible(graph, goal):
    raise NotImplementedError

def is_consistent(graph, goal):
    raise NotImplementedError
