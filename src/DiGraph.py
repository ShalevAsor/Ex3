from src.GraphInterface import GraphInterface
from src.node_data import NodeData
from src.edge_data import EdgeData


class DiGraph(GraphInterface):

    def __init__(self):
        self.Nodes = {}
        self.Edges = {}
        self.Neighbors = {int: []}
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
        ans = False
        if weight < 0 or id1 == id2:  # negative weight and edge from node to himself does not allowed
            return ans
        if id1 not in self.Nodes or id2 not in self.Nodes:  # one of the vertices is not in the graph
            return ans  # false
        else:  # the nodes is in the graph
            edge_key = self.__hash__(id1, id2)  # create hashcode from the edge src and dest
            if self.has_edge(id1, id2):
                if self.Edges.get(edge_key).weight == weight:  # the weight is equal to the given weight
                    return ans  # dont update the weight and return false
                else:  # update the weight and return true
                    self.Edges.get(edge_key).weight = weight
                    return ans
            else:  # there is no edge between id1 and id2
                p_edge = EdgeData(id1, id2, weight)  # create new edge
                self.Edges[edge_key] = p_edge  # add it to the graph
                self.get_node(id1).Out[id2] = weight
                self.get_node(id2).In[id1] = weight
                self.Neighbors[id1].append(self.Nodes.get(id2))
                self.Neighbors[id2].append(self.Nodes.get(id1))
                self.ESize += 1  # increase the edge size by 1
                self.MC += 1  # increase the mode count by 1
                ans = True

        return ans

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
            p_node = NodeData(node_id, pos=pos)  # create a new node
            self.Nodes[node_id] = p_node  # add the node to the graph
            self.Neighbors[node_id] = []  # init empty list
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
            r_node = self.get_node(node_id)  # pointer to the node
            for p_node in self.Neighbors.get(node_id):  # all the node neighbors (in and out)
                if self.has_edge(p_node.key, node_id):
                    del self.Edges[self.__hash__(p_node.key, node_id)]  # remove the edge
                    self.ESize -= 1
                if self.has_edge(node_id, p_node.key):
                    del self.Edges[self.__hash__(node_id, p_node.key)]  # remove the edge
                    self.ESize -= 1
                self.Neighbors.get(p_node.key).remove(r_node)  # remove the node from neighbors
        del self.Nodes[node_id]  # remove the node from the graph
        self.VSize -= 1
        del self.Neighbors[node_id]
        self.MC += 1
        return True

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        """
        remove the edge between (node_id1,node_id2)
        :param node_id1: the edge source
        :param node_id2: the edge destination
        :return: true if the edge removed successfully, else return false
        """
        if self.has_edge(node_id1, node_id2):  # if there is an edge between id1 to id2
            del self.Edges[self.__hash__(node_id1, node_id2)]  # remove the edge
            self.Neighbors[node_id1].remove(self.get_node(node_id2))  # remove the from the neighbors
            self.Neighbors[node_id2].remove(self.get_node(node_id1))
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
        if id1 in self.Nodes:
            return self.get_node(id1).In

    def all_out_edges_of_node(self, id1: int) -> dict:
        """
        return a dictionary represents the nodes connected from node_id
        :param id1: the id of the node
        :return: dictionary of all the nodes connected from node_id
        """
        if id1 in self.Nodes:
            return self.get_node(id1).Out

    def has_edge(self, node_id1: int, node_id2: int) -> bool:
        """
         return true if there is an edge between node_id1 to node_id2
        :param node_id1: the id of the src node
        :param node_id2: the id of the dest node
        :return: true if there is edge (node_id1,node_id2) else return false
        """
        edge_key = self.__hash__(node_id1, node_id2)
        if edge_key in self.Edges:
            ans = True
        else:
            ans = False
        return ans

    def get_edge(self, node_id1: int, node_id2: int) -> EdgeData:
        """
        return the edge between (node_id1,node_id2)
        :param node_id1: the src node
        :param node_id2: the dest node
        :return: the EdgeData of (node_id1,node_id2) if there is no edge return None
        """
        if self.has_edge(node_id1, node_id2):
            return self.Edges.get(self.__hash__(node_id1, node_id2))
        else:
            return None

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
