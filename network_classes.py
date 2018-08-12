from abc import ABC
import numpy as np
from node_class import Node, NodeType

class Network(ABC):
    def __init__(self):
        pass

    def getDistance(self, node1, node2):
        pass


class Grid(Network):
    def __init__(self, size=(3, 3), reach=1):
        self.__init_node_matrix(size)
        self.reach = reach
        self.size = size
        self.nNodes = size[0]*size[1]

    def __init_node_matrix(self, size):
        self.nodeArray = np.zeros((size), dtype=Node)
        for i in range(size[0]):
            for j in range(size[1]):
                self.nodeArray[i, j] = Node((i, j))

    def __getitem__(self, key):
        return self.nodeArray[key[0], key[1]]


    def set_node_to_tx(self, id):
        self.nodeArray[id[0], id[1]].type = NodeType.TX

    def set_node_to_gw(self, id):
        self.nodeArray[id[0], id[1]].type = NodeType.GATEWAY

    def set_node_to_relay(self, id):
        self.nodeArray[id[0], id[1]].type = NodeType.RELAY

    def get_distance_between_nodes(self, node1, node2):
        return max(abs(node1.id[0] - node2.id[0]), abs(node1.id[1] - node2.id[1]))

    def get_nodes_within_reach(self, node):
        # Returns an array of the nodes within reach of input node
        nodesWithinReach = []
        (x, y) = node.id
        for i in range(x - self.reach, x + self.reach+1):
            for j in range(y - self.reach, y + self.reach+1):
                if (i, j) == (x, y) or (i < 0) or (j < 0) or (i >= self.size[0]) or (j >= self.size[1]):
                    pass
                else:
                    nodesWithinReach.append(self[(i, j)])

        return nodesWithinReach

    def is_within_reach(self, node1, node2):
        # returns boolean of whether node1 and node2 are within reach of each other
        return self.get_distance_between_nodes(node1, node2) <= self.reach

