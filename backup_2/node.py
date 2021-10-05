import simpy
import parameters
import random
import numpy as np
import math

class Node:
    def __init__(self, env, id, name, arr_rate, vcs=False):
        self.env = env
        self.id = id
        self.name = name
        self.backoff = -1
        self.cont_window = parameters.CW_0
        self.vcs = vcs
        self.isSending = False

class Packet:
    def __init__(self, packetId, node):
        self.id = packetId
        self.node = node
        self.isTransmitting = False
