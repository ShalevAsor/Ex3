from src.node_data import NodeData
from src.edge_data import EdgeData
from src.GraphInterface import GraphInterface


class DiGraph(GraphInterface):

    def __init__(self):
        self.Nodes = {}
        self.Edges = {}  # Quick access to edges aka. get(src).get(dest)->Edge
        self.src_to_dest = {}  # key: node id,  value: dictionary of nodes whom this node id point towards.
        self.dest_to_src = {}  # key: node id,  value: dictionary of nodes whom point towards this node id.

        self.MC = 0
        self.VSize = 0
        self.ESize = 0

    def v_size(self) -> int:
        """
        return the number of vertices in this graph
        :return: number of vertices
        """
        return self.VSize

    def e_size(self) -> int:
        """
        return the number of edges in the graph
        :return: the number of edges
        """
        return self.ESize

    def get_mc(self) -> int:
        """
         return the mode count current status,each change in the graph should
         increase the mode count
        :return: current mode count
        """
        return self.MC

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        """
        connect two nodes in the graph with the given weight and return true
        if there is an edge between this nodes the weight will be update
        if one of the vertices or the weight is negative or there is an edge already between
        (id1,id2) return false
        :param id1: the src node
        :param id2: the dest node
        :param weight: the weight of the edge (should be positive number)
        :return: true if (id1,id2) was connected successfully else return false
        """
        if weight < 0 or id1 == id2:
            return False
        elif id1 not in self.Nodes or id2 not in self.Nodes:  # if either of nodes not in the graph
            return False
        elif id2 in self.Edges.get(id1):  # Edge exist already
            return False
        else:
            e = EdgeData(id1, id2, weight)
            self.Edges[id1][id2] = e  # quick access to edges
            self.src_to_dest[id1][id2] = self.get_node(id2)  # add to list id1-->id2
            self.dest_to_src[id2][id1] = self.get_node(id1)  # add to list id2<--id1
            self.ESize += 1
            self.MC += 1
            return True

    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        """
        add a new vertex into this graph, if this vertex already in the graph return false
        :param node_id: the id of the new node
        :param pos: the node position
        :return: true if the node successfully added to the graph, else return flase
        """
        ans = False
        if node_id in self.Nodes:  # if the node already in the graph return false
            return ans
        else:
            new_node = NodeData(node_id, pos=pos)  # create a new node
            self.Nodes[node_id] = new_node  # add the node to the graph
            self.src_to_dest[node_id] = {}  # init new dictionary
            self.dest_to_src[node_id] = {}  # init new dictionary
            self.Edges[node_id] = {}  # init new dictionary
            self.VSize += 1  # increase the node size by 1
            self.MC += 1
            ans = True
        return ans

    def remove_node(self, node_id: int) -> bool:
        """
        remove the vertex that associated with the given node_id from the graph
        and remove all the edges that associated with this node_id
        :param node_id: the node that should removed from the graph
        :return: true if the node removed successfully
        """
        if node_id not in self.Nodes:  # if the node is not in the graph dont do anything
            return False
        else:
            for key in self.dest_to_src[node_id]:
                del self.Edges[key][node_id]
                del self.src_to_dest[key][node_id]
                self.ESize -= 1
            for key in self.src_to_dest[node_id]:
                self.dest_to_src[key].pop(node_id)
                self.ESize -= 1
            self.Nodes.pop(node_id)
            self.Edges.pop(node_id)
            self.src_to_dest.pop(node_id)
            self.dest_to_src.pop(node_id)
            self.MC += 1
            self.VSize -= 1
            return True

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        """
        remove the edge between (node_id1,node_id2)
        :param node_id1: the edge source
        :param node_id2: the edge destination
        :return: true if the edge removed successfully, else return false
        """
        if self.has_edge(node_id1, node_id2):  # if there is an edge between id1 to id2
            del self.Edges[node_id1][node_id2]  # remove it from all the lists
            del self.src_to_dest[node_id1][node_id2]
            del self.dest_to_src[node_id2][node_id1]
            self.ESize -= 1
            self.MC += 1
            ans = True
        else:  # if there is no edge between them return false
            ans = False
        return ans

    def get_all_v(self) -> dict:
        """
        This method return a dictionary represents the nodes in the Graph
        :return: dictionary of all the nodes in the Graph
        """
        return self.Nodes

    def all_in_edges_of_node(self, id1: int) -> dict:
        """
        return a dictionary represents the nodes that connected to node_id
        :param id1: the id of the node
        :return: dictionary of all the nodes connected to (into) node_id
        """
        return self.dest_to_src[id1]

    def all_out_edges_of_node(self, id1: int) -> dict:
        """
        return a dictionary represents the nodes connected from node_id
        :param id1: the id of the node
        :return: dictionary of all the nodes connected from node_id
        """
        return self.src_to_dest[id1]

    def has_edge(self, node_id1: int, node_id2: int) -> bool:
        """
         return true if there is an edge between node_id1 to node_id2
        :param node_id1: the id of the src node
        :param node_id2: the id of the dest node
        :return: true if there is edge (node_id1,node_id2) else return false
        """
        if node_id1 not in self.Nodes or node_id2 not in self.Nodes:  # if either of nodes not in the graph return False
            return False
        if node_id2 not in self.Edges[node_id1]:  # if both are in graph but there is no edge return False
            return False
        return self.Edges[node_id1][node_id2]

    def get_edge(self, node_id1: int, node_id2: int) -> EdgeData:
        """
        return the edge between (node_id1,node_id2)
        :param node_id1: the src node
        :param node_id2: the dest node
        :return: the EdgeData of (node_id1,node_id2) if there is no edge return None
        """
        if node_id1 not in self.Nodes or node_id2 not in self.Nodes:  # if either of nodes not in the graph return None
            return None
        if node_id2 not in self.Edges[node_id1]:  # if both are in graph but there is no edge return None
            return None
        return self.Edges[node_id1][node_id2]

    def get_node(self, node_id) -> NodeData:
        """
         return the node from the graph that associated with the given key
        :param node_id: the id of the node
        :return: the node associated with node_id
        """
        if node_id not in self.Nodes:
            return None
        else:
            return self.Nodes.get(node_id)

    # Additional methods
    def __hash__(self, node_id1: int, node_id2: int) -> int:
        """
        create unique key from two integers
        :param node_id1: first integer
        :param node_id2: second integer
        :return: unique key
        """
        return hash((node_id1, node_id2))

    def __repr__(self):
        """
         basic string format represents the graph
        :return: string represents the graph
        """
        return f"DiGraph[Nodes:{self.Nodes},Edges:{self.Edges},Edge_size:{self.ESize},Node_size:{self.VSize}]"
