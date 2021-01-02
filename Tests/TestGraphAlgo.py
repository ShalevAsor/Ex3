import unittest
from src.GraphAlgo import GraphAlgo
from src.DiGraph import DiGraph
import random


def graph_creator(v_size: int) -> GraphAlgo:
    e = DiGraph()
    i = 1
    while i <= v_size:
        e.add_node(i)
        i += 1
    g = GraphAlgo(e)
    return g


def graph_creator_with_edges(v_size: int, e_size: int) -> GraphAlgo:
    """
    generate graph with v_size vertices and e_size edges randomly
    :param v_size: number of vertices
    :param e_size: number of edges
    :return: GraphAlgo with the given number of edges and vertices
    """

    t = DiGraph()
    v, e = 1, 1
    while v <= v_size:
        t.add_node(v)
        v += 1
    while e <= e_size:
        r_src = random.randint(1, v_size)
        r_dest = random.randint(1, v_size)
        r_weight = random.uniform(0.1, 20)
        if not t.has_edge(r_src,r_dest):
            t.add_edge(r_src, r_dest, r_weight)
            e += 1

    g = GraphAlgo(t)
    return g


class MyTestCase(unittest.TestCase):

    def test_shortest_path(self):
        """
        This test verify shortest_path return the correct path for src node to dest node
        the shortest path will be with the lowest weight of all the path
        """
        g_1 = graph_creator(5)  # simple graph with 5 vertices
        g_1.get_graph().add_edge(1, 2, 3)
        g_1.get_graph().add_edge(1, 3, 0.5)
        g_1.get_graph().add_edge(3, 2, 0.3)
        # the shortest path is : 1-->3-->2 and the weight is :0.8
        self.assertEqual(g_1.shortest_path(1, 2), (0.8, [1, 3, 2]))
        g_2 = graph_creator(5)  # second graph
        g_2.get_graph().add_edge(1, 2, 1)
        g_2.get_graph().add_edge(2, 5, 14)
        g_2.get_graph().add_edge(1, 3, 2)
        g_2.get_graph().add_edge(1, 5, 16)
        g_2.get_graph().add_edge(2, 3, 4)
        g_2.get_graph().add_edge(3, 4, 1)
        g_2.get_graph().add_edge(4, 5, 4)
        # the shortest path is : 1-->3-->4-->5 , weight:7.0
        self.assertEqual(g_2.shortest_path(1, 5), (7, [1, 3, 4, 5]))
        g_3 = graph_creator(6)
        g_3.get_graph().add_edge(1, 2, 1)
        g_3.get_graph().add_edge(2, 3, 0.5)
        g_3.get_graph().add_edge(3, 4, 0.6)
        g_3.get_graph().add_edge(4, 5, 12)
        g_3.get_graph().add_edge(4, 6, 1)
        g_3.get_graph().add_edge(6, 5, 3)
        # the shortest path is: 1-->2-->3-->4-->6-->5 , weight: 6.1
        self.assertEqual((6.1, [1, 2, 3, 4, 6, 5]), g_3.shortest_path(1, 5))
        g_4 = graph_creator(2)  # init graph with two nodes
        self.assertEqual((-1, []), g_4.shortest_path(1, 6))  # node 6 is not in the graph-there is no path
        self.assertEqual((0, [1]), g_4.shortest_path(1, 1))  # shortest path from node to itself
        self.assertEqual((-1, []), g_4.shortest_path(1, 2))  # node 1 and 2 is in the graph with no path between them



if __name__ == '__main__':
    unittest.main()
