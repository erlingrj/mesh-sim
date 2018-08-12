import matplotlib.pyplot as plt

def get_flat_index(node, size):
    # Returns the flattend out index of a node.
    return node.id[0]*size[0] + node.id[1]


def visualize(timeline, network):
    #TODO: One color per packet
    #TODO: Display packet_info when clicking on packet.
    # Create a visual of the timeline
    fig, ax = plt.subplots()
    packet_array = []
    for _ in range(network.nNodes):
        packet_array.append(list())

    for packet in timeline:
        packet_array[get_flat_index(packet.txNode, network.size)].append((packet.txStart,packet.txStop - packet.txStart))

    for idx in range(network.nNodes):
        ax.broken_barh(xranges = packet_array[idx], yrange = (idx-0.5, 1))

    plt.show()


#TODO: Create functions that produce statistics about a simulation based on timeline and network

#TODO: We want Monte Carlo Simulation and find the

def analyze_data(timeline, network):
    # For oneToAll, what data do we want?
    # 1. Time to reach all  = worst case in that sim
    # 2.
    pass