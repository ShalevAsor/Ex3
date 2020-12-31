import math
from typing import List


from GraphAlgoInterface import GraphAlgoInterface


class GraphAlgo(GraphAlgoInterface):
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


    def __init__(self, graph=None):
        """
        init graph algo to work on a specific graph
        :param graph: the graph of GraphAlgo
        """
        self.Graph = graph

    def load_from_json(self, file_name: str) -> bool:
        pass

    def save_to_json(self, file_name: str) -> bool:
        pass

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        """
          return list represent the shortest path from the source vertex to the destination vertex
         src--->node1---->node2----->...----->dest
        this method based on Dijkstra's algorithm.
        :param id1:the src node
        :param id2:the dest node
        :return: list of the shortest path
        """
        pass

    def connected_component(self, id1: int) -> list:
        pass

    def connected_components(self) -> List[list]:
        pass

    def plot_graph(self) -> None:
        pass

    # --------------------------- algorithms ------------------------ #
   # def Dijkstras(self) ->tuple:


