import simpy
import numpy as np
import random
import math

import node
from node import Packet
import parameters

class CSMA:
    def __init__(self, env, arrival_rate, vcs=False):
        self.vcs = vcs
        self.env = env
        self.arrival_rate = arrival_rate
        self.col_A = 0
        self.col_C = 0
        self.tx_A = 0
        self.tx_C = 0
        self.srcs = []
        self.dest = []
        self.medium = []
        self.packetId = 0 #number of Packets in common medium
        self.srcs.append(node.Node(env, 0, "A", arrival_rate, vcs))
        self.srcs.append(node.Node(env, 1, "C", arrival_rate, vcs))
        self.dest.append(node.Node(env, 2, "B", arrival_rate, vcs))
        self.dest.append(node.Node(env, 3, "D", arrival_rate, vcs))
        for i in range(len(self.srcs)):
            self.env.process(self.transmit(self.env,self.srcs[i]))

    def transmit(self, env, node):
        while True:
            yield env.timeout(100)#self.generate_interarrival())
            node.arrival = env.now
            print("Packet ID %d ready for TX at %s at %d" % (self.packetId, node.name, env.now))
            p = Packet(self.packetId, node)
            self.medium.append(p)
            self.packetId += 1
            
            difs = parameters.DIFS_DUR
            if node.backoff == -1:
                node.backoff = random.randint(0, node.cont_window-1)
            print("%s backoff is %d" % (node.name, node.backoff))
            senseTimeout = difs + node.backoff

            while senseTimeout > 0:
                print("Node %s is sensing" % node.name)
                yield env.timeout(1)
                senseTimeout -= 1
                if senseTimeout < parameters.DIFS_DUR:
                    node.backoff -= 1
                if self.senseCollision(p):
                    print("%s: Other src is sending. Pausing TX at %d" % (node.name, node.arrival))
                    return
                #sending frame
                p.isTransmitting = True
                yield env.timeout(parameters.FRAME_SIZE)
                yield env.timeout(parameters.SIFS_DUR)
                yield env.timeout(parameters.ACK)
                node.backoff = -1
                p.isTransmitting = False
                return


                
            
    
    def senseCollision(self, packet):
        '''
        if (len(self.medium) > 0):
            for other in self.medium:
                if other.id != packet.id and other.isTransmitting == False:
                    print(other.id)
                    return False
                else:
                    return True
        else: 
            return False
        '''
        for other in self.medium:
            if other.id != packet.id and other.isTransmitting == True:
                return True
            else:
                return False
            

    def generate_interarrival(self):
        return np.random.exponential(1/(parameters.SLOT_DUR*200))


def main():
    env = simpy.Environment()
    csma = CSMA(env,100)
    #csma.transmit(env)
    env.run(until=400)


if __name__ == "__main__":
    main()
