
class Packet():
    def __init__(self, txNode, txStart, txStop, origin, packetCount, TTL=0):
        self.txNode = txNode
        self.txStart = txStart
        self.txStop = txStop
        self.origin = origin
        self.packetCount = packetCount
        self.TTL = TTL

    def display(self):
        print("TX: {}, [{:10.3f}-{:10.3}], Origin: {}, Count: {}".format(self.txNode.id, self.txStart, self.txStop,
                                                                         self.origin.id, self.packetCount))