

class Timeline():
    def __init__(self):
        self.timeline = []

    def __getitem__(self, index):
        return self.timeline[index]

    def __len__(self):
        return len(self.timeline)


    def add_packet(self, packet):
        self.timeline.append(packet)

    def sort(self):
        self.timeline.sort(key=lambda x: x.txStart, reverse=False)

    def display(self):
        for packet in self.timeline:
            packet.display()

    def get_overlapping_packets(self, step):
        # Returns the packets overlapping with the packet at index step

        overlappingPackets = []
        packet1 = self[step]

        # Search backwards in time
        # Check if we are at first iteration
        if step > 0:
            idx = step -1
            packet2 = self[idx]
            while packet2.txStop > packet1.txStart:
                overlappingPackets.append(packet2)
                idx -= 1
                if idx < 0:
                    break
                else:
                    packet2 = self[idx]

        # Search forward
        idx = step + 1
        if idx < len(self.timeline):
            packet2 = self[idx]
            while packet2.txStart < packet1.txStop:
                overlappingPackets.append(packet2)
                idx += 1
                if idx >= len(self.timeline):
                    break
                else:
                    packet2 = self[idx]

        return overlappingPackets






