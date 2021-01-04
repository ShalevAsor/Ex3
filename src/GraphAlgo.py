import math
from typing import List
from collections import deque
import heapq
import json
from src import GraphInterface
from src.DiGraph import DiGraph
from src.edge_data import EdgeData
from src.node_data import NodeData
from src.GraphAlgoInterface import GraphAlgoInterface
from src.DiGraph import DiGraph


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

        def __init__(self, parent: int, current: int, weight: float = math.inf):
            self.parent_key = parent
            self.current_key = current
            self.weight = weight

        def __repr__(self):
            return f"cur_key:{self.current_key},p_key:{self.parent_key},weight:{self.weight}"

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
        loaded = False
        g = DiGraph()
        try:
            with open(file_name, "r") as file:
                my_graph = json.load(file)
                list_of_nodes=my_graph["Nodes"]
                list_of_edges=my_graph["Edges"]
                for k in list_of_nodes:
                    g.add_node(k["id"],k["pos"])
                for k in list_of_edges:
                    g.add_edge(k["src"], k["dest"], k["w"])

                loaded = True
        except IOError as ex:
            print(ex)
        finally:
            self.Graph=g
            return loaded

    def save_to_json(self, file_name: str) -> bool:
        saved = False
        try:
            with open(file_name, "w") as file:
                # json.dump(["Nodes", self.Graph.Nodes, "Edges", self.Graph.Edges], default=lambda o: o.__dict__,
                #           fp=file)
                json.dump( self.Graph, default=lambda o: o.__dict__,
                          fp=file)
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
            return (-1, [])  # there is no path
        s_path = [float, []]
        p_t = self.dijkstras(self.get_graph().get_node(id1), self.get_graph().get_node(id2))
        i, size, no_path = 0, len(p_t[1]), 0
        p_s_node = self.get_sub_node(p_t[1], id2)  # get_sub_node return the node by the give key from the list
        if p_s_node is None: return (-1, [])  # get_sub_node returned None= there is no path
        s_path[1].append(p_s_node.current_key)  # add to the list
        s_path[0] = p_s_node.weight  # the shortest path weight
        while p_s_node.current_key != id1:
            s_path[1].append(p_s_node.parent_key)  # add the parent
            p_s_node = self.get_sub_node(p_t[1], p_s_node.parent_key)  # to get his parent
            if no_path == size - 1:  # there is no path
                return (-1, [])
            no_path += 1
        s_path[1].reverse()  # reverse the list
        return tuple(s_path)

    def connected_component(self, id1: int) -> list:
        if self.Graph.get_node(id1) is None or self.Graph is None:
            return None

        stack = deque()
        scc = {}
        for key, value in self.Graph.get_all_v().items():
            value.visited = False
            value.w = -1
            value.t = -1

        for key, value in self.Graph.get_all_v().items():
            if value.w == -1:
                self.findSC(value, stack, scc, self.get_graph())

        self.staticNum = 0
        for key, value in scc.items():
            for x in value:
                if x.key == id1:
                    return value

        pass

    def connected_components(self) -> List[list]:
        if self.Graph is None:
            return None

        stack = deque()
        scc = {}
        for key, value in self.Graph.get_all_v().items():
            value.visited = False
            value.w = -1
            value.t = -1

        for key, value in self.Graph.get_all_v().items():
            if value.w == -1:
                self.findSC(value, stack, scc, self.get_graph())

        self.staticNum = 0
        TheList = []
        for key, value in scc.items():
            TheList.append(value)
        return TheList
        pass

    def plot_graph(self) -> None:
        pass

    def get_sub_node(self, path: list, key: int) -> SubNode:
        i = 0
        size = len(path)
        while i < size:
            if path[i].current_key == key:
                return path[i]
            i += 1

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

    def findSC(self, vertex: NodeData, stack: deque(), hashmap: {}, graph: GraphInterface):
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
                self.findSC(curr_node, stack, hashmap, graph)
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

