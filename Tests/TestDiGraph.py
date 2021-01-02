import unittest
from src.DiGraph import DiGraph
from src.node_data import NodeData

class MyTestCase(unittest.TestCase):

    def test_add_node(self):
        """
        verify add_node is adding the node only if he is not in the graph already
        """
        g = DiGraph()
        for i in range(5):
            g.add_node(i)
        self.assertEqual(0, g.get_node(0).key)
        self.assertEqual(1, g.get_node(1).key)
        self.assertEqual(2, g.get_node(2).key)
        self.assertEqual(3, g.get_node(3).key)
        self.assertEqual(4, g.get_node(4).key)
        self.assertEqual(None, g.get_node(5))  # verify return None value when ordering un-existing node
        self.assertFalse(g.add_node(0))        # verify that cant add same node
        self.assertTrue(g.add_node(5, pos=(12, 11.3, 0)))  # add new node with pos
        self.assertTrue(g.Nodes.__contains__(5))  # g contains the node above
        self.assertEqual(g.Nodes.get(5).pos, (12, 11.3, 0))  # the node pos are equals

    def test_add_edge(self):
        """
         This test verify that connect (node1,node2) is not equal to connect (node2,node1),
         also that negative weight and connect nodes that are not in the graph is not allow
        """
        g = DiGraph()  # create a new graph
        g.add_node(1)  # add two nodes to g
        g.add_node(2)
        g.add_node(3)
        self.assertFalse(g.add_edge(1, 6, 1))  # node6 is not in the graph
        self.assertFalse(g.add_edge(1, 1, 5))  # cannot add edge between node to himself
        self.assertTrue(g.add_edge(1, 2, 12))  # add edge between (1,2)
        self.assertFalse(g.add_edge(1, 2, 12))  # there is edge already between (1,2) with this weight
        self.assertFalse(g.add_edge(1, 2, 1))  # does not allow update in place there is an edge already
        self.assertTrue(g.add_edge(2, 1, 12))  # allows to add edge between (2,1)
        self.assertEqual(g.get_edge(2, 1).weight, 12)
        self.assertFalse(g.add_edge(2, 1, 6))
        self.assertFalse(g.add_edge(1, 3, -4))  # should not allow negative weight

    def test_all_in_all_out(self):
        """
        this test verify the returned list of nodes pointing to
        and nodes pointing from id1
        this test will be preformed over a simple graph looks like:

            1--►3
            |   ▲
            |  /
            ▼ /
            2
        :return: dict
        """
        g = DiGraph()  # create a new graph
        g.add_node(1)  # add two nodes to g
        g.add_node(2)
        g.add_node(3)
        g.add_edge(1, 2, 12)
        g.add_edge(1, 3, 13)
        g.add_edge(2, 3, 23)
        node1_all_out = {2: g.get_node(2), 3: g.get_node(3)}
        self.assertDictEqual(node1_all_out,g.all_out_edges_of_node(1))
        # print(g.all_out_edges_of_node(1))
        # print(g.all_out_edges_of_node(2))
        # print(g.all_out_edges_of_node(3))
        # print(g.all_in_edges_of_node(1))
        # print(g.all_in_edges_of_node(2))
        # print(g.all_in_edges_of_node(3))

    def test_remove_node_ESize(self):
        """
        verify that the node has been removed and all the edges he was connected with
        also verify the ESize
        this test will be preformed over a simple graph looks like:

            1◄--►3
            |   ▲
            |  /
            ▼ ▼
             2
        """
        g = DiGraph()  # create a new graph
        g.add_node(1)  # add two nodes to g
        g.add_node(2)
        g.add_node(3)
        g.add_edge(1, 2, 12)
        g.add_edge(1, 3, 13)
        g.add_edge(2, 3, 23)
        g.add_edge(3, 2, 32)
        g.add_edge(3, 1, 31)
        self.assertEqual(5, g.ESize)
        g.remove_node(3)
        self.assertEqual(1, g.ESize)
        self.assertEqual(12, g.get_edge(1, 2).weight)  # verify that the only edge remaining is 1-->2 in weight of 12
        self.assertEqual(None, g.get_edge(2, 1))
        self.assertTrue(g.has_edge(1, 2))
        self.assertFalse(g.has_edge(2, 1))
        self.assertFalse(g.has_edge(3, 1))
        self.assertFalse(g.has_edge(1, 3))
        # print(g.all_out_edges_of_node(1))
        # print(g.all_out_edges_of_node(2))
        # print(g.all_out_edges_of_node(3))
        # print(" ")
        # print(g.all_in_edges_of_node(1))
        # print(g.all_in_edges_of_node(2))
        # print(g.all_in_edges_of_node(3))
        # print(" ")
        # g.remove_node(2)
        # print(g.all_out_edges_of_node(1))
        # print(g.all_out_edges_of_node(3))
        # print(" ")
        # print(g.all_in_edges_of_node(1))
        # print(g.all_in_edges_of_node(3))

    def test_remove_edge(self):
        """
         verify that the method remove_edge is removing the correct edge
        """
        g = DiGraph()
        g.add_node(1)
        g.add_node(2)
        g.add_edge(1, 2, 1)
        # basic graph with two vertices
        self.assertFalse(g.remove_edge(1, 1))  # there is no edge
        self.assertTrue(g.remove_edge(1, 2))  # remove the edge between (1,2)
        self.assertFalse(g.has_edge(1, 2))  # there is no edge
        self.assertFalse(g.remove_edge(1, 2))  # there is no edge
        self.assertFalse(g.remove_edge(2, 1))  # there is no edge between (2,1)
        self.assertTrue(g.add_edge(2, 1, 5))
        self.assertTrue(g.remove_edge(2, 1))  # remove the edge
        self.assertTrue(g.add_edge(2, 1, 1))  # the edge removed

    def test_v_size(self):
        """
        v_size return the correct number of vertices in the graph
        """
        g = DiGraph()
        g.add_node(1)
        g.add_node(2)
        self.assertEqual(g.VSize, 2)
        g.remove_node(2)
        self.assertEqual(g.VSize, 1)  # node 2 has been removed
        g.remove_node(1)
        self.assertEqual(g.VSize, 0)  # node 1 has been removed
        self.assertFalse(g.remove_node(1))  # node 1 is not in the graph
        self.assertEqual(g.VSize, 0)  # Vsize is 0
        g.add_node(1)
        g.add_node(2)
        g.add_node(3)
        g.add_edge(1, 2, 1)
        self.assertEqual(g.VSize, 3)  # there are three vertices in the graph
        g.remove_node(2)
        self.assertEqual(g.VSize, 2)

    def test_e_size(self):
        """
        e_size return the correct number of edges in the graph
        """
        g = DiGraph()
        g.add_node(1)
        g.add_node(2)
        g.add_edge(1, 2, 1)
        self.assertEqual(g.ESize, 1)  # there is one edge in the graph
        self.assertTrue(g.remove_edge(1, 2))  # remove the edge
        self.assertEqual(g.ESize, 0)  # there is no edge in the graph
        self.assertTrue(g.add_edge(1, 2, 1))
        self.assertTrue(g.add_edge(2, 1, 2))
        self.assertEqual(g.ESize, 2)
        self.assertFalse(g.add_edge(2, 1, 4))  # update the weight of the edge
        self.assertEqual(g.ESize, 2)  # the edge size is still 2
        self.assertTrue(g.remove_node(1))  # node1 has connected with two edges
        self.assertEqual(g.ESize, 0)  # there is no edge in the graph

    def test_get_mc(self):
        """
        verify that each change in the graph the mc increased at least by 1
        """
        g = DiGraph()
        self.assertEqual(g.get_mc(), 0)  # there are no changes made in the graph
        g.add_node(1)
        self.assertEqual(g.get_mc(), 1)  # added one node to the graph
        g.remove_node(1)
        self.assertEqual(g.get_mc(), 2)  # the node has been removed
        g.add_node(1)
        g.add_node(2)
        self.assertEqual(g.get_mc(), 4)
        g.add_edge(1, 2, 1)
        self.assertEqual(g.get_mc(), 5)  # after the edge was connected the mc should be increased by 1
        g.remove_edge(1, 2)
        self.assertEqual(g.get_mc(), 6)
        self.assertFalse(g.remove_edge(1, 2))  # there is no edge between (1,2)
        self.assertEqual(g.get_mc(), 6)  # the mc should stay 6
        self.assertFalse(g.remove_node(3))  # 3 is not in the graph
        self.assertEqual(g.get_mc(), 6)  # the mc should stay 7
        g.add_edge(1, 2, 2)
        self.assertEqual(g.get_mc(), 7)
        g.add_edge(1, 2, 2)
        self.assertEqual(g.get_mc(), 7)
        g.add_edge(1, 2, 3)
        self.assertEqual(g.get_mc(), 7)  # the weight of the edge has been update ,so the mc increased by 1

    def test_get_all_v(self):
        """
        get_all_v need to return all the vertices in the graph
        """
        g = DiGraph()
        self.assertEqual(g.get_all_v(), {})  # there are no edges in the graph
        g.add_node(1)
        p_node = NodeData(key=1)
        g_vertices = {1: p_node}
        self.assertEqual(g.get_all_v(), g_vertices)
        g.remove_node(1)
        self.assertEqual(g.get_all_v(), {})




if __name__ == '__main__':
     unittest.main()


























