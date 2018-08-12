from enum import Enum
import numpy as np


class NodeType(Enum):
    TX = 1
    RELAY = 2
    GATEWAY = 3


#TODO: Update with more statistics for the node.
# 1. How many packets were sent by the node?
# 2. How many packet receives were failed, by interference?

#TODO: How do we make use of self.type?

#TODO: Need a sort of a sending_queue to store the planned packet_sends.

class Node():
    def __init__(self, id, nodeType=NodeType.RELAY):
        self.id = id
        self.type = nodeType
        self.busyUntil = -1
        self.receivedPackets = []

        # Statistics
        self.failed_recvs = 0

    def display(self):
        print(self.id)

    def set_busy_until(self, busy_until):
        self.busyUntil = busy_until

    def add_received_packet(self, packet):
        self.receivedPackets.append(packet)


