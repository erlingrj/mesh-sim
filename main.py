from random import random
from abc import ABC, abstractmethod
import numpy as np
from enum import Enum

from packet_class import *
from node_class import *
from timeline_class import *
from network_classes import *
from simulator_classes import *
from misc import *


nNodes = 5
packetSize = 0.5
nPackets = 1
nRetransmissions = 1
txp = 20
jitter = 10

size = (10, 10)

grid = Grid(size=size, reach=1)
sim = Sim_OneToAll(grid, nPackets = nPackets, txp_ms = txp)

(tl, network) = sim.simulate_until_end()

visualize(tl, network)
