from abc import ABC
import numpy as np
from random import random

from packet_class import *
from node_class import *

from timeline_class import Timeline
from network_classes import *
from simulator_classes import *
from time import time



#TODO: How can we utilize object orientation in a best way with an abstract base-class
# One child class per simulation type
# But use abstract methods so that they implement the same methods and return similar variables
# What simulations are useful?
# CheckInTime (allToGW)
# allToAll


class Simulator(ABC):
    def __init__(self):
        pass


class Sim_OneToAll(Simulator):
    # TODO: Include retransmissions and sending several packets. nRetransmissions are already an input parameter
    def __init_timeline(self):
        self.timeline = Timeline()

        # in OneToAll we can already initialize all the packets from the single TX
        for period in range(self.nPackets):
            startTime = period * self.txp_ms + random() * self.jitter_ms
            stopTime = startTime + self.packetSize_bits/1000
            TTL = 0
            origin = self.txNodes[0]
            txNode = self.txNodes[0]
            packetCount = period
            self.timeline.add_packet(Packet(txNode, startTime, stopTime, origin, packetCount, TTL))

    def __init__(self, network,
                 nPackets=10,
                 nRetransmission = 5,
                 txp_ms=40,
                 jitter_ms=10,
                 packetSize_bits=369,
                 rampUpDelay_ms=0.139,
                 processingDelay_ms=0.09,
                 clockDrift_ppm=40):
        # Init member variables
        self.network = network
        self.nNodes = self.network.size[0] * self.network.size[1]
        self.nPackets = nPackets
        self.txp_ms = txp_ms
        self.jitter_ms = jitter_ms
        self.packetSize_bits = packetSize_bits
        self.rampUpDelay_ms = rampUpDelay_ms
        self.processingDelay_ms = processingDelay_ms
        self.clockDrift_ppm = clockDrift_ppm

        # Init simulation specific variables
        self.step = 0
        self.network.set_node_to_tx((0, 0))
        self.txNodes = [self.network[0, 0]]
        self.network.set_node_to_gw((network.size[0] - 1, network.size[1] - 1))
        self.gwNodes = [self.network[(network.size[0] - 1, network.size[1] - 1)]]
        self.timer_start = 0
        self.timer_time = 0

        # Init timeline
        self.__init_timeline()

    def simulate_next_packet(self):
        """ Simulates the system one packet into the future."""
        packet = self.timeline[self.step] #Get next packet

        #Get the nodes that are within reach of this packet
        nodesWithinReach = self.network.get_nodes_within_reach(packet.txNode)

        # Remove nodes that already received this packet
        for node in list(nodesWithinReach):
            if packet.origin == node:
                nodesWithinReach.pop(nodesWithinReach.index(node))

            else:
                for recvPacket in node.receivedPackets:
                    if (packet.origin.id, packet.packetCount) == (recvPacket.origin.id, recvPacket.packetCount):
                        nodesWithinReach.pop(nodesWithinReach.index(node))
                        break



        # Remove nodes that were busy at txStart
        # And update busy variables of the nodes within reach
        for node in list(nodesWithinReach):
            if node.busyUntil > packet.txStart:
                nodesWithinReach.pop(nodesWithinReach.index(node))
            else:
                # If not busy, the node will start receiving
                # Update its "busy until" variable
                node.set_busy_until(packet.txStop + self.processingDelay_ms)

        # Get overlapping packets
        # TODO: Remove packets that are too far away to possible affect it (greater than 2 * reach)¨
        overlappingPackets = self.timeline.get_overlapping_packets(self.step)

        # TODO: Take into account that forward_collisions are avoided if one of the nodes "overshadows" the other

        for overlappingPacket in overlappingPackets:
            for node in list(nodesWithinReach):
                if self.network.is_within_reach(overlappingPacket.txNode, node):
                    node.failed_recvs += 1
                    nodesWithinReach.pop(nodesWithinReach.index(node))


        # Remaining nodes will have received the packet successfully

        # Update received_packet array of the nodes
        # Update the timeline with new packets

        for node in list(nodesWithinReach):
            node.add_received_packet(packet)

            # Create a new packet
            newStartTime= packet.txStop + self.jitter_ms * random()
            newStopTime = newStartTime + self.packetSize_bits/1000

            # Node is now busy until this send is over
            node.set_busy_until(newStopTime + self.rampUpDelay_ms)
            newPacket = Packet(node, newStartTime, newStopTime, packet.origin, packet.packetCount, packet.TTL+1)
            self.timeline.add_packet(newPacket)

        self.timeline.sort()
        self.step += 1


    def simulate_until_end(self):
        # Simulates all nPackets and returns the timeline and the nodematrix
        self.timer_start = time()
        while self.step < len(self.timeline):
            self.simulate_next_packet()
        self.timer_time = time() - self.timer_start

        print("DONE. Time = {}".format(self.timer_time))
        return (self.timeline, self.network)

