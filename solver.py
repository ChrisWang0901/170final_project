import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_network, average_pairwise_distance
from networkx.algorithms import approximation
import sys
import random
import os


def solve(G):
    """
    Args:
        G: networkx.Graph

    Returns:
        T: networkx.Graph
    """

    # TODO: your code here!
    # find the min weight dominating set
    d_set = nx.algorithms.approximation.min_weighted_dominating_set(G)
    ld_set = list(d_set)
    g = nx.Graph()
    g.add_nodes_from(d_set)
    
    # connect all the nodes by running shortest path in the orignal set
    unconnected_nodes = d_set.copy()
    start = unconnected_nodes.pop()
    while unconnected_nodes:
    	
    	end = unconnected_nodes.pop() if unconnected_nodes else random.choice(ld_set)

    	# make sure start != end
    	while start == end:
    		end = random.choice(ld_set)
    	# print("start", start, "end", end)
    	path = nx.shortest_path(G, start, end)
        # print(path)
    	for i in range(len(path) - 1):
    		g.add_edge(path[i], path[i + 1], weight = G[path[i]][path[i + 1]]['weight'])
    		if path[i] in unconnected_nodes:
    			unconnected_nodes.remove(path[i])


    #find the minimum spanning tree in the graph
    print(g.edges)
    T = nx.minimum_spanning_tree(g)
    print(T.edges)

    return T




# Here's an example of how to run your solver.

# Usage: python3 solver.py test.in

if __name__ == '__main__':
    # assert len(sys.argv) == 2
    # path = sys.argv[1]
    for path in os.listdir('inputs'):
	    G = read_input_file('inputs/'+ path)
	    T = solve(G)
	    assert is_valid_network(G, T)
	    name = path[:-3]
	    print("Average  pairwise distance: {}".format(average_pairwise_distance(T)))
	    write_output_file(T, f'outputs/{name}.out')
