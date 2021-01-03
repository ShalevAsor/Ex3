import unittest
from src.GraphAlgo import GraphAlgo
from src.DiGraph import DiGraph
from src.node_data import NodeData
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
        x = random.uniform(0.1, 35)
        y = random.uniform(0.1, 35)
        position = (x, y, 0)
        t.add_node(v, pos=position)
        v += 1
    while e <= e_size:
        r_src = random.randint(1, v_size)
        r_dest = random.randint(1, v_size)
        r_weight = random.uniform(0.1, 20)
        if not t.has_edge(r_src, r_dest):
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

    def test_save_to_json(self):
        g = graph_creator_with_edges(10, 10)
        # g=graph_creator(5)
        # g.get_graph().add_edge(1,2,1)
        # g.get_graph().add_edge(2,1,2)
        # g.get_graph().add_edge(4,5,10)
        self.assertTrue(g.save_to_json("random_graph"))
        e = GraphAlgo()
        e.load_from_json("../data/A5")
        print(e)


    def test_SCC_algo(self):
        """
        this test will verify the functionality of connected_component/connected_components
        functions and will be preformed over this graph:

         1  ➡  2
         ⬆  ↗  ⬇
         4 ⬅  3

         5 ➡  6
            ↖ ⬇
         8 ⬅ 7

         therefore 3 strongly connected components are presented within this disconnected graph:
         [8], [5,6,7], [1,2,3,4]

        :return:
        """
        g = graph_creator(8)
        g.get_graph().add_edge(1, 2, 5)
        g.get_graph().add_edge(2, 3, 6)
        g.get_graph().add_edge(3, 4, 7)
        g.get_graph().add_edge(4, 1, 8)
        g.get_graph().add_edge(4, 2, 8)
        g.get_graph().add_edge(5, 6, 8)
        g.get_graph().add_edge(6, 7, 8)
        g.get_graph().add_edge(7, 5, 8)
        g.get_graph().add_edge(7, 8, 8)
        list1 = g.connected_component(6)  # the strongly connected list whom node 6 belongs to
        list2 = g.connected_components()  # list of all the strongly connected components
        list1manual = [NodeData(7), NodeData(6), NodeData(5)]
        self.assertEqual(list1,list1manual)
        self.assertEqual(list2,[[NodeData(4),NodeData(3),NodeData(2),NodeData(1)],[NodeData(8)],list1manual])



if __name__ == '__main__':
    unittest.main()
