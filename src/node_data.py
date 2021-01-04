import math
class NodeData:
    """
    This class represent an Node(vertex) in the graph each Node has a unique key
    """

    def __init__(self, key: int, info: str = "", tag: int = 0, pos: tuple = None):
        """
        init a new node with an unique key
        :param key: - each node has a unique key
        :param info: the node information (str)
        :param tag: tag of the node (usually used for algorithms)
        :param pos: 3D point represents the node position
        """
        self.id = key
        self.info = info
        self.tag = tag
        self.pos = pos
        # -------algorithms variable field-------
        self.visited = False
        self.w = -1
        self.t = -1

    def get_x(self) -> float:
        if self.pos is not None:
            return self.pos[0]
        return -1

    def get_y(self) -> float:
        if self.pos is not None:
            return self.pos[1]
        return -1

    def __repr__(self):
        """
        print basic information about this node
        :return: String with the node key and position
        """
        return f"Node:{self.key} pos:{self.pos}"

    def __eq__(self, o: object) -> bool:
        if self is o: return True
        if o.key == self.key and o.pos == self.pos:
            return True
        else:
            return False


if __name__ == '__main__':
    n = NodeData(1)
    print(n)
    n2 = NodeData(2)
    print(n2)
    n3 = NodeData(3, pos=(12.3, 12.01, 0))
    print(n3)