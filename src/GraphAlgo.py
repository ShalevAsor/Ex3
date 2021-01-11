import heapq
import json
import math
from collections import deque
from random import randint
from typing import List

import matplotlib.pyplot as plt
from matplotlib.patches import ConnectionPatch

from src import GraphInterface
from src.AbstractGraph import AbstractGraph as AG
from src.DiGraph import DiGraph
from src.GraphAlgoInterface import GraphAlgoInterface
from src.node_data import NodeData


class GraphAlgo(GraphAlgoInterface):
    staticNum = 0
    """
    This class represent directed weighted graph algorithms, it support basic methods like load and save from json file.
    it also support few algorithms like BFS and Dijkstra's  that used for methods like connected_component
    and shortestPath.
    each method in this class is attached with explanations.
    """

    # ---------------------inner class--------------------- #
    class SubNode:
        """
        This inner class used in Dijkstra's Algorithm
        """

        def __init__(self, parent: int, current: int, weight: float = math.inf, name = None):
            self.parent_key = parent
            self.current_key = current
            self.weight = weight

            #  *--------Trajan's variables-----------*
            self.name = name
            self.index = None
            self.lowlink = None
            self.adj = []
            self.on_stack = False

        def __repr__(self):
            return f"cur_key:{self.current_key},p_key:{self.parent_key},weight:{self.weight}"

        def __le__(self, other):
            if self.weight < other.weight:
                return -1
            else:
                return 1

        def __lt__(self, other):
            if self.weight < other.weight:
                return -1
            else:
                return 1
            # ---------------------GraphAlgo methods--------------------- #

    def __init__(self, graph: GraphInterface = None):
        """
        init graph algo to work on a specific graph
        :param graph: the graph of GraphAlgo
        """
        self.Graph = graph

    def get_graph(self) -> GraphInterface:
        """
        :return: the directed weighted graph that the GraphAlgo works on
        """
        return self.Graph

    def load_from_json(self, file_name: str) -> bool:
        """
        load graph represents in a json file , this load method support two types of json files
        :param file_name: the path of the json
        :return: true if the loading process was completed successfully, else return false
        """
        loaded = False
        g = DiGraph()
        try:
            with open(file_name, "r") as file:
                my_graph = json.load(file)
                # empty graph case:
                if my_graph is None:
                    g = DiGraph()
                    self.Graph = g
                    loaded = True
                    return True
                # the graph is not empty
                list_of_nodes = my_graph["Nodes"]
                list_of_edges = my_graph["Edges"]

                try:
                    for k in list_of_nodes:
                        if 'pos' in k:  # the node has a position
                            p = tuple(float(i) for i in k["pos"].strip("()").split(","))  # string to float
                            g.add_node(k["id"], p)
                        else:  # add only the key of the node
                            g.add_node(k["id"])
                    for k in list_of_edges:  # add the edges
                        g.add_edge(k["src"], k["dest"], k["w"])
                except AttributeError:  # the second json format
                    for k in list_of_nodes:
                        if "pos" in k:  # the node has a position
                            try:
                                p = tuple(float(i) for i in k["pos"].strip("()").split(","))  # string to flaot
                                g.add_node(k["key"], p)  # add the key and the pos
                            except AttributeError:
                                p = k.get("pos")
                                g.add_node(k["key"], (float(p[0]), float(p[1]), float(p[2])))  # string to float
                        else:
                            g.add_node(k["key"])  # add the key of the node

                    for k in list_of_edges:  # add the edges
                        g.add_edge(k["src"], k["dest"], k["weight"])

                loaded = True
        except IOError as ex:
            print(ex)
        finally:
            self.Graph = g  # init the graph
            return loaded

    def save_to_json(self, file_name: str) -> bool:
        """
        save the graph into a json file
        :param file_name: the path of the file
        :return: true if the save process was completed successfully, else return false
        """
        saved = False
        Edges = []
        if self.get_graph() is None:  # the graph is empty
            try:
                with open(file_name, "w") as file:
                    json.dump(self.get_graph(), fp=file)
                    saved = True
            except IOError as ex:
                print(ex)
            return saved
        else:  # make list of nodes and edges and add it into a AbstractGraph object
            Nodes = list(self.get_graph().get_all_v().values())
            for node in Nodes:
                curr_node_neighbors = self.get_graph().all_out_edges_of_node(node.key)
                for neigh_node in curr_node_neighbors:
                    Edges.append(self.get_graph().get_edge(node.key, neigh_node))
            graph_obj = AG(Nodes, Edges)
            try:  # use dump from the AG object
                with open(file_name, "w") as file:
                    json.dump(graph_obj, default=lambda o: o.__dict__, fp=file)
                    saved = True
            except IOError as ex:
                print(ex)
            finally:
                return saved

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        """
          return list represent the shortest path from the source vertex to the destination vertex
         src--->node1---->node2----->...----->dest
        this method based on Dijkstra's algorithm.
        :param id1:the src node
        :param id2:the dest node
        :return: list of the shortest path
        """
        if id1 not in self.Graph.Nodes or id2 not in self.Graph.Nodes:
            return (float('inf'), [])  # there is no path
        s_path = [float, []]
        p_t = self.dijkstras(self.get_graph().get_node(id1), self.get_graph().get_node(id2))
        i, size, no_path = 0, len(p_t[1]), 0
        p_s_node = self.get_sub_node(p_t[1], id2)  # get_sub_node return the node by the give key from the list
        if p_s_node is None: return (float('inf'), [])  # get_sub_node returned None= there is no path
        s_path[1].append(p_s_node.current_key)  # add to the list
        s_path[0] = p_s_node.weight  # the shortest path weight
        while p_s_node.current_key != id1:
            s_path[1].append(p_s_node.parent_key)  # add the parent
            p_s_node = self.get_sub_node(p_t[1], p_s_node.parent_key)  # to get his parent
            if no_path == size - 1:  # there is no path
                return (float('inf'), [])
            no_path += 1
        s_path[1].reverse()  # reverse the list
        return tuple(s_path)

    def connected_component(self, id1: int) -> list:
        """
        this function is taking the main trajan's algorithm
        and iterates each list in the list of strongly
        connected components until it finds the
        desired node id, then returns the list it was found at.
        Returns
        -------
        """
        if self.Graph.get_node(id1) is None or self.Graph is None:
            return []
        listA = self.Trajans()
        for scc in listA:
            if id1 in scc:
                return scc
        return None

    def connected_components(self) -> List[list]:
        """
        Returns simple returns the value of trajan's algorithm
        aka List(list) of strongly connected components
        """
        if self.Graph is None:
            return []
        return self.Trajans()

    def plot_graph(self) -> None:
        # data members
        positionOfNodes = {}
        nodes_list = self.Graph.get_all_v().values()
        edges_list = list()
        x_max = 0
        y_max = 0
        history = {}
        for node in nodes_list:
            if node.get_x() > x_max:
                x_max = node.get_x()
            if node.get_y() > y_max:
                y_max = node.get_y()

        for node in nodes_list:
            if node.pos is None:  # take care of a case where node dont have position
                if x_max == 0 and y_max == 0:  # in case all nodes without position we pick a arena in size of nodes*7
                    x_max = randint(len(nodes_list), len(nodes_list) * 10)
                    y_max = randint(len(nodes_list), len(nodes_list) * 10)
                x_final = x_max
                y_final = y_max
                if x_final in history.keys():  # in case of duplicate generated pos,
                    temp = x_final
                    x_final = randint(0, x_max)  # we randomize until we get a new one,
                    y_final = randint(0, y_max)  # therefore time complexity increases but
                    if x_final == temp and hash(temp) in history.keys():
                        x_final = hash(temp)
                    else:
                        x_final += hash(hash(temp))

                node.pos = (x_final, y_final, 0)  # graph will look more elegant

            #  add node position x,y values in two lists
            positionOfNodes[node.key] = [node.get_x(), node.get_y()]
            history[node.get_x()] = node.get_y()
            #  visit each node's neighbor to track all edges
            curr_node_neighbors = self.Graph.all_out_edges_of_node(node.key).values()
            for neigh_node in curr_node_neighbors:
                #  insert each edge as (src,dest) tuple in the list
                edges_list.append((node.key, neigh_node.key))
        # print(edges_list)

        # plot for the nodes and their annotation
        fig, ax1 = plt.subplots(figsize=(12.8, 14.2))
        for node, value in positionOfNodes.items():
            ax1.scatter(value[0], value[1], c='c')

            ax1.annotate(node, (value[0], value[1]), alpha=1)

        # creating arrows for each edge by iterating the edges_list
        coordsA = "data"
        coordsB = "data"
        for edge in edges_list:
            node_src = self.Graph.get_node(edge[0])
            node_dest = self.Graph.get_node(edge[1])
            xyA = (node_src.get_x(), node_src.get_y())
            xyB = (node_dest.get_x(), node_dest.get_y())
            con = ConnectionPatch(xyA, xyB, coordsA, coordsB,
                                  arrowstyle="-|>", shrinkA=10, shrinkB=9,
                                  mutation_scale=20, alpha=0.6, fc="k")
            ax1.add_artist(con)
        plt.title('Directed_Weighted_Graph')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.show()

    def get_sub_node(self, path: list, key: int) -> SubNode:
        i = 0
        size = len(path)
        while i < size:
            if path[i].current_key == key:
                return path[i]
            i += 1

    def __eq__(self, o: GraphInterface) -> bool:
        if self is o: return True
        return self.Graph.__eq__(o.Graph)

    def __repr__(self):
        return f"GraphAlgo:{self.Graph}"

    # --------------------------- algorithms ------------------------ #
    def dijkstras(self, src: NodeData, dest: NodeData) -> list:
        """
         Dijkstras algorithm - https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
        :param src: the source of the path
        :param dest:the destination of the path
        :return: list of weight and  path
        """
        short_path = []
        visited = {int: int}
        dist_and_path = [0.0, [int]]
        heap_priority = []
        sub_node = GraphAlgo.SubNode(src.key, src.key, 0.0)  # create subnode for the src
        heapq.heappush(heap_priority, (0.0, sub_node))  # add the src to the heap
        while len(heap_priority) != 0:
            p_sub_node = heapq.heappop(heap_priority)[1]  # get and remove the subnode with the lowest weight
            current_key = p_sub_node.current_key
            if dest.key == current_key:  # the path has found
                short_path.append(p_sub_node)
                return [p_sub_node.weight, short_path]
            if current_key not in visited:  # this vertex is not visited
                visited[current_key] = 1  # mark him as visited
                short_path.append(p_sub_node)  # add him to the path
                dist_and_path[0] += p_sub_node.weight  # add the weight
                for p_edge in self.Graph.all_out_edges_of_node(current_key):  # all this node  out neighbors
                    if p_edge not in visited:
                        p_dest = GraphAlgo.SubNode(current_key, p_edge)
                        smallest_weight = p_sub_node.weight + self.get_graph().get_edge(current_key, p_edge).weight
                        if smallest_weight < p_dest.weight:
                            p_dest.weight = smallest_weight
                            heapq.heappush(heap_priority, (p_dest.weight, p_dest))  # add the tuple to the heap
                            # Note: the heap compare the weight of the vertex
                            dist_and_path[0] += p_dest.weight
        dist_and_path[1] = short_path
        return dist_and_path

    # this is the recursive trajan algorithm implementation that first firstly used
    # unfortunately this version does not support large graphs in python due to stackoverflow of recursive calls
    # therefore we had to implement an iterative version of it
    def find_sc(self, vertex: NodeData, stack: deque, hashmap: {}, graph: GraphInterface):
        """
        Trajan's algorithm - https://en.wikipedia.org/wiki/Tarjan%27s_strongly_connected_components_algorithm
        :param vertex: NodeData
        :param stack: deque()
        :param hashmap: dictionary
        :param graph: DiGraph
        :return: void
        function will manipulate the given hashmap so that each value is a list of nodes in the same
        strongly connected component represented by the key
        """
        stack.append(vertex)
        vertex.visited = True
        vertex.w = self.staticNum
        vertex.t = self.staticNum
        self.staticNum += 1
        for key, curr_node in self.get_graph().all_out_edges_of_node(vertex.key).items():
            if curr_node.w == -1:
                self.find_sc(curr_node, stack, hashmap, graph)
                vertex.t = (min(vertex.t, curr_node.t))
            elif curr_node.visited:
                vertex.t = (min(vertex.t, curr_node.w))

        tmp = -1
        if vertex.t == vertex.w:
            while tmp != vertex.key:
                node = stack.pop()
                tmp = node.key
                if vertex.t not in hashmap:
                    hashmap[vertex.t] = []
                    hashmap[vertex.t].append(node)
                else:
                    hashmap[vertex.t].append(node)

                node.visited = False


    def Trajans(self) -> [[]]:
        """
        this is the iterative implementation of trajan's algorithm
        Returns list(list()) including all the Strongly connected component
        -------

        """
        ed = {}
        for n in self.get_graph().get_all_v().keys():
            ed[n] = self.SubNode(-1, -1, -1, n)

        for n in self.get_graph().get_all_v().keys():
            for neigh in self.get_graph().all_out_edges_of_node(n).keys():
                ed[n].adj.append(ed[neigh])
        vs = ed.values()
        i = 0
        stack = []
        call_stack = []
        comps = []
        for v in vs:
            if v.index is None:
                call_stack.append((v, 0))
                while call_stack:
                    v, pi = call_stack.pop()
                    # If this is first time we see v
                    if pi == 0:
                        v.index = i
                        v.lowlink = i
                        i += 1
                        stack.append(v)
                        v.on_stack = True
                    # If we just backtracked on something
                    if pi > 0:
                        prev = v.adj[pi - 1]
                        v.lowlink = min(v.lowlink, prev.lowlink)
                    # Find the next thing to recurse on
                    while pi < len(v.adj) and v.adj[pi].index is not None:
                        w = v.adj[pi]
                        if w.on_stack:
                            v.lowlink = min(v.lowlink, w.index)
                        pi += 1
                    # If we found something with index=None, recurse
                    if pi < len(v.adj):
                        w = v.adj[pi]
                        call_stack.append((v, pi + 1))
                        call_stack.append((w, 0))
                        continue
                    # If v is the root of a connected component
                    if v.lowlink == v.index:
                        comp = []
                        while True:
                            w = stack.pop()
                            w.on_stack = False
                            comp.append(w.name)
                            if w is v:
                                break
                        comps.append(comp)
        return comps