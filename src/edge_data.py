class EdgeData:
    """
    This class represent an edge on the graph, each edge has src- the source node
    and dest- the destination node , each edge attached with a weight
    """
    def __init__(self,source:int,destination:int,we:float,info:str=None,tag:int=-1):
        """
        simple constructor with default data for info and tag,usually used for algorithms
        :param source: the source vertex
        :param destination: the destination vertex
        :param we: the weight of the edge
        :param info: data of the edge
        :param tag: data of the edge
        """
        self.src=source
        self.dest=destination
        self.weight=we
        self.info=info
        self.tag=tag

    def __repr__(self):
        return f"Edge:src:[{self.src}],dest:[{self.dest}],weight:[{self.weight}]"
