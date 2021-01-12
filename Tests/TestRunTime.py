import json
import unittest
import networkx as nx
from src.GraphAlgo import GraphAlgo
from src.DiGraph import DiGraph
from src.node_data import NodeData
import sys
import random
from datetime import datetime


def compares_run_time_cc(v_size: int, e_size: int) -> list:
    """
    This method compares the run time of connected_components between GraphAlgo to networkx
    the edges and node positions are randomly
    :param v_size: number of vertices
    :param e_size:  number of edges
    :return: list, int the first place networkx graph results and the second GraphAlgo results
    """
    graph_list = graph_generator(v_size, e_size)  # graph A
    graph_algo = graph_list[0]  # graph algo and nx graph has the same vertices and edges
    nx_graph = graph_list[1]
    start_time = datetime.now()  # calculation of run time
    nx_results = nx.strongly_connected_components(nx_graph)
    end_time = datetime.now()
    nx_toList = []
    for cc in nx_results:
        nx_toList.append([n for n in cc])
    run_time_nx = end_time - start_time
    print("run time of networkx graph:", run_time_nx)
    start_time = datetime.now()  # calculation of run time
    my_results = graph_algo.connected_components()
    end_time = datetime.now()
    run_time_my = end_time - start_time
    print("run time of GraphAlgo :", run_time_my)
    for list in nx_toList:  # sorting inner lists
        list.sort()
    for list in my_results:  # sorting inner lists
        list.sort()
    return [nx_toList, my_results]


def compares_run_time_cc_json(file_name: str) -> list:
    """
    Compares the running time of the Connected components method in GraphAlgo  and Networkx
    The graph is created from json file
    :param file_name:
    :return: list , the first place is the results of nx graph and the second is the results of GraphAlgo
    """
    graph_algo = GraphAlgo()
    graph_algo.load_from_json(file_name)  # load the json
    g = nx.Graph()
    nx_graph = g.to_directed()
    for node in graph_algo.get_graph().get_all_v().values():  # copies all data to nx_graph
        nx_graph.add_node(node.key, pos=node.pos)
    for edges in graph_algo.get_graph().Edges.values():
        for edge in edges.values():
            nx_graph.add_edge(edge.src, edge.dest, weight=edge.weight)
    start_time = datetime.now()  # cc run time of networkx
    nx_results = nx.strongly_connected_components(nx_graph)
    end_time = datetime.now()
    nx_toList = []
    for cc in nx_results:
        nx_toList.append([n for n in cc])
    run_time_nx = end_time - start_time
    print("run time of networkx graph:", run_time_nx)
    start_time = datetime.now()  # cc run time of GraphAlgo
    my_results = graph_algo.connected_components()
    end_time = datetime.now()
    run_time_my = end_time - start_time
    print("run time of GraphAlgo :", run_time_my)

    for list in nx_toList:      # sorting inner lists
        list.sort()
    for list in my_results:     # sorting inner lists
        list.sort()
    return [nx_toList, my_results]


def compares_run_time_cc_of_node(node_id: int, v_size: int, e_size: int) -> list:
    """
    This method compares the run time of connected_component between GraphAlgo to networkx
    the edges and node positions are randomly
    :param v_size: number of vertices
    :param e_size:  number of edges
    :param node_id: the key of the vertex
    :return: list, int the first place networkx graph results and the second GraphAlgo results
    """
    graph_list = graph_generator(v_size, e_size)  # graph A
    graph_algo = graph_list[0]
    nx_graph = graph_list[1]
    nx_results = []
    start_time = datetime.now()
    for cc_of_node in nx.strongly_connected_components(nx_graph):  # use strongly connected components to get the cc
        # of node
        if node_id in cc_of_node:
            nx_results = list(cc_of_node)
    end_time = datetime.now()
    run_time_nx = end_time - start_time
    print("run time of networkx graph:", run_time_nx)
    start_time = datetime.now()
    my_results = graph_algo.connected_component(node_id)
    end_time = datetime.now()
    cc = list()
    i = 0
    for node in my_results:
        cc.append(node)
        i += 1
    cc.sort(reverse=True)  # sort the list
    nx_results.sort(reverse=True)
    run_time_graph_algo = end_time - start_time
    print("run time of GraphAlgo :", run_time_graph_algo)
    return [nx_results, cc]


def compares_run_time_cc_of_node_json(node_id: int, file_name: str) -> list:
    """
    Compares the running time of the Connected component method in GraphAlgo  and Networkx
    The graph is created from json file
    :param node_id:
    :param file_name:
    :return:
    """
    graph_algo = GraphAlgo()
    graph_algo.load_from_json(file_name)
    g = nx.Graph()
    nx_graph = g.to_directed()
    for node in graph_algo.get_graph().get_all_v().values():
        nx_graph.add_node(node.key, pos=node.pos)
    for edges in graph_algo.get_graph().Edges.values():
        for edge in edges.values():
            nx_graph.add_edge(edge.src, edge.dest, weight=edge.weight)
    start_time = datetime.now()
    for cc_of_node in nx.strongly_connected_components(nx_graph):
        if node_id in cc_of_node:
            nx_results = cc_of_node
    end_time = datetime.now()
    run_time_nx = end_time - start_time
    print("run time of networkx graph:", run_time_nx)
    start_time = datetime.now()
    my_results = graph_algo.connected_component(node_id)
    end_time = datetime.now()
    cc = list()
    i = 0
    for node in my_results:
        cc.append(node)
        i += 1
    cc.sort()
    run_time_graph_algo = end_time - start_time
    print("run time of GraphAlgo :", run_time_graph_algo)
    nx_results_toList = []
    for i in nx_results:
        nx_results_toList.append(i)
    return [nx_results_toList, cc]


def compares_run_time_sp(src: int, dest: int, v_size: int, e_size: int) -> list:
    """
    This method compares the run time of shortest_path method between GraphAlgo to networkx
    the edges and node positions are randomly
    :param v_size: number of vertices
    :param e_size:  number of edges
    :return: list, int the first place networkx graph results and the second GraphAlgo results
    """
    results = [float('inf'), [], float('inf'), []]
    graph_list = graph_generator(v_size, e_size)
    graph_algo = graph_list[0]
    nx_graph = graph_list[1]
    start_time = datetime.now()
    try:  # use try and except in case that there is no path
        nx_path = nx.shortest_path(nx_graph, src, dest, weight="weight")
        end_time = datetime.now()
        run_time_nx = end_time - start_time
        print("run time of networkx graph:", run_time_nx)
        results[1] = nx_path
    except Exception as ex:
        print(ex)
        end_time = datetime.now()
        run_time_nx = end_time - start_time
        print("run time of networkx graph:", run_time_nx)
    try:  # the shortest path length not included in the run time of shortest path
        nx_length = nx.shortest_path_length(nx_graph, src, dest, weight="weight")
        results[0] = nx_length
    except Exception as ex:
        print(ex)
    start_time = datetime.now()
    graph_algo_results = graph_algo.shortest_path(src, dest)
    end_time = datetime.now()
    run_time_my = end_time - start_time
    print("run time of GraphAlgo :", run_time_my)
    results[2] = graph_algo_results[0]
    results[3] = graph_algo_results[1]
    return results


def compares_run_time_sp_json(src: int, dest: int, file_name: str) -> list:
    """
    Compares the running time of the shortest path method in GraphAlgo  and Networkx
    The graph is created from json file
    :param file_name: json path
    :param src: source of the path
    :param dest: destination of the path
    """
    results = [-1, [], -1, []]
    graph_algo = GraphAlgo()
    graph_algo.load_from_json(file_name)
    g = nx.Graph()
    nx_graph = g.to_directed()
    for node in graph_algo.get_graph().get_all_v().values():
        nx_graph.add_node(node.key, pos=node.pos)
    for edges in graph_algo.get_graph().Edges.values():
        for edge in edges.values():
            nx_graph.add_edge(edge.src, edge.dest, weight=edge.weight)
    start_time = datetime.now()
    try:
        nx_path = nx.shortest_path(nx_graph, src, dest, weight="weight")
        end_time = datetime.now()
        run_time_nx = end_time - start_time
        print("run time of networkx graph:", run_time_nx)
        results[1] = nx_path
    except Exception as ex:
        print(ex)
        end_time = datetime.now()
        run_time_nx = end_time - start_time
        print("run time of networkx graph:", run_time_nx)
    try:
        nx_length = nx.shortest_path_length(nx_graph, src, dest, weight="weight")
        results[0] = nx_length
    except Exception as ex:
        print(ex)
    start_time = datetime.now()
    graph_algo_results = graph_algo.shortest_path(src, dest)
    end_time = datetime.now()
    run_time_my = end_time - start_time
    print("run time of GraphAlgo :", run_time_my)
    results[2] = graph_algo_results[0]
    results[3] = graph_algo_results[1]
    return results


def graph_generator(v_size: int, e_size: int) -> list:
    """
    generate graph with v_size vertices and e_size edges randomly
    :param v_size: number of vertices
    :param e_size: number of edges
    :return: GraphAlgo with the given number of edges and vertices
    """

    my_graph = DiGraph()
    g = nx.Graph()
    nx_graph = g.to_directed()
    v, e = 1, 1
    while v <= v_size:
        x = random.uniform(0.1, 35)
        y = random.uniform(0.1, 35)
        position = (x, y, 0)
        my_graph.add_node(v, pos=position)
        nx_graph.add_node(v, pos=position)
        v += 1
    while e <= e_size:
        r_src = random.randint(1, v_size)
        r_dest = random.randint(1, v_size)
        r_weight = random.uniform(0.1, 200.1)
        if not my_graph.has_edge(r_src, r_dest):
            my_graph.add_edge(r_src, r_dest, r_weight)
            nx_graph.add_edge(r_src, r_dest, weight=r_weight)
            e += 1

    graph_algo = GraphAlgo(my_graph)
    return [graph_algo, nx_graph]


def load_java(self) -> list:
    """
    function to load the java results file
    used for single purpose
    """
    try:
        with open("../data/JavaResults", "r") as file:
            jsonObject = json.load(file)
            ConnectedComponentsToNode = jsonObject["ConnectedComponentsToNode"]
            NumOfScc = jsonObject["NumOfScc"]
            ShortestPathDist = jsonObject["ShortestPathDist"]
            ShortestPath = jsonObject["ShortestPath"]
            list = [ConnectedComponentsToNode, NumOfScc, ShortestPathDist, ShortestPath]
            return list
    except IOError as ex:
        print(ex)


class MyTestCase(unittest.TestCase):
    """
    compares the run time of three type of graphs:  GraphAlgo, DW_GraphAlgo(java), and networkx directed weighted graph
    each test examines the runtime of each graph and the correctness of the results
    """

    def test_comparison_shortest_path(self):
        """
        In this test we will compare the performance of the networkx library
        against the performance of our graph in java,
        in comparison we will refer to the run times and compare the results of the shortest path
        this test checks the above on four graphs and graphs from json files:
        graph A: 100 vertices 1k edges, B: 1k v, 10k e , C:  10kv, 100k e, D: 100k v, 1m e
        """
        shortest_pd = load_java(self)[2]
        shortest_p = load_java(self)[3]
        print("shortest_path:\n")
        # -------------graph A------------#
        print("Graph A:\n")
        results = compares_run_time_sp(1, 30, 100, 1000)
        self.assertEqual(results[0], results[2])  # path weight of networkx and GrpahAlgo
        self.assertEqual(results[1], results[3])  # path of networkx nad GraphAlgo
        # -------------graph B------------#
        print("\nGraph B:\n")
        results = compares_run_time_sp(10, 900, 1000, 10000)
        self.assertEqual(results[0], results[2])  # path weight of networkx and GrpahAlgo
        self.assertListEqual(results[1], results[3])  # path of networkx nad GraphAlgo
        # -------------graph C------------#
        print("\nGraph C:\n")
        results = compares_run_time_sp(2800, 36, 10000, 100000)
        self.assertEqual(results[0], results[2])  # path weight of networkx and GrpahAlgo
        self.assertListEqual(results[1], results[3])  # path of networkx nad GraphAlgo
        # -------------graph D------------#
        print("\nGraph D:\n")
        results = compares_run_time_sp(15000, 99999, 100000, 1000000)
        self.assertEqual(results[0], results[2])  # path weight of networkx and GrpahAlgo
        self.assertListEqual(results[1], results[3])  # path of networkx nad GraphAlgo
        # -------------graph A5 from data folder------------#
        print("shortest_path (json):\n")
        print("\nGraph A5:\n")
        file_name = "../data/A5"
        results = compares_run_time_sp_json(1, 6, file_name)
        self.assertEqual(results[0], results[2])  # path weight of networkx and GrpahAlgo
        self.assertListEqual(results[1], results[3])  # path of networkx nad GraphAlgo
        self.assertEqual(results[2], shortest_pd[1])  # path weight of java and GraphAlgo
        self.assertEqual(results[3], shortest_p[1])  # path of java and GraphAlgo
        # -------------graph G_10_80_0.json from data folder------------#
        print("\nGraph G_10_80_0:\n")
        file_name = "../data/G_10_80_0.json"
        results = compares_run_time_sp_json(1, 4, file_name)
        self.assertEqual(results[0], results[2])  # path weight of networkx and GrpahAlgo
        self.assertListEqual(results[1], results[3])  # path of networkx nad GraphAlgo
        self.assertEqual(results[2], shortest_pd[4])  # path weight of java and GraphAlgo
        self.assertEqual(results[3], shortest_p[4])  # path of java and GraphAlgo
        # -------------graph G_1000_8000_0.json from data folder------------#
        print("\nGraph G_1000_8000_0:\n")
        file_name = "../data/G_1000_8000_0.json"
        results = compares_run_time_sp_json(0, 44, file_name)
        self.assertEqual(results[0], results[2])  # path weight of networkx and GrpahAlgo
        self.assertListEqual(results[1], results[3])  # path of networkx nad GraphAlgo
        self.assertEqual(results[2], shortest_pd[7])  # path weight of java and GraphAlgo
        self.assertEqual(results[3], shortest_p[7])  # path of java and GraphAlgo
        # -------------graph G_20000_160000_0.json from data folder------------#
        print("\nGraph G_20000_160000_0:\n")
        file_name = "../data/G_20000_160000_0.json"
        results = compares_run_time_sp_json(18, 1500, file_name)
        self.assertEqual(results[0], results[2])  # path weight of networkx and GrpahAlgo
        self.assertListEqual(results[1], results[3])  # path of networkx nad GraphAlgo
        self.assertEqual(results[2], shortest_pd[10])  # path weight of java and GraphAlgo
        self.assertEqual(results[3], shortest_p[10])  # path of java and GraphAlgo
        # -------------graph G_30000_240000_0.json from data folder------------#
        print("\nGraph G_30000_240000_0:\n")
        file_name = "../data/G_30000_240000_0.json"
        results = compares_run_time_sp_json(1203, 3, file_name)
        self.assertEqual(results[0], results[2])  # path weight of networkx and GrpahAlgo
        self.assertListEqual(results[1], results[3])  # path of networkx nad GraphAlgo
        self.assertEqual(results[2], shortest_pd[13])  # path weight of java and GraphAlgo
        self.assertEqual(results[3], shortest_p[13])  # path of java and GraphAlgo
        # -------------------------- on_circle-------------------------#
        # -------------graph G_30000_240000_1.json from data folder------------#
        print("\nGraph G_30000_240000_1:\n")
        file_name = "../data/G_30000_240000_1.json"
        results = compares_run_time_sp_json(24, 605, file_name)
        self.assertEqual(results[0], results[2])  # path weight of networkx and GrpahAlgo
        self.assertListEqual(results[1], results[3])  # path of networkx nad GraphAlgo
        # -------------graph G_20000_160000_1.json from data folder------------#
        print("\nGraph G_20000_160000_1:\n")
        file_name = "../data/G_20000_160000_1.json"
        results = compares_run_time_sp_json(1, 82, file_name)
        self.assertEqual(results[0], results[2])  # path weight of networkx and GrpahAlgo
        self.assertListEqual(results[1], results[3])  # path of networkx nad GraphAlgo
        # -------------graph G_10000_80000_1.json from data folder------------#
        print("\nGraph G_10000_80000_1:\n")
        file_name = "../data/G_10000_80000_1.json"
        results = compares_run_time_sp_json(91, 4, file_name)
        self.assertEqual(results[0], results[2])  # path weight of networkx and GrpahAlgo
        self.assertListEqual(results[1], results[3])  # path of networkx nad GraphAlgo

    def test_comparison_connected_components(self):
        """
        In this test we will compare the performance of the networkx library
        against the performance of GraphAlgo
        in comparison we will refer to the run times and compare the results of the shortest path
        this test checks the above on four sizes of graphs
        graph A: 100 vertices 100 edges, B: 10k v, 10k e , C:  100kv, 100k e, D: 1m v, 100k e
        """
        print("connected_components:\n")

        # -------------graph A------------#
        print("Graph A:")
        results = compares_run_time_cc(100, 100)
        print(results[0])
        self.assertEqual(results[0], results[1])
        # -------------graph B------------#
        print("\nGraph B:\n")
        results = compares_run_time_cc(10000, 10000)
        self.assertEqual(results[0], results[1])
        # -------------graph C------------#
        print("\nGraph C:\n")
        results = compares_run_time_cc(100000, 100000)
        self.assertEqual(results[0], results[1])
        # -------------graph D------------#
        print("\nGraph D:\n")
        results = compares_run_time_cc(1000000, 100000)
        self.assertEqual(results[0], results[1])

    def test_comparison_connected_components_json(self):
        """
        In this test we will compare the performance of the networkx library
        against the performance of GraphAlgo
        in comparison we will refer to the run times and compare the results of the shortest path
        this test checks the above on graphs from json files
        """
        connected_cc = load_java(self)[1]
        print("connected_components (json):\n")
        # -------------graph A5 from data folder------------#
        print("Graph A5:\n")
        file_name = "../data/A5"
        results = compares_run_time_cc_json(file_name)
        self.assertEqual(results[0], results[1])  # compare to networkx
        self.assertEqual(results[0], connected_cc[1])  # compare to java
        # -------------graph G_10_80_0.json from data folder------------#
        print("\nGraph G_10_80_0:\n")
        file_name = "../data/G_10_80_0.json"
        results = compares_run_time_cc_json(file_name)
        self.assertEqual(results[0], results[1])  # compare to networkx
        self.assertEqual(results[0], connected_cc[4])  # compare to java
        # -------------graph G_1000_8000_0.json from data folder------------#
        print("\nGraph G_1000_8000_0:\n")
        file_name = "../data/G_1000_8000_0.json"
        results = compares_run_time_cc_json(file_name)
        self.assertEqual(results[0], results[1])  # compare to networkx
        self.assertEqual(results[0], connected_cc[7])  # compare to java

        # -------------------------- on_circle-------------------------#
        # -------------graph G_30000_240000_1.json from data folder------------#
        print("\nGraph G_30000_240000_1:\n")
        file_name = "../data/G_30000_240000_1.json"
        results = compares_run_time_cc_json(file_name)
        self.assertEqual(results[0], results[1])  # compare to networkx
        # -------------graph G_20000_160000_1.json from data folder------------#
        print("\nGraph G_20000_160000_1:\n")
        file_name = "../data/G_20000_160000_1.json"
        results = compares_run_time_cc_json(file_name)
        self.assertEqual(results[0], results[1])  # compare to networkx
        # -------------graph G_10000_80000_1.json from data folder------------#
        print("\nGraph G_10000_80000_1:\n")
        file_name = "../data/G_10000_80000_1.json"
        results = compares_run_time_cc_json(file_name)
        self.assertEqual(results[0], results[1])  # compare to networkx

    def test_comparison_connected_component(self):
        """
        In this test we will compare the performance of the networkx library
        against the performance of GraphAlgo
        in comparison we will refer to the run times and compare the results of the connected_component
        of certain id's
        this test checks the above on four sizes of graphs:
        graph A: 100 vertices 100 edges, B: 10k v, 10k e , C:  100kv, 100k e, D: 1m v, 100k e
        """
        print("connected_component:\n")
        # -------------graph A------------#
        print("Graph A:\n")
        results = compares_run_time_cc_of_node(13, 100, 100)
        self.assertEqual(results[0], results[1])
        # -------------graph B------------#
        print("\nGraph B:\n")
        results = compares_run_time_cc_of_node(990, 10000, 10000)
        self.assertEqual(results[0], results[1])
        # -------------graph C------------#
        print("\nGraph C:\n")
        results = compares_run_time_cc_of_node(1, 100000, 100000)
        self.assertEqual(results[0], results[1])
        # -------------graph D------------#
        print("\nGraph D:\n")
        results = compares_run_time_cc_of_node(430, 1000000, 100000)
        self.assertEqual(results[0], results[1])

    def test_comparison_connected_component_json(self):
        """
        In this test we will compare the performance of the networkx library
        against the performance of GraphAlgo
        in comparison we will refer to the run times and compare the results of the connected_component
        of certain node_id's
        this test checks the above on graphs from json files
        """
        connected_cc = load_java(self)[0]
        print("connected_component (json):\n")
        # -------------graph A5 from data folder------------#
        print("Graph A5:\n")
        file_name = "../data/A5"
        results = compares_run_time_cc_of_node_json(20, file_name)
        self.assertEqual(results[0], results[1])
        self.assertEqual(connected_cc[1], results[0])  # compare to java
        # -------------graph G_10_80_0.json from data folder------------#
        print("\nGraph G_10_80_0:\n")
        file_name = "../data/G_10_80_0.json"
        results = compares_run_time_cc_of_node_json(0, file_name)
        self.assertEqual(results[0], results[1])
        self.assertEqual(connected_cc[4], results[0])  # compare to java
        # -------------graph G_1000_8000_0.json from data folder------------#
        print("\nGraph G_1000_8000_0:\n")
        file_name = "../data/G_1000_8000_0.json"
        results = compares_run_time_cc_of_node_json(8, file_name)
        self.assertEqual(results[0], results[1])
        self.assertEqual(connected_cc[7], results[0])  # compare to java

        # -------------------------- on_circle-------------------------#
        # -------------graph G_30000_240000_1.json from data folder------------#
        print("\nGraph G_30000_240000_1:\n")
        file_name = "../data/G_30000_240000_1.json"
        results = compares_run_time_cc_of_node_json(444, file_name)
        self.assertEqual(results[0], results[1])
        # -------------graph G_20000_160000_1.json from data folder------------#
        print("\nGraph G_20000_160000_1:\n")
        file_name = "../data/G_20000_160000_1.json"
        results = compares_run_time_cc_of_node_json(12330, file_name)
        self.assertEqual(results[0], results[1])
        # -------------graph G_10000_80000_1.json from data folder------------#
        print("\nGraph G_10000_80000_1:\n")
        file_name = "../data/G_10000_80000_1.json"
        results = compares_run_time_cc_of_node_json(3, file_name)
        self.assertEqual(results[0], results[1])


if __name__ == '__main__':
    unittest.main()