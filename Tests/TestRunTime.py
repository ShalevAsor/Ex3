import unittest
import networkx as nx
from src.GraphAlgo import GraphAlgo
from src.DiGraph import DiGraph
from src.node_data import NodeData

class MyTestCase(unittest.TestCase):
    def test_comparison_shortest_path(self):
        """
        In this test we will compare the performance of the networkx library
        against the performance of our graph in java,
        in comparison we will refer to the run times and compare the results of the shortest path
        this test checks the above on three graphs
        """
        my_graph=GraphAlgo()
        my_graph.load_from_json("../data/A5")
        list_of_nodes=my_graph.get_graph().get_all_v().values()
        list_of_edges=my_graph.get_graph().Edges.values()
        nx_graph=nx.Graph()
        print(tuple(list_of_nodes))
        nx_graph.add_nodes_from(list_of_nodes)
        nx_graph.add_edges_from(list_of_edges)
        print(nx.shortest_path(nx_graph,source=1,target=6))


if __name__ == '__main__':
    unittest.main()
